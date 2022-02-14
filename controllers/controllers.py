# -*- coding: utf-8 -*-
from odoo import http

# class Itsm(http.Controller):
#     @http.route('/itsm/itsm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/itsm/itsm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('itsm.listing', {
#             'root': '/itsm/itsm',
#             'objects': http.request.env['itsm.itsm'].search([]),
#         })

#     @http.route('/itsm/itsm/objects/<model("itsm.itsm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('itsm.object', {
#             'object': obj
#         })