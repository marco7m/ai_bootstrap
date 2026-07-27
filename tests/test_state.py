from __future__ import annotations

import os
import json
import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.planner import BootstrapPlan, WriteResult
from ai_workflow_bootstrap.core.scanner import RepoProfile
from ai_workflow_bootstrap.core.state import build_state, load_state, new_state, save_state, state_path
from ai_workflow_bootstrap.core.lifecycle import content_hash
from ai_workflow_bootstrap.core.template_pack import load_default_template_pack


class StateTests(unittest.TestCase):
    def test_loads_legacy_state_and_ignores_unknown_future_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = state_path(Path(tmp))
            path.parent.mkdir(parents=True)
            path.write_text(
                json.dumps(
                    {
                        "tool_name": "ai-workflow-bootstrap",
                        "tool_version": "0.1.0",
                        "template_pack": "default",
                        "template_pack_version": "0.4.0",
                        "applied_at": "2026-07-15T16:33:56Z",
                        "target_path": tmp,
                        "files": {
                            "docs/INDEX.md": {"status": "overwritten", "template_hash": "a" * 64},
                            "bad-entry.md": "not-an-object",
                        },
                        "future_field": {"ignored": True},
                    }
                ),
                encoding="utf-8",
            )

            loaded = load_state(path)

            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.template_pack_version, "0.4.0")
            self.assertNotIn("applied_content_hash", loaded.files["docs/INDEX.md"])
            self.assertEqual(loaded.files["bad-entry.md"], {})

    def test_malformed_global_state_fails_actionably(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = state_path(Path(tmp))
            path.parent.mkdir(parents=True)
            path.write_text("[]\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "top-level JSON must be an object"):
                load_state(path)

    def test_state_merge_retains_unselected_provenance_and_records_exact_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prior = new_state(
                target_path=str(root),
                template_pack="default",
                template_pack_version="0.4.0",
                enabled_workflows=["spec-driven", "living-docs"],
                tool_version="0.1.0",
                files={
                    "docs/INDEX.md": {
                        "status": "written",
                        "lifecycle": "seeded",
                        "applied_content_hash": content_hash("old seed\n"),
                    }
                },
            )
            plan = BootstrapPlan(
                target=root,
                profile=RepoProfile(project_name="Example", repo_name="example"),
                pack=load_default_template_pack(),
                results=[],
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs"},
                force=True,
                dry_run=False,
                managed_only=True,
            )
            result = WriteResult(
                path=root / "AGENTS.md",
                status="overwritten",
                message="managed update",
                content="managed\n",
                template="templates/AGENTS.md",
                template_hash="b" * 64,
                existing=True,
                lifecycle="managed",
            )

            state = build_state(plan=plan, results=[result], tool_version="test", prior_state=prior)

            self.assertEqual(
                state.files["docs/INDEX.md"]["applied_content_hash"],
                content_hash("old seed\n"),
            )
            self.assertEqual(
                state.files["AGENTS.md"]["applied_content_hash"],
                content_hash("managed\n"),
            )
            self.assertEqual(state.files["AGENTS.md"]["applied_version"], "0.6.0")

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
