# -*- coding: utf-8 -*-
{
    'name': "POS demo",
    'summary': "Point of sale demo module",
    'description': """Long description""",
    'author': "Parth Gajjar",
    'website': "http://www.example.com",
    'category': 'Point of Sale',
    'version': '14.0.1',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_assets.xml'
    ],
    'qweb': [
        'static/src/xml/pos_demo.xml'
    ],

    'assets': {
        'point_of_sale.assets': [
            'pos_demo/static/src/scss/pos_demo.scss',
            'pos_demo/static/src/js/pos_demo.js',
        ],
    }
}
