# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends(
        "date",
        "picking_id.actual_date",
        "scrap_ids.actual_date",
        "raw_material_production_id.actual_date",
        "production_id.actual_date",
        "consume_unbuild_id.actual_date",
        "unbuild_id.actual_date",
    )
    def _compute_actual_date(self):
        tz = self._get_timezone()
        context_actual_date = self.env.context.get("actual_date")
        records = self.filtered(
            lambda r: r.production_id
            or r.raw_material_production_id
            or r.consume_unbuild_id
            or r.unbuild_id
        )
        for rec in records:
            actual_date = context_actual_date or rec.scrap_ids.actual_date
            if actual_date:
                rec.actual_date = actual_date
                continue
            unbuild_actual_date = (
                rec.consume_unbuild_id.actual_date or rec.unbuild_id.actual_date
            )
            if unbuild_actual_date:
                rec.actual_date = unbuild_actual_date
                continue
            mo_actual_date = (
                rec.production_id.actual_date
                or rec.raw_material_production_id.actual_date
            )
            if mo_actual_date:
                rec.actual_date = mo_actual_date
                continue
            rec.actual_date = fields.Date.context_today(
                self.with_context(tz=tz), rec.date
            )
        return super(StockMove, self - records)._compute_actual_date()
