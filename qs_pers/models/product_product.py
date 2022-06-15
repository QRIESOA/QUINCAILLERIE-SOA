from odoo import fields, models, api


class ModelName(models.Model):
    _inherit = "product.product"
    detail_price_product = fields.Monetary(
        string='PV DET(MGA)',
        related='product_tmpl_id.detail_price')
