# -*- coding: utf-8 -*-
# from odoo import http


# class ./local-addons/qsPers(http.Controller):
#     @http.route('/qs_pers/qs_pers/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/qs_pers/qs_pers/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('qs_pers.listing', {
#             'root': '/qs_pers/qs_pers',
#             'objects': http.request.env['qs_pers.qs_pers'].search([]),
#         })

#     @http.route('/qs_pers/qs_pers/objects/<model("qs_pers.qs_pers"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('qs_pers.object', {
#             'object': obj
#         })
