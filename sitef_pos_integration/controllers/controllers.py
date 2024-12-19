# -*- coding: utf-8 -*-
# from odoo import http


# class SitefPosIntegration(http.Controller):
#     @http.route('/sitef_pos_integration/sitef_pos_integration', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sitef_pos_integration/sitef_pos_integration/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sitef_pos_integration.listing', {
#             'root': '/sitef_pos_integration/sitef_pos_integration',
#             'objects': http.request.env['sitef_pos_integration.sitef_pos_integration'].search([]),
#         })

#     @http.route('/sitef_pos_integration/sitef_pos_integration/objects/<model("sitef_pos_integration.sitef_pos_integration"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sitef_pos_integration.object', {
#             'object': obj
#         })
