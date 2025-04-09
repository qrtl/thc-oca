# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Field Float Decimal Place",
    "version": "16.0.1.0.0",
    "category": "Technical Settings",
    "license": "AGPL-3",
    "author": "Quartile, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/server-ux",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "security/field_float_decimal_security.xml",
        "views/field_float_decimal_views.xml",
    ],
    "installable": True,
}
