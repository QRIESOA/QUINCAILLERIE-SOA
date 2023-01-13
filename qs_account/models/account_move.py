#-*- coding: utf-8 -*-

from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    # delivery_time = fields.Float(string='Delivery Time')
    is_charge = fields.Boolean()