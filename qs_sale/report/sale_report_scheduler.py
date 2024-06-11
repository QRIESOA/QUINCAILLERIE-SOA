# coding: utf-8

import base64

from odoo import models, api, fields, _


class SaleReport(models.AbstractModel):
    _name = "sale.report.scheduler"
    _description = "Sale Report Scheduler"

    @api.model
    def _cron_daily_sales_report(self):
        now = fields.Datetime.now()
        # TODO: FETCH ORDERS ONLY IN 'ORDER' STATE
        domain = [
            ("date", ">=", now.replace(hour=0, minute=0, second=1)),
            ("date", "<=", now.replace(hour=23, minute=59, second=59)),
        ]
        report_data = self.env["sale.report"].read_group(
            domain,
            ["price_total:sum", "margin:sum", "purchase_price:sum"],
            ["categ_id"],
        )
        total = {
            "turnover_total": 0,
            "margin_total": 0,
            "purchase_price_total": 0,
        }

        for data in report_data:
            total["turnover_total"] += data["price_total"]
            total["margin_total"] += data["margin"]
            total["purchase_price_total"] += data["purchase_price"]

        pdf = self.env.ref("qs_sale.report_sale_scheduler")._render_qweb_pdf(
            None, data={"values": report_data, "total": total}
        )
        mail_values = {
            "subject": _("Sales Daily Report"),
            "body_html": _("Please find attached the daily sales report."),
            "email_to": self.env["ir.config_parameter"].sudo().get_param('qs_sale.email_daily_report'),
            "attachment_ids": [
                (
                    0,
                    0,
                    {
                        "name": "daily_sales_report.pdf",
                        "type": "binary",
                        "datas": base64.b64encode(pdf[0]),
                        "mimetype": "application/pdf",
                    },
                )
            ],
        }
        mail = self.env["mail.mail"].create(mail_values)
        mail.send()
