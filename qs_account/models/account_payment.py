# -*- coding: utf-8 -*-

from odoo import models, fields, api

class account_payment(models.Model):
    _inherit = "account.payment"

    is_spec = fields.Boolean(string="is_spec", compute="_compute_is_spec")

    @api.depends()
    def _compute_is_spec(self):
        self.is_spec = self.env.user.has_group('qs_account.group_account_user_spec')