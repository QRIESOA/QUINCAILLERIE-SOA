#-*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    # delivery_time = fields.Float(string='Delivery Time')
    is_charge = fields.Boolean()
    is_spec = fields.Boolean(string="is_spec", compute="_compute_is_spec")

    @api.depends()
    def _compute_is_spec(self):
        self.is_spec = self.env.user.has_group('qs_account.group_account_user_spec')

    @api.model
    def get_spec(self):
        return self.env.user.has_group('qs_account.group_account_user_spec')