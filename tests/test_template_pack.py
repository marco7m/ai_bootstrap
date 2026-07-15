from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.applier import apply_plan
from ai_workflow_bootstrap.core.planner import build_plan
from ai_workflow_bootstrap.core.scanner import RepoProfile
from ai_workflow_bootstrap.core.state import build_state
from ai_workflow_bootstrap.core.template_pack import load_default_template_pack, load_template_pack


def _profile() -> RepoProfile:
    return RepoProfile(
        project_name="Example Project",
        repo_name="example-project",
        detected_stacks=["python"],
        commands={"test": "python -m unittest"},
        top_dirs=["src"],
    )


def _rust_profile() -> RepoProfile:
    return RepoProfile(
        project_name="Rust Example",
        repo_name="rust-example",
        detected_stacks=["rust"],
        commands={
            "dev": "make dev",
            "run": "make run",
            "clean-dev": "make clean-dev",
            "test": "make test",
            "lint": "make lint",
            "typecheck": "make typecheck",
        },
        top_dirs=["src"],
    )


class TemplatePackTests(unittest.TestCase):
    def test_manifest_references_existing_templates_and_known_obsolete_paths(self) -> None:
        pack = load_default_template_pack()

        self.assertEqual(pack.name, "default")
        self.assertEqual(pack.version, "0.4.0")
        templated_specs = [*pack.files, *pack.context_fragments, *pack.compositions]
        for spec in templated_specs:
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
        self.assertEqual({spec.path for spec in pack.project_owned_paths}, {"AGENTS.project.md"})

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

    def test_unified_workflow_generates_complete_surface_without_ai_context(self) -> None:
        pack = load_default_template_pack()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            plan = build_plan(
                target,
                profile=_profile(),
                pack=pack,
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs", "skill/spec-driven", "skill/maintainability-audit", "skill/living-docs"},
                force=False,
                dry_run=True,
            )
            planned = {str(item.path) for item in plan.results if item.kind == "file"}

            self.assertIn(str(target / "AGENTS.md"), planned)
            self.assertIn(str(target / "docs/INDEX.md"), planned)
            self.assertIn(str(target / "docs/CAPABILITIES.md"), planned)
            self.assertIn(str(target / ".agents/skills/living-docs/SKILL.md"), planned)
            self.assertIn(str(target / ".agents/skills/living-docs/scripts/check_links.py"), planned)
            self.assertNotIn(str(target / "docs/AI_CONTEXT.md"), planned)
            self.assertNotIn(str(target / "AGENTS.project.md"), planned)

    def test_unified_workflow_can_omit_skills_without_omitting_docs(self) -> None:
        pack = load_default_template_pack()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            no_skill_plan = build_plan(
                target,
                profile=_profile(),
                pack=pack,
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs"},
                force=False,
                dry_run=True,
            )

            no_skill_paths = {str(item.path) for item in no_skill_plan.results if item.kind == "file"}
            self.assertIn(str(target / "AGENTS.md"), no_skill_paths)
            self.assertIn(str(target / "docs/INDEX.md"), no_skill_paths)
            self.assertFalse(any(".agents/skills" in path for path in no_skill_paths))

    def test_rust_policy_is_conditional_and_project_instructions_are_on_demand(self) -> None:
        groups = {"spec-driven", "living-docs"}
        pack = load_default_template_pack()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            rust_plan = build_plan(
                target,
                profile=_rust_profile(),
                pack=pack,
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups=groups,
                force=False,
                dry_run=True,
            )
            by_path = {item.path: item for item in rust_plan.results if item.kind == "file"}
            self.assertIn(target / "Makefile", by_path)
            self.assertIn("cargo run --release", by_path[target / "Makefile"].content)
            self.assertIn(target / ".gitignore", by_path)
            self.assertIn(target / "docs/architecture/rust-development.md", by_path)
            self.assertIn("Rust development lifecycle", by_path[target / "AGENTS.md"].content)
            self.assertNotIn(target / "AGENTS.project.md", by_path)

            python_plan = build_plan(
                target,
                profile=_profile(),
                pack=pack,
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups=groups,
                force=False,
                dry_run=True,
            )
            python_paths = {item.path for item in python_plan.results if item.kind == "file"}
            self.assertNotIn(target / "Makefile", python_paths)
            self.assertNotIn(target / ".gitignore", python_paths)
            self.assertNotIn(target / "docs/architecture/rust-development.md", python_paths)
            agents = next(item for item in python_plan.results if item.path == target / "AGENTS.md")
            self.assertNotIn("Rust development lifecycle", agents.content)

    def test_project_owned_instructions_are_never_created_or_overwritten(self) -> None:
        groups = {"spec-driven", "living-docs"}
        pack = load_default_template_pack()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            missing_plan = build_plan(
                target,
                profile=_profile(),
                pack=pack,
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups=groups,
                force=True,
                dry_run=False,
            )
            apply_plan(missing_plan, dry_run=False)
            project_agents = target / "AGENTS.project.md"
            self.assertFalse(project_agents.exists())

            custom = "# Project rules\n\n- Always preserve this exact text.\n"
            project_agents.write_text(custom, encoding="utf-8")
            preserve_plan = build_plan(
                target,
                profile=_profile(),
                pack=pack,
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups=groups,
                force=True,
                dry_run=False,
            )
            preserved = next(item for item in preserve_plan.results if item.path == project_agents)
            self.assertEqual(preserved.status, "preserved")
            self.assertEqual(preserved.ownership, "project")
            apply_plan(preserve_plan, dry_run=False)
            self.assertEqual(project_agents.read_text(encoding="utf-8"), custom)
            state = build_state(plan=preserve_plan, results=preserve_plan.results, tool_version="test")
            self.assertEqual(state.files["AGENTS.project.md"], {"status": "preserved", "ownership": "project"})

    def test_managed_agents_overwrite_warns_how_to_migrate_project_rules(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "AGENTS.md").write_text("# Custom local rule\n", encoding="utf-8")
            plan = build_plan(
                target,
                profile=_profile(),
                pack=load_default_template_pack(),
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs"},
                force=True,
                dry_run=True,
            )
            agents = next(item for item in plan.results if item.path == target / "AGENTS.md")
            self.assertEqual(agents.status, "overwritten")
            self.assertIn("move repository-specific instructions to AGENTS.project.md", agents.message)
            self.assertIn("preserved even with --force", agents.message)

    def test_manifest_rejects_project_owned_path_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "manifest.json").write_text(
                json.dumps(
                    {
                        "files": [{"path": "AGENTS.project.md", "template": "seed.md"}],
                        "project_owned_paths": [{"path": "AGENTS.project.md"}],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "Project-owned paths"):
                load_template_pack(root)

    def test_manifest_rejects_normalized_project_owned_path_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "manifest.json").write_text(
                json.dumps(
                    {
                        "compositions": [
                            {"path": "./AGENTS.project.md", "template": "lines.md", "mode": "ensure-lines"}
                        ],
                        "project_owned_paths": [{"path": "AGENTS.project.md"}],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "Project-owned paths"):
                load_template_pack(root)

    def test_manifest_rejects_duplicate_outputs_fragments_and_unknown_modes(self) -> None:
        invalid_manifests = (
            (
                {
                    "files": [{"path": "same", "template": "one"}],
                    "compositions": [{"path": "./same", "template": "two", "mode": "ensure-lines"}],
                },
                "Output paths must be unique",
            ),
            (
                {
                    "context_fragments": [
                        {"name": "same", "template": "one"},
                        {"name": "same", "template": "two"},
                    ]
                },
                "Context fragment names must be unique",
            ),
            (
                {"compositions": [{"path": "file", "template": "one", "mode": "unknown"}]},
                "Unsupported composition modes",
            ),
        )
        for payload, message in invalid_manifests:
            with self.subTest(message=message), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "manifest.json").write_text(json.dumps(payload), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, message):
                    load_template_pack(root)

    def test_template_source_cannot_escape_pack(self) -> None:
        pack = load_default_template_pack()
        with self.assertRaisesRegex(ValueError, "stay inside the pack"):
            pack.template_path("../outside.md")

    def test_generated_clean_dev_preserves_release_with_fake_cargo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            plan = build_plan(
                target,
                profile=_rust_profile(),
                pack=load_default_template_pack(),
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs"},
                force=False,
                dry_run=False,
            )
            apply_plan(plan, dry_run=False)
            (target / "target/debug").mkdir(parents=True)
            (target / "target/release").mkdir(parents=True)
            release_probe = target / "target/release/app"
            release_probe.write_text("release", encoding="utf-8")
            fake_bin = target / "fake-bin"
            fake_bin.mkdir()
            fake_cargo = fake_bin / "cargo"
            fake_cargo.write_text(
                "#!/bin/sh\n"
                "printf '%s\\n' \"$*\" > cargo-args.txt\n"
                "if [ \"$*\" = 'clean --profile dev' ]; then rm -rf target/debug; fi\n",
                encoding="utf-8",
            )
            fake_cargo.chmod(0o755)
            env = os.environ.copy()
            env["PATH"] = f"{fake_bin}:{env.get('PATH', '')}"
            completed = subprocess.run(["make", "clean-dev"], cwd=target, env=env, text=True, capture_output=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual((target / "cargo-args.txt").read_text(encoding="utf-8"), "clean --profile dev\n")
            self.assertFalse((target / "target/debug").exists())
            self.assertTrue(release_probe.exists())

    def test_generated_link_checker_accepts_rust_document(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            plan = build_plan(
                target,
                profile=_rust_profile(),
                pack=load_default_template_pack(),
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs", "skill/living-docs"},
                force=False,
                dry_run=False,
            )
            apply_plan(plan, dry_run=False)
            checker = target / ".agents/skills/living-docs/scripts/check_links.py"
            completed = subprocess.run([sys.executable, str(checker)], cwd=target, text=True, capture_output=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stderr)

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
