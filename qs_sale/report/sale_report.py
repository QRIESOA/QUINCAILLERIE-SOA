# coding: utf-8

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    purchase_price = fields.Float("Cost")

    def _select_additional_fields(self, fields):
        fields["purchase_price"] = (
            ", SUM(l.purchase_price / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS purchase_price"
        )
        return super()._select_additional_fields(fields)
