# -*- coding: utf-8 -*-

from odoo import models, fields, api


class qs_pers_inv(models.Model):
    _inherit = 'stock.picking'

    mobil_name_inv = fields.Char(
        'Mobile phone',
        related='partner_id.phone',
        readonly=True)
