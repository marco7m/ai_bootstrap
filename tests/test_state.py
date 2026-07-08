from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.planner import BootstrapPlan, WriteResult
from ai_workflow_bootstrap.core.scanner import RepoProfile
from ai_workflow_bootstrap.core.template_pack import load_default_template_pack
from ai_workflow_bootstrap.core.state import load_state, new_state, save_state, state_path
from ai_workflow_bootstrap.core.state import build_state


class StateTests(unittest.TestCase):
    def test_state_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = state_path(root)
            state = new_state(
                target_path=str(root),
                template_pack="default",
                template_pack_version="0.1.0",
                enabled_workflows=["spec-driven"],
                tool_version="0.1.0",
                files={
                    "AGENTS.md": {
                        "status": "written",
                        "template": "templates/AGENTS.md",
                        "template_hash": "abc123",
                    }
                },
                optional_modules=[],
            )

            save_state(path, state)
            loaded = load_state(path)

            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.tool_name, "ai-workflow-bootstrap")
            self.assertEqual(loaded.template_pack, "default")
            self.assertEqual(loaded.enabled_workflows, ["spec-driven"])
            self.assertEqual(loaded.files["AGENTS.md"]["template_hash"], "abc123")

    def test_build_state_uses_relative_file_paths_and_skips_external_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = load_default_template_pack()
            profile = RepoProfile(project_name="Example", repo_name="example")
            plan = BootstrapPlan(
                target=root,
                profile=profile,
                pack=pack,
                results=[],
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs"},
                force=False,
                dry_run=False,
                backup_existing=True,
                install_global_codex=True,
            )
            results = [
                WriteResult(
                    path=root / "docs/AI_CONTEXT.md",
                    status="written",
                    message="created/updated",
                    template="templates/docs/AI_CONTEXT.md",
                    template_hash="abc123",
                ),
                WriteResult(
                    path=Path("/home/example/.codex/AGENTS.md"),
                    status="written",
                    message="created/updated",
                    template="templates/global/AGENTS.md",
                    template_hash="def456",
                ),
            ]

            state = build_state(plan=plan, results=results, tool_version="0.1.0")

            self.assertTrue(os.path.isabs(state.target_path))
            self.assertIn("docs/AI_CONTEXT.md", state.files)
            self.assertNotIn("/home/example/.codex/AGENTS.md", state.files)
            self.assertTrue(all(not key.startswith("/") for key in state.files))
            self.assertEqual(state.files["docs/AI_CONTEXT.md"]["template_hash"], "abc123")


if __name__ == "__main__":
    unittest.main()
