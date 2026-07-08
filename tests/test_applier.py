from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.applier import apply_plan
from ai_workflow_bootstrap.core.planner import build_plan
from ai_workflow_bootstrap.core.scanner import RepoProfile
from ai_workflow_bootstrap.core.template_pack import load_default_template_pack


class ApplierTests(unittest.TestCase):
    def test_does_not_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "AGENTS.md").write_text("custom\n", encoding="utf-8")
            profile = RepoProfile(
                project_name="Example Project",
                repo_name="example-project",
                detected_stacks=[],
                commands={},
                top_dirs=[],
            )
            pack = load_default_template_pack()
            plan = build_plan(
                target,
                profile=profile,
                pack=pack,
                enabled_workflows=["spec-driven"],
                enabled_groups={"spec-driven", "skill/spec-driven", "skill/maintainability-audit"},
                force=False,
                dry_run=False,
                backup_existing=True,
            )

            results = apply_plan(plan, dry_run=False, backup_existing=True)

            agents = next(item for item in results if item.path.name == "AGENTS.md")
            self.assertEqual(agents.status, "skipped")
            self.assertEqual((target / "AGENTS.md").read_text(encoding="utf-8"), "custom\n")

    def test_creates_backup_when_forced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "AGENTS.md").write_text("custom\n", encoding="utf-8")
            profile = RepoProfile(
                project_name="Example Project",
                repo_name="example-project",
                detected_stacks=[],
                commands={},
                top_dirs=[],
            )
            pack = load_default_template_pack()
            plan = build_plan(
                target,
                profile=profile,
                pack=pack,
                enabled_workflows=["spec-driven"],
                enabled_groups={"spec-driven", "skill/spec-driven", "skill/maintainability-audit"},
                force=True,
                dry_run=False,
                backup_existing=True,
            )

            results = apply_plan(plan, dry_run=False, backup_existing=True)

            agents = next(item for item in results if item.path.name == "AGENTS.md")
            backups = list(target.glob("AGENTS.md.bak-*"))
            self.assertEqual(agents.status, "written")
            self.assertIn("Project name: Example Project", (target / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(encoding="utf-8"), "custom\n")


if __name__ == "__main__":
    unittest.main()
