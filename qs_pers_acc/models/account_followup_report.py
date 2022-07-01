# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from collections import OrderedDict
from datetime import datetime as dt


def filtre(data):
    ordered = dict(sorted(data.items(), key=lambda item: item[1]))
    sorte = ordered.keys()
    return list(sorte)


class AccountFollowupReportInherit(models.AbstractModel):
    _inherit = "account.followup.report"

    def _get_lines(self, options, line_id=None):
        res = super(AccountFollowupReportInherit, self)._get_lines(options, line_id)
        result = []
        date_null = []
        date_not_null = {}
        for index, a in enumerate(res):
            x = a.get("columns", [])
            try:
                date_echeance = x[1]["name"]
                date_echeance = str(date_echeance).replace("/", "-")
                date_object = dt.strptime(date_echeance, "%d-%m-%Y").date()
                date_not_null[index] = date_object
            except Exception as e:
                date_null.append(index)
        list_sorted = filtre(date_not_null)
        for a in date_null:
            list_sorted.append(a)
        for key in list_sorted:
            result.append(res[key])
        return result
