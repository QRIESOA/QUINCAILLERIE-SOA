# -*- coding: utf-8 -*-
{
    'name': "qs_pers_inv",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Valisoa RAMILIJAONA",
    'website': "http://www.valisoaramilijaona.mg",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale', 'sales_team', 'stock_account', 'stock_enterprise', 'qs_pers'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'security/groups.xml',
        'views/templates.xml',
        'views/security.xml',
    ],
    # only loaded in demonstration mode

    'installable': True,
    'auto_install': False,
    'application': True,
}
