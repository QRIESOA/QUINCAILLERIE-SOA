from odoo import fields, models, api


class ModelName(models.Model):
    _inherit = 'stock.valuation.layer'
    _description = 'Description'

    source_location = fields.Char(
        string='De',
        related="stock_move_id.location_id.display_name")
    destination_location = fields.Char(
        string='Vers',
        related="stock_move_id.location_dest_id.display_name")
