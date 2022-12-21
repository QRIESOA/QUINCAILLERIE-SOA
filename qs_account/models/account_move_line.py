# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'


    taxed_price_unit = fields.Float(
        compute="_get_price_tax_included", string='Price Tax Incl.', digits='Product Price')
    subtotal_ttc = fields.Float(
        compute="compute_subtotal_ttc", string='Price Tax Incl.', digits='Product Price')

    def _get_price_tax_included(self):
        for line in self:
            taxed_price_unit = 0.0
            if line.quantity:
                taxes = line.tax_ids.compute_all(
                    line.price_unit, line.currency_id, line.quantity, product=line.product_id and line.product_id or False)
                tax_amount = sum(t.get('amount', 0.0)
                                 for t in taxes.get('taxes', []))
                taxed_price_unit = line.price_unit + (tax_amount/line.quantity)
            line.taxed_price_unit = taxed_price_unit

    
    @api.depends('quantity', 'taxed_price_unit', 'tax_ids', 'discount')
    def compute_subtotal_ttc(self):
        for line in self:
            price = line.price_unit * line.quantity * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids._origin.compute_all(price, line.move_id.currency_id, line.quantity, product=line.product_id, partner=line.move_id.partner_id)
            tax_amount = sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
            try:
                taxed_price_ttc = price + (tax_amount/line.quantity)
            except ZeroDivisionError:
                taxed_price_ttc = price
            line.subtotal_ttc = taxed_price_ttc

    @api.onchange('quantity', 'discount', 'price_unit', 'tax_ids')
    def _onchange_price_subtotal(self):
        super(AccountMoveLine, self)._onchange_price_subtotal()
        for line in self:
            taxed_price_unit = 0.0
            if line.quantity:
                taxes = self.tax_ids.compute_all(
                    line.price_unit, line.currency_id, line.quantity, product=line.product_id and line.product_id or False)
                tax_amount = sum(t.get('amount', 0.0)
                                 for t in taxes.get('taxes', []))
                taxed_price_unit = line.price_unit + (tax_amount/line.quantity)
            line.taxed_price_unit = taxed_price_unit
