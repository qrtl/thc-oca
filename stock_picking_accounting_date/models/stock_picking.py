# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    accounting_date = fields.Date(
        help="Accounting date for stock valuation journal entry.",
    )
    show_accounting_date = fields.Boolean(compute="_compute_show_accounting_date")
    is_editable_accounting_date = fields.Boolean(
        compute="_compute_is_editable_accounting_date", string="Is Editable"
    )

    def _compute_is_editable_accounting_date(self):
        for record in self:
            if self.env.user.has_group("stock.group_stock_manager"):
                record.is_editable_accounting_date = True
            else:
                record.is_editable_accounting_date = record.state not in [
                    "done",
                    "cancel",
                ]

    def _compute_show_accounting_date(self):
        self.show_accounting_date = False
        for pick in self:
            valued_moves = pick.move_ids.with_company(pick.company_id).filtered(
                lambda move: move.product_id.detailed_type == "product"
                and move.product_id.valuation == "real_time"
                and not (
                    move.location_id._should_be_valued()
                    and move.location_dest_id._should_be_valued()
                )
            )
            if valued_moves:
                pick.show_accounting_date = True
