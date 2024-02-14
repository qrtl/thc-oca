# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re

from markupsafe import Markup

from odoo import models


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    def _render_template(self, template, values=None):
        result = super()._render_template(template, values)
        if isinstance(template, str):
            lang_match = re.search(r'lang="([^"]+)"', str(result))
            lang_code = (
                lang_match.group(1) if lang_match else "en_US"
            )  # Default to 'en_US' if not found
            view_id = self.env["ir.model.data"]._xmlid_to_res_id(
                template, raise_if_not_found=False
            )
            # If a view_id was found, search for and return the ir.ui.view record
            custom_qweb_labels = (
                self.env["custom.qweb.label"]
                .with_context(lang=lang_code)
                .sudo()
                .search(
                    [
                        "|",
                        ("template_id", "=", view_id),
                        ("related_template_ids", "in", [view_id]),
                    ]
                )
            )
            if custom_qweb_labels:
                for rec in custom_qweb_labels:
                    existing_label = ">" + rec.existing_label + "<"
                    custom_label = ">" + (rec.custom_label or "") + "<"
                    # Directly update the result with the replaced string
                    result = Markup(str(result).replace(existing_label, custom_label))
        return result
