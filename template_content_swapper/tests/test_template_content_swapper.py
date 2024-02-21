# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestTemplateStringSwapper(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        jp = (
            cls.env["res.lang"]
            .with_context(active_test=False)
            .search([("code", "=", "ja_JP")])
        )
        cls.env["base.language.install"].create({"lang_ids": jp.ids}).lang_install()

    def test_template_string_swapper(self):
        template = "web.external_layout_standard"
        view = self.env["ir.ui.view"]._get(template).sudo()
        values = {"company": self.env.company, "report_type": "pdf", "o": view}
        self.env["template.content.mapping"].create(
            {
                "template_id": view.id,
                "content_from": "Page:",
                "content_to": "Page-No:",
                "lang": "en_US",
            }
        )
        result = self.env["ir.ui.view"]._render_template(template, values)
        self.assertFalse("Page:" in str(result))
        self.assertTrue("Page-No:" in str(result))
        view = self.env["ir.ui.view"].with_context(lang="ja_JP").browse(view.id)
        values = {"company": self.env.company, "report_type": "pdf", "o": view}
        result = (
            self.env["ir.ui.view"]
            .with_context(lang="ja_JP")
            ._render_template(template, values)
        )
        self.assertTrue("ページ:" in str(result))
        self.env["template.content.mapping"].create(
            {
                "template_id": view.id,
                "content_from": "ページ:",
                "content_to": "ページ番号:",
                "lang": "ja_JP",
            }
        )
        result = (
            self.env["ir.ui.view"]
            .with_context(lang="ja_JP")
            ._render_template(template, values)
        )
        self.assertFalse("ページ:" in str(result))
        self.assertTrue("ページ番号:" in str(result))
