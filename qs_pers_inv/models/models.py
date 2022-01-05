# -*- coding: utf-8 -*-

from odoo import models, fields, api


class qs_pers_inv(models.Model):
    _inherit = 'stock.picking'

    mobil_name_inv = fields.Char(
        'Mobile phone',
        related='partner_id.phone',
        readonly=True)

    compute_field_sale = fields.Boolean(string="check field", compute='get_user_sale')

    @api.depends('compute_field_sale', 'user_id')
    def get_user_sale(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if not res_user.has_group('sales_team.group_sale_salesman'):
            print("ato izy true inv")
            self.compute_field_sale = True
        else:
            print("ato izy false eh inv")
            self.compute_field_sale = False
