# Copyright 2021-2024 Quartile
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, models
from odoo.exceptions import AccessError
from odoo.tools.translate import _


class IrModelAccess(models.Model):
    _inherit = "ir.model.access"

    @api.model
    def _readonly_exclude_models(self):
        """Models updtate/create by system, and should be excluded from checking"""
        return (
            self.sudo()
            .search(
                [
                    ("group_id", "=", False),
                    "|",
                    ("perm_write", "=", True),
                    "|",
                    ("perm_create", "=", True),
                    ("perm_unlink", "=", True),
                ]
            )
            .mapped("model_id.model")
        )

    @api.model
    def _test_readonly(self, model):
        exclude_models = self._readonly_exclude_models()
        if model not in exclude_models and self.env.user.is_readonly_user:
            return True
        return False

    @api.model
    def _test_restrict_update(self, model):
        # Get the IDs of unresticted users for the model if it's restricted
        self.env.cr.execute(
            """
            SELECT gurel.uid
            FROM ir_model m
            LEFT JOIN ir_model_res_groups_update_allowed_rel mgrel ON m.id = mgrel.ir_model_id
            LEFT JOIN res_groups_users_rel gurel ON mgrel.res_groups_id = gurel.gid
            WHERE m.model = %s
              AND m.restrict_update = true
            """,
            (model,),
        )
        query_res = self.env.cr.fetchall()
        return bool(query_res) and (self.env.uid,) not in query_res

    @api.model
    def check(self, model, mode="read", raise_exception=True):
        if self.env.su:
            return True
        res = super().check(model, mode, raise_exception)
        if mode != "read" and raise_exception:
            if self._test_readonly(model) or self._test_restrict_update(model):
                raise AccessError(
                    _(
                        "You are only allowed to read this record. (%(model)s - %(mode)s)"
                    )
                    % {"model": model, "mode": mode}
                )
        return res
