from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.applier import apply_plan
from ai_workflow_bootstrap.core.planner import build_plan
from ai_workflow_bootstrap.core.scanner import RepoProfile
from ai_workflow_bootstrap.core.template_pack import load_default_template_pack


def _profile() -> RepoProfile:
    return RepoProfile(
        project_name="Example Project",
        repo_name="example-project",
        detected_stacks=["python"],
        commands={"test": "python -m unittest"},
        top_dirs=["src"],
    )


class TemplatePackTests(unittest.TestCase):
    def test_manifest_references_existing_templates_and_known_obsolete_paths(self) -> None:
        pack = load_default_template_pack()

        self.assertEqual(pack.name, "default")
        self.assertEqual(pack.version, "0.3.0")
        for spec in pack.files:
            self.assertTrue(pack.template_path(spec.template).exists(), spec.template)
        self.assertEqual(
            {spec.path for spec in pack.obsolete_files},
            {
                "docs/WORKFLOW_MODULES.md",
                "docs/PROJECT_SPEC.md",
                "docs/IMPLEMENTATION_STATUS.md",
                "docs/CANONICAL_DECISIONS.md",
                "docs/AI_CONTEXT.md",
            },
        )

    def test_workflow_preserves_two_approval_gates_and_single_template_owners(self) -> None:
        pack = load_default_template_pack()
        agents = pack.read_template("templates/AGENTS.md")
        guide = pack.read_template("templates/docs/SPEC_DRIVEN.md")
        skill = pack.read_template("templates/.agents/skills/spec-driven/SKILL.md")

        self.assertIn("explicit spec approval", agents)
        self.assertIn("explicit approval of both plan and tasks", agents)
        self.assertIn("Spec approval does not approve the implementation approach", guide)
        self.assertIn("Spec approval is not implementation approval", skill)
        self.assertIn("changes/_templates/spec.md", guide)
        self.assertNotIn("# Change Spec: <title>", guide)
        self.assertNotIn("# Implementation Plan: <title>", guide)

    def test_context_artifacts_stay_within_word_budgets(self) -> None:
        pack = load_default_template_pack()
        budgets = {
            "templates/AGENTS.md": 800,
            "templates/docs/SPEC_DRIVEN.md": 1000,
            "templates/docs/INDEX.md": 250,
            "templates/.agents/skills/spec-driven/SKILL.md": 300,
            "templates/.agents/skills/maintainability-audit/SKILL.md": 300,
            "templates/.agents/skills/living-docs/SKILL.md": 300,
        }

        for template, maximum in budgets.items():
            words = len(pack.read_template(template).split())
            self.assertLessEqual(words, maximum, f"{template}: {words} > {maximum}")

    def test_generated_skills_have_minimal_valid_frontmatter(self) -> None:
        pack = load_default_template_pack()
        skill_templates = [spec.template for spec in pack.files if spec.path.endswith("/SKILL.md")]

        for template in skill_templates:
            text = pack.read_template(template)
            self.assertTrue(text.startswith("---\n"), template)
            frontmatter = text.split("---\n", 2)[1]
            keys = {line.split(":", 1)[0] for line in frontmatter.splitlines() if ":" in line}
            self.assertEqual(keys, {"name", "description"}, template)

    def test_living_docs_separate_baseline_current_state_and_approved_target(self) -> None:
        pack = load_default_template_pack()
        index = pack.read_template("templates/docs/INDEX.md")
        capabilities = pack.read_template("templates/docs/CAPABILITIES.md")
        policy = pack.read_template("templates/docs/LIVING_DOCUMENTATION.md")
        skill = pack.read_template("templates/.agents/skills/living-docs/SKILL.md")

        self.assertIn("Knowledge status: `scaffold`", index)
        self.assertIn("Baseline evidence", index)
        for state in ("unknown", "absent", "partial", "implemented", "verified", "deprecated"):
            self.assertIn(f"`{state}`", capabilities)
        self.assertIn("| Current state | Evidence | Approved target | Active change |", capabilities)
        self.assertIn("`verified` now while its next evolution is approved", capabilities)
        self.assertIn("Keep unapproved ideas", capabilities)
        self.assertIn("Code can show what exists but cannot alone prove intended behavior", policy)
        self.assertIn("scripts/check_links.py", skill)

    def test_default_and_living_only_generate_new_surface_without_ai_context(self) -> None:
        pack = load_default_template_pack()
        modes = (
            (
                ["spec-driven", "living-docs"],
                {"spec-driven", "living-docs", "skill/spec-driven", "skill/maintainability-audit", "skill/living-docs"},
                True,
            ),
            (["living-docs"], {"living-docs", "skill/living-docs"}, False),
        )

        for workflows, groups, expects_agents in modes:
            with self.subTest(workflows=workflows), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp)
                plan = build_plan(
                    target,
                    profile=_profile(),
                    pack=pack,
                    enabled_workflows=workflows,
                    enabled_groups=groups,
                    force=False,
                    dry_run=True,
                )
                planned = {str(item.path) for item in plan.results if item.kind == "file"}

                self.assertIn(str(target / "docs/INDEX.md"), planned)
                self.assertIn(str(target / "docs/CAPABILITIES.md"), planned)
                self.assertIn(str(target / ".agents/skills/living-docs/SKILL.md"), planned)
                self.assertIn(str(target / ".agents/skills/living-docs/scripts/check_links.py"), planned)
                self.assertNotIn(str(target / "docs/AI_CONTEXT.md"), planned)
                self.assertEqual(str(target / "AGENTS.md") in planned, expects_agents)

    def test_spec_only_and_no_skill_preserve_group_boundaries(self) -> None:
        pack = load_default_template_pack()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            spec_plan = build_plan(
                target,
                profile=_profile(),
                pack=pack,
                enabled_workflows=["spec-driven"],
                enabled_groups={"spec-driven", "skill/spec-driven", "skill/maintainability-audit"},
                force=False,
                dry_run=True,
            )
            no_skill_plan = build_plan(
                target,
                profile=_profile(),
                pack=pack,
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs"},
                force=False,
                dry_run=True,
            )

            spec_paths = {str(item.path) for item in spec_plan.results if item.kind == "file"}
            no_skill_paths = {str(item.path) for item in no_skill_plan.results if item.kind == "file"}
            self.assertIn(str(target / "AGENTS.md"), spec_paths)
            self.assertNotIn(str(target / "docs/INDEX.md"), spec_paths)
            self.assertNotIn(str(target / ".agents/skills/living-docs/SKILL.md"), spec_paths)
            self.assertIn(str(target / "docs/INDEX.md"), no_skill_paths)
            self.assertFalse(any(".agents/skills" in path for path in no_skill_paths))

    def test_generated_link_checker_accepts_valid_docs_and_rejects_broken_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            pack = load_default_template_pack()
            plan = build_plan(
                target,
                profile=_profile(),
                pack=pack,
                enabled_workflows=["living-docs"],
                enabled_groups={"living-docs", "skill/living-docs"},
                force=False,
                dry_run=False,
            )
            apply_plan(plan, dry_run=False)
            checker = target / ".agents/skills/living-docs/scripts/check_links.py"

            valid = subprocess.run([sys.executable, str(checker)], cwd=target, text=True, capture_output=True, check=False)
            self.assertEqual(valid.returncode, 0, valid.stderr)

            probe = target / "docs/product/link-check-probe.md"
            probe.write_text("[broken](missing.md)\n", encoding="utf-8")
            broken = subprocess.run([sys.executable, str(checker)], cwd=target, text=True, capture_output=True, check=False)
            self.assertEqual(broken.returncode, 1)
            self.assertIn("missing.md", broken.stderr)

            probe.write_text("```md\n[example](missing.md)\n```\n[anchor](#local)\n[web](https://example.com)\n", encoding="utf-8")
            ignored = subprocess.run([sys.executable, str(checker)], cwd=target, text=True, capture_output=True, check=False)
            self.assertEqual(ignored.returncode, 0, ignored.stderr)


if __name__ == "__main__":
    unittest.main()
