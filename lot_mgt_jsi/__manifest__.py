# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Lot Mgt. - JSI',
    'version': '1.0.1',
    'sequence': 20,
    'summary': 'Lot Management',
    'author': 'OdooHK - jsi',
    'description': """
     Lot Auto Populate
""",

    'depends': ['purchase_stock', 'mrp'],
    'data': [
        'views/views.xml',
    ],
    'installable': True,
}
