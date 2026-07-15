from __future__ import annotations

import unittest

from ai_workflow_bootstrap.core.workflow import resolve_workflow_selection


class WorkflowSelectionTests(unittest.TestCase):
    def test_only_workflow_enables_spec_and_living_docs(self) -> None:
        workflows, groups = resolve_workflow_selection(include_skills=True)

        self.assertEqual(workflows, ["spec-driven", "living-docs"])
        self.assertIn("spec-driven", groups)
        self.assertIn("living-docs", groups)
        self.assertIn("skill/spec-driven", groups)
        self.assertIn("skill/maintainability-audit", groups)
        self.assertIn("skill/living-docs", groups)

    def test_include_skills_can_be_disabled(self) -> None:
        workflows, groups = resolve_workflow_selection(include_skills=False)

        self.assertEqual(workflows, ["spec-driven", "living-docs"])
        self.assertEqual(groups, {"spec-driven", "living-docs"})
        self.assertNotIn("skill/maintainability-audit", groups)


if __name__ == "__main__":
    unittest.main()
