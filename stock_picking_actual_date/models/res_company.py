# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytz

from odoo import fields, models

_tzs = [
    (tz, tz)
    for tz in sorted(
        pytz.all_timezones, key=lambda tz: tz if not tz.startswith("Etc/") else "_"
    )
]


def _tz_get(self):
    return _tzs


class ResCompany(models.Model):
    _inherit = "res.company"

    tz = fields.Selection(
        _tz_get,
        string="Timezone",
        default=lambda self: self._context.get("tz"),
        help="When assigning the actual date of a stock move, "
        "this timezone will be used for conversion.",
    )
