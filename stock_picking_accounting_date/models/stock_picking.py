# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    accounting_date = fields.Date(
        help="Accounting date for stock valuation journal entry.",
    )
    show_accounting_date = fields.Boolean(compute="_compute_show_accounting_date")

    def _check_internal_or_transit_location_type(self, locations):
        self.ensure_one()
        locations = set(locations)
        if any(location.usage not in ["internal", "transit"] for location in locations):
            return False
        return True

    def _compute_show_accounting_date(self):
        for pick in self:
            pick.show_accounting_date = False
            move_ids = pick.move_ids.with_company(pick.company_id).filtered(
                lambda move: move.product_id.detailed_type == "product"
                and move.product_id.valuation == "real_time"
            )
            if move_ids:
                move_source_locations = [move.location_id for move in move_ids]
                move_dest_locations = [move.location_dest_id for move in move_ids]
                locations = move_source_locations + move_dest_locations
                if not self._check_internal_or_transit_location_type(locations):
                    pick.show_accounting_date = True
