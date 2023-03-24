# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'QS Sales',
    'version': '1.2',
    'category': 'Sales/Sales',
    'summary': 'Sales internal machinery',
    'description': """
This module contains all the common features of Sales Management and eCommerce.
    """,
    'depends': ['sale'],
    'data': [
        # 'report/sale_report_templates.xml'
        # 'security/base_groups.xml',
        'data/partner_data.xml',
        'views/sale_order_views.xml',
    ],
    'demo': [
        
    ],
    'installable': True,
    'auto_install': False,
    'assets': {
    },
    'license': 'LGPL-3',
}
