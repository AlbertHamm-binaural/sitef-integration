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
    "data": [

    ],
    
    "images": ["static/description/icon.png"],
    "application": True,
    "assets": {
        "point_of_sale.assets": [
            "sitef_pos_integration/static/src/js/*.js",
            "sitef_pos_integration/static/src/xml/*.xml",
            "sitef_pos_integration/static/src/css/*.css",
        ],
    },
    "binaural": True,
}