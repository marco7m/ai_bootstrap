from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.applier import PlanConflictError, apply_plan
from ai_workflow_bootstrap.core.planner import build_plan
from ai_workflow_bootstrap.core.scanner import RepoProfile
from ai_workflow_bootstrap.core.template_pack import load_default_template_pack


def _profile() -> RepoProfile:
    return RepoProfile(project_name="Example Project", repo_name="example-project")


class ApplierTests(unittest.TestCase):
    def test_make_conflict_blocks_all_writes_with_actionable_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "Cargo.toml").write_text("[package]\nname='example'\nversion='0.1.0'\n", encoding="utf-8")
            makefile = target / "Makefile"
            makefile.write_text("run:\n\tcargo run --features desktop\n", encoding="utf-8")
            plan = build_plan(
                target,
                profile=RepoProfile(project_name="Example", repo_name="example", detected_stacks=["rust"]),
                pack=load_default_template_pack(),
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs"},
                force=True,
                dry_run=False,
            )
            conflict = next(item for item in plan.results if item.status == "conflict")
            self.assertIn("Current definition", conflict.message)
            self.assertIn("Required definition", conflict.message)
            self.assertIn("--force does not bypass repository-owned file conflicts", conflict.message)
            self.assertIn("rerun the bootstrap", conflict.message)

            with self.assertRaisesRegex(PlanConflictError, "Blocked before writing any files"):
                apply_plan(plan, dry_run=False)

            self.assertFalse((target / "AGENTS.md").exists())
            self.assertEqual(makefile.read_text(encoding="utf-8"), "run:\n\tcargo run --features desktop\n")
    def test_without_force_preserves_existing_and_legacy_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            agents = target / "AGENTS.md"
            legacy = target / "docs/PROJECT_SPEC.md"
            agents.write_text("custom\n", encoding="utf-8")
            legacy.parent.mkdir(parents=True)
            legacy.write_text("legacy\n", encoding="utf-8")
            plan = build_plan(
                target,
                profile=_profile(),
                pack=load_default_template_pack(),
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs"},
                force=False,
                dry_run=False,
            )

            results = apply_plan(plan, dry_run=False)

            self.assertEqual(next(item for item in results if item.path == agents).status, "skipped")
            self.assertEqual(agents.read_text(encoding="utf-8"), "custom\n")
            self.assertEqual(legacy.read_text(encoding="utf-8"), "legacy\n")
            self.assertFalse(any(item.kind == "deletion" for item in results))

    def test_force_overwrites_without_backup_and_deletes_known_legacy_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            agents = target / "AGENTS.md"
            legacy = target / "docs/PROJECT_SPEC.md"
            agents.write_text("custom\n", encoding="utf-8")
            legacy.parent.mkdir(parents=True)
            legacy.write_text("legacy\n", encoding="utf-8")
            plan = build_plan(
                target,
                profile=_profile(),
                pack=load_default_template_pack(),
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs"},
                force=True,
                dry_run=False,
            )

            deletion = next(item for item in plan.results if item.path == legacy)
            self.assertEqual(deletion.kind, "deletion")
            self.assertEqual(deletion.status, "deleted")
            results = apply_plan(plan, dry_run=False)

            self.assertEqual(next(item for item in results if item.path == agents).status, "overwritten")
            self.assertIn("Project: Example Project", agents.read_text(encoding="utf-8"))
            self.assertFalse(legacy.exists())
            self.assertEqual(list(target.rglob("*.bak-*")), [])

    def test_force_spec_only_does_not_delete_living_legacy_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            legacy = target / "docs/PROJECT_SPEC.md"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("legacy\n", encoding="utf-8")
            plan = build_plan(
                target,
                profile=_profile(),
                pack=load_default_template_pack(),
                enabled_workflows=["spec-driven"],
                enabled_groups={"spec-driven"},
                force=True,
                dry_run=False,
            )

            apply_plan(plan, dry_run=False)

            self.assertTrue(legacy.exists())
            self.assertFalse(any(item.kind == "deletion" for item in plan.results))

    def test_legacy_directory_is_reported_and_never_recursively_deleted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            legacy = target / "docs/PROJECT_SPEC.md"
            legacy.mkdir(parents=True)
            (legacy / "keep.txt").write_text("keep\n", encoding="utf-8")
            plan = build_plan(
                target,
                profile=_profile(),
                pack=load_default_template_pack(),
                enabled_workflows=["living-docs"],
                enabled_groups={"living-docs"},
                force=True,
                dry_run=False,
            )

            deletion = next(item for item in plan.results if item.path == legacy)
            self.assertEqual(deletion.kind, "deletion")
            self.assertEqual(deletion.status, "skipped")
            apply_plan(plan, dry_run=False)
            self.assertTrue((legacy / "keep.txt").exists())


if __name__ == "__main__":
    unittest.main()
