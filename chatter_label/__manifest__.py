# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Chatter Label - JSI',
    'version': '1.0.1',
    'category': 'mail',
    'sequence': 20,
    'summary': 'Change Chatter Label',
    'description': """
""",

    'depends': ['mail'],
    'data': [
        'views/chatter_label.xml',
    ],
    'installable': True,
    'qweb': ['static/src/xml/chatter_label.xml'],
}
