from odoo import fields, models, api, _
from odoo.exceptions import UserError, Warning


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, values):
        msg = "Le prix unitaire de certains articles n'est pas conforme (en ROUGE), veuillez appeler votre responsable pour changer les prix. "
        if self.price_unit != 0:
            print("ato create true")
            raise UserError(msg)
        return super(SaleOrderLineInherit, self).create(values)

    def write(self, values):
        msg = "Le prix unitaire de certains articles n'est pas conforme (en ROUGE), veuillez appeler votre responsable pour changer les prix. "
        if self.price_unit != 0:
            print("ato write true")
            raise UserError(msg)
        return super(SaleOrderLineInherit, self).write(values)
