from odoo import fields


def custom_get_digits(self, env):
    precision = 0
    float_decimal_rec = env["field.float.decimal"].search(
        [
            ("res_model_name", "=", self.model_name),
            ("field_name", "=", self.name),
            ("company_id", "=", env.company.id),
        ],
        limit=1,
    )
    if not float_decimal_rec:
        float_decimal_rec = env["field.float.decimal"].search(
            [
                ("res_model_name", "=", self.model_name),
                ("field_name", "=", self.name),
                ("company_id", "=", False),
            ],
            limit=1,
        )
    if float_decimal_rec:
        precision = float_decimal_rec.digits
    if isinstance(self._digits, str):
        if precision:
            return 16, precision
        precision = env["decimal.precision"].precision_get(self._digits)
        return 16, precision
    elif isinstance(self._digits, tuple) and len(self._digits) == 2 and precision:
        return self._digits[0], precision
    else:
        return self._digits


fields.Float.get_digits = custom_get_digits
