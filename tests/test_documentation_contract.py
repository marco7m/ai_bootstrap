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
                {"café-current-contract", "repeated-heading", "repeated-heading-1"},
            )

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
            path = Path(tmp) / "baseline.md"
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
