from __future__ import annotations

import json
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from contextlib import redirect_stderr
from pathlib import Path

from ai_workflow_bootstrap import cli
from ai_workflow_bootstrap.core.state import state_path


class CliTests(unittest.TestCase):
    def test_help_mentions_tui(self) -> None:
        help_text = cli.build_parser().format_help()

        self.assertIn("Interactive TUI", help_text)
        self.assertIn("python -m ai_workflow_bootstrap tui", help_text)

    def test_dry_run_completes_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = cli.main(["--dry-run", str(target)])

            self.assertEqual(exit_code, 0)
            self.assertEqual(list(target.iterdir()), [])
            self.assertNotIn(".cursor", buffer.getvalue())
            self.assertNotIn(".codex", buffer.getvalue())

    def test_tui_is_not_treated_as_a_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tui_dir = Path(tmp) / "tui"
            stderr = io.StringIO()

            from unittest import mock

            with mock.patch(
                "ai_workflow_bootstrap.tui._load_textual",
                side_effect=ImportError('Textual is required for the TUI.\nInstall with:\npip install -e ".[tui]"'),
            ):
                with redirect_stderr(stderr):
                    exit_code = cli.main(["tui"])

            self.assertEqual(exit_code, 1)
            self.assertFalse(tui_dir.exists())
            self.assertIn("Textual is required for the TUI.", stderr.getvalue())
            self.assertFalse((Path.cwd() / "tui").exists())

    def test_real_run_writes_state_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = cli.main([str(target)])

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
            self.assertIn(".agents/skills/living-docs/SKILL.md", data["files"])
            self.assertTrue(all(not key.startswith("/") for key in data["files"]))
            self.assertFalse(any(key.startswith(".cursor") for key in data["files"]))
            self.assertFalse(any(key.startswith("~/.codex") for key in data["files"]))

    def test_dry_run_does_not_write_state_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = cli.main(["--dry-run", str(target)])

            self.assertEqual(exit_code, 0)
            self.assertFalse(state_path(target).exists())

    def test_living_docs_only_writes_living_docs_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = cli.main(["--living-docs-only", str(target)])

            self.assertEqual(exit_code, 0)
            data = json.loads(state_path(target).read_text(encoding="utf-8"))
            self.assertEqual(data["enabled_workflows"], ["living-docs"])
            self.assertNotIn("AGENTS.md", data["files"])
            self.assertIn("docs/AI_CONTEXT.md", data["files"])
            self.assertNotIn(".agents/skills/spec-driven/SKILL.md", data["files"])
            self.assertIn(".agents/skills/living-docs/SKILL.md", data["files"])
            self.assertTrue(all(not key.startswith("/") for key in data["files"]))


if __name__ == "__main__":
    unittest.main()
