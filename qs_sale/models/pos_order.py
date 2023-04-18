# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from datetime import timedelta
from functools import partial
from itertools import groupby

import psycopg2
import pytz
import re

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero, float_round, float_repr, float_compare
from odoo.exceptions import ValidationError, UserError
from odoo.http import request
from odoo.osv.expression import AND
import base64

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"

    note_client = fields.Char(string="Note", compute="_compute_note_client", store=True)
    
    
    @api.depends('lines')
    def _compute_note_client(self):
        for rec in self:
            list_note_client = []
            if rec.lines and rec.lines.mapped('sale_order_origin_id'):
                list_note_client = list(set(rec.lines.mapped('sale_order_origin_id').filtered(lambda so: so.note_client != "" and so.note_client != False).mapped('note_client')))
            if list_note_client:
                rec.note_client = ', '.join(list_note_client)
            else:
                rec.note_client = ''

    def _prepare_invoice_vals(self):
        res = super(PosOrder, self)._prepare_invoice_vals()
        list_note_client = list(set(self.lines.mapped('sale_order_origin_id').filtered(lambda so: so.note_client != "" or so.note_client != False).mapped('note_client')))
        if list_note_client:
            note_client = ', '.join(list_note_client)
            res['note_client'] = note_client
        return res
    
    @api.model
    def _order_fields(self, ui_order):
        fields = super(PosOrder, self)._order_fields(ui_order)
        fields['note_client'] = ui_order.get('note_client', False)
        return fields
    
    def _export_for_ui(self, order):
        result = super(PosOrder, self)._export_for_ui(order)
        result.update({
            'note_client': order.note_client,
        })
        return result