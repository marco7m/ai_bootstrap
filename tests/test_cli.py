from __future__ import annotations

import json
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from ai_workflow_bootstrap import cli
from ai_workflow_bootstrap.core.state import state_path


class CliTests(unittest.TestCase):
    def test_dry_run_completes_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = cli.main(["--dry-run", str(target)])

            self.assertEqual(exit_code, 0)
            self.assertEqual(list(target.iterdir()), [])

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
