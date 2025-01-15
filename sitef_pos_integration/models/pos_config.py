from odoo import models, fields, api
import hashlib
import logging

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = "pos.config"

    username_sitef = fields.Char(related="company_id.username_sitef", string="Username", readonly=False)
    password_sitef = fields.Char(related="company_id.password_sitef", string="Password", readonly=False)
    idbranch_sitef = fields.Integer(related="company_id.idbranch_sitef", string="Id Branch", readonly=False)
    codestall_sitef = fields.Char(related="company_id.codestall_sitef", string="Code Stall", readonly=False)
    issuingbank_sitef = fields.Selection(related="company_id.issuingbank_sitef", string="Banco Emisor", readonly=False)
    url_sitef = fields.Char(related="company_id.url_sitef", string="URL", readonly=False)
    encrypted_password = fields.Char(string="Encrypted Password", compute="_encrypted_password")
    
    @api.depends('password')
    def _encrypted_password(self):
        for record in self:
            if record.password:
                record.encrypted_password = hashlib.md5(record.password.encode()).hexdigest()
            else:
                record.encrypted_password = ''
    
    