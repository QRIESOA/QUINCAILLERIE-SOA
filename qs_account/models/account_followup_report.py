# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
from odoo import models, fields, api
from odoo.tools.misc import formatLang, format_date, get_lang
from odoo.tools.translate import _
from odoo.tools import append_content_to_html, DEFAULT_SERVER_DATE_FORMAT, html2plaintext
from odoo.exceptions import UserError
from odoo.addons.account_followup.models.account_followup_report import AccountFollowupReport as OriginalAccountFollowupReport

class AccountFollowupReport(models.AbstractModel):
    _inherit = "account.followup.report"


    @api.model
    def get_all(self, records):
        res_ids = records['ids'] if 'ids' in records else records.ids  # records come from either JS or server.action
        partner = self.env['res.partner'].browse(res_ids)
        partner = partner.with_context(allowed_company_ids=[self.env.company.id], uid=self.env.user.id)
        aml_recs = partner.unreconciled_aml_ids.sorted().filtered(lambda aml: not aml.currency_id.is_zero(aml.amount_residual_currency))
        for aml in aml_recs:
            aml.blocked = False


    @api.model
    def get_late(self, records):
        today = fields.Date.today()
        res_ids = records['ids'] if 'ids' in records else records.ids  # records come from either JS or server.action
        partner = self.env['res.partner'].browse(res_ids)
        partner = partner.with_context(allowed_company_ids=[self.env.company.id], uid=self.env.user.id)
        aml_recs = partner.unreconciled_aml_ids.sorted().filtered(lambda aml: not aml.currency_id.is_zero(aml.amount_residual_currency))
        for aml in aml_recs:
            if today <= aml.date_maturity:
                aml.blocked = True
            else:
                aml.blocked = False

    def _get_columns_name(self, options):
        res = super(AccountFollowupReport, self)._get_columns_name(options)
        if not self.env.user.has_group('qs_account.group_account_user_spec'):
            res = res[:6] + res[7:]
        return res
    
    def _get_lines(self, options, line_id=None):
        # Get date format for the lang
        partner = options.get('partner_id') and self.env['res.partner'].browse(options['partner_id']) or False
        if not partner:
            return []

        lang_code = partner.lang if self._context.get('print_mode') else self.env.user.lang or get_lang(self.env).code
        lines = []
        res = {}
        today = fields.Date.today()
        line_num = 0
        for l in partner.unreconciled_aml_ids.sorted().filtered(lambda aml: not aml.currency_id.is_zero(aml.amount_residual_currency)):
            if l.company_id == self.env.company:
                if self.env.context.get('print_mode') and l.blocked:
                    continue
                currency = l.currency_id or l.company_id.currency_id
                if currency not in res:
                    res[currency] = []
                res[currency].append(l)
        for currency, aml_recs in res.items():
            total = 0
            total_issued = 0
            columns = []
            for aml in aml_recs:
                if not aml.blocked:
                    amount = aml.amount_residual_currency if aml.currency_id else aml.amount_residual
                    date_due = format_date(self.env, aml.date_maturity or aml.move_id.invoice_date or aml.date, lang_code=lang_code)
                    total += not aml.blocked and amount or 0
                    is_overdue = today > aml.date_maturity if aml.date_maturity else today > aml.date
                    is_payment = aml.payment_id
                    if is_overdue or is_payment:
                        total_issued += not aml.blocked and amount or 0
                    if is_overdue:
                        date_due = {'name': date_due, 'class': 'color-red date', 'style': 'white-space:nowrap;text-align:center;color: red;'}
                    if is_payment:
                        date_due = ''
                    move_line_name = self._format_aml_name(aml.name, aml.move_id.ref)
                    if self.env.context.get('print_mode'):
                        move_line_name = {'name': move_line_name, 'style': 'text-align:right; white-space:normal;'}
                    amount = formatLang(self.env, amount, currency_obj=currency)
                    line_num += 1
                    expected_pay_date = format_date(self.env, aml.expected_pay_date, lang_code=lang_code) if aml.expected_pay_date else ''
                    invoice_origin = aml.move_id.invoice_origin or ''
                    if len(invoice_origin) > 43:
                        invoice_origin = invoice_origin[:40] + '...'
                    columns = [
                        format_date(self.env, aml.move_id.invoice_date or aml.date, lang_code=lang_code),
                        date_due,
                        invoice_origin,
                        move_line_name,
                        (expected_pay_date and expected_pay_date + ' ') + (aml.internal_note or ''),
                        {'name': '', 'blocked': aml.blocked},
                        amount,
                    ]
                    if self.env.context.get('print_mode'):
                        columns = columns[:4] + columns[6:]
                    else:
                        if not self.env.user.has_group('qs_account.group_account_user_spec'):
                            columns = columns[:5] + columns[6:]
                    lines.append({
                        'id': aml.id,
                        'account_move': aml.move_id,
                        'name': aml.move_id.name,
                        'caret_options': 'followup',
                        'move_id': aml.move_id.id,
                        'type': is_payment and 'payment' or 'unreconciled_aml',
                        'unfoldable': False,
                        'columns': [type(v) == dict and v or {'name': v} for v in columns],
                    })
            total_due = formatLang(self.env, total, currency_obj=currency)
            line_num += 1
            lines.append({
                'id': line_num,
                'name': '',
                'class': 'total',
                'style': 'border-top-style: double',
                'unfoldable': False,
                'level': 3,
                'columns': [{'name': v} for v in [''] * (3 if self.env.context.get('print_mode') else (4 if not self.env.user.has_group('qs_account.group_account_user_spec') else 5)) + [total >= 0 and _('Total Due') or '', total_due]],
            })
            if total_issued > 0:
                total_issued = formatLang(self.env, total_issued, currency_obj=currency)
                line_num += 1
                lines.append({
                    'id': line_num,
                    'name': '',
                    'class': 'total',
                    'unfoldable': False,
                    'level': 3,
                    'columns': [{'name': v} for v in [''] * (3 if self.env.context.get('print_mode') else (4 if not self.env.user.has_group('qs_account.group_account_user_spec') else 5)) + [_('Total Overdue'), total_issued]],
                })
            # Add an empty line after the total to make a space between two currencies
            line_num += 1
            lines.append({
                'id': line_num,
                'name': '',
                'class': '',
                'style': 'border-bottom-style: none',
                'unfoldable': False,
                'level': 0,
                'columns': [{} for col in columns],
            })
        # Remove the last empty line
        if lines:
            lines.pop()
        return lines
    
OriginalAccountFollowupReport._get_lines = AccountFollowupReport._get_lines