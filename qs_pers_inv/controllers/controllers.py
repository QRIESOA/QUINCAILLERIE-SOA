# -*- coding: utf-8 -*-
# from odoo import http


# class ./local-addons/qsPers(http.Controller):
#     @http.route('/qs_pers_inv/qs_pers_inv/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/qs_pers_inv/qs_pers_inv/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('qs_pers_inv.listing', {
#             'root': '/qs_pers_inv/qs_pers_inv',
#             'objects': http.request.env['qs_pers_inv.qs_pers_inv'].search([]),
#         })

#     @http.route('/qs_pers_inv/qs_pers_inv/objects/<model("qs_pers_inv.qs_pers_inv"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('qs_pers_inv.object', {
#             'object': obj
#         })
