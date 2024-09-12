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

    def _sequence_actual_date_matches(self, move, date):
        sequence = move.name
        format_values = move._get_sequence_format_param(sequence)[1]
        sequence_number_reset = move._deduce_sequence_number_reset(sequence)
        year_start, year_end = move._get_sequence_date_range(sequence_number_reset)
        year_match = (
            not format_values["year"]
            or move._year_match(format_values["year"], year_start)
        ) and (
            not format_values["year_end"]
            or move._year_match(format_values["year_end"], year_end)
        )
        month_match = not format_values["month"] or format_values["month"] == date.month
        return year_match and month_match

    def write(self, vals):
        res = super().write(vals)
        if "actual_date" in vals and vals["actual_date"]:
            for rec in self:
                if rec.state != "done":
                    continue
                account_moves = rec.move_ids.account_move_ids
                if not account_moves:
                    continue
                account_moves.button_draft()
                for move in account_moves:
                    if self._sequence_actual_date_matches(move, rec.actual_date):
                        move.date = rec.actual_date
                    else:
                        move.name = False
                        move.date = rec.actual_date
                    move.action_post()
        return res
