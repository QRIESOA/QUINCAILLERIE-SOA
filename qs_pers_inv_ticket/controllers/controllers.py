# -*- coding: utf-8 -*-
# from odoo import http


# class ./qs-addons/qsPersInvTicket(http.Controller):
#     @http.route('/./qs-addons/qs_pers_inv_ticket/./qs-addons/qs_pers_inv_ticket/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/./qs-addons/qs_pers_inv_ticket/./qs-addons/qs_pers_inv_ticket/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('./qs-addons/qs_pers_inv_ticket.listing', {
#             'root': '/./qs-addons/qs_pers_inv_ticket/./qs-addons/qs_pers_inv_ticket',
#             'objects': http.request.env['./qs-addons/qs_pers_inv_ticket../qs-addons/qs_pers_inv_ticket'].search([]),
#         })

#     @http.route('/./qs-addons/qs_pers_inv_ticket/./qs-addons/qs_pers_inv_ticket/objects/<model("./qs-addons/qs_pers_inv_ticket../qs-addons/qs_pers_inv_ticket"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('./qs-addons/qs_pers_inv_ticket.object', {
#             'object': obj
#         })
