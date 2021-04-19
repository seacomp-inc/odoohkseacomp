# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "limit_validation-jsi",
    'version': '12.0.1.0',
    'author':"OdooHK - jsi",
    'summary': """
        Limit sales Confirmation and Delivery validation""",
    'description': """
        Limit sales Confirmation and Delivery validation
    """,
    'depends': ['sale_stock', 'account_reports', 'quality_control'],
    'data': [
        'views/res_partner.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_view.xml',
        'views/res_config_settings_views.xml',
    ],
}
