# -*- coding: utf-8 -*-

{
    'name': 'Fetch Purchase Orders',
    'version':  '20.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Fetch Purchase Orders""",
    'description': """Fetch Purchase Orders""",
    'sequence': -10,
    'category': 'Fetch Purchase Orders',
    'application': True,
    'installable': True,
    'depends': ['base','purchase'],
    'data': [
        "security/ir.access.csv",
        "wizard/purchase_order_wizard_views.xml",
        "views/purchase_order_views.xml",

    ]
}
