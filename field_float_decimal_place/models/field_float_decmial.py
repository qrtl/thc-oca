# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FieldFloatDecimal(models.Model):
    _name = "field.float.decimal"
    _description = "Field Float Decimal"
    _order = "res_model_id, field_id"

    res_model_id = fields.Many2one(
        "ir.model", string="Model", ondelete="cascade", required=True
    )
    res_model_name = fields.Char("Model Name", related="res_model_id.model", store=True)
    field_id = fields.Many2one(
        "ir.model.fields",
        domain="[('model_id', '=', res_model_id), ('ttype', '=', 'float')]",
        string="Field",
        ondelete="cascade",
        required=True,
    )
    field_name = fields.Char("Field Name", related="field_id.name", store=True)
    digits = fields.Integer()
    company_id = fields.Many2one("res.company", string="Company")
