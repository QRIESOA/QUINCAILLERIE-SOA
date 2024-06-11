# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    "name": "QS Sales",
    "version": "1.2",
    "category": "Sales/Sales",
    "summary": "Sales internal machinery",
    "description": """
This module contains all the common features of Sales Management and eCommerce.
    """,
    "depends": [
        "sale_stock",
        "thermal_invoice",
        "qs_pers_acc",
        "pos_sale",
        "sale_margin",
        "custom_pos_receipt",
    ],
    "data": [
        # DATA
        "data/ir_cron_data.xml",
        "data/partner_data.xml",
        # REPORT
        "report/sale_report.xml",
        "report/report_stockpicking_operations.xml",
        "report/report_deliveryslip.xml",
        "report/report_invoice.xml",
        "report/sale_report_scheduler_report.xml",
        # SECURITY
        "security/ir.model.access.csv",
        "security/base_groups.xml",
        # VIEWS
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
        "views/account_move_views.xml",
        "views/res_config_views.xml",
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
    "assets": {
        "point_of_sale.assets": [
            "qs_sale/static/src/js/SaleOrderFetcher.js",
            "qs_sale/static/src/js/models.js",
            "qs_sale/static/src/js/TicketScreen.js",
        ],
        "web.assets_qweb": [
            "qs_sale/static/src/xml/pos.xml",
        ],
    },
    "license": "LGPL-3",
}
