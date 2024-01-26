# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'QS Product',
    'version': '1.2',
    'category': 'Product/Products',
    'summary': 'Product internal machinery',
    'description': """
    Long description of module's product
    """,
    'depends': ['base','product'],
    'data': [
        'report/product_template.xml',
        'report/product_list_price.xml',
        'reports/book_rent_report.xml',
        'reports/book_rent_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
