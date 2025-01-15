from odoo import models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def button_enviar(self, **kwargs):
        print("Hello")
        pass