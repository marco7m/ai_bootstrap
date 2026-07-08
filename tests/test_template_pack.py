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
                enabled_groups={"spec-driven", "living-docs", "cursor", "skill/spec-driven", "skill/living-docs"},
                force=False,
                dry_run=True,
                backup_existing=True,
                install_global_codex=False,
            )

            planned = {str(item.path) for item in plan.results if item.kind == "file"}
            self.assertIn(str(target / "AGENTS.md"), planned)
            self.assertIn(str(target / "docs/SPEC_DRIVEN.md"), planned)
            self.assertIn(str(target / "docs/AI_CONTEXT.md"), planned)
            self.assertIn(str(target / "docs/LIVING_DOCUMENTATION.md"), planned)
            self.assertIn(str(target / ".agents/skills/spec-driven/SKILL.md"), planned)
            self.assertIn(str(target / ".agents/skills/living-docs/SKILL.md"), planned)
            self.assertIn(str(target / ".cursor/rules/spec-driven-always.mdc"), planned)
            self.assertIn(str(target / ".cursor/plans/README.md"), planned)

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
                enabled_groups={"spec-driven", "cursor", "skill/spec-driven"},
                force=False,
                dry_run=True,
                backup_existing=True,
                install_global_codex=False,
            )

            planned = {str(item.path) for item in plan.results if item.kind == "file"}
            self.assertIn(str(target / "AGENTS.md"), planned)
            self.assertIn(str(target / "docs/SPEC_DRIVEN.md"), planned)
            self.assertNotIn(str(target / "docs/AI_CONTEXT.md"), planned)
            self.assertNotIn(str(target / "docs/LIVING_DOCUMENTATION.md"), planned)
            self.assertIn(str(target / ".agents/skills/spec-driven/SKILL.md"), planned)
            self.assertNotIn(str(target / ".agents/skills/living-docs/SKILL.md"), planned)
            self.assertIn(str(target / ".cursor/rules/spec-driven-always.mdc"), planned)
            self.assertIn(str(target / ".cursor/plans/README.md"), planned)

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
                install_global_codex=False,
            )

            planned = {str(item.path) for item in plan.results if item.kind == "file"}
            self.assertIn(str(target / "docs/AI_CONTEXT.md"), planned)
            self.assertIn(str(target / "docs/LIVING_DOCUMENTATION.md"), planned)
            self.assertNotIn(str(target / "AGENTS.md"), planned)
            self.assertNotIn(str(target / "docs/SPEC_DRIVEN.md"), planned)
            self.assertNotIn(str(target / ".agents/skills/spec-driven/SKILL.md"), planned)
            self.assertIn(str(target / ".agents/skills/living-docs/SKILL.md"), planned)
            self.assertNotIn(str(target / ".cursor/rules/spec-driven-always.mdc"), planned)
            self.assertNotIn(str(target / ".cursor/plans/README.md"), planned)

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
                enabled_groups={"spec-driven", "living-docs", "cursor"},
                force=False,
                dry_run=True,
                backup_existing=True,
                install_global_codex=False,
            )

            planned = {str(item.path) for item in plan.results if item.kind == "file"}
            self.assertIn(str(target / "AGENTS.md"), planned)
            self.assertIn(str(target / "docs/AI_CONTEXT.md"), planned)
            self.assertNotIn(str(target / ".agents/skills/spec-driven/SKILL.md"), planned)
            self.assertNotIn(str(target / ".agents/skills/living-docs/SKILL.md"), planned)
            self.assertIn(str(target / ".cursor/rules/spec-driven-always.mdc"), planned)
            self.assertIn(str(target / ".cursor/plans/README.md"), planned)

    def test_global_codex_template_is_only_planned_when_enabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_home:
            with tempfile.TemporaryDirectory() as tmp_target:
                target = Path(tmp_target)
                profile = RepoProfile(
                    project_name="Example Project",
                    repo_name="example-project",
                    detected_stacks=[],
                    commands={},
                    top_dirs=[],
                )
                pack = load_default_template_pack()

                import os
                from unittest import mock

                with mock.patch.dict(os.environ, {"HOME": tmp_home}):
                    plan = build_plan(
                        target,
                        profile=profile,
                        pack=pack,
                        enabled_workflows=["spec-driven", "living-docs"],
                        enabled_groups={
                            "spec-driven",
                            "living-docs",
                            "cursor",
                            "skill/spec-driven",
                            "skill/living-docs",
                            "global_codex",
                        },
                        force=False,
                        dry_run=True,
                        backup_existing=True,
                        install_global_codex=True,
                    )

                global_paths = [item.path for item in plan.results if str(item.path).endswith(".codex/AGENTS.md")]
                self.assertEqual(len(global_paths), 1)
                self.assertFalse(global_paths[0].exists())


if __name__ == "__main__":
    unittest.main()
