# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CustomReportLabel(models.Model):
    _name = "custom.report.label"

    @api.model
    def _lang_get(self):
        return self.env["res.lang"].get_installed()

    name = fields.Char(compute="_compute_name", store=True, readonly=True)
    model_id = fields.Many2one("ir.model", required=True, ondelete="cascade")
    report_id = fields.Many2one("ir.actions.report")
    existing_label = fields.Char(
        required=True,
        help="Enter the label to replace.\n" "Example: 'Description'.",
    )
    custom_label = fields.Char(
        help="Input your new label.\n"
        "Example: 'New Description'. This replaces the existing label.",
    )
    active_lang_count = fields.Integer(compute="_compute_active_lang_count")
    lang = fields.Selection(
        _lang_get, string="Language", default=lambda self: self.env.lang
    )

    @api.depends("lang")
    def _compute_active_lang_count(self):
        lang_count = len(self.env["res.lang"].get_installed())
        for rec in self:
            rec.active_lang_count = lang_count

    @api.onchange("model_id")
    def _onchange_model_id(self):
        return {"domain": {"report_id": [("model", "=", self.model_id.model)]}}

    @api.depends("existing_label", "custom_label")
    def _compute_name(self):
        for record in self:
            if record.existing_label:
                record.name = (
                    f"{record.existing_label or ''} -> {record.custom_label or ''}"
                )
            else:
                record.name = False
