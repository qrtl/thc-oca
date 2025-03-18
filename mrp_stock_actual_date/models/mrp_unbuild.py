# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MrpUnbuild(models.Model):
    _name = "mrp.unbuild"
    _inherit = ["mrp.unbuild", "actual.date.mixin"]

    def write(self, vals):
        res = super().write(vals)
        if "actual_date" in vals:
            for rec in self:
                if rec.state != "done":
                    continue
                account_moves = (rec.consume_line_ids + rec.produce_line_ids).mapped(
                    "account_move_ids"
                )
                if not account_moves:
                    continue
                account_moves._update_accounting_date()
        return res
