from odoo import fields, models, api, _
from odoo.exceptions import UserError, Warning


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    # price_unit_comparison = fields.Boolean(compute="price_unit_comparison_func", default=False)
    #
    # def price_unit_comparison_func(self):
    #     msg = "Le prix unitaire de certains articles n'est pas conforme (en ROUGE), veuillez appeler votre responsable pour changer les prix. "
    #     for rec in self:
    #         if rec.price_unit == 0:
    #             raise UserError(msg)
    #             rec.price_unit_comparison = True
    #         else:
    #             rec.price_unit_comparison = False

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
