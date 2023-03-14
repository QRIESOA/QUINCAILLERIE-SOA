# -*- coding: utf-8 -*-

{
    "name": "SQ Account",
    "version": "0.1",
    "sequence": 100,
    "category": "Account/Account",
    "author": "Nexources",
    "website": "https://www.nexources.com/",
    "summary": "Track every user operation",

    "depends": [
        'account', "account_followup", "qs_pers_acc",
    ],
    "data": [
        # data

        # security
        'security/account_security.xml',
        # views

        'views/account_move_views.xml',

        # wizard

        # report
        'report/report_invoice.xml'
    ],
    
    'installable': True,
    'auto_install': False,
    'application': False,

    "assets": {
        "web.assets_backend": [
            "qs_account/static/src/js/form_no_edit.js"
        ]
    }
}
