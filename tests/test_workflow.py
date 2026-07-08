from __future__ import annotations

import unittest

from ai_workflow_bootstrap.core.workflow import resolve_workflow_selection


class WorkflowSelectionTests(unittest.TestCase):
    def test_recommended_mode_enables_spec_and_living_docs(self) -> None:
        workflows, groups = resolve_workflow_selection(mode="recommended", include_skills=True)

        self.assertEqual(workflows, ["spec-driven", "living-docs"])
        self.assertIn("spec-driven", groups)
        self.assertIn("living-docs", groups)
        self.assertIn("skill/spec-driven", groups)
        self.assertIn("skill/living-docs", groups)

    def test_spec_driven_mode_excludes_living_docs(self) -> None:
        workflows, groups = resolve_workflow_selection(mode="spec-driven", include_skills=True)

        self.assertEqual(workflows, ["spec-driven"])
        self.assertIn("spec-driven", groups)
        self.assertNotIn("living-docs", groups)
        self.assertIn("skill/spec-driven", groups)
        self.assertNotIn("skill/living-docs", groups)

    def test_living_docs_only_mode_excludes_spec_driven(self) -> None:
        workflows, groups = resolve_workflow_selection(mode="living-docs", include_skills=True)

        self.assertEqual(workflows, ["living-docs"])
        self.assertIn("living-docs", groups)
        self.assertNotIn("spec-driven", groups)
        self.assertIn("skill/living-docs", groups)
        self.assertNotIn("skill/spec-driven", groups)

    def test_include_skills_can_be_disabled(self) -> None:
        workflows, groups = resolve_workflow_selection(mode="recommended", include_skills=False)

        self.assertEqual(workflows, ["spec-driven", "living-docs"])
        self.assertEqual(groups, {"spec-driven", "living-docs"})


if __name__ == "__main__":
    unittest.main()
