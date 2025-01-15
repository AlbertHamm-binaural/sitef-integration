from odoo import models, fields, api
import hashlib
import logging

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = "pos.config"

    username = fields.Char(related="company_id.username", string="Username", readonly=False)
    password = fields.Char(related="company_id.password", string="Password", readonly=False)
    idbranch = fields.Integer(related="company_id.idbranch", string="Id Branch", readonly=False)
    codestall = fields.Char(related="company_id.codestall", string="Code Stall", readonly=False)
    issuingbank = fields.Selection(related="company_id.issuingbank", string="Banco Emisor", readonly=False)
    url = fields.Char(related="company_id.url", string="URL", readonly=False)
    encrypted_password = fields.Char(string="Encrypted Password", compute="_encrypted_password")
    
    @api.depends('password')
    def _encrypted_password(self):
        for record in self:
            if record.password:
                record.encrypted_password = hashlib.md5(record.password.encode()).hexdigest()
            else:
                record.encrypted_password = ''
    
    