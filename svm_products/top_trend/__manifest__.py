# -*- coding: utf-8 -*-
{
    'name': 'Top Trending Products',
    'category': 'Sales',
    'description': 'This app will predict products trend',
    'summary': '',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/top.result.views.xml',
        'views/top.trend.views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}