# -*- coding: utf-8 -*-
{
    'name': "mrr_jsi",

    'summary': """
        mrr_jsi""",

    'description': """
        mrr_jsi
    """,

    'depends': ['purchase','stock','mrp'],

    # always loaded
    'data': [
        'views/mrp_bom_view.xml',
        'report/mrp_report_bom_structure.xml',
        'report/mrp_report_views_main.xml',
        
    ],
}
