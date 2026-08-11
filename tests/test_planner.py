from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.planner import build_plan
from ai_workflow_bootstrap.core.lifecycle import content_hash
from ai_workflow_bootstrap.core.scanner import RepoProfile
from ai_workflow_bootstrap.core.template_pack import load_default_template_pack
from ai_workflow_bootstrap.core.template_pack import TemplateObsoleteFileSpec, TemplatePack
from ai_workflow_bootstrap.core.applier import apply_plan


class PlannerTests(unittest.TestCase):
    def test_legacy_incident_state_preserves_all_evolved_seeded_owners_under_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            seeded_paths = {
                "docs/INDEX.md": "# Established index\n",
                "docs/CAPABILITIES.md": "# Established capabilities\n",
                "docs/product/README.md": "# Established product\n",
                "docs/architecture/README.md": "# Established architecture\n",
                "docs/ROADMAP.md": "# Established roadmap\n",
            }
            for relative, content in seeded_paths.items():
                path = target / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            agents = target / "AGENTS.md"
            agents.write_text("# Old managed policy\n", encoding="utf-8")
            legacy_state = {
                relative: {"status": "overwritten", "template_hash": "a" * 64}
                for relative in seeded_paths
            }

            plan = build_plan(
                target,
                profile=RepoProfile(project_name="Example", repo_name="example"),
                pack=load_default_template_pack(),
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs"},
                force=True,
                dry_run=False,
                prior_files=legacy_state,
            )

            for relative, original in seeded_paths.items():
                result = next(item for item in plan.results if item.path == target / relative)
                self.assertEqual(result.lifecycle, "seeded")
                self.assertEqual(result.status, "preserved")
                self.assertIn("provenance is unavailable", result.message)
                self.assertEqual((target / relative).read_text(encoding="utf-8"), original)
            self.assertEqual(
                next(item for item in plan.results if item.path == agents).status,
                "overwritten",
            )

            apply_plan(plan, dry_run=False)
            for relative, original in seeded_paths.items():
                self.assertEqual((target / relative).read_text(encoding="utf-8"), original)
            self.assertIn("Project: Example", agents.read_text(encoding="utf-8"))

    def test_untouched_seed_updates_but_project_drift_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            index = target / "docs/INDEX.md"
            index.parent.mkdir(parents=True)
            index.write_text("old seed\n", encoding="utf-8")
            pack = load_default_template_pack()
            prior = {"docs/INDEX.md": {"applied_content_hash": content_hash("old seed\n")}}

            safe_plan = build_plan(
                target,
                profile=RepoProfile(project_name="Example", repo_name="example"),
                pack=pack,
                enabled_workflows=["living-docs"],
                enabled_groups={"living-docs"},
                force=True,
                dry_run=True,
                prior_files=prior,
            )
            self.assertEqual(next(item for item in safe_plan.results if item.path == index).status, "updated")

            index.write_text("project knowledge\n", encoding="utf-8")
            drift_plan = build_plan(
                target,
                profile=RepoProfile(project_name="Example", repo_name="example"),
                pack=pack,
                enabled_workflows=["living-docs"],
                enabled_groups={"living-docs"},
                force=True,
                dry_run=True,
                prior_files=prior,
            )
            self.assertEqual(next(item for item in drift_plan.results if item.path == index).status, "preserved")

    def test_reviewed_baseline_seed_is_preserved_under_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            baseline = target / "docs/LIVING_DOCUMENTATION_BASELINE.md"
            baseline.parent.mkdir(parents=True)
            original = "# Reviewed baseline\n\n- Baseline status: `established`\n"
            baseline.write_text(original, encoding="utf-8")
            prior = {
                "docs/LIVING_DOCUMENTATION_BASELINE.md": {
                    "applied_content_hash": content_hash("old generated baseline\n"),
                    "applied_version": "0.6.0",
                }
            }

            plan = build_plan(
                target,
                profile=RepoProfile(project_name="Example", repo_name="example"),
                pack=load_default_template_pack(),
                enabled_workflows=["living-docs"],
                enabled_groups={"living-docs"},
                force=True,
                dry_run=False,
                prior_files=prior,
            )
            result = next(item for item in plan.results if item.path == baseline)
            self.assertEqual(result.status, "preserved")

            apply_plan(plan, dry_run=False)
            self.assertEqual(baseline.read_text(encoding="utf-8"), original)

    def test_managed_only_excludes_seeded_and_obsolete_operations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            legacy = target / "docs/AI_CONTEXT.md"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("legacy\n", encoding="utf-8")
            plan = build_plan(
                target,
                profile=RepoProfile(project_name="Example", repo_name="example"),
                pack=load_default_template_pack(),
                enabled_workflows=["spec-driven", "living-docs"],
                enabled_groups={"spec-driven", "living-docs"},
                force=True,
                dry_run=True,
                managed_only=True,
            )

            self.assertTrue(any(item.path == target / "AGENTS.md" for item in plan.results))
            self.assertFalse(any(item.lifecycle == "seeded" for item in plan.results))
            self.assertFalse(
                any(item.path == target / "docs/LIVING_DOCUMENTATION_BASELINE.md" for item in plan.results)
            )
            self.assertFalse(any(item.kind == "deletion" for item in plan.results))

    def test_generated_path_cannot_follow_symlink_outside_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside:
            target = Path(tmp)
            (target / "docs").symlink_to(Path(outside), target_is_directory=True)

            with self.assertRaisesRegex(ValueError, "stay inside the target repository"):
                build_plan(
                    target,
                    profile=RepoProfile(project_name="Example", repo_name="example"),
                    pack=load_default_template_pack(),
                    enabled_workflows=["spec-driven", "living-docs"],
                    enabled_groups={"spec-driven", "living-docs"},
                    force=False,
                    dry_run=True,
                )

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
                prior_files={"docs/AI_CONTEXT.md": {"applied_content_hash": content_hash("legacy\n")}},
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
