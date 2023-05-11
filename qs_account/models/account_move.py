#-*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    # delivery_time = fields.Float(string='Delivery Time')
    is_charge = fields.Boolean()
    is_spec = fields.Boolean(string="is_spec", compute="_compute_is_spec")
    # journal_paie_name = fields.Char(string="payment journal", compute='journal_name_compute', store=True)
    payment_paie_date = fields.Date(compute='journal_name_compute', store=True, string="payment date")
    # communication = fields.Char(compute='journal_name_compute', store=True)
    about_payment = fields.Char(compute='_compute_about_payment')

    @api.depends('payment_id')
    def journal_name_compute(self):
        for rec in self:
            invoice_to_w = self.env["account.move"].search([('name', '=', rec.ref)])
            invoice_to_w.write({"payment_paie_date": rec.payment_id.date})


    def _compute_about_payment(self):
        for rec in self:
            rec.about_payment = False
            json_values = rec._get_reconciled_info_JSON_values()
            if json_values:
                rec.about_payment = ', '.join(val.get('ref', '') for val in json_values)

    @api.depends()
    def _compute_is_spec(self):
        self.is_spec = self.env.user.has_group('qs_account.group_account_user_spec')

    @api.model
    def get_spec(self):
        return self.env.user.has_group('qs_account.group_account_user_spec')