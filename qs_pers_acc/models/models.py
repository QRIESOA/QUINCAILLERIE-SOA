# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta


class qs_pers_acc(models.Model):
    _inherit = 'account.move'

    mobile_phone = fields.Char(
        'Mobile phone',
        related='partner_id.phone',
        readonly=True)

    email_partner = fields.Char(
        'Mobile phone',
        related='partner_id.email',
        readonly=True)

