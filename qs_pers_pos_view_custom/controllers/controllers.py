# -*- coding: utf-8 -*-
# from odoo import http


# class ./qs-addons/qsPersPosViewCustom(http.Controller):
#     @http.route('/./qs-addons/qs_pers_pos_view_custom/./qs-addons/qs_pers_pos_view_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/./qs-addons/qs_pers_pos_view_custom/./qs-addons/qs_pers_pos_view_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('./qs-addons/qs_pers_pos_view_custom.listing', {
#             'root': '/./qs-addons/qs_pers_pos_view_custom/./qs-addons/qs_pers_pos_view_custom',
#             'objects': http.request.env['./qs-addons/qs_pers_pos_view_custom../qs-addons/qs_pers_pos_view_custom'].search([]),
#         })

#     @http.route('/./qs-addons/qs_pers_pos_view_custom/./qs-addons/qs_pers_pos_view_custom/objects/<model("./qs-addons/qs_pers_pos_view_custom../qs-addons/qs_pers_pos_view_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('./qs-addons/qs_pers_pos_view_custom.object', {
#             'object': obj
#         })
