# -*- coding: utf-8 -*
from odoo import api, fields, models


class ProdcutTemplate(models.Model):
    _inherit = 'product.template'

    product_pricelist = fields.Char('Product Pricelist')

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
        return result

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """
            Add dynamic pricelist fields
        :param allfields:
        :param attributes:
        :return:
        """
        res = super(ProdcutTemplate, self).fields_get(allfields, attributes)
        pricelists = self.get_pricelists()
        for pricelist in pricelists:
            values = {'name': 'pricelist_' + str(pricelist.get('id')),
                      'type': 'float',
                      'string': pricelist.get('name'),
                      'exportable': False,
                      'selectable': False,
                      'searchable': False}
            res['pricelist_' + str(pricelist.get('id'))] = values
        return res

    def read(self, fields=None, load='_classic_read'):
        """
            Add dynamic price value of pricelist we want to display
        :param fields:
        :param load:
        :return:
        """
        fields = list(filter(lambda f: f in self._fields.keys(), fields))
        res = super(ProdcutTemplate, self).read(fields, load)
        if self._context.get('readPricelist', False):
            pricelists = self.get_pricelists()
            pricelist_obj = self.env['product.pricelist']
            product_tmpl_obj = self.env['product.template']
            for values in res:
                if 'id' in values.keys():
                    record = product_tmpl_obj.browse(values.get('id'))
                    for pricelist in pricelists:
                        pricelist = pricelist_obj.browse(pricelist.get('id'))
                        price = pricelist.price_get(record.product_variant_id.id, 1)
                        values['pricelist_'+str(pricelist.id)] = price.get(pricelist.id)
        return res

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        fields = list(filter(lambda f: f in self._fields.keys(), fields))
        return super(ProdcutTemplate, self).read_group(domain, fields, groupby, offset, limit, orderby, lazy)

    def _update_cache(self, values, validate=True):
        values = values.items()
        values = [val for val in values if val[0] in self._fields]
        values = dict(values)
        super(ProdcutTemplate, self)._update_cache(values, validate)