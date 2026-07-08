from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.planner import build_plan
from ai_workflow_bootstrap.core.scanner import RepoProfile
from ai_workflow_bootstrap.core.template_pack import load_default_template_pack


class TemplatePackTests(unittest.TestCase):
    def test_manifest_references_existing_templates(self) -> None:
        pack = load_default_template_pack()

        self.assertEqual(pack.name, "default")
        self.assertTrue(pack.root.exists())
        for spec in pack.files:
            self.assertTrue(pack.template_path(spec.template).exists(), spec.template)

    def test_default_includes_spec_driven_and_living_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            profile = RepoProfile(
                project_name="Example Project",
                repo_name="example-project",
                detected_stacks=["python"],
                commands={"build": "python -m build"},
                top_dirs=["src"],
            )
            pack = load_default_template_pack()

            plan = build_plan(
                target,
                profile=profile,
                pack=pack,
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs", "skill/spec-driven", "skill/living-docs"},
                force=False,
                dry_run=True,
                backup_existing=True,
            )

            planned = {str(item.path) for item in plan.results if item.kind == "file"}
            self.assertIn(str(target / "AGENTS.md"), planned)
            self.assertIn(str(target / "docs/SPEC_DRIVEN.md"), planned)
            self.assertIn(str(target / "docs/AI_CONTEXT.md"), planned)
            self.assertIn(str(target / "docs/LIVING_DOCUMENTATION.md"), planned)
            self.assertIn(str(target / ".agents/skills/spec-driven/SKILL.md"), planned)
            self.assertIn(str(target / ".agents/skills/living-docs/SKILL.md"), planned)
            self.assertFalse(any(".cursor" in item.path.parts for item in plan.results))
            self.assertFalse(any(".codex" in item.path.parts for item in plan.results))

    def test_no_living_docs_excludes_living_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
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
                enabled_groups={"spec-driven", "skill/spec-driven"},
                force=False,
                dry_run=True,
                backup_existing=True,
            )

            planned = {str(item.path) for item in plan.results if item.kind == "file"}
            self.assertIn(str(target / "AGENTS.md"), planned)
            self.assertIn(str(target / "docs/SPEC_DRIVEN.md"), planned)
            self.assertNotIn(str(target / "docs/AI_CONTEXT.md"), planned)
            self.assertNotIn(str(target / "docs/LIVING_DOCUMENTATION.md"), planned)
            self.assertIn(str(target / ".agents/skills/spec-driven/SKILL.md"), planned)
            self.assertNotIn(str(target / ".agents/skills/living-docs/SKILL.md"), planned)
            self.assertFalse(any(".cursor" in item.path.parts for item in plan.results))
            self.assertFalse(any(".codex" in item.path.parts for item in plan.results))

    def test_living_docs_only_excludes_spec_driven(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
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
                enabled_workflows=["living-docs"],
                enabled_groups={"living-docs", "skill/living-docs"},
                force=False,
                dry_run=True,
                backup_existing=True,
            )

            planned = {str(item.path) for item in plan.results if item.kind == "file"}
            self.assertIn(str(target / "docs/AI_CONTEXT.md"), planned)
            self.assertIn(str(target / "docs/LIVING_DOCUMENTATION.md"), planned)
            self.assertNotIn(str(target / "AGENTS.md"), planned)
            self.assertNotIn(str(target / "docs/SPEC_DRIVEN.md"), planned)
            self.assertNotIn(str(target / ".agents/skills/spec-driven/SKILL.md"), planned)
            self.assertIn(str(target / ".agents/skills/living-docs/SKILL.md"), planned)
            self.assertFalse(any(".cursor" in item.path.parts for item in plan.results))
            self.assertFalse(any(".codex" in item.path.parts for item in plan.results))

    def test_no_skill_excludes_both_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
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
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs"},
                force=False,
                dry_run=True,
                backup_existing=True,
            )

            planned = {str(item.path) for item in plan.results if item.kind == "file"}
            self.assertIn(str(target / "AGENTS.md"), planned)
            self.assertIn(str(target / "docs/AI_CONTEXT.md"), planned)
            self.assertNotIn(str(target / ".agents/skills/spec-driven/SKILL.md"), planned)
            self.assertNotIn(str(target / ".agents/skills/living-docs/SKILL.md"), planned)
            self.assertFalse(any(".cursor" in item.path.parts for item in plan.results))
            self.assertFalse(any(".codex" in item.path.parts for item in plan.results))


if __name__ == "__main__":
    unittest.main()
