from odoo import fields, models, api


class ModelName(models.Model):
    _inherit = 'stock.move.line'
    ticket_number_pos = fields.Many2one('pos.order', 'Réf commande PDV', related='picking_id.pos_order_id')
    ticket_number_sale = fields.Many2one('sale.order', 'Note d\'achat PDV',
                                         related='picking_id.pos_order_id.lines.sale_order_origin_id')
    ticket_number_sale_stock = fields.Many2one('sale.order', 'Note d\'achat VENTE',
                                               related='picking_id.sale_id')
    ticket_number_invoice = fields.Many2many('account.move', string='Facture VENTE',
                                             related='picking_id.sale_id.invoice_ids')
