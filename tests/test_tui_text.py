from __future__ import annotations

import unittest

from ai_workflow_bootstrap.tui_text import SUPPORTED_LANGUAGES, detect_default_language, t


class TuiTextTests(unittest.TestCase):
    def test_detect_default_language_pt_br_locale(self) -> None:
        self.assertEqual(detect_default_language({"LC_ALL": "pt_BR.UTF-8"}), "pt-BR")

    def test_detect_default_language_pt_locale(self) -> None:
        self.assertEqual(detect_default_language({"LANG": "pt_PT.UTF-8"}), "pt-BR")

    def test_detect_default_language_falls_back_to_english(self) -> None:
        self.assertEqual(detect_default_language({"LANG": "en_US.UTF-8"}), "en")

    def test_translation_returns_portuguese(self) -> None:
        self.assertIn("Esta ferramenta", t("pt-BR", "app_intro"))

    def test_translation_returns_english(self) -> None:
        self.assertIn("This tool prepares", t("en", "app_intro"))

    def test_unknown_language_falls_back_to_english(self) -> None:
        self.assertEqual(t("es", "app_intro"), t("en", "app_intro"))

    def test_unknown_key_returns_clear_fallback(self) -> None:
        self.assertEqual(t("en", "missing_key"), "[missing:missing_key]")

    def test_supported_languages_include_expected_entries(self) -> None:
        self.assertEqual(SUPPORTED_LANGUAGES, ("en", "pt-BR"))


if __name__ == "__main__":
    unittest.main()
