# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CustomQwebLabel(models.Model):
    _name = "custom.qweb.label"

    @api.model
    def _lang_get(self):
        return self.env["res.lang"].get_installed()

    name = fields.Char(compute="_compute_name", store=True, readonly=True)
    template_id = fields.Many2one(
        "ir.ui.view", domain=[("type", "=", "qweb")], required=True
    )
    related_template_ids = fields.Many2many(
        "ir.ui.view", compute="_compute_related_template_ids", store=True
    )
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

    @api.depends("existing_label", "custom_label")
    def _compute_name(self):
        for record in self:
            if record.existing_label:
                record.name = (
                    f"{record.existing_label or ''} -> {record.custom_label or ''}"
                )
            else:
                record.name = False

    @api.depends("template_id")
    def _compute_related_template_ids(self):
        for rec in self:
            if rec.template_id:
                xml_id = rec.template_id.get_external_id()
                template = 't-call="%s"' % xml_id[rec.template_id.id]
                # Search for views containing the dynamic t-call in arch_db
                views = self.env["ir.ui.view"].search([("arch_db", "ilike", template)])
                if views:
                    rec.related_template_ids = views.ids
                else:
                    rec.related_template_ids = False
            else:
                rec.related_template_ids = False

    @api.depends("lang")
    def _compute_active_lang_count(self):
        lang_count = len(self.env["res.lang"].get_installed())
        for rec in self:
            rec.active_lang_count = lang_count
