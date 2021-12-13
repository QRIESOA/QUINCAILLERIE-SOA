# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartnerS2PC(models.Model):
    _inherit = 'res.partner'
    STAT = fields.Char('STAT', index=1)
    RCS = fields.Char('RCS', index=1)
    CIF = fields.Char('CIF', index=1)


