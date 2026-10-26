"""Regression checks for explicit outdated-translation exceptions."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import verify_translations as verifier


class OutdatedTranslationsTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.docs = self.root / "docs"
        self.i18n = self.root / "i18n"
        self.doc = "sdk/guide"
        self.frontmatter = '---\ntitle: "Guide"\nsidebar_label: "Guide"\n---\n'
        self.current = self.frontmatter + (
            "# Guide\n## New section {#new}\n"
            "[Reference](https://example.org/new)\n"
            "```go\nnewAPI()\n```\n:::note\nNew guidance.\n:::\n"
            + "The updated guide explains the new behavior. " * 40
        )
        self.old = self.frontmatter + (
            "# Guide\n## Old section {#old}\n"
            "[Reference](https://example.org/old)\nOld guidance.\n"
        )
        self.write(self.docs, self.doc + ".md", self.current)
        for locale in ("de", "fr"):
            self.write(self.locale_dir(locale), self.doc + ".md", self.old)
        overrides = patch.multiple(
            verifier,
            ENGLISH_DOCS_DIR=self.docs,
            I18N_BASE=self.i18n,
            LOCALES=["de", "fr"],
            ENGLISH_ONLY=set(),
            OUTDATED_TRANSLATIONS={self.doc: {"de"}},
        )
        overrides.start()
        self.addCleanup(overrides.stop)

    def locale_dir(self, locale):
        return self.i18n / locale / "docusaurus-plugin-content-docs" / "current"

    @staticmethod
    def write(base, path, content):
        destination = base / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

    def categories(self, locale):
        return {issue.category for issue in verifier.verify_locale(
            locale, verifier.get_english_doc_paths()
        )}

    def test_content_exception_is_limited_to_marked_locale(self):
        self.assertEqual(self.categories("de"), set())
        self.assertEqual(self.categories("fr"), {
            "CODE_BLOCKS", "LINKS", "HEADINGS", "ADMONITIONS", "CONTENT_PARITY",
        })

    def test_removing_marker_resumes_content_checks(self):
        verifier.OUTDATED_TRANSLATIONS[self.doc].remove("de")
        self.assertIn("LINKS", self.categories("de"))
        self.write(self.locale_dir("de"), self.doc + ".md", self.current)
        self.assertEqual(self.categories("de"), set())

    def test_other_pages_still_have_content_checks(self):
        self.write(self.docs, "sdk/other.md", self.current)
        self.write(self.locale_dir("de"), "sdk/other.md", self.old)
        self.assertIn("LINKS", self.categories("de"))

    def test_outdated_translation_must_still_exist(self):
        (self.locale_dir("de") / (self.doc + ".md")).unlink()
        self.assertEqual(self.categories("de"), {"MISSING"})

    def test_frontmatter_and_extra_files_still_checked(self):
        self.write(self.locale_dir("de"), self.doc + ".md", "# No metadata\n")
        self.write(self.locale_dir("de"), "sdk/extra.md", self.old)
        self.assertEqual(self.categories("de"), {"FRONTMATTER", "EXTRA"})

    def test_theme_checks_still_apply(self):
        theme_path = "docusaurus-theme-classic/footer.json"
        self.write(self.i18n / "en", theme_path, json.dumps({"test.key": {}}))
        self.write(self.i18n / "de", theme_path, "{}")
        self.assertEqual(
            {issue.category for issue in verifier.verify_theme_translations("de")},
            {"THEME_UNTRANSLATED"},
        )

    def test_summary_reports_skipped_content_checks(self):
        verifier.OUTDATED_TRANSLATIONS[self.doc].add("fr")
        output = io.StringIO()
        with contextlib.redirect_stdout(output), self.assertRaises(SystemExit) as result:
            verifier.main()
        self.assertEqual(result.exception.code, 0)
        self.assertIn("content checks skipped: sdk/guide", output.getvalue())
        self.assertIn("2 translations awaiting updates", output.getvalue())
        self.assertNotIn("All translations verified", output.getvalue())


if __name__ == "__main__":
    unittest.main()
