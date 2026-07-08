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

    def test_build_plan_renders_all_enabled_templates(self) -> None:
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
                force=False,
                dry_run=True,
                backup_existing=True,
                install_global_codex=False,
                with_cursor=True,
                with_skill=True,
            )

            planned_paths = {str(item.path) for item in plan.results}
            for spec in pack.files:
                if spec.group in {"core", "cursor", "skill"}:
                    self.assertIn(str(target / spec.path), planned_paths, spec.path)

            self.assertTrue(any(item.path.name == "AGENTS.md" and item.content for item in plan.results))
            self.assertTrue(any(item.path.name == "SKILL.md" for item in plan.results))

    def test_build_plan_includes_global_codex_path_without_writing(self) -> None:
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
                        force=False,
                        dry_run=True,
                        backup_existing=True,
                        install_global_codex=True,
                        with_cursor=False,
                        with_skill=False,
                    )

                global_paths = [item.path for item in plan.results if str(item.path).endswith(".codex/AGENTS.md")]
                self.assertEqual(len(global_paths), 1)
                self.assertFalse(global_paths[0].exists())


if __name__ == "__main__":
    unittest.main()
