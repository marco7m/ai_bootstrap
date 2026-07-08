from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.planner import build_plan
from ai_workflow_bootstrap.core.scanner import RepoProfile
from ai_workflow_bootstrap.core.template_pack import load_default_template_pack


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

            agents = next(item for item in plan.results if item.path.name == "AGENTS.md")
            self.assertEqual(plan.results[0].kind, "directory")
            self.assertEqual(plan.results[0].status, "written")
            self.assertIn("Project name: Example Project", agents.content)
            self.assertIn("Project purpose", next(item for item in plan.results if item.path.name == "PROJECT_SPEC.md").content)
            self.assertIn("Read on demand.", next(item for item in plan.results if item.path.name == "AI_CONTEXT.md").content)
            self.assertTrue(any(item.path.name == "START_PROMPT.md" for item in plan.results))
            self.assertTrue(any(str(item.path).endswith(".agents/skills/spec-driven/SKILL.md") for item in plan.results))
            self.assertTrue(any(str(item.path).endswith(".agents/skills/living-docs/SKILL.md") for item in plan.results))
            self.assertFalse(any(".cursor" in item.path.parts for item in plan.results))
            self.assertFalse(any(".codex" in item.path.parts for item in plan.results))


if __name__ == "__main__":
    unittest.main()
