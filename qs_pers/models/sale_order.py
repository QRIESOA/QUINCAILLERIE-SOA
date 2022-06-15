from odoo import api, fields, models, tools, _


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('price_subtotal', 'product_uom_qty', 'purchase_price')
    def _compute_margin(self):
        for line in self:
            if line.product_id.ttc_logic:
                line.margin = line.price_total - (line.purchase_price * line.product_uom_qty)
                line.margin_percent = line.price_total and line.margin / line.price_total
            else:
                line.margin = line.price_subtotal - (line.purchase_price * line.product_uom_qty)
                line.margin_percent = line.price_subtotal and line.margin / line.price_subtotal
