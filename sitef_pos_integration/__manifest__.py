{
    "name": "Binaural Sitef",
    "license": "LGPL-3",
    "author": "Binauraldev",
    "website": "https://binauraldev.com/",
    "category": "Accounting/Accounting",
    "version": "1.0",
    "depends": [
        "base",
        "point_of_sale",
    ],
    
    "images": ["static/description/icon.png"],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings.xml",
        "views/report_sitef.xml",
        "wizard/pos_report_sitef.xml",
        "report/cash_report.xml",
    ],
    
    "assets": {
        "point_of_sale.assets": [
            "sitef_pos_integration/static/src/js/payment_control.js",
            "sitef_pos_integration/static/src/js/CambioForm.js",
            "sitef_pos_integration/static/src/js/ValidarPagoMovilForm.js",
            "sitef_pos_integration/static/src/js/ValidarTransferenciaForm.js",

            "sitef_pos_integration/static/src/xml/payment_control.xml",
            "sitef_pos_integration/static/src/xml/CambioForm.xml",
            "sitef_pos_integration/static/src/xml/ValidarPagoMovilForm.xml",
            "sitef_pos_integration/static/src/xml/ValidarTransferenciaForm.xml",

            "sitef_pos_integration/static/src/css/*.css",
        ],
    },
    "binaural": True,
}