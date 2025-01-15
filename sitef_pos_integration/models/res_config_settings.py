from odoo import fields, models

import logging

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    username = fields.Char(related="company_id.username", string="Username", readonly=False)
    password = fields.Char(related="company_id.password", string="Password", readonly=False)
    idbranch = fields.Integer(related="company_id.idbranch", string="Id Branch", readonly=False)
    codestall = fields.Char(related="company_id.codestall", string="Code Stall", readonly=False)
    issuingbank = fields.Selection(related="company_id.issuingbank", string="Banco Emisor", readonly=False)
    url = fields.Char(related="company_id.url", string="URL", readonly=False)