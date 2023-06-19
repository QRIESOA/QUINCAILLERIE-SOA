# -*- coding: utf-8 -*-
from locale import currency
from odoo import models, fields, api


class qs_pers_acc(models.Model):
    _inherit = "account.move"
    mobile_phone = fields.Char(
        "Mobile phone", related="partner_id.phone", readonly=True
    )

    email_partner = fields.Char("Email", related="partner_id.email", readonly=True)

    product_marge_ids = fields.One2many(
        "product.item.marge",
        "move_id",
    )

    def compute_product_product_ids(self):
        for rec in self:
            rec.product_marge_ids = [(5, 0, 0)]
            marge_ids = []
            if rec.invoice_line_ids:
                for line in rec.invoice_line_ids:
                    for variant in line.product_id.product_variant_ids:
                        variant._compute_pricelists()
                    marge_ids.append((0, 0, {"product_id": line.product_id.id}))

            rec.product_marge_ids = marge_ids


class ProductTemplateInherit(models.Model):
    transport = fields.Float(string="Transport")
    _inherit = "product.template"
    pricelist_ex_ids = fields.One2many(
        "product.pricelist.item", "product_tmpl_id", string="Product pricelist"
    )


class ProductProductInherit(models.Model):
    _inherit = "product.product"

    transport = fields.Float(
        string="Transport", related="product_tmpl_id.transport", default=0
    )
    tmpl_price = fields.Float(
        string="Prix d'achat",
        related="product_tmpl_id.standard_price",
        default=0,
        store=True,
    )
    pc_det = fields.Float(
        string="PV DET", compute="_compute_pricelists", default=0, store=True
    )
    pc_det_marge = fields.Float(
        string="%PV DET", compute="_compute_pc_det_marge", default=0, store=True
    )
    pc_gros = fields.Float(
        string="PV GROS", compute="_compute_pricelists", default=0, store=True
    )
    pc_gros_marge = fields.Float(
        string="%PV GROS", compute="_compute_pc_gros_marge", default=0, store=True
    )
    pc_cr1 = fields.Float(
        string="PV CR1", compute="_compute_pricelists", default=0, store=True
    )
    pc_cr1_marge = fields.Float(
        string="%PV CR1", compute="_compute_pc_cr1_marge", default=0, store=True
    )
    pc_cr2 = fields.Float(
        string="PV CR2", compute="_compute_pricelists", default=0, store=True
    )
    pc_cr2_marge = fields.Float(
        string="%PV CR2", compute="_compute_pc_cr2_marge", default=0, store=True
    )
    pc_cr3 = fields.Float(
        string="PV CR3", compute="_compute_pricelists", default=0, store=True
    )
    pc_cr3_marge = fields.Float(
        string="%PV CR3", compute="_compute_pc_cr3_marge", default=0, store=True
    )
    pc_cr4 = fields.Float(
        string="PV CR4", compute="_compute_pricelists", default=0, store=True
    )
    pc_cr4_marge = fields.Float(
        string="%PV CR4", compute="_compute_pc_cr4_marge", default=0, store=True
    )

    @api.depends(
        "product_tmpl_id",
        "product_tmpl_id.pricelist_ex_ids",
        "product_tmpl_id.pricelist_ex_ids.fixed_price",
    )
    def _compute_pricelists(self):
        for record in self:
            ids = record.product_tmpl_id.pricelist_ex_ids.pricelist_id.mapped("id")
            if 1 not in ids:
                record.pc_det = 0
                record.pc_det_marge = 0
            if 8 not in ids:
                record.pc_gros = 0
                record.pc_gros_marge = 0
            if 7 not in ids:
                record.pc_cr1 = 0
                record.pc_cr1_marge = 0
            if 4 not in ids:
                record.pc_cr2_marge = 0
                record.pc_cr2 = 0
            if 5 not in ids:
                record.pc_cr3_marge = 0
                record.pc_cr3 = 0
            if 6 not in ids:
                record.pc_cr4_marge = 0
                record.pc_cr4 = 0
            for item in record.product_tmpl_id.pricelist_ex_ids:
                if item.pricelist_id.id == 1:
                    record.pc_det = item.fixed_price
                elif item.pricelist_id.id == 8:
                    record.pc_gros = item.fixed_price
                elif item.pricelist_id.id == 7:
                    record.pc_cr1 = item.fixed_price
                elif item.pricelist_id.id == 4:
                    record.pc_cr2 = item.fixed_price
                elif item.pricelist_id.id == 5:
                    record.pc_cr3 = item.fixed_price
                elif item.pricelist_id.id == 6:
                    record.pc_cr4 = item.fixed_price

    @api.depends("tmpl_price", "pc_det")
    def _compute_pc_det_marge(self):
        for record in self:
            if record.tmpl_price:
                if record.tmpl_price > 0:
                    record.pc_det_marge = (
                        record.pc_det - (record.tmpl_price + record.transport)
                    ) / (record.tmpl_price + record.transport)

    @api.depends("tmpl_price", "pc_gros")
    def _compute_pc_gros_marge(self):
        for record in self:
            if record.tmpl_price:
                if record.tmpl_price > 0:
                    record.pc_gros_marge = (
                        record.pc_gros - (record.tmpl_price + record.transport)
                    ) / (record.tmpl_price + record.transport)

    @api.depends("tmpl_price", "pc_cr1")
    def _compute_pc_cr1_marge(self):
        for record in self:
            if record.tmpl_price:
                if record.tmpl_price > 0:
                    record.pc_cr1_marge = (
                        record.pc_cr1 - (record.tmpl_price + record.transport)
                    ) / (record.tmpl_price + record.transport)

    @api.depends("tmpl_price", "pc_cr2")
    def _compute_pc_cr2_marge(self):
        for record in self:
            if record.tmpl_price:
                if record.tmpl_price > 0:
                    record.pc_cr2_marge = (
                        record.pc_cr2 - (record.tmpl_price + record.transport)
                    ) / (record.tmpl_price + record.transport)

    @api.depends("tmpl_price", "pc_cr3")
    def _compute_pc_cr3_marge(self):
        for record in self:
            if record.tmpl_price:
                if record.tmpl_price > 0:
                    record.pc_cr3_marge = (
                        record.pc_cr3 - (record.tmpl_price + record.transport)
                    ) / (record.tmpl_price + record.transport)

    @api.depends("tmpl_price", "pc_cr4")
    def _compute_pc_cr4_marge(self):
        for record in self:
            if record.tmpl_price:
                if record.tmpl_price > 0:
                    record.pc_cr4_marge = (
                        record.pc_cr4 - (record.tmpl_price + record.transport)
                    ) / (record.tmpl_price + record.transport)


class ItemMarge(models.Model):
    _name = "product.item.marge"

    product_id = fields.Many2one("product.product")
    move_id = fields.Many2one("account.move")

    transport = fields.Float(
        string="Transport", related="product_id.product_tmpl_id.transport", default=0
    )
    tmpl_price = fields.Float(
        string="Prix d'achat",
        related="product_id.product_tmpl_id.standard_price",
    )
    pc_det = fields.Float(
        string="PV DET",
        related="product_id.pc_det",
    )
    pc_det_marge = fields.Float(
        string="%PV DET",
        related="product_id.pc_det_marge",
    )
    pc_gros = fields.Float(
        string="PV GROS",
        related="product_id.pc_gros",
    )
    pc_gros_marge = fields.Float(
        string="%PV GROS",
        related="product_id.pc_gros_marge",
    )
    pc_cr1 = fields.Float(
        string="PV CR1",
        related="product_id.pc_cr1",
    )
    pc_cr1_marge = fields.Float(
        string="%PV CR1",
        related="product_id.pc_cr1_marge",
    )
    pc_cr2 = fields.Float(
        string="PV CR2",
        related="product_id.pc_cr2",
    )
    pc_cr2_marge = fields.Float(
        string="%PV CR2",
        related="product_id.pc_cr2_marge",
    )
    pc_cr3 = fields.Float(
        string="PV CR3",
        related="product_id.pc_cr3",
    )
    pc_cr3_marge = fields.Float(
        string="%PV CR3",
        related="product_id.pc_cr3_marge",
    )
    pc_cr4 = fields.Float(
        string="PV CR4",
        related="product_id.pc_cr4",
    )
    pc_cr4_marge = fields.Float(
        string="%PV CR4",
        related="product_id.pc_cr4_marge",
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="product_id.currency_id",
    )
