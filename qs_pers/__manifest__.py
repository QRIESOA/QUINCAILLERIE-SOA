# -*- coding: utf-8 -*-
{
    'name': "qs_pers",

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
    'depends': ['base', 'sale', 'sale_stock', 'stock_account', 'payment'],

    # always loaded
    'data': [
        'data/paper_format.xml',
        'views/views.xml',
        'views/templates.xml',
        'report/report_with_price.xml',
        'report/sale_report_inherit.xml',
        'report/sale_report.xml',
        'report/A7_paperformat.xml',
        'report/small_external_layout.xml'
    ],
    # only loaded in demonstration mode
    'qweb': [],
    'demo': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
