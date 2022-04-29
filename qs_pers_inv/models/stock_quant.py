from odoo import fields, models, api


class ModelName(models.Model):
    _inherit = 'stock.quant'
    ref_interne = fields.Char(
        string='Réf interne',
        related='product_id.default_code', store=True)
    article_nom = fields.Char(
        string="Nom d'article",
        related='product_id.name', store=True)
