from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.planner import build_plan
from ai_workflow_bootstrap.core.scanner import RepoProfile
from ai_workflow_bootstrap.core.template_pack import load_default_template_pack
from ai_workflow_bootstrap.core.template_pack import TemplateObsoleteFileSpec, TemplatePack


class PlannerTests(unittest.TestCase):
    def test_build_plan_renders_current_default_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            profile = RepoProfile(
                project_name="Example Project",
                repo_name="example-project",
                detected_stacks=["python"],
                commands={"build": "python -m build"},
                top_dirs=["src"],
            )
            plan = build_plan(
                target,
                profile=profile,
                pack=load_default_template_pack(),
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={
                    "spec-driven",
                    "living-docs",
                    "skill/spec-driven",
                    "skill/maintainability-audit",
                    "skill/living-docs",
                },
                force=False,
                dry_run=True,
            )

            agents = next(item for item in plan.results if item.path.name == "AGENTS.md")
            self.assertEqual(plan.results[0].kind, "directory")
            self.assertIn("Project: Example Project", agents.content)
            self.assertIn("Knowledge status: `scaffold`", next(item for item in plan.results if item.path.name == "INDEX.md").content)
            self.assertIn("Approved target", next(item for item in plan.results if item.path.name == "CAPABILITIES.md").content)
            self.assertIn("Current contract", next(item for item in plan.results if str(item.path).endswith("docs/product/README.md")).content)
            self.assertIn("Current architecture", next(item for item in plan.results if str(item.path).endswith("docs/architecture/README.md")).content)
            self.assertFalse(any(item.path.name == "AI_CONTEXT.md" and item.kind == "file" for item in plan.results))
            self.assertTrue(any(str(item.path).endswith("living-docs/scripts/check_links.py") for item in plan.results))

    def test_force_preview_places_deletions_after_writes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            legacy = target / "docs/AI_CONTEXT.md"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("legacy\n", encoding="utf-8")
            plan = build_plan(
                target,
                profile=RepoProfile(project_name="Example", repo_name="example"),
                pack=load_default_template_pack(),
                enabled_workflows=["living-docs"],
                enabled_groups={"living-docs"},
                force=True,
                dry_run=True,
            )

            deletion_index = next(index for index, item in enumerate(plan.results) if item.path == legacy)
            last_write_index = max(index for index, item in enumerate(plan.results) if item.kind == "file")
            self.assertGreater(deletion_index, last_write_index)
            self.assertEqual(plan.results[deletion_index].status, "deleted")

    def test_obsolete_path_cannot_escape_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            pack = TemplatePack(
                name="unsafe",
                version="1",
                root=target,
                obsolete_files=[TemplateObsoleteFileSpec(path="../outside.md", group="living-docs")],
            )

            with self.assertRaisesRegex(ValueError, "stay inside"):
                build_plan(
                    target,
                    profile=RepoProfile(project_name="Example", repo_name="example"),
                    pack=pack,
                    enabled_workflows=["living-docs"],
                    enabled_groups={"living-docs"},
                    force=True,
                    dry_run=True,
                )


if __name__ == "__main__":
    unittest.main()
