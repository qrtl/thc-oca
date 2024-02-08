# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re

from odoo import api, models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    @api.model
    def _render_qweb_html(self, report_ref, docids, data=None):
        html, render_type = super(IrActionsReport, self)._render_qweb_html(
            report_ref, docids, data
        )
        html_content_str = html.decode("utf-8")
        report = self._get_report(report_ref)
        # Extract the language code from the HTML content
        lang_match = re.search(r'data-oe-lang="([^"]+)"', html_content_str)
        lang_code = (
            lang_match.group(1) if lang_match else "en_US"
        )  # Default to 'en_US' if not found
        custom_report_labels = (
            self.env["custom.report.label"]
            .with_context(lang=lang_code)
            .search(
                [
                    ("model_id.model", "=", report.model),
                    "|",
                    ("report_id", "=", report.id),
                    ("report_id", "=", False),
                ]
            )
        )
        if custom_report_labels:
            for rec in custom_report_labels:
                html_content_str = html_content_str.replace(
                    ">" + rec.existing_label + "<", ">" + (rec.custom_label or "") + "<"
                )
        html = html_content_str.encode()
        return html, render_type
