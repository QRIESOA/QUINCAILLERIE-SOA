# -*- coding: utf-8 -*-

from odoo import models, fields, api
from lxml import etree

import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        result = super(SaleOrder, self).fields_view_get(
            view_id, view_type, toolbar=toolbar, submenu=submenu
        )

        _logger.info("fields_view_get called with view_type: %s", view_type)

        if view_type in ("tree", "form", "kanban", "list") and not self.env.user.has_group(
            "qs_sale_restrict.group_no_create_no_edit_sale"
        ):
            if toolbar:
                if "print" in result.get("toolbar", {}):
                    result["toolbar"]["print"] = []
                if "action" in result.get("toolbar", {}):
                    result["toolbar"]["action"] = []
            arch = etree.XML(result["arch"])
            for node in arch.xpath("//tree | //form | //kanban"):
                node.set("create", "false")
                node.set("edit", "false")
                node.set("delete", "false")
                result["arch"] = etree.tostring(arch)
        return result
