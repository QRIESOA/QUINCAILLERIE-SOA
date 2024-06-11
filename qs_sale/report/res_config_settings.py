# coding: utf-8

import base64

from odoo import models, fields, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    email_daily_report = fields.Char(string="Email to daily report", config_parameter="qs_sale.email_daily_report")

    