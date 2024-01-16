# Copyright 2024 Quartile Limited (https://www.quartile.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class FloatConverter(models.AbstractModel):
    _inherit = "ir.qweb.field.float"

    @api.model
    def record_to_html(self, record, field_name, options):
        if "precision" not in options and "decimal_precision" not in options:
            dp_qweb_recs = self.env["decimal.precision.qweb"].search(
                [("res_model_name", "=", record._name), ("field_name", "=", field_name)]
            )
            score = 0
            precision_rec = False
            for dp_qweb_rec in dp_qweb_recs:
                score_rec = dp_qweb_rec._get_score(record)
                if score_rec > score:
                    precision_rec = dp_qweb_rec
            if precision_rec:
                options = dict(options, precision=precision_rec.digits)
        return super().record_to_html(record, field_name, options)
