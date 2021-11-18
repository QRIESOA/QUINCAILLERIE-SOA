# -*- coding: utf-8 -*-
# from odoo import http


# class ./local-addons/qsPers(http.Controller):
#     @http.route('/qs_pers_pos/qs_pers_pos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/qs_pers_pos/qs_pers_pos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('qs_pers_pos.listing', {
#             'root': '/qs_pers_pos/qs_pers_pos',
#             'objects': http.request.env['qs_pers_pos.qs_pers_pos'].search([]),
#         })

#     @http.route('/qs_pers_pos/qs_pers_pos/objects/<model("qs_pers_pos.qs_pers_pos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('qs_pers_pos.object', {
#             'object': obj
#         })
