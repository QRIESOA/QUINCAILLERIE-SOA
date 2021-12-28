# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartnerS2PC(models.Model):
    _inherit = 'res.partner'
    STAT = fields.Char('STAT', index=1)
    RCS = fields.Char('RCS', index=1)
    CIF = fields.Char('CIF', index=1)

    @api.model
    def _default_terms(self):
        return self.env['account.payment.term'].search([('name', '=', 'IMMEDIAT')], limit=1).id

    property_payment_term_id = fields.Many2one('account.payment.term', company_dependent=True,
                                               string='Customer Payment Terms',
                                               domain="[('company_id', 'in', [current_company_id, False])]",
                                               help="This payment term will be used instead of the default one for sales orders and customer invoices",
                                               default=_default_terms)
