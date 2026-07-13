# Change Spec: TUI overwrite control

## 1. Summary

Add an explicit overwrite control to the interactive TUI so users can perform the equivalent of the CLI `apply --force` flow without leaving the guided interface.

## 2. Problem

The preview says an existing generated file can be overwritten only with force, but the TUI always plans with `force=False` and exposes no way to change that. Users must know and switch to the CLI to complete an overwrite from the TUI.

## 3. Goal

Make overwrite an intentional, visible TUI option while preserving the current safe default and the CLI's backup behavior.

## 4. Scope

- Add an unchecked TUI checkbox for overwriting existing generated files.
- Use its value for preview, dry run, and apply planning.
- When enabled, show planned overwrites in the preview and apply them with the existing automatic backup policy.
- Add Portuguese and English UI copy.
- Cover the control and planning contract with focused tests.

## 5. Out of Scope

- Changing CLI flags or their behavior.
- Adding a TUI option to disable backups.
- Changing backup naming, storage, or collision behavior.
- Altering templates or generated-file contents.

## 6. Users / Actors

- A developer using the TUI to update previously generated bootstrap files.

## 7. Functional Requirements

- The TUI must display an overwrite checkbox near its other run settings.
- The checkbox must be unchecked by default.
- With it unchecked, existing differing files must remain skipped, matching current TUI behavior.
- With it checked, preview and dry run must classify eligible differing existing files as overwrites.
- With it checked, Apply must overwrite eligible existing files after the user types `APPLY`.
- TUI overwrites must create backups using the existing default backup behavior.
- The checkbox label and explanatory text must be available in English and pt-BR.

## 8. Non-Functional Requirements

### Maintainability

The TUI must pass the setting through the existing plan-building boundary; it must not duplicate planner or backup logic.

### Modularity / Architecture

`core.planner` remains the single owner of overwrite classification and `core.applier` remains the single owner of applying backups and writes.

### Security / Privacy

The default stays non-destructive. Enabling overwrite must not expose file contents or add logging of them.

### Reliability

Preview, dry run, and apply must use the same overwrite setting so their displayed result matches the eventual operation.

### Performance

The checkbox must not add filesystem scans beyond the TUI's existing preview work.

### Observability

The table must continue to show whether a file will be skipped, unchanged, written, or overwritten.

### Simplicity

Use one checkbox only. Reuse the current unconditional backup behavior rather than introducing backup configuration to the TUI.

## 9. User Flow / System Flow

1. The user selects a target and sees the default safe preview.
2. If files need replacement, they enable “Overwrite existing files”.
3. The preview refreshes and marks eligible files as overwritten.
4. The user types `APPLY` and chooses Apply.
5. The existing applier creates backups and writes replacements.

## 10. Edge Cases

- Existing files identical to their rendered template remain unchanged even when overwrite is enabled.
- Changing the control after a preview must refresh the preview before apply.
- A dry run with overwrite enabled must not create backups or write files.
- An invalid target path must retain the existing error behavior.

## 11. Constraints

- Preserve the current CLI behavior and default safe TUI behavior.
- Keep the change scoped to the TUI, its localized text, tests, and user-facing TUI documentation if needed.
- Do not add dependencies.

## 12. Assumptions

- TUI users want the same backup-on-force policy as `ai-bootstrap apply --force`.
- The existing `APPLY` text confirmation remains sufficient confirmation when overwrite is selected.

## 13. Acceptance Criteria

- The TUI exposes an unchecked overwrite option in both supported languages.
- Enabling it changes previews from skipped to overwritten where applicable.
- Applying with it enabled overwrites files and produces the existing backups.
- Applying with it disabled does not overwrite existing differing files.
- Existing focused and new tests pass.

## 14. Open Questions

None.
