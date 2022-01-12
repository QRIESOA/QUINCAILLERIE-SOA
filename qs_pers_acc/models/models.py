# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta


class qs_pers_acc(models.Model):
    _inherit = 'account.move'

    mobile_phone = fields.Char(
        'Mobile phone',
        related='partner_id.phone',
        readonly=True)

    email_partner = fields.Char(
        'Email',
        related='partner_id.email',
        readonly=True)


class AccountMoveLineInherited(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def get_pricelists(self):
        """
        Get pricelists which we want to display in product list
        :return: dict : dictionary with pricelist id and name
        """
        pricelists = self.env['product.pricelist'].search([])
        result = list()
        for pricelist in pricelists:
            values = {'id': pricelist.id, 'name': pricelist.name, 'display': pricelist.display_in_products}
            result.append(values)
        print(result)
        return result


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'
    transport = fields.Float(string="Transport")
