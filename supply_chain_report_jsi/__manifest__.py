# -*- coding: utf-8 -*-
{
    'name': "supply Chain Report-jsi",

    'summary': """
        supply Chain Report-jsi""",

    'description': """
        supply Chain Report-jsi
    """,

    'depends': ['purchase','stock','sale_margin', 'sale'],

    'data': [
        'views/stock_move_views.xml',
        'views/sale_order_line_views.xml',
        'actions/base_automation.xml',
    ],
}
