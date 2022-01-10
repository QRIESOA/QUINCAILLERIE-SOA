# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ./qs-addons/qs_pers_pos_view_custom(models.Model):
#     _name = './qs-addons/qs_pers_pos_view_custom../qs-addons/qs_pers_pos_view_custom'
#     _description = './qs-addons/qs_pers_pos_view_custom../qs-addons/qs_pers_pos_view_custom'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
