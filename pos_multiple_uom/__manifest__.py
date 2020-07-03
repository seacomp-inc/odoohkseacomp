# -*- coding: utf-8 -*-
{
    'name': "POS Multiple Uom",
    'summary': 'POS multiple unit of measure',
    'category': 'Point of Sale',
    'version': '13.0.1',
    'license': "AGPL-3",
    'description': """
        With this module you can sell your products with different units of measure in POS.
        add best before field in receive picking's wizard so you can can directly add date from wizard.
    """,

    'author': "Odoo-India",

    'depends': [
        'base_automation',
        'point_of_sale',
        'product_expiry',
    ],

    'data': [
        'views/product_multiple_uom.xml',
        'security/ir.model.access.csv',
        'views/pos_multi_uom_template.xml',
        'views/product_multiple_uom_view.xml',
        'views/stock_lot_fields_view.xml',
    ],

    'installable': True,
    'auto_install': False,
}
