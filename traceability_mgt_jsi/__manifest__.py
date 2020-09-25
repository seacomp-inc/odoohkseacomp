# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Traceability Mgt. - JSI',
    'version': '1.0.1',
    'sequence': 20,
    'summary': 'Traceability Management',
    'author': 'OdooHK - jsi',
    'description': """
     
""",

    'depends': ['sale_stock', 'purchase', 'mrp'],
    'data': [
        'views/sale.xml',
        'views/stock.xml',
        'views/purchase.xml',
        'views/mrp_production.xml',
    ],
    'installable': True,
}
