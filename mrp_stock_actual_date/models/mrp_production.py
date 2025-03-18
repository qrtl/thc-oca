# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MrpProduction(models.Model):
    _name = "mrp.production"
    _inherit = ["mrp.production", "actual.date.mixin"]

    def write(self, vals):
        res = super().write(vals)
        if "actual_date" in vals:
            for rec in self:
                if rec.state != "done":
                    continue
                account_moves = (
                    rec.move_raw_ids + rec.move_finished_ids
                ).account_move_ids
                if not account_moves:
                    continue
                account_moves._update_accounting_date()
        return res
