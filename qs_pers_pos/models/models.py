# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from datetime import timedelta
from datetime import date

from functools import partial

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

from odoo import models, fields, api


class qs_pers_pos(models.Model):
    _inherit = 'pos.order'

    def _prepare_invoice_vals(self):
        to_day = date.today() + timedelta(days=60)
        timezone = pytz.timezone(self._context.get('tz') or self.env.user.tz or 'UTC')
        invoice_vals = super(qs_pers_pos, self)._prepare_invoice_vals()
        invoice_vals['invoice_date_due'] = to_day
        return invoice_vals
