# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta
import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo.tools.translate import _
import json
import logging
from datetime import timedelta
from collections import defaultdict

from odoo import api, fields, models, _
from odoo.tools import float_compare, float_round
from odoo.exceptions import UserError, Warning
import pytz

_logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)


class qs_pers(models.Model):
    _inherit = 'sale.order'

    mobil_name_sale = fields.Char(
        'Mobile phone',
        related='partner_id.phone',
        readonly=True)
    email_sale = fields.Char(
        'email',
        related='partner_id.email',
        readonly=True)

    credit_sale_limit = fields.Monetary("limite de credit sales", related="partner_id.credit_limit")

    def check_credit_limit(self):
        if self.credit_sale_limit > 0:
            if self.credit_sale_limit < self.partner_id.total_due + self.amount_total:
                raise UserError("Ce client doit payer son credit")

    def _action_confirm_qs(self):
        """ Implementation of additionnal mecanism of Sales Order confirmation.
            This method should be extended when the confirmation should generated
            other documents. In this method, the SO are in 'sale' state (not yet 'done').
        """
        self.check_credit_limit()
        # create an analytic account if at least an expense product
        for order in self:
            if any(expense_policy not in [False, 'no'] for expense_policy in
                   order.order_line.mapped('product_id.expense_policy')):
                if not order.analytic_account_id:
                    order._create_analytic_account()

        return True

    def action_confirm_qs(self):
        self.check_credit_limit()
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write(self._prepare_confirmation_values())

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm_qs()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        return True


class ResPartner(models.Model):
    _inherit = "res.partner"
    credit_limit = fields.Monetary("Limite de credit", index=True)
    compute_field = fields.Boolean(string="check field", compute='get_user')

    @api.depends('compute_field')
    def get_user(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('sales_team.group_sale_salesman') and not res_user.has_group(
                'sales_team.group_sale_salesman_all_leads'):
            self.compute_field = True
        else:
            self.compute_field = False


class SaleOrderLineInherited(models.Model):
    _inherit = 'sale.order.line'

    qty_delivered_method = fields.Selection(selection_add=[('stock_move', 'Stock Moves')])
    route_id = fields.Many2one('stock.location.route', string='Route', domain=[('sale_selectable', '=', True)],
                               ondelete='restrict', check_company=True)
    move_ids = fields.One2many('stock.move', 'sale_line_id', string='Stock Moves')
    product_type = fields.Selection(related='product_id.detailed_type')
    virtual_available_at_date = fields.Float(compute='_compute_qty_at_date', digits='Product Unit of Measure')
    scheduled_date = fields.Datetime(compute='_compute_qty_at_date')
    forecast_expected_date = fields.Datetime(compute='_compute_qty_at_date')
    free_qty_today = fields.Float(compute='_compute_qty_at_date', digits='Product Unit of Measure')
    qty_available_today = fields.Float(compute='_compute_qty_at_date')
    warehouse_id = fields.Many2one(related='order_id.warehouse_id')
    qty_to_deliver = fields.Float(compute='_compute_qty_to_deliver', digits='Product Unit of Measure')
    is_mto = fields.Boolean(compute='_compute_is_mto')
    display_qty_widget = fields.Boolean(compute='_compute_qty_to_deliver')

    def notification_test(self):
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': ('Your Custom Title'),
                'message': 'Your Custom Message',
                'type': 'success',  # types: success,warning,danger,info
                'sticky': True,  # True/False will display for few seconds if false
            },
        }
        return notification

    @api.depends(
        'product_id', 'customer_lead', 'product_uom_qty', 'product_uom', 'order_id.commitment_date',
        'move_ids', 'move_ids.forecast_expected_date', 'move_ids.forecast_availability')
    def _compute_qty_at_date(self):
        """ Compute the quantity forecasted of product at delivery date. There are
        two cases:
         1. The quotation has a commitment_date, we take it as delivery date
         2. The quotation hasn't commitment_date, we compute the estimated delivery
            date based on lead time"""
        treated = self.browse()
        # If the state is already in sale the picking is created and a simple forecasted quantity isn't enough
        # Then used the forecasted data of the related stock.move
        for line in self.filtered(lambda l: l.state == 'sale'):
            if not line.display_qty_widget:
                continue
            moves = line.move_ids.filtered(lambda m: m.product_id == line.product_id)
            line.forecast_expected_date = max(moves.filtered("forecast_expected_date").mapped("forecast_expected_date"),
                                              default=False)
            line.qty_available_today = 0
            line.free_qty_today = 0
            for move in moves:
                line.qty_available_today += move.product_uom._compute_quantity(move.reserved_availability,
                                                                               line.product_uom)
                line.free_qty_today += move.product_id.uom_id._compute_quantity(move.forecast_availability,
                                                                                line.product_uom)
            line.scheduled_date = line.order_id.commitment_date or line._expected_date()
            line.virtual_available_at_date = False
            treated |= line

        qty_processed_per_product = defaultdict(lambda: 0)
        grouped_lines = defaultdict(lambda: self.env['sale.order.line'])
        # We first loop over the SO lines to group them by warehouse and schedule
        # date in order to batch the read of the quantities computed field.
        for line in self.filtered(lambda l: l.state in ('draft', 'sent')):
            if not (line.product_id and line.display_qty_widget):
                continue
            grouped_lines[(line.warehouse_id.id, line.order_id.commitment_date or line._expected_date())] |= line

        for (warehouse, scheduled_date), lines in grouped_lines.items():
            product_qties = lines.mapped('product_id').with_context(to_date=scheduled_date, warehouse=warehouse).read([
                'qty_available',
                'free_qty',
                'virtual_available',
            ])
            qties_per_product = {
                product['id']: (product['qty_available'], product['free_qty'], product['virtual_available'])
                for product in product_qties
            }
            for line in lines:
                line.scheduled_date = scheduled_date
                qty_available_today, free_qty_today, virtual_available_at_date = qties_per_product[line.product_id.id]
                line.qty_available_today = qty_available_today - qty_processed_per_product[line.product_id.id]
                line.free_qty_today = free_qty_today - qty_processed_per_product[line.product_id.id]
                line.virtual_available_at_date = virtual_available_at_date - qty_processed_per_product[
                    line.product_id.id]
                line.forecast_expected_date = False
                product_qty = line.product_uom_qty
                if line.product_uom and line.product_id.uom_id and line.product_uom != line.product_id.uom_id:
                    line.qty_available_today = line.product_id.uom_id._compute_quantity(line.qty_available_today,
                                                                                        line.product_uom)
                    line.free_qty_today = line.product_id.uom_id._compute_quantity(line.free_qty_today,
                                                                                   line.product_uom)
                    line.virtual_available_at_date = line.product_id.uom_id._compute_quantity(
                        line.virtual_available_at_date, line.product_uom)
                    product_qty = line.product_uom._compute_quantity(product_qty, line.product_id.uom_id)
                qty_processed_per_product[line.product_id.id] += product_qty
            treated |= lines

            print(self.env.user.name)

            msg = _('La quantité en stock est insuffisante, il ne reste que %s') % (free_qty_today)
            if treated:
                if free_qty_today < treated[-1].product_uom_qty:
                    self.notification_test()
                    print("efa vita print notification test")

        remaining = (self - treated)
        remaining.virtual_available_at_date = False
        remaining.scheduled_date = False
        remaining.forecast_expected_date = False
        remaining.free_qty_today = False
        remaining.qty_available_today = False

    compute_field_sale = fields.Boolean(string="check field", compute='get_user_sale')

    @api.depends('compute_field_sale')
    def get_user_sale(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('sales_team.group_sale_salesman') and not res_user.has_group(
                'sales_team.group_sale_salesman_all_leads'):
            print("ato izy true")
            self.compute_field_sale = True
        else:
            print("ato izy false eh")
            self.compute_field_sale = False
