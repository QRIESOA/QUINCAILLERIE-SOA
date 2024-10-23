# -*- coding: utf-8 -*-

from odoo import models, fields


class PosConfig(models.Model):
    _inherit = "pos.config"

    is_cash_box = fields.Boolean(string="Is cash box")
