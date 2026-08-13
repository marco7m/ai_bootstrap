from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.applier import apply_plan
from ai_workflow_bootstrap.core.lifecycle import BLOCKING_STATUSES, content_hash
from ai_workflow_bootstrap.core.planner import build_plan
from ai_workflow_bootstrap.core.scanner import RepoProfile, detect_repo_profile
from ai_workflow_bootstrap.core.state import build_state, new_state
from ai_workflow_bootstrap.core.template_pack import load_default_template_pack


GROUPS = {
    "spec-driven",
    "living-docs",
    "skill/spec-driven",
    "skill/maintainability-audit",
    "skill/living-docs",
}
WORKFLOWS = ["spec-driven", "living-docs"]


def _normalized(text: str) -> str:
    return " ".join(text.split())


def _profile(name: str, stack: str) -> RepoProfile:
    commands = {"test": "python -m unittest"} if stack == "python" else {"test": "make test"}
    return RepoProfile(
        project_name=name,
        repo_name=name,
        detected_stacks=[stack],
        commands=commands,
        top_dirs=["src"],
    )


def _generate(root: Path, profile: RepoProfile) -> None:
    plan = build_plan(
        root,
        profile=profile,
        pack=load_default_template_pack(),
        enabled_workflows=WORKFLOWS,
        enabled_groups=GROUPS,
        force=False,
        dry_run=False,
    )
    apply_plan(plan, dry_run=False)


def _write_no_spec_repair(root: Path, *, completed: bool = True) -> Path:
    repair = root / "docs/changes/restore-existing-contract"
    repair.mkdir(parents=True, exist_ok=True)
    (repair / "plan.md").write_text(
        "# Implementation Plan: Restore Existing Contract\n\n"
        "- Existing authority: [Product contract](../../product/README.md)\n"
        "- Behavioral novelty: `none`\n\n"
        "## Reproduction\n\nA deterministic contract regression reproduces the defect.\n\n"
        "## Diagnosed Cause\n\nThe fixture implementation diverged from the linked contract.\n\n"
        "## Repair Boundary\n\nRestore only the linked behavior.\n\n"
        "## Risks, Regression and Validation\n\nRun focused and aggregate checks.\n",
        encoding="utf-8",
    )
    checkbox = "x" if completed else " "
    disposition = (
        "- Living documentation: `no-update-needed` — synthetic repair changes no durable owner\n"
        if completed
        else "- Living documentation: `pending`\n"
    )
    (repair / "tasks.md").write_text(
        "# Tasks: Restore Existing Contract\n\n"
        f"- [{checkbox}] Restore the contract\n"
        f"- [{checkbox}] Validate the regression\n\n"
        "## Closeout Disposition\n\n"
        + disposition
        + "\n### Maintainability audit scope\n\n"
        "| Repository-relative path |\n"
        "| --- |\n"
        "| `docs/changes/restore-existing-contract` |\n\n"
        "### Maintainability finding dispositions\n\n"
        "| Finding code | Path | Disposition | Rationale or reference |\n"
        "| --- | --- | --- | --- |\n"
        "| _None_ | — | no-findings | Synthetic repair scope has no findings |\n",
        encoding="utf-8",
    )
    (repair / "notes.md").write_text(
        "# Notes: Restore Existing Contract\n\n"
        "The focused regression and aggregate closeout passed.\n",
        encoding="utf-8",
    )
    return repair


def _run_closeout(root: Path, repair: Path) -> subprocess.CompletedProcess[str]:
    checker = root / ".agents/skills/living-docs/scripts/check_docs.py"
    return subprocess.run(
        [sys.executable, str(checker), str(root), "--closeout", repair.relative_to(root).as_posix()],
        text=True,
        capture_output=True,
        check=False,
    )


def _run_change_links(root: Path, repair: Path) -> subprocess.CompletedProcess[str]:
    checker = root / ".agents/skills/living-docs/scripts/check_links.py"
    return subprocess.run(
        [sys.executable, str(checker), str(root), "--change", repair.relative_to(root).as_posix()],
        text=True,
        capture_output=True,
        check=False,
    )


class SpecDrivenWorkflowTests(unittest.TestCase):
    def test_compact_surfaces_preserve_non_trivial_gate_without_forcing_a_spec(self) -> None:
        pack = load_default_template_pack()
        agents = pack.read_template("templates/AGENTS.md")
        skill = pack.read_template("templates/.agents/skills/spec-driven/SKILL.md")
        prompt = pack.read_template("templates/docs/START_PROMPT.md")

        for text in (agents, skill, prompt):
            self.assertIn("Every non-trivial implementation", text)
            self.assertIn("plan.md", text)
            self.assertIn("tasks.md", text)
            self.assertIn("explicit approval", text)
        self.assertIn("does not automatically require a new spec", agents)
        self.assertIn("trivial, unequivocal and low risk", agents)
        self.assertIn("one sentence", skill)
        self.assertIn("Do not create an artifact only to record classification", skill)

    def test_detailed_guide_owns_routes_repair_shape_and_compact_handoff(self) -> None:
        guide = load_default_template_pack().read_template("templates/docs/SPEC_DRIVEN.md")

        for route in (
            "New behavior or contract change",
            "Clear-contract bug",
            "Ambiguous bug or authority conflict",
            "Behavior-preserving refactor or maintenance",
            "Trivial unequivocal work",
            "Read-only investigation",
        ):
            self.assertIn(route, guide)
        self.assertIn("Every non-trivial implementation", guide)
        self.assertIn("docs/changes/<repair>/plan.md", guide)
        self.assertIn("intentionally has no `spec.md`", guide)
        self.assertIn("Reproduction", guide)
        self.assertIn("Diagnosed cause", guide)
        self.assertIn("Repair boundary", guide)
        self.assertIn("Compact handoff", guide)
        self.assertIn("Do not print a standard classification block", _normalized(guide))

    def test_existing_artifact_templates_support_a_no_spec_repair(self) -> None:
        pack = load_default_template_pack()
        plan = pack.read_template("templates/docs/changes/_templates/plan.md")
        tasks = pack.read_template("templates/docs/changes/_templates/tasks.md")
        notes = pack.read_template("templates/docs/changes/_templates/notes.md")

        for marker in (
            "Existing authority",
            "Behavioral novelty",
            "Reproduction",
            "Diagnosed cause",
            "Repair boundary",
            "Regression",
        ):
            self.assertIn(marker, plan)
        self.assertIn("Confirm plan and tasks were explicitly approved", tasks)
        self.assertIn("Stop if behavioral novelty", tasks)
        self.assertNotIn("Re-read approved spec and plan", tasks)
        self.assertIn(
            "Do not create this file when there is nothing material to record",
            _normalized(notes),
        )

    def test_fresh_python_rust_and_node_profiles_deliver_the_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            profiles = [_profile("python-example", "python"), _profile("rust-example", "rust")]
            for profile in profiles:
                root = base / profile.repo_name
                root.mkdir()
                _generate(root, profile)
                repair = _write_no_spec_repair(root)
                result = (
                    _run_change_links(root, repair)
                    if profile.detected_stacks == ["rust"]
                    else _run_closeout(root, repair)
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertFalse((repair / "spec.md").exists())
                self.assertIn("Every non-trivial implementation", (root / "AGENTS.md").read_text())

            node = base / "node-example"
            node.mkdir()
            (node / "package.json").write_text(
                '{"scripts":{"build":"vite build","test":"vitest run"}}\n',
                encoding="utf-8",
            )
            node_profile = detect_repo_profile(node, "Node Example")
            self.assertIn("node", node_profile.detected_stacks)
            self.assertEqual(node_profile.commands["test"], "npm run test")
            _generate(node, node_profile)
            node_agents = (node / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("npm run test", node_agents)
            self.assertNotIn("cargo test", node_agents)
            repair = _write_no_spec_repair(node)
            self.assertEqual(_run_closeout(node, repair).returncode, 0)

    def test_no_spec_closeout_keeps_existing_failure_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _generate(root, _profile("example", "python"))
            repair = _write_no_spec_repair(root, completed=False)

            pending = _run_closeout(root, repair)
            _write_no_spec_repair(root, completed=True)
            notes = repair / "notes.md"
            notes.write_text(
                notes.read_text(encoding="utf-8") + "\n[Missing](../../product/missing.md)\n",
                encoding="utf-8",
            )
            broken_link = _run_closeout(root, repair)

        self.assertEqual(pending.returncode, 1)
        self.assertIn("closeout-invalid", pending.stderr)
        self.assertEqual(broken_link.returncode, 1)
        self.assertIn("broken-link", broken_link.stderr)

    def test_upgrade_from_071_updates_managed_and_preserves_project_knowledge(self) -> None:
        pack = load_default_template_pack()
        self.assertEqual(pack.version, "0.8.0")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            old_agents = "# Managed workflow from pack 0.7.1\n"
            old_seed = "# Initial index from pack 0.7.1\n"
            evolved_seed = old_seed + "\nProject-owned knowledge.\n"
            project_rules = "# Project rules\n\nPreserve this exact text.\n"
            (root / "AGENTS.md").write_text(old_agents, encoding="utf-8")
            (root / "docs/INDEX.md").write_text(evolved_seed, encoding="utf-8")
            (root / "AGENTS.project.md").write_text(project_rules, encoding="utf-8")
            prior_files = {
                "AGENTS.md": {
                    "status": "unchanged",
                    "lifecycle": "managed",
                    "template": "templates/AGENTS.md",
                    "template_hash": content_hash(old_agents),
                    "applied_content_hash": content_hash(old_agents),
                    "applied_version": "0.7.1",
                },
                "docs/INDEX.md": {
                    "status": "unchanged",
                    "lifecycle": "seeded",
                    "template": "templates/docs/INDEX.md",
                    "template_hash": content_hash(old_seed),
                    "applied_content_hash": content_hash(old_seed),
                    "applied_version": "0.7.1",
                },
            }
            prior = new_state(
                target_path=str(root),
                template_pack="default",
                template_pack_version="0.7.1",
                enabled_workflows=WORKFLOWS,
                tool_version="test",
                files=prior_files,
            )
            preview = build_plan(
                root,
                profile=_profile("upgrade-example", "python"),
                pack=pack,
                enabled_workflows=WORKFLOWS,
                enabled_groups=GROUPS,
                force=True,
                dry_run=True,
                prior_files=prior.files,
            )
            preview_by_path = {
                item.path.relative_to(root).as_posix(): item for item in preview.results
            }
            self.assertEqual(preview_by_path["AGENTS.md"].status, "overwritten")
            self.assertEqual(preview_by_path["docs/INDEX.md"].status, "preserved")
            self.assertFalse({item.status for item in preview.results} & BLOCKING_STATUSES)
            plan = build_plan(
                root,
                profile=_profile("upgrade-example", "python"),
                pack=pack,
                enabled_workflows=WORKFLOWS,
                enabled_groups=GROUPS,
                force=True,
                dry_run=False,
                prior_files=prior.files,
            )
            by_path = {item.path.relative_to(root).as_posix(): item for item in plan.results}
            self.assertEqual(by_path["AGENTS.md"].status, "overwritten")
            self.assertEqual(by_path["docs/INDEX.md"].status, "preserved")
            self.assertFalse({item.status for item in plan.results} & BLOCKING_STATUSES)
            results = apply_plan(plan, dry_run=False)
            state = build_state(plan=plan, results=results, tool_version="test", prior_state=prior)

            self.assertEqual(state.template_pack_version, "0.8.0")
            self.assertEqual((root / "docs/INDEX.md").read_text(), evolved_seed)
            self.assertEqual((root / "AGENTS.project.md").read_text(), project_rules)
            self.assertIn("Every non-trivial implementation", (root / "AGENTS.md").read_text())

            managed_only = build_plan(
                root,
                profile=_profile("upgrade-example", "python"),
                pack=pack,
                enabled_workflows=WORKFLOWS,
                enabled_groups=GROUPS,
                force=True,
                dry_run=False,
                prior_files=state.files,
                managed_only=True,
            )
            self.assertNotIn(root / "docs/INDEX.md", {item.path for item in managed_only.results})
            self.assertFalse({item.status for item in managed_only.results} & BLOCKING_STATUSES)
            apply_plan(managed_only, dry_run=False)
            self.assertEqual((root / "docs/INDEX.md").read_text(), evolved_seed)
            self.assertEqual((root / "AGENTS.project.md").read_text(), project_rules)

            reapply = build_plan(
                root,
                profile=_profile("upgrade-example", "python"),
                pack=pack,
                enabled_workflows=WORKFLOWS,
                enabled_groups=GROUPS,
                force=True,
                dry_run=True,
                prior_files=state.files,
            )
            self.assertFalse({item.status for item in reapply.results} & BLOCKING_STATUSES)
            repair = _write_no_spec_repair(root)
            self.assertEqual(_run_closeout(root, repair).returncode, 0)
            self.assertFalse((repair / "spec.md").exists())


if __name__ == "__main__":
    unittest.main()
