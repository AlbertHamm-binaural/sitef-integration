from odoo import fields, models

class ResCompany(models.Model):
    _inherit = "res.company"
    
    username = fields.Char()
    password = fields.Char()
    idbranch = fields.Char()
    codestall = fields.Char()
    issuingbank = fields.Selection([
        ("102", "(0102) Banco de Venezuela"),
        ("104", "(0104) Banco Venezolano de Crédito"),
        ("105", "(0105) Banco Mercantil"),
        ("108", "(0108) Banco Provincial"),
        ("114", "(0114) Bancaribe"),
        ("115", "(0115) Banco Exterior"),
        ("116", "(0116) Banco Occidental de Descuento (BOD)"),
        ("128", "(0128) Banco Caroní"),
        ("134", "(0134) Bancrecer"),
        ("151", "(0151) Banco Nacional de Crédito (BNC)"),
        ("156", "(0156) 100% Banco"),
        ("157", "(0157) DelSur Banco Universal"),
        ("163", "(0163) Banco del Tesoro"),
        ("166", "(0166) Banco Agrícola de Venezuela"),
        ("172", "(0172) Bancamiga Banco Universal"),
        ("173", "(0173) Banco Activo"),
        ("174", "(0174) Banplus"),
        ("175", "(0175) Banco Bicentenario"),
        ("177", "(0177) Banco de la Fuerza Armada Nacional Bolivariana (BANFANB)")
    ])