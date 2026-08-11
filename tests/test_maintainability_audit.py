from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.applier import apply_plan
from ai_workflow_bootstrap.core.planner import build_plan
from ai_workflow_bootstrap.core.scanner import RepoProfile
from ai_workflow_bootstrap.core.template_pack import load_default_template_pack


def _audit_script() -> Path:
    return load_default_template_pack().template_path(
        "templates/.agents/skills/maintainability-audit/scripts/audit_repository.py"
    )


def _write_knowledge_base(root: Path) -> None:
    (root / "docs/product").mkdir(parents=True, exist_ok=True)
    (root / "docs/architecture").mkdir(parents=True, exist_ok=True)
    (root / "docs/decisions").mkdir(parents=True, exist_ok=True)
    (root / "docs/INDEX.md").write_text(
        "# Index\n\n"
        "- [Product](product/README.md)\n"
        "- [Architecture](architecture/README.md)\n"
        "- [Capabilities](CAPABILITIES.md)\n"
        "- [Decisions](decisions/README.md)\n",
        encoding="utf-8",
    )
    (root / "docs/product/README.md").write_text("# Product\n", encoding="utf-8")
    (root / "docs/architecture/README.md").write_text("# Architecture\n", encoding="utf-8")
    (root / "docs/decisions/README.md").write_text("# Decisions\n", encoding="utf-8")
    (root / "docs/CAPABILITIES.md").write_text(
        "# Capabilities\n\n"
        "| Capability | Product contract | Architecture | Current state | Evidence | Approved target | Active change |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n",
        encoding="utf-8",
    )


def _profile(name: str, stack: str) -> RepoProfile:
    return RepoProfile(
        project_name=name,
        repo_name=name,
        detected_stacks=[stack],
        commands={"test": "python -m unittest"} if stack == "python" else {"test": "make test"},
        top_dirs=["src"],
    )


class MaintainabilityAuditTests(unittest.TestCase):
    def _run(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(_audit_script()), str(root), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def _json(self, root: Path, *args: str) -> dict[str, object]:
        result = self._run(root, *args, "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_requires_an_explicit_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(Path(tmp))

        self.assertEqual(result.returncode, 2)
        self.assertIn("--path", result.stderr)
        self.assertIn("--repo-wide", result.stderr)

    def test_large_markdown_is_advisory_and_output_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_knowledge_base(root)
            large = root / "docs/architecture/large.md"
            large.write_text("# Large\n" + "cohesive reference\n" * 250, encoding="utf-8")

            first = self._run(root, "--path", "docs/architecture/large.md")
            second = self._run(root, "--path", "docs/architecture/large.md")

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertIn("large-file-review", first.stdout)
        self.assertIn("advisory", first.stdout)
        self.assertIn("docs/architecture/large.md", first.stdout)

    def test_small_file_does_not_cross_the_size_signal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_knowledge_base(root)
            small = root / "src/small.py"
            small.parent.mkdir()
            small.write_text("def answer():\n    return 42\n", encoding="utf-8")

            report = self._json(root, "--path", "src/small.py")

        self.assertNotIn(
            "large-file-review",
            {finding["code"] for finding in report["findings"]},
        )

    def test_substantive_repo_reports_a_missing_required_knowledge_owner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            (root / "src/app.py").write_text("VALUE = 1\n", encoding="utf-8")
            (root / "docs").mkdir()

            report = self._json(root, "--repo-wide")

        missing_paths = {
            finding["path"]
            for finding in report["findings"]
            if finding["code"] == "knowledge-owner-placeholder"
        }
        self.assertEqual(
            missing_paths,
            {"docs/product/README.md", "docs/architecture/README.md"},
        )

    def test_orphan_current_doc_is_reported_and_linked_doc_is_not(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_knowledge_base(root)
            detail = root / "docs/product/gameplay.md"
            detail.write_text("# Gameplay\n", encoding="utf-8")

            orphan_report = self._json(root, "--repo-wide")
            (root / "docs/product/README.md").write_text(
                "# Product\n\n- [Gameplay](gameplay.md)\n",
                encoding="utf-8",
            )
            linked_report = self._json(root, "--repo-wide")

        self.assertIn(
            "orphan-current-doc",
            {finding["code"] for finding in orphan_report["findings"]},
        )
        self.assertNotIn(
            "orphan-current-doc",
            {finding["code"] for finding in linked_report["findings"]},
        )

    def test_concentration_is_independent_from_size_and_size_remains_advisory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_knowledge_base(root)
            rows = "".join(
                (
                    f"| Capability {index} | [Product](product/README.md#cap-{index}) "
                    f"| [Architecture](architecture/README.md#cap-{index}) "
                    "| `partial` | evidence | — | — |\n"
                )
                for index in range(4)
            )
            (root / "docs/CAPABILITIES.md").write_text(
                "# Capabilities\n\n"
                "| Capability | Product contract | Architecture | Current state | Evidence | Approved target | Active change |\n"
                "| --- | --- | --- | --- | --- | --- | --- |\n"
                + rows,
                encoding="utf-8",
            )

            small_report = self._json(root, "--repo-wide")
            (root / "docs/architecture/README.md").write_text(
                "# Architecture\n" + "focused responsibility\n" * 250,
                encoding="utf-8",
            )
            large_report = self._json(root, "--repo-wide")

        self.assertIn(
            "knowledge-owner-concentration",
            {finding["code"] for finding in small_report["findings"]},
        )
        self.assertNotIn(
            "large-file-review",
            {finding["code"] for finding in small_report["findings"]},
        )
        self.assertIn(
            "knowledge-owner-concentration",
            {finding["code"] for finding in large_report["findings"]},
        )
        self.assertIn(
            "large-file-review",
            {finding["code"] for finding in large_report["findings"]},
        )

    def test_completed_change_requires_living_doc_disposition(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_knowledge_base(root)
            tasks = root / "docs/changes/example/tasks.md"
            tasks.parent.mkdir(parents=True)
            tasks.write_text(
                "# Tasks\n\n- [x] Implement behavior\n- [x] Validate behavior\n",
                encoding="utf-8",
            )

            missing = self._json(root, "--path", "docs/changes/example/tasks.md")
            tasks.write_text(
                "# Tasks\n\n"
                "- [x] Implement behavior\n"
                "- [x] Validate behavior\n\n"
                "## Closeout Disposition\n\n"
                "- Living documentation: `no-update-needed` — behavior is internal only\n"
                "- Maintainability: `accepted` — cohesive local implementation\n",
                encoding="utf-8",
            )
            justified = self._json(root, "--path", "docs/changes/example/tasks.md")

        self.assertIn(
            "change-closeout-undispositioned",
            {finding["code"] for finding in missing["findings"]},
        )
        self.assertNotIn(
            "change-closeout-undispositioned",
            {finding["code"] for finding in justified["findings"]},
        )

    def test_grandfathered_completed_change_remains_visible_as_legacy_debt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_knowledge_base(root)
            tasks = root / "docs/changes/old/tasks.md"
            tasks.parent.mkdir(parents=True)
            tasks.write_text("# Tasks\n\n- [x] Implement\n", encoding="utf-8")
            (root / "docs/LIVING_DOCUMENTATION_BASELINE.md").write_text(
                "# Baseline\n\n"
                "- Baseline status: `established`\n"
                "- Baseline evidence: `reviewed fixture`\n\n"
                "## Grandfathered closeout debt\n\n"
                "| Change artifact | Debt status | Review evidence or rationale |\n"
                "| --- | --- | --- |\n"
                "| `docs/changes/old` | unresolved | fixture |\n\n"
                "## Reviewed debt dispositions\n\n"
                "| Change artifact | Disposition | Review evidence or rationale |\n"
                "| --- | --- | --- |\n"
                "| _None_ | — | — |\n",
                encoding="utf-8",
            )

            report = self._json(root, "--path", "docs/changes/old/tasks.md")

        codes = {finding["code"] for finding in report["findings"]}
        self.assertIn("legacy-closeout-debt", codes)
        self.assertNotIn("change-closeout-undispositioned", codes)

    def test_scoped_change_does_not_report_unrelated_knowledge_debt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_knowledge_base(root)
            (root / "docs/product/orphan.md").write_text("# Orphan\n", encoding="utf-8")
            tasks = root / "docs/changes/example/tasks.md"
            tasks.parent.mkdir(parents=True)
            tasks.write_text("# Tasks\n\n- [ ] Implement behavior\n", encoding="utf-8")

            report = self._json(root, "--path", "docs/changes/example/tasks.md")

        self.assertNotIn(
            "orphan-current-doc",
            {finding["code"] for finding in report["findings"]},
        )

    def test_sensitive_and_cache_paths_are_skipped_without_content_leakage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_knowledge_base(root)
            secret = "DO_NOT_EMIT_THIS_SECRET"
            (root / ".env").write_text(f"TOKEN={secret}\n", encoding="utf-8")
            cached = root / "__pycache__/large.py"
            cached.parent.mkdir()
            cached.write_text(f"# {secret}\n" * 600, encoding="utf-8")

            result = self._run(
                root,
                "--path",
                ".env",
                "--path",
                "__pycache__",
                "--format",
                "json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(secret, result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report["scope"]["inspected_files"], 0)
        self.assertEqual(report["findings"], [])

    def test_generated_workflow_integrates_audit_without_silent_scope_expansion(self) -> None:
        pack = load_default_template_pack()
        agents = pack.read_template("templates/AGENTS.md")
        spec_skill = pack.read_template("templates/.agents/skills/spec-driven/SKILL.md")
        audit_skill = pack.read_template("templates/.agents/skills/maintainability-audit/SKILL.md")
        living_skill = pack.read_template("templates/.agents/skills/living-docs/SKILL.md")
        guide = pack.read_template("templates/docs/SPEC_DRIVEN.md")
        policy = pack.read_template("templates/docs/LIVING_DOCUMENTATION.md")
        spec_template = pack.read_template("templates/docs/changes/_templates/spec.md")
        plan_template = pack.read_template("templates/docs/changes/_templates/plan.md")
        tasks_template = pack.read_template("templates/docs/changes/_templates/tasks.md")

        self.assertIn("code or living-knowledge maintainability", agents)
        self.assertIn("Before drafting the spec", spec_skill)
        self.assertIn("After implementation", spec_skill)
        self.assertIn("audit_repository.py", audit_skill)
        self.assertIn("advisory observation", audit_skill)
        self.assertIn("threshold", audit_skill)
        self.assertIn("compact hubs", living_skill)
        self.assertIn("check_docs.py", living_skill)
        self.assertIn("silent scope expansion", guide)
        self.assertIn("Scoped audit evidence", spec_template)
        self.assertIn("Finding disposition", plan_template)
        self.assertIn("## Closeout Disposition", tasks_template)
        self.assertIn("Living documentation: `pending`", tasks_template)
        self.assertIn("compact navigation hubs", policy)

    def test_generated_audit_executes_in_fresh_python_and_rust_projects(self) -> None:
        pack = load_default_template_pack()
        groups = {
            "spec-driven",
            "living-docs",
            "skill/spec-driven",
            "skill/maintainability-audit",
            "skill/living-docs",
        }
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            for name, stack in (("python-example", "python"), ("rust-example", "rust")):
                target = base / name
                target.mkdir()
                plan = build_plan(
                    target,
                    profile=_profile(name, stack),
                    pack=pack,
                    enabled_workflows=["spec-driven", "living-docs"],
                    enabled_groups=groups,
                    force=False,
                    dry_run=False,
                )
                apply_plan(plan, dry_run=False)
                source = target / "src/example.py"
                source.parent.mkdir(exist_ok=True)
                source.write_text("def answer():\n    return 42\n", encoding="utf-8")
                audit = (
                    target
                    / ".agents/skills/maintainability-audit/scripts/audit_repository.py"
                )
                result = subprocess.run(
                    [sys.executable, str(audit), str(target), "--path", "src/example.py"],
                    text=True,
                    capture_output=True,
                    check=False,
                )

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("No advisory maintainability signals", result.stdout)


if __name__ == "__main__":
    unittest.main()
