# -*- coding: utf-8 -*-
# from odoo import http


# class ./qs-addons/qsPersContact(http.Controller):
#     @http.route('/./qs-addons/qs_pers_contact/./qs-addons/qs_pers_contact/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/./qs-addons/qs_pers_contact/./qs-addons/qs_pers_contact/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('./qs-addons/qs_pers_contact.listing', {
#             'root': '/./qs-addons/qs_pers_contact/./qs-addons/qs_pers_contact',
#             'objects': http.request.env['./qs-addons/qs_pers_contact../qs-addons/qs_pers_contact'].search([]),
#         })

#     @http.route('/./qs-addons/qs_pers_contact/./qs-addons/qs_pers_contact/objects/<model("./qs-addons/qs_pers_contact../qs-addons/qs_pers_contact"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('./qs-addons/qs_pers_contact.object', {
#             'object': obj
#         })
