from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from ai_workflow_bootstrap import tui
from ai_workflow_bootstrap.core.lifecycle import content_hash
from ai_workflow_bootstrap.core.state import new_state, save_state, state_path


class TuiTests(unittest.TestCase):
    def test_widget_ids_are_unique(self) -> None:
        ids = [
            tui.LANGUAGE_SELECT_ID,
            tui.PROJECT_SELECT_ID,
            tui.PROJECT_MESSAGE_ID,
            tui.PATH_INPUT_ID,
            tui.INCLUDE_SKILLS_ID,
            tui.OVERWRITE_EXISTING_ID,
            tui.RESET_PROJECT_KNOWLEDGE_ID,
            tui.RESET_CONFIRM_INPUT_ID,
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
        self.assertFalse(hasattr(tui, "MODE_SELECT_ID"))

    def test_plan_uses_force_only_when_overwrite_is_enabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            existing_file = root / "docs" / "SPEC_DRIVEN.md"
            existing_file.parent.mkdir(parents=True)
            existing_file.write_text("existing content", encoding="utf-8")

            safe_plan = tui._plan_from_ui(str(root), True, dry_run=True)
            forced_plan = tui._plan_from_ui(str(root), True, dry_run=True, force=True)

            safe_result = next(item for item in safe_plan.results if item.path == existing_file)
            forced_result = next(item for item in forced_plan.results if item.path == existing_file)

            self.assertEqual(safe_result.status, "skipped")
            self.assertEqual(forced_result.status, "overwritten")

    def test_reset_preview_is_separate_from_managed_update(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            index = root / "docs/INDEX.md"
            index.parent.mkdir(parents=True)
            index.write_text("# Project knowledge\n", encoding="utf-8")

            ordinary = tui._plan_from_ui(str(root), True, dry_run=True, force=True)
            reset = tui._plan_from_ui(
                str(root),
                True,
                dry_run=True,
                force=False,
                reset_project_knowledge=True,
            )

            self.assertEqual(next(item for item in ordinary.results if item.path == index).status, "preserved")
            self.assertEqual(next(item for item in reset.results if item.path == index).status, "reset")

    def test_force_preview_lists_known_legacy_deletion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            legacy = root / "docs/AI_CONTEXT.md"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("legacy\n", encoding="utf-8")
            save_state(
                state_path(root),
                new_state(
                    target_path=str(root),
                    template_pack="default",
                    template_pack_version="0.4.0",
                    enabled_workflows=["spec-driven", "living-docs"],
                    tool_version="0.1.0",
                    files={
                        "docs/AI_CONTEXT.md": {
                            "status": "written",
                            "applied_content_hash": content_hash("legacy\n"),
                        }
                    },
                ),
            )

            plan = tui._plan_from_ui(str(root), True, dry_run=True, force=True)
            deletion = next(item for item in plan.results if item.path == legacy)

            self.assertEqual(deletion.kind, "deletion")
            self.assertEqual(deletion.status, "deleted")

    def test_plan_always_enables_both_workflows_and_surfaces_make_remediation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Cargo.toml").write_text("[workspace]\nmembers=[]\n", encoding="utf-8")
            (root / "Makefile").write_text("run:\n\tcargo run --features desktop\n", encoding="utf-8")

            plan = tui._plan_from_ui(str(root), True, dry_run=True, force=True)

            self.assertEqual(plan.enabled_workflows, ["spec-driven", "living-docs"])
            conflict = next(item for item in plan.results if item.status == "conflict")
            self.assertIn("Current definition", conflict.message)
            self.assertIn("Required definition", conflict.message)
            self.assertIn("--force does not bypass repository-owned file conflicts", conflict.message)

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
