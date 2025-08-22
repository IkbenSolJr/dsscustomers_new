# -*- coding: utf-8 -*-
# from odoo import http


# class Dsscustomers(http.Controller):
#     @http.route('/dsscustomers/dsscustomers', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dsscustomers/dsscustomers/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dsscustomers.listing', {
#             'root': '/dsscustomers/dsscustomers',
#             'objects': http.request.env['dsscustomers.dsscustomers'].search([]),
#         })

#     @http.route('/dsscustomers/dsscustomers/objects/<model("dsscustomers.dsscustomers"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dsscustomers.object', {
#             'object': obj
#         })
