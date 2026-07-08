from __future__ import annotations

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from ai_workflow_bootstrap import cli
from ai_workflow_bootstrap.core.state import state_path


def _legacy_pattern(*parts: str) -> str:
    return "".join(parts)


class CliTests(unittest.TestCase):
    def test_help_mentions_tui_default_and_apply(self) -> None:
        help_text = cli.build_parser().format_help()

        self.assertIn("Open the guided TUI by default", help_text)
        self.assertIn("ai-bootstrap tui", help_text)
        self.assertIn("ai-bootstrap apply [path]", help_text)
        self.assertIn("Examples:", help_text)

    def test_no_args_opens_tui(self) -> None:
        with mock.patch("ai_workflow_bootstrap.cli._run_tui", return_value=0) as run_tui:
            exit_code = cli.main([])

        self.assertEqual(exit_code, 0)
        run_tui.assert_called_once_with([])

    def test_tui_subcommand_opens_tui(self) -> None:
        with mock.patch("ai_workflow_bootstrap.cli._run_tui", return_value=0) as run_tui:
            exit_code = cli.main(["tui"])

        self.assertEqual(exit_code, 0)
        run_tui.assert_called_once_with([])

    def test_apply_dry_run_completes_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = cli.main(["apply", "--dry-run", str(target)])

            self.assertEqual(exit_code, 0)
            self.assertFalse(state_path(target).exists())
            self.assertNotIn(".cursor", buffer.getvalue())
            self.assertNotIn(".codex", buffer.getvalue())
            self.assertIn(".agents/skills/maintainability-audit/SKILL.md", buffer.getvalue())

    def test_apply_writes_state_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = cli.main(["apply", str(target)])

            self.assertEqual(exit_code, 0)
            state_file = state_path(target)
            self.assertTrue(state_file.exists())
            data = json.loads(state_file.read_text(encoding="utf-8"))
            self.assertEqual(data["tool_name"], "ai-workflow-bootstrap")
            self.assertTrue(os.path.isabs(data["target_path"]))
            self.assertEqual(data["enabled_workflows"], ["spec-driven", "living-docs"])
            self.assertIn("AGENTS.md", data["files"])
            self.assertIn("docs/AI_CONTEXT.md", data["files"])
            self.assertIn(".agents/skills/spec-driven/SKILL.md", data["files"])
            self.assertIn(".agents/skills/maintainability-audit/SKILL.md", data["files"])
            self.assertIn(".agents/skills/living-docs/SKILL.md", data["files"])
            self.assertTrue(all(not key.startswith("/") for key in data["files"]))

    def test_apply_no_living_docs_writes_spec_only_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = cli.main(["apply", "--no-living-docs", str(target)])

            self.assertEqual(exit_code, 0)
            data = json.loads(state_path(target).read_text(encoding="utf-8"))
            self.assertEqual(data["enabled_workflows"], ["spec-driven"])
            self.assertIn("AGENTS.md", data["files"])
            self.assertIn("docs/SPEC_DRIVEN.md", data["files"])
            self.assertNotIn("docs/AI_CONTEXT.md", data["files"])
            self.assertIn(".agents/skills/maintainability-audit/SKILL.md", data["files"])
            self.assertNotIn(".agents/skills/living-docs/SKILL.md", data["files"])

    def test_dry_run_does_not_write_state_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = cli.main(["apply", "--dry-run", str(target)])

            self.assertEqual(exit_code, 0)
            self.assertFalse(state_path(target).exists())

    def test_no_args_without_textual_shows_message_and_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            original_cwd = Path.cwd()
            os.chdir(tmp)
            try:
                stderr = io.StringIO()
                with mock.patch(
                    "ai_workflow_bootstrap.tui._load_textual",
                    side_effect=ImportError('Textual is required for the TUI.\nInstall with:\npip install -e ".[tui]"'),
                ):
                    with redirect_stderr(stderr):
                        exit_code = cli.main([])

                self.assertEqual(exit_code, 1)
                self.assertIn("Textual is required for the TUI.", stderr.getvalue())
                self.assertFalse(any(Path(tmp).iterdir()))
            finally:
                os.chdir(original_cwd)

    def test_bootstrap_sdd_is_a_thin_launcher(self) -> None:
        path = Path("bootstrap_sdd.py")
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")

        self.assertLessEqual(len(text.splitlines()), 12)
        self.assertIn("from ai_workflow_bootstrap.cli import main", text)
        self.assertIn("raise SystemExit(main(sys.argv[1:]))", text)
        self.assertNotIn(_legacy_pattern(".", "cur", "sor/plans"), text)
        self.assertNotIn(_legacy_pattern(".", "cur", "sor/rules"), text)
        self.assertNotIn(_legacy_pattern("global ", "Codex"), text)
        self.assertNotIn(_legacy_pattern("Codex ", "or Cursor"), text)
        self.assertNotIn(_legacy_pattern("--global-", "codex"), text)
        self.assertNotIn(_legacy_pattern("--no-", "cursor"), text)


if __name__ == "__main__":
    unittest.main()
