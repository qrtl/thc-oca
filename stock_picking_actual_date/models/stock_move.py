# Copyright 2023-2024 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    actual_date = fields.Date(
        compute="_compute_actual_date",
        store=True,
    )

    @api.depends("date", "picking_id.actual_date")
    def _compute_actual_date(self):
        for rec in self:
            if rec.picking_id.actual_date:
                rec.actual_date = rec.picking_id.actual_date
                continue
            tz = self.env.company.partner_id.tz or self.env.user.tz
            rec.actual_date = fields.Date.context_today(
                self.with_context(tz=tz), rec.date
            )

    def _prepare_account_move_vals(
        self,
        credit_account_id,
        debit_account_id,
        journal_id,
        qty,
        description,
        svl_id,
        cost,
    ):
        am_vals = super(StockMove, self)._prepare_account_move_vals(
            credit_account_id,
            debit_account_id,
            journal_id,
            qty,
            description,
            svl_id,
            cost,
        )
        # i.e. Inventory adjustments with actual date
        if self._context.get("force_period_date"):
            self.write({"actual_date": self._context["force_period_date"]})
            return am_vals
        if self.actual_date:
            am_vals.update({"date": self.actual_date})
        return am_vals

    def _get_price_unit(self):
        """Passes the actual_date to be used in currency conversion for receipts
        in foreign currency purchases.
        """
        self.ensure_one()
        self = self.with_context(actual_date=self.actual_date)
        return super()._get_price_unit()
