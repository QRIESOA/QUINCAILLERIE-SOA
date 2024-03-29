# -*- coding: utf-8 -*-

import logging
import math
import re
import time

from lxml import etree
from odoo import api, fields, models, tools, _

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
try:
    from num2words import num2words
except ImportError:
    _logger.warning("The num2words python library is not installed, amount-to-text features won't be fully available.")
    num2words = None

CURRENCY_DISPLAY_PATTERN = re.compile(r'(\w+)\s*(?:\((.*)\))?')


class qs_pers(models.Model):
    _inherit = 'sale.order'

    def has_duplicates(values):
        if len(values) != len(set(values)):
            raise ValidationError(_('Les articles en double dans la ligne de commande ne sont pas autorisés'))

    @api.constrains('order_line')
    def check_duplicate_article(self):
        for record in self:
            products_in_lines = record.mapped('order_line.product_id')
            for product in products_in_lines:
                lines_count = len(record.order_line.filtered(lambda line: line.product_id == product))
                if lines_count > 1:
                    raise ValidationError(_('Les articles en double dans la ligne de commande ne sont pas autorisés'))

            # if len(products_in_lines) != len(set(products_in_lines)):
            #     print("true")
            #     print(len(products_in_lines))
            #     print(len(set(self.order_line.product_id)))
            #     raise ValidationError(_('Les articles en double dans la ligne de commande ne sont pas autorisés'))
            # else:
            #     print(len(products_in_lines))
            #     print(len(set(products_in_lines)))
            #     raise models.ValidationError(
            #         _('Les articles en double dans la ligne de commande ne sont pas autorisés'))

        return True

    # def write(self, values):
    #     for order in self:
    #         products_in_lines = order.mapped('order_line.product_id')
    #         if len(products_in_lines) != len(set(products_in_lines)):
    #             print("true")
    #
    #             print(len(products_in_lines))
    #             print(len(set(self.order_line.product_id)))
    #             raise ValidationError(_('Les articles en double dans la ligne de commande ne sont pas autorisés'))
    #         else:
    #             print(len(products_in_lines))
    #             print(len(set(products_in_lines)))
    #             raise ValidationError(_('Les articles en double dans la ligne de commande ne sont pas autorisés'))
    #     return super(qs_pers, self).write(values)
    #
    # @api.constrains('order_line')
    # def _check_duplicate_product(self):
    #     for rec in self:
    #         exist_product_list = []
    #         for line in rec.order_line:
    #             print(line.product_id)
    #             if line.product_id in exist_product_list:
    #                 raise ValidationError(_('Product should be one per line.'))
    #                 exist_product_list.append(line.product_id.id)

    note_nda = fields.Text(string="Note sur NDA", index=1)

    show_pricelist = fields.Char(string="Liste de prix associé", related='pricelist_id.name')

    compute_field_sale = fields.Boolean(string="check field", compute='get_user_sale')

    @api.depends('compute_field_sale', 'user_id')
    def get_user_sale(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('sales_team.group_sale_salesman') and not res_user.has_group(
                'sales_team.group_sale_salesman_all_leads'):

            self.compute_field_sale = True
        else:

            self.compute_field_sale = False

    mobil_name_sale = fields.Char(
        'Mobile phone',
        related='partner_id.phone',
        readonly=True)
    email_sale = fields.Char(
        'email',
        related='partner_id.email',
        readonly=True)

    credit_sale_limit = fields.Monetary("limite de credit sales", related="partner_id.credit_limit")
    total_due_sale = fields.Monetary("limite de credit sales", related="partner_id.total_due")

    def check_credit_limit(self):
        if self.credit_sale_limit > 0:
            if self.credit_sale_limit < self.total_due_sale + self.amount_total:
                raise UserError("Ce client doit payer son credit")

    def _action_confirm(self):
        """ Implementation of additionnal mecanism of Sales Order confirmation.
            This method should be extended when the confirmation should generated
            other documents. In this method, the SO are in 'sale' state (not yet 'done').
        """
        self.check_credit_limit()
        self.update_prices()
        return super(qs_pers, self)._action_confirm()

    def action_confirm(self):
        self.check_credit_limit()
        self.update_prices()
        return super(qs_pers, self).action_confirm()

    @api.depends('amount_total')
    def get_amount_letter(self):
        amount = self.currency_id.amount_to_text(self.amount_total)
        return amount


class ResCurrencyInherited(models.Model):
    _inherit = "res.currency"

    def amount_to_text(self, amount):
        self.ensure_one()

        def _num2words(number, lang):
            try:
                return num2words(number, lang='fr').title()
            except NotImplementedError:
                return num2words(number, lang='fr').title()

        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""

        formatted = "%.{0}f".format(self.decimal_places) % amount
        parts = formatted.partition('.')
        integer_value = int(parts[0])
        fractional_value = int(parts[2] or 0)

        lang = tools.get_lang(self.env)
        amount_words = tools.ustr('{amt_value} {amt_word}').format(
            amt_value=_num2words(integer_value, lang=lang.iso_code),
            amt_word=self.currency_unit_label,
        )
        if not self.is_zero(amount - integer_value):
            amount_words += ' ' + _('et') + tools.ustr(' {amt_value} {amt_word}').format(
                amt_value=_num2words(fractional_value, lang=lang.iso_code),
                amt_word=self.currency_subunit_label,
            )
        return amount_words


class ResPartner(models.Model):
    _inherit = "res.partner"
    credit_limit = fields.Monetary("Limite de credit", index=True, tracking=True)
    compute_field = fields.Boolean(string="check field", compute='get_user')
    compute_field_credit_l = fields.Boolean(string="check field 1", compute='get_user_connect')
    compute_field_lst_price = fields.Boolean(string="check field 1", compute='get_user_connect_grc_lst')

    @api.depends("compute_field_credit_l","user_id")
    def get_user_connect(self):
        # res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if self.env.user.has_group('qs_pers.group_partner_credit_limit'):
            self.compute_field_credit_l = True
        else:
            self.compute_field_credit_l = False

    @api.depends("compute_field_lst_price","user_id")
    def get_user_connect_grc_lst(self):
        # res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if self.env.user.has_group('qs_pers.group_partner_lst_price'):
            self.compute_field_lst_price = True
        else:
            self.compute_field_lst_price = False

    @api.onchange("credit_limit")
    def check_total_due_value(self):
        if self.credit_limit > 0:
            if self.credit_limit < self.total_due:
                raise UserError("La limite de crédit doit être supérieure aux factures impayées actuelles.")

    @api.depends_context('company', 'allowed_company_ids')
    def _compute_for_followup(self):
        """
        Compute the fields 'total_due', 'total_overdue','followup_level' and 'followup_status'
        """
        first_followup_level = self.env['account_followup.followup.line'].search([('company_id', '=', self.env.company.id)], order="delay asc", limit=1)
        followup_data = self._query_followup_level()
        today = fields.Date.context_today(self)
        for record in self:
            total_due = 0
            total_overdue = 0
            for aml in record.unreconciled_aml_ids:
                if aml.company_id == self.env.company:
                    amount = aml.amount_residual
                    total_due += amount
                    is_overdue = today > aml.date_maturity if aml.date_maturity else today > aml.date
                    if is_overdue:
                        total_overdue += amount
            record.total_due = total_due
            record.total_overdue = total_overdue
            if record.id in followup_data:
                record.followup_status = followup_data[record.id]['followup_status']
                record.followup_level = self.env['account_followup.followup.line'].browse(followup_data[record.id]['followup_level']) or first_followup_level
            else:
                record.followup_status = 'no_action_needed'
                record.followup_level = first_followup_level

    @api.depends('compute_field', 'user_id')
    def get_user(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('sales_team.group_sale_salesman') and not res_user.has_group(
                'sales_team.group_sale_salesman_all_leads'):
            self.compute_field = True
        else:
            self.compute_field = False


class SaleOrderLineInherited(models.Model):
    _inherit = 'sale.order.line'

    tax_id_name = fields.Char(string="Taxes", related='tax_id.name')
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

    # def notification_test(self):
    #     notification = {
    #         'type': 'ir.actions.client',
    #         'tag': 'display_notification',
    #         'params': {
    #             'title': ('Your Custom Title'),
    #             'message': 'Your Custom Message',
    #             'type': 'success',  # types: success,warning,danger,info
    #             'sticky': True,  # True/False will display for few seconds if false
    #         },
    #     }
    #     return notification

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

            if treated:
                msg_price_unit = "Le prix unitaire de cet article n'est pas conforme, veuillez appeler votre responsable pour changer le prix."
                if treated[-1].price_unit == 0:
                    raise UserError(msg_price_unit)
                    print("efa vita print notification test")

            msg = _('La quantité en stock est insuffisante, il ne reste que %s') % (free_qty_today)
            if treated:
                if free_qty_today < treated[-1].product_uom_qty:
                    res_user = self.env['res.users'].search([('id', '=', self._uid)])
                    if not res_user.has_group('qs_pers.group_qs_vente_neg'):
                        raise UserError(msg)
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
