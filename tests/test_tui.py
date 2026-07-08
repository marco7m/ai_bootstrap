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
            tui.PATH_INPUT_ID,
            tui.MODE_SELECT_ID,
            tui.INCLUDE_SKILLS_ID,
            tui.PREVIEW_BUTTON_ID,
            tui.DRY_RUN_BUTTON_ID,
            tui.APPLY_BUTTON_ID,
            tui.CANCEL_BUTTON_ID,
            tui.PREVIEW_TABLE_ID,
            tui.CONFIRM_INPUT_ID,
            tui.STATUS_ID,
        ]

        self.assertEqual(len(ids), len(set(ids)))

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
