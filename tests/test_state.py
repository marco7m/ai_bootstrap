from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.planner import BootstrapPlan, WriteResult
from ai_workflow_bootstrap.core.scanner import RepoProfile
from ai_workflow_bootstrap.core.state import build_state, load_state, new_state, save_state, state_path
from ai_workflow_bootstrap.core.template_pack import load_default_template_pack


class StateTests(unittest.TestCase):
    def test_state_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = state_path(root)
            state = new_state(
                target_path=str(root),
                template_pack="default",
                template_pack_version="0.3.0",
                enabled_workflows=["spec-driven"],
                tool_version="0.1.0",
                files={"AGENTS.md": {"status": "written", "template_hash": "abc123"}},
            )

            save_state(path, state)
            loaded = load_state(path)

            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.template_pack, "default")
            self.assertEqual(loaded.files["AGENTS.md"]["template_hash"], "abc123")

    def test_build_state_skips_external_and_deletion_results(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = BootstrapPlan(
                target=root,
                profile=RepoProfile(project_name="Example", repo_name="example"),
                pack=load_default_template_pack(),
                results=[],
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs"},
                force=True,
                dry_run=False,
            )
            results = [
                WriteResult(
                    path=root / "docs/INDEX.md",
                    status="written",
                    message="created/updated",
                    template="templates/docs/INDEX.md",
                    template_hash="abc123",
                ),
                WriteResult(
                    path=root / "docs/AI_CONTEXT.md",
                    status="deleted",
                    message="obsolete generated file will be deleted",
                    kind="deletion",
                ),
                WriteResult(path=Path("/tmp/example/AGENTS.md"), status="written", message="created/updated"),
            ]

            state = build_state(plan=plan, results=results, tool_version="0.1.0")

            self.assertTrue(os.path.isabs(state.target_path))
            self.assertIn("docs/INDEX.md", state.files)
            self.assertNotIn("docs/AI_CONTEXT.md", state.files)
            self.assertNotIn("/tmp/example/AGENTS.md", state.files)


if __name__ == "__main__":
    unittest.main()
