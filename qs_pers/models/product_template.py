from odoo import fields, models, api


class ModelName(models.Model):
    _inherit = 'product.template'
    _description = 'Description'

    available_in_pos = fields.Boolean(string='Available in POS',
                                      help='Check if you want this product to appear in the Point of Sale.',
                                      default=False)
    repere = fields.Char(
        string='Repère',
        required=False)

    detail_price = fields.Monetary(
        string='PV DET(MGA)',
        compute='_get_pv_det')

    def _get_pv_det(self):
        for record in self:
            pv_det = 0
            pricelist = record.env['product.pricelist.item'].search([
                '|', ('product_tmpl_id', '=', record.id), ('product_id', 'in', record.product_variant_ids.ids)])
            for rec in pricelist:
                if rec.pricelist_id.display_name == 'PV DET (MGA)':
                    pv_det = rec.fixed_price
                    break
                else:
                    pv_det = 0
            record.detail_price = pv_det
