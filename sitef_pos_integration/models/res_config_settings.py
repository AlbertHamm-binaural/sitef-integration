from odoo import fields, models

import logging

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    username_sitef = fields.Char(related="company_id.username", string="Username", readonly=False)
    password_sitef = fields.Char(related="company_id.password", string="Password", readonly=False)
    idbranch_sitef = fields.Integer(related="company_id.idbranch", string="Id Branch", readonly=False)
    codestall_sitef = fields.Char(related="company_id.codestall", string="Code Stall", readonly=False)
    issuingbank_sitef = fields.Selection(related="company_id.issuingbank", string="Banco Emisor", readonly=False)
    url_sitef = fields.Char(related="company_id.url", string="URL", readonly=False)