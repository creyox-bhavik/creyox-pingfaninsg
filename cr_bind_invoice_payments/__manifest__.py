# -*- coding: utf-8 -*-
{
    'name': 'Bind Payments With Invoice',
    'version': '16.0.0.1',
    'license': 'LGPL-3',
    'category': 'Accounting',
    'author': 'Creyox Technologies',
    'description': """This module helps to bind the payments with it's original invoice.""",
    'depends': ['account'],
    'demo': [
        'data/account_data.xml'
    ],
    'data': [
        'views/account_move_views.xml',
        'views/account_payment_views.xml',
        'report/report_invoice.xml',
    ],
    'qweb': [],
    "images": ["static/description/icon.png"],
    'application': True,
    'installable': True,
    'auto_install': False,
}
