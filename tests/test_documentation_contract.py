from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.template_pack import load_default_template_pack


def _contract_module():
    path = load_default_template_pack().template_path(
        "templates/.agents/skills/living-docs/scripts/documentation_contract.py"
    )
    spec = importlib.util.spec_from_file_location("documentation_contract", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class DocumentationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = _contract_module()

    def test_heading_slug_preserves_space_and_authored_hyphens_around_punctuation(self) -> None:
        self.assertEqual(
            self.contract.heading_slug("Integrated reliability qualification — 2026-08-07"),
            "integrated-reliability-qualification--2026-08-07",
        )
        self.assertEqual(self.contract.heading_slug("Alpha  beta-gamma"), "alpha--beta-gamma")

    def test_heading_fragments_support_links_duplicates_and_unicode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "doc.md"
            path.write_text(
                "# Café & [Current Contract](contract.md)\n"
                "## Repeated heading\n"
                "## Repeated heading\n",
                encoding="utf-8",
            )

            self.assertEqual(
                self.contract.heading_fragments(path),
                {"café--current-contract", "repeated-heading", "repeated-heading-1"},
            )

    def test_percent_encoded_unicode_fragment_resolves_without_ascii_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "docs/source.md"
            target = root / "docs/target.md"
            source.parent.mkdir()
            source.write_text("# Source\n", encoding="utf-8")
            target.write_text("# Interação segura\n", encoding="utf-8")

            resolved, fragment = self.contract.resolve_local_target(
                root,
                source,
                "target.md#intera%C3%A7%C3%A3o-segura",
            )

            self.assertEqual(resolved, target)
            self.assertEqual(fragment, "interação-segura")
            self.assertTrue(self.contract.fragment_exists(target, fragment))
            self.assertFalse(self.contract.fragment_exists(target, "interacao-segura"))

    def test_markdown_links_ignore_images_and_fenced_examples(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "doc.md"
            path.write_text(
                "[Current](current.md)\n![Image](ignored.png)\n"
                "```md\n[Example](ignored.md)\n```\n",
                encoding="utf-8",
            )

            self.assertEqual(self.contract.markdown_links(path), ["current.md"])

    def test_capability_rows_keep_authority_routes_and_state(self) -> None:
        rows = self.contract.parse_capability_rows(
            "| Capability | Product contract | Architecture | Current state | Evidence | Approved target | Active change |\n"
            "| --- | --- | --- | --- | --- | --- | --- |\n"
            "| Play | [Rules](product/play.md) | [Runtime](architecture/play.md) | `partial` | tests | — | — |\n"
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].product_link, "product/play.md")
        self.assertEqual(rows[0].architecture_link, "architecture/play.md")
        self.assertEqual(rows[0].state, "partial")

    def test_closeout_accepts_only_updated_or_justified_no_update(self) -> None:
        updated = self.contract.closeout_disposition("- Living documentation: `updated`\n")
        justified = self.contract.closeout_disposition(
            "- Living documentation: `no-update-needed` — generated output is unchanged\n"
        )
        follow_up = self.contract.closeout_disposition(
            "- Living documentation: `follow-up` — later\n"
        )
        generic = self.contract.closeout_disposition(
            "- Living documentation: `no-update-needed`\n"
            "- Living documentation rationale: `no docs`\n"
        )

        self.assertTrue(updated.valid)
        self.assertTrue(justified.valid)
        self.assertFalse(follow_up.valid)
        self.assertFalse(generic.valid)

    def test_baseline_requires_evidence_and_disjoint_safe_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/changes/old").mkdir(parents=True)
            (root / "docs/changes/done").mkdir(parents=True)
            path = root / "docs/LIVING_DOCUMENTATION_BASELINE.md"
            path.write_text(
                "# Baseline\n\n"
                "- Baseline status: `established`\n"
                "- Baseline evidence: `review at abc123`\n\n"
                "## Grandfathered closeout debt\n\n"
                "| Change artifact | Debt status | Review evidence or rationale |\n"
                "| --- | --- | --- |\n"
                "| `docs/changes/old` | unresolved | inventory review |\n\n"
                "## Reviewed debt dispositions\n\n"
                "| Change artifact | Disposition | Review evidence or rationale |\n"
                "| --- | --- | --- |\n"
                "| `docs/changes/done` | reviewed | owner review |\n",
                encoding="utf-8",
            )

            baseline = self.contract.parse_baseline(path)

        self.assertEqual(baseline.status, "established")
        self.assertEqual(baseline.grandfathered, {"docs/changes/old"})
        self.assertEqual(baseline.reviewed, {"docs/changes/done"})
        self.assertEqual(baseline.errors, ())

    def test_baseline_rejects_unknown_values_placeholders_duplicates_and_missing_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/changes/old").mkdir(parents=True)
            path = root / "docs/LIVING_DOCUMENTATION_BASELINE.md"
            path.write_text(
                "# Baseline\n\n"
                "- Baseline status: `established`\n"
                "- Baseline evidence: `reviewed fixture`\n\n"
                "## Grandfathered closeout debt\n\n"
                "| Change artifact | Debt status | Review evidence or rationale |\n"
                "| --- | --- | --- |\n"
                "| `docs/changes/old` | banana | |\n"
                "| `docs/changes/old` | unresolved | duplicate |\n"
                "| `docs/changes/missing` | unresolved | reviewed inventory |\n\n"
                "## Reviewed debt dispositions\n\n"
                "| Change artifact | Disposition | Review evidence or rationale |\n"
                "| --- | --- | --- |\n"
                "| _None_ | — | — |\n",
                encoding="utf-8",
            )

            baseline = self.contract.parse_baseline(path)

        joined = "\n".join(baseline.errors)
        self.assertIn("unsupported value 'banana'", joined)
        self.assertIn("non-placeholder evidence", joined)
        self.assertIn("duplicate change path", joined)
        self.assertIn("listed change directory does not exist", joined)
        self.assertNotIn("docs/changes/old", baseline.grandfathered)

    def test_baseline_rejects_unsafe_overlap_and_real_unestablished_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/changes/old").mkdir(parents=True)
            path = root / "docs/LIVING_DOCUMENTATION_BASELINE.md"
            path.write_text(
                "# Baseline\n\n"
                "- Baseline status: `unestablished`\n"
                "- Baseline evidence: _not established_\n\n"
                "## Grandfathered closeout debt\n\n"
                "| Change artifact | Debt status | Review evidence or rationale |\n"
                "| --- | --- | --- |\n"
                "| `docs/changes/old` | unresolved | inventory |\n"
                "| `docs/changes/../old` | unresolved | unsafe |\n\n"
                "## Reviewed debt dispositions\n\n"
                "| Change artifact | Disposition | Review evidence or rationale |\n"
                "| --- | --- | --- |\n"
                "| `docs/changes/old` | reviewed | owner review |\n",
                encoding="utf-8",
            )

            baseline = self.contract.parse_baseline(path)

        joined = "\n".join(baseline.errors)
        self.assertIn("unestablished baseline cannot list change paths", joined)
        self.assertIn("invalid change path", joined)
        self.assertIn("both grandfathered and reviewed", joined)
        self.assertEqual(baseline.grandfathered, frozenset())
        self.assertEqual(baseline.reviewed, frozenset())

    def test_baseline_rejects_encoded_symlink_and_malformed_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            changes = root / "docs/changes"
            real = changes / "real"
            real.mkdir(parents=True)
            (changes / "linked").symlink_to(real, target_is_directory=True)
            path = root / "docs/LIVING_DOCUMENTATION_BASELINE.md"
            path.write_text(
                "# Baseline\n\n"
                "- Baseline status: `established`\n"
                "- Baseline evidence: `reviewed fixture`\n\n"
                "## Grandfathered closeout debt\n\n"
                "| Change artifact | Debt status | Review evidence or rationale |\n"
                "| --- | --- | --- |\n"
                "| `docs/changes/linked` | unresolved | inventory |\n"
                "| `docs/changes/%2e%2e` | unresolved | encoded |\n"
                "| `docs/changes/real` | unresolved | evidence | extra |\n\n"
                "## Reviewed debt dispositions\n\n"
                "| Change artifact | Disposition | Review evidence or rationale |\n"
                "| --- | --- | --- |\n"
                "| _None_ | — | — |\n",
                encoding="utf-8",
            )

            baseline = self.contract.parse_baseline(path)

        joined = "\n".join(baseline.errors)
        self.assertIn("must not be a symlink", joined)
        self.assertIn("%2e%2e", joined)
        self.assertIn("exactly three cells", joined)

    def test_maintainability_closeout_parses_scope_and_typed_dispositions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "src/example.py"
            source.parent.mkdir()
            source.write_text("pass\n", encoding="utf-8")
            follow_up = root / "docs/changes/follow-up/spec.md"
            follow_up.parent.mkdir(parents=True)
            follow_up.write_text("# Spec\n", encoding="utf-8")
            tasks = root / "docs/changes/active/tasks.md"
            tasks.parent.mkdir(parents=True)
            tasks.write_text(
                "# Tasks\n\n"
                "### Maintainability audit scope\n\n"
                "| Repository-relative path |\n| --- |\n| `src/example.py` |\n\n"
                "### Maintainability finding dispositions\n\n"
                "| Finding code | Path | Disposition | Rationale or reference |\n"
                "| --- | --- | --- | --- |\n"
                "| `large-file-review` | `src/example.py` | accepted | Cohesive boundary |\n"
                "| `manual-follow-up` | `src/example.py` | separate-spec | `docs/changes/follow-up/spec.md` |\n",
                encoding="utf-8",
            )

            parsed = self.contract.parse_maintainability_closeout(root, tasks)

        self.assertEqual(parsed.scope, ("src/example.py",))
        self.assertEqual([item.value for item in parsed.dispositions], ["accepted", "separate-spec"])
        self.assertEqual(parsed.errors, ())

    def test_maintainability_closeout_rejects_unknown_and_incomplete_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "src/example.py"
            source.parent.mkdir()
            source.write_text("pass\n", encoding="utf-8")
            tasks = root / "docs/changes/active/tasks.md"
            tasks.parent.mkdir(parents=True)
            tasks.write_text(
                "# Tasks\n\n"
                "### Maintainability audit scope\n\n"
                "| Repository-relative path |\n| --- |\n| `src/example.py` |\n\n"
                "### Maintainability finding dispositions\n\n"
                "| Finding code | Path | Disposition | Rationale or reference |\n"
                "| --- | --- | --- | --- |\n"
                "| `large-file-review` | `src/example.py` | banana | |\n"
                "| `accepted-empty` | `src/example.py` | accepted | |\n"
                "| `other` | `src/example.py` | separate-spec | missing.md |\n",
                encoding="utf-8",
            )

            parsed = self.contract.parse_maintainability_closeout(root, tasks)

        joined = "\n".join(parsed.errors)
        self.assertIn("unsupported maintainability disposition 'banana'", joined)
        self.assertIn("separate-spec requires an existing safe spec reference", joined)

    def test_local_targets_cannot_escape_repository(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "docs/index.md"
            source.parent.mkdir()
            source.write_text("# Index\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "outside repository"):
                self.contract.resolve_local_target(root, source, "../../outside.md")


if __name__ == "__main__":
    unittest.main()
