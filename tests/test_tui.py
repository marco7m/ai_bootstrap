from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from ai_workflow_bootstrap import tui


class TuiTests(unittest.TestCase):
    def test_widget_ids_are_unique(self) -> None:
        ids = [
            tui.LANGUAGE_SELECT_ID,
            tui.PROJECT_SELECT_ID,
            tui.PROJECT_MESSAGE_ID,
            tui.PATH_INPUT_ID,
            tui.MODE_SELECT_ID,
            tui.INCLUDE_SKILLS_ID,
            tui.OVERWRITE_EXISTING_ID,
            tui.PREVIEW_BUTTON_ID,
            tui.DRY_RUN_BUTTON_ID,
            tui.APPLY_BUTTON_ID,
            tui.CANCEL_BUTTON_ID,
            tui.CURRENT_DIRECTORY_BUTTON_ID,
            tui.HOME_BUTTON_ID,
            tui.PARENT_BUTTON_ID,
            tui.REFRESH_PROJECTS_BUTTON_ID,
            tui.PREVIEW_TABLE_ID,
            tui.CONFIRM_INPUT_ID,
            tui.STATUS_ID,
            tui.APP_INTRO_ID,
            tui.SPEC_DRIVEN_HELP_ID,
            tui.LIVING_DOCS_HELP_ID,
            tui.SKILLS_HELP_ID,
            tui.DRY_RUN_HELP_ID,
            tui.STATUS_HELP_ID,
        ]

        self.assertEqual(len(ids), len(set(ids)))

    def test_plan_uses_force_only_when_overwrite_is_enabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            existing_file = root / "docs" / "SPEC_DRIVEN.md"
            existing_file.parent.mkdir(parents=True)
            existing_file.write_text("existing content", encoding="utf-8")

            safe_plan = tui._plan_from_ui(str(root), "recommended", True, dry_run=True)
            forced_plan = tui._plan_from_ui(str(root), "recommended", True, dry_run=True, force=True)

            safe_result = next(item for item in safe_plan.results if item.path == existing_file)
            forced_result = next(item for item in forced_plan.results if item.path == existing_file)

            self.assertEqual(safe_result.status, "skipped")
            self.assertEqual(forced_result.status, "overwritten")
            self.assertTrue(forced_result.needs_backup)

    def test_missing_textual_prints_install_message(self) -> None:
        stderr = io.StringIO()

        from unittest import mock

        with mock.patch(
            "ai_workflow_bootstrap.tui._load_textual",
            side_effect=ImportError('Textual is required for the TUI.\nInstall with:\npip install -e ".[tui]"'),
        ):
            with redirect_stderr(stderr):
                exit_code = tui.main([])

        self.assertEqual(exit_code, 1)
        self.assertIn("Textual is required for the TUI.", stderr.getvalue())
        self.assertIn('pip install -e ".[tui]"', stderr.getvalue())

    def test_tui_entrypoint_does_not_create_a_path_when_dependency_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stderr = io.StringIO()

            from unittest import mock

            with mock.patch(
                "ai_workflow_bootstrap.tui._load_textual",
                side_effect=ImportError('Textual is required for the TUI.\nInstall with:\npip install -e ".[tui]"'),
            ):
                with redirect_stderr(stderr):
                    exit_code = tui.main([])

            self.assertEqual(exit_code, 1)
            self.assertFalse((root / "tui").exists())
            self.assertIn("Textual is required for the TUI.", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
