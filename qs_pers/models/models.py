# -*- coding: utf-8 -*-

from odoo import models, fields, api


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


class ResPartner(models.Model):
    _inherit = "res.partner"
    term_pdv = fields.Float(string="terms dans pos", required=False)
