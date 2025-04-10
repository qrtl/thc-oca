# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MrpProduction(models.Model):
    _name = "mrp.production"
    _inherit = ["mrp.production", "actual.date.mixin"]

    def _get_stock_move_field_name(self):
        return "move_raw_ids"

    def _get_stock_moves(self):
        self.ensure_one()
        return self.move_raw_ids + self.move_finished_ids
