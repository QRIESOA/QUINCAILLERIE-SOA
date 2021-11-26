# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta
import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo.tools.translate import _

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
    credit_limit = fields.Monetary("Limite de credit")
    # limite_balance = fields.Monetary('Limite de credit')
