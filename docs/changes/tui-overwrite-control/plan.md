# Implementation Plan: TUI overwrite control

## 1. Summary

Expose the existing planner `force` capability through one opt-in TUI checkbox, preserving backup behavior in `core.applier`.

## 2. Relevant Existing Context

`ai_workflow_bootstrap.tui._plan_from_ui` currently always passes `force=False`. The planner already classifies forced replacements and the applier already creates backups for planned overwrites. UI copy is centralized in `tui_text.py`; focused TUI tests live in `tests/test_tui.py`.

## 3. Existing Conventions Found

- Folder structure: presentation in `ai_workflow_bootstrap/tui.py`; planning and writes in `core/`.
- Naming style: module-level widget ID constants and localized text keys.
- Testing pattern: standard-library `unittest` tests around public or small helper contracts.
- Persistence/data access pattern: TUI saves state only after `apply_plan` succeeds.

## 4. Proposed Changes

1. Add an overwrite widget ID, checkbox, localized labels, and a brief backup explanation.
2. Pass its boolean value into `_plan_from_ui` for preview, dry run, and apply.
3. Refresh the preview when this setting changes.
4. Test safe and forced plan classification for an existing differing generated file.
5. Update the TUI capability list in the README.

## 5. Module Boundaries

- `tui.py` owns collecting and passing the user setting.
- `core.planner` continues owning forced-overwrite classification.
- `core.applier` continues owning backup creation and writes.
- The TUI must not implement backup logic or write files itself.

## 6. Architecture Locality Check

Expected changes are confined to TUI presentation, TUI text, a focused TUI test, TUI documentation, and the planner's existing overwrite classification. They are all one conceptual area; no refactor is needed.

## 7. Data / API / Interface Impact

The interactive interface gains one unchecked checkbox. CLI arguments and generated output formats remain unchanged.

## 8. Security / Privacy Impact

This adds a destructive operation behind an explicit opt-in while retaining the existing `APPLY` confirmation and automatic backups. It does not introduce secrets, network calls, or additional logging.

## 9. Dependency Impact

None. The existing optional Textual dependency is sufficient.

## 10. Risks

- Preview could disagree with Apply if force is not propagated consistently.
- Users could mistake overwrite as unprotected; copy must state that backups are created.

## 11. Validation Strategy

- Test the helper's plan classification with force disabled and enabled for the same existing differing generated file.
- Retain the widget-ID uniqueness test with the new control.
- Run the full test suite.

No visual snapshot test is needed: it would be brittle and would not protect the planner/applier behavior.

## 12. Execution Steps

1. Add and localize the setting.
2. Wire it through planning and preview refresh.
3. Add contract tests and README documentation.
4. Run validation and inspect the diff.

## 13. Rollback / Recovery

Remove the UI setting; core overwrite and backup behavior are unchanged. Files overwritten through the new control retain their `.bak-<timestamp>` backups.

## 14. Notes

No architecture smell: presentation is using an existing engine capability through its intended boundary.
