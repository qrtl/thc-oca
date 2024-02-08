# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CustomReportLabel(models.Model):
    _name = "custom.report.label"

    name = fields.Char(required=True)
    model_id = fields.Selection(
        selection="_list_all_models", string="Model", required=True
    )
    template_id = fields.Many2one("ir.actions.report")
    existing_label = fields.Char(
        help="Enter the label to replace, including '>' and '<'.\n"
        "Example: '>Description<'."
    )
    custom_label = fields.Char(
        help="Input your new label, including symbols.\n"
        "Example: '>New Description<'. This replaces the existing label."
    )

    @api.model
    def _list_all_models(self):
        lang = self.env.lang or "en_US"
        self._cr.execute(
            "SELECT model, COALESCE(name->>%s, name->>'en_US') FROM ir_model ORDER BY 2",
            [lang],
        )
        vals = self._cr.fetchall()
        return vals

    @api.onchange("model_id")
    def _onchange_model_id(self):
        return {"domain": {"template_id": [("model", "=", self.model_id)]}}
