# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta


class qs_pers_acc(models.Model):
    _inherit = 'account.move'

    mobile_phone = fields.Char(
        'Mobile phone',
        related='partner_id.phone',
        readonly=True)
    for_price_list_ids = fields.One2many('account.move.line', 'move_id', string='Pricelist reference',
                                         copy=False, readonly=True,
                                         states={'draft': [('readonly', False)]}, compute="_price_to_invoice_line_rec")

    @api.depends('invoice_line_ids')
    def _price_to_invoice_line_rec(self):
        for record in self:
            record.for_price_list_ids = record.invoice_line_ids

    email_partner = fields.Char(
        'Email',
        related='partner_id.email',
        readonly=True)


class AccountMoveLineInherited(models.Model):
    _inherit = 'account.move.line'
    price_unit_qs = fields.Float(string="P.A", compute='_get_price_unii_qs')

    @api.depends('price_unit')
    def _get_price_unii_qs(self):
        for record in self:
            if record.price_unit:
                record.price_unit_qs = record.price_unit
            else:
                record.price_unit_qs = 0

    transport = fields.Float(string="Transport", compute='_get_transport')

    @api.depends('product_id')
    def _get_transport(self):
        for record in self:
            if record.product_id.transport:
                record.transport = record.product_id.transport
            else:
                record.transport = 0

    pv_det = fields.Float(string='PV DET', compute='_get_pv_det', readonly=0, index=True)
    pv_det_marge = fields.Float(string='% PV DET', compute='_get_marge_pv_det')

    @api.depends('product_id')
    def _get_pv_det(self):
        for record in self:
            pricelist = self.env['product.pricelist'].search([('name', '=', 'PV DET')])
            if pricelist:
                # print(pricelist.name)
                for rec in pricelist.item_ids:
                    if record.product_id.id == rec.product_tmpl_id.id:
                        record.pv_det = rec.fixed_price
                        break
                    else:
                        record.pv_det = 0
            else:
                record.pv_det = 0

    @api.depends('pv_det')
    def _get_marge_pv_det(self):
        for record in self:
            if record.price_unit_qs != 0 and record.pv_det != 0:
                denom = float(record.price_unit_qs)
                num = (record.pv_det - record.price_unit_qs)
                record.pv_det_marge = (num / denom)
            else:
                record.pv_det_marge = 0

    pv_gros = fields.Float(string='PV GROS', compute='_get_pv_gros', readonly=0, index=True)
    pv_gros_marge = fields.Float(string='% PV GROS', compute='_get_marge_pv_gros')

    @api.depends('product_id')
    def _get_pv_gros(self):
        for record in self:
            pricelist = self.env['product.pricelist'].search([('name', '=', 'PV GROS')])
            if pricelist:
                # print(pricelist.name)
                for rec in pricelist.item_ids:
                    if record.product_id.id == rec.product_tmpl_id.id:
                        record.pv_gros = rec.fixed_price
                        break
                    else:
                        record.pv_gros = 0
            else:
                record.pv_gros = 0

    @api.depends('pv_gros')
    def _get_marge_pv_gros(self):
        for record in self:
            if record.price_unit_qs != 0 and record.pv_gros != 0:
                denom = float(record.price_unit_qs)
                num = (record.pv_gros - record.price_unit_qs)
                record.pv_gros_marge = (num / denom)
            else:
                record.pv_gros_marge = 0

    pv_cr1 = fields.Float(string='PV CR1', compute='_get_pv_cr1', readonly=0, index=True)
    pv_cr1_marge = fields.Float(string='% PV CR1', compute='_get_marge_pv_cr1', index=True)

    @api.depends('product_id')
    def _get_pv_cr1(self):
        for record in self:
            pricelist = self.env['product.pricelist'].search([('name', '=', 'PV CR1')])
            if pricelist:
                # print(pricelist.name)
                for rec in pricelist.item_ids:
                    if record.product_id.id == rec.product_tmpl_id.id:
                        record.pv_cr1 = rec.fixed_price
                        break
                    else:
                        record.pv_cr1 = 0
            else:
                record.pv_cr1 = 0

    @api.depends('pv_cr1')
    def _get_marge_pv_cr1(self):
        for record in self:
            if record.price_unit_qs != 0 and record.pv_cr1 != 0:
                denom = float(record.price_unit_qs)
                num = (record.pv_cr1 - record.price_unit_qs)
                record.pv_cr1_marge = (num / denom)
            else:
                record.pv_cr1_marge = 0

    pv_cr2 = fields.Float(string='PV CR2', compute='_get_pv_cr2', readonly=0, index=True)
    pv_cr2_marge = fields.Float(string='% PV CR2', compute='_get_marge_pv_cr2')

    @api.depends('product_id')
    def _get_pv_cr2(self):
        for record in self:
            pricelist = self.env['product.pricelist'].search([('name', '=', 'PV CR2')])
            if pricelist:
                # print(pricelist.name)
                for rec in pricelist.item_ids:
                    if record.product_id.id == rec.product_tmpl_id.id:
                        record.pv_cr2 = rec.fixed_price
                        break
                    else:
                        record.pv_cr2 = 0
            else:
                record.pv_cr2 = 0

    @api.depends('pv_cr2')
    def _get_marge_pv_cr2(self):
        for record in self:
            if record.price_unit_qs != 0 and record.pv_cr2 != 0:
                denom = float(record.price_unit_qs)
                num = (record.pv_cr2 - record.price_unit_qs)
                record.pv_cr2_marge = (num / denom)
            else:
                record.pv_cr2_marge = 0

    pv_cr3 = fields.Float(string='PV CR3', compute='_get_pv_cr3', readonly=0, index=True)
    pv_cr3_marge = fields.Float(string='% PV CR3', compute='_get_marge_pv_cr3')

    @api.depends('product_id')
    def _get_pv_cr3(self):
        for record in self:
            pricelist = self.env['product.pricelist'].search([('name', '=', 'PV CR3')])
            if pricelist:
                # print(pricelist.name)
                for rec in pricelist.item_ids:
                    if record.product_id.id == rec.product_tmpl_id.id:
                        record.pv_cr3 = rec.fixed_price
                        break
                    else:

                        record.pv_cr3 = 0
            else:
                record.pv_cr3 = 0

    @api.depends('pv_cr3')
    def _get_marge_pv_cr3(self):
        for record in self:
            if record.price_unit_qs != 0 and record.pv_cr3 != 0:
                denom = float(record.price_unit_qs)
                num = (record.pv_cr3 - record.price_unit_qs)
                record.pv_cr3_marge = (num / denom)
            else:
                record.pv_cr3_marge = 0

    pv_cr4 = fields.Float(string='PV CR4', compute='_get_pv_cr4', readonly=0, index=True)
    pv_cr4_marge = fields.Float(string='% PV CR4', compute='_get_marge_pv_cr4')

    @api.depends('product_id')
    def _get_pv_cr4(self):
        for record in self:
            pricelist = self.env['product.pricelist'].search([('name', '=', 'PV CR4')])
            if pricelist:
                # print(pricelist.name)
                for rec in pricelist.item_ids:
                    if record.product_id.id == rec.product_tmpl_id.id:
                        record.pv_cr4 = rec.fixed_price
                        break
                    else:
                        record.pv_cr4 = 0
            else:
                record.pv_cr4 = 0

    @api.depends('pv_cr4')
    def _get_marge_pv_cr4(self):
        for record in self:
            if record.price_unit_qs != 0 and record.pv_cr4 != 0:
                denom = float(record.price_unit_qs)
                num = (record.pv_cr4 - record.price_unit_qs)
                record.pv_cr4_marge = (num / denom)
            else:
                record.pv_cr4_marge = 0


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'
    transport = fields.Float(string="Transport")
