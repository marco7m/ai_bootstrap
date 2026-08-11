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


GROUPS = {
    "spec-driven",
    "living-docs",
    "skill/spec-driven",
    "skill/maintainability-audit",
    "skill/living-docs",
}


def _generate(root: Path) -> Path:
    plan = build_plan(
        root,
        profile=RepoProfile(project_name="Example", repo_name="example", detected_stacks=["python"]),
        pack=load_default_template_pack(),
        enabled_workflows=["spec-driven", "living-docs"],
        enabled_groups=GROUPS,
        force=False,
        dry_run=False,
    )
    apply_plan(plan, dry_run=False)
    return root / ".agents/skills/living-docs/scripts/check_docs.py"


class DocsCheckerTests(unittest.TestCase):
    def _run(self, checker: Path, root: Path, *args: str, cwd: Path | None = None):
        return subprocess.run(
            [sys.executable, str(checker), str(root), *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_fresh_scaffold_passes_and_reports_unestablished_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as other:
            root = Path(tmp)
            checker = _generate(root)
            result = self._run(checker, root, cwd=Path(other))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("baseline-unestablished", result.stdout)
        self.assertIn("Documentation checks passed", result.stdout)

    def test_orphan_owner_and_wrong_capability_authority_are_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            checker = _generate(root)
            (root / "docs/product/orphan.md").write_text("# Orphan\n", encoding="utf-8")
            (root / "docs/CAPABILITIES.md").write_text(
                "# Capabilities\n\n"
                "| Capability | Product contract | Architecture | Current state | Evidence | Approved target | Active change |\n"
                "| --- | --- | --- | --- | --- | --- | --- |\n"
                "| Play | [Wrong](architecture/README.md) | [Wrong](product/README.md) | `partial` | — | — | — |\n",
                encoding="utf-8",
            )
            result = self._run(checker, root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("orphan-current-owner", result.stderr)
        self.assertIn("target must stay under docs/product", result.stderr)
        self.assertIn("target must stay under docs/architecture", result.stderr)

    def test_established_baseline_grandfathers_only_listed_debt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            checker = _generate(root)
            old = root / "docs/changes/old"
            new = root / "docs/changes/new"
            old.mkdir(parents=True)
            new.mkdir(parents=True)
            completed = "# Tasks\n\n- [x] Implement\n- [x] Validate\n"
            (old / "tasks.md").write_text(completed, encoding="utf-8")
            (new / "tasks.md").write_text(completed, encoding="utf-8")
            (root / "docs/LIVING_DOCUMENTATION_BASELINE.md").write_text(
                "# Baseline\n\n"
                "- Baseline status: `established`\n"
                "- Baseline evidence: `reviewed inventory at test fixture`\n\n"
                "## Grandfathered closeout debt\n\n"
                "| Change artifact | Debt status | Review evidence or rationale |\n"
                "| --- | --- | --- |\n"
                "| `docs/changes/old` | unresolved | fixture review |\n\n"
                "## Reviewed debt dispositions\n\n"
                "| Change artifact | Disposition | Review evidence or rationale |\n"
                "| --- | --- | --- |\n"
                "| _None_ | — | — |\n",
                encoding="utf-8",
            )
            result = self._run(checker, root)

            (new / "tasks.md").write_text(
                completed
                + "\n## Closeout Disposition\n\n"
                "- Living documentation: `updated`\n",
                encoding="utf-8",
            )
            baseline_path = root / "docs/LIVING_DOCUMENTATION_BASELINE.md"
            baseline_path.write_text(
                baseline_path.read_text(encoding="utf-8")
                .replace("| _None_ | — | — |", "| `docs/changes/old` | reviewed | owner review |", 1)
                .replace("| `docs/changes/old` | unresolved | fixture review |", "| _None_ | — | — |"),
                encoding="utf-8",
            )
            reviewed = self._run(checker, root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("docs/changes/new/tasks.md", result.stderr)
        self.assertNotIn("docs/changes/old/tasks.md", result.stderr)
        self.assertEqual(reviewed.returncode, 0, reviewed.stderr)

    def test_targeted_closeout_rejects_pending_and_accepts_final_dispositions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            checker = _generate(root)
            change = root / "docs/changes/active"
            change.mkdir(parents=True)
            tasks = change / "tasks.md"
            tasks.write_text(
                "# Tasks\n\n- [ ] Implement\n\n"
                "## Closeout Disposition\n\n"
                "- Living documentation: `pending`\n"
                "- Maintainability findings: `pending`\n",
                encoding="utf-8",
            )
            pending = self._run(checker, root, "--closeout", "docs/changes/active")
            tasks.write_text(
                "# Tasks\n\n- [x] Implement\n\n"
                "## Closeout Disposition\n\n"
                "- Living documentation: `no-update-needed` — only fixture content changed\n"
                "- Maintainability findings: `no-findings in scoped audit`\n",
                encoding="utf-8",
            )
            complete = self._run(checker, root, "--closeout", "docs/changes/active")

        self.assertEqual(pending.returncode, 1)
        self.assertIn("closeout-invalid", pending.stderr)
        self.assertIn("closeout-maintainability", pending.stderr)
        self.assertEqual(complete.returncode, 0, complete.stderr)

    def test_invalid_supported_fragment_is_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            checker = _generate(root)
            product = root / "docs/product/README.md"
            product.write_text("# Product\n\n[Missing](../architecture/README.md#missing)\n", encoding="utf-8")
            result = self._run(checker, root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("broken-fragment", result.stderr)

    def test_targeted_closeout_cannot_escape_repository(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            checker = _generate(root)
            result = self._run(checker, root, "--closeout", "../../outside")

        self.assertEqual(result.returncode, 1)
        self.assertIn("closeout-path", result.stderr)


if __name__ == "__main__":
    unittest.main()
