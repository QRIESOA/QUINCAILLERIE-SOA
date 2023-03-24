# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def set_default_partner(self):
        return self.env.ref("qs_sale.client_comptant")

    partner_id = fields.Many2one("res.partner", default=lambda self: self.env.ref("qs_sale.client_comptant").id)
    note_client = fields.Char(string="Note")
    can_create = fields.Boolean(string='Can create partenair', default=False, compute="_compute_can_create")

    @api.depends("name")
    def _compute_can_create(self):
        self.can_create = self.env.user.has_group("base.group_partner_manager")