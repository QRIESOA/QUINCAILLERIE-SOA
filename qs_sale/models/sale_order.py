# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    partner_id = fields.Many2one("res.partner", default=lambda self: self.env.ref("qs_sale.client_comptant").id)
    note_client = fields.Char(string="Note")
    can_change_list = fields.Boolean(string='Can create partner', default=lambda self: self.env.user.has_group("qs_sale.group_partner_change_list_so"), compute="_compute_can_create")

    # @api.depends()
    def _compute_can_create(self):
        self.can_change_list = self.env.user.has_group("qs_sale.group_partner_change_list_so")

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['note_client'] = self.note_client

        return res
    
    def write(self, vals):
        super(SaleOrder, self).write(vals)
        if 'pricelist_id' in vals and self.state == 'draft':
            self.update_prices()
    

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        res = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)
        res['note_client'] = order.note_client
        return res