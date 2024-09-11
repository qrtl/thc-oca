# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    actual_date = fields.Date(help="Actual date of stock picking.")
    is_editable_actual_date = fields.Boolean(
        compute="_compute_is_editable_actual_date", string="Is Editable"
    )

    def _compute_is_editable_actual_date(self):
        for rec in self:
            rec.is_editable_actual_date = False
            if rec.state not in ["done", "cancel"] or self.env.user.has_group(
                "stock.group_stock_manager"
            ):
                rec.is_editable_actual_date = True

    def write(self, vals):
        res = super().write(vals)
        if "actual_date" in vals:
            for rec in self:
                if rec.state != "done":
                    continue
                account_moves = rec.move_ids.account_move_ids
                if not account_moves:
                    continue
                account_moves.button_draft()
                account_moves.name = False
                account_moves.date = rec.actual_date
                account_moves.action_post()
        return res
