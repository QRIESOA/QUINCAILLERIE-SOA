# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPickingInherited(models.Model):
    _inherit = 'stock.picking'
    ticket_number = fields.Char(string="Note d'achat",
                                related='pos_order_id.lines.sale_order_origin_id.name')
    ref_number = fields.Char(string="Numéro ticket de caisse",
                             related='pos_order_id.pos_reference')


class StockQuantInherited(models.Model):
    _inherit = 'stock.quant'
    product_name = fields.Char(string="Articles", related="product_id.name", index=True, store="True")
    product_ref = fields.Char(string="Réf", related="product_id.default_code", index=True, store="True")
