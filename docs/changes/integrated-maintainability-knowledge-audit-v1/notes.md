# Notes: Integrated Maintainability and Knowledge Audit v1

## Validation

- `python -m unittest discover -s tests -v`: all 103 tests passed.
- Focused audit/template/living-doc/workflow contracts passed, including real
  generated-script execution in temporary Python and Rust repositories.
- `python -m compileall -q ai_workflow_bootstrap` passed.
- Default manifest JSON validation passed at version `0.6.0`.
- The skill-creator validator accepted the revised generated
  `maintainability-audit` skill.
- The generated skills remain within 300 words and generated `AGENTS.md`
  remains within 800 words.
- `python -m build` could not start because the active Python environment has no
  optional `build` module. No dependency was installed; repository-native
  validation is complete.

## Audit disposition

The first repo-wide execution inspected 127 eligible files.

- `tests/test_template_pack.py` crossed the source review threshold because the
  initial implementation placed audit-specific contracts there. This
  change-local finding was resolved by moving those contracts to
  `tests/test_maintainability_audit.py`; the template-pack test returned below
  the threshold.
- Root `README.md` crossed only the Markdown line threshold and remains a
  cohesive user-facing guide. Its generated-file inventory and maintainability
  section were updated, but no split is justified by the current change.
- `ai_workflow_bootstrap/tui.py` crossed the source line threshold. It is
  unrelated pre-existing debt and is routed as a possible separate refactor
  spec, not added to this approved scope.
- Seven completed historical changes predate the `0.6.0` closeout marker. Their
  current durable outcomes are already represented by repository owners or
  superseded workflow history; retroactively editing temporal artifacts would
  add churn without improving this change. The findings are accepted as legacy
  advisory evidence.
- This change's approved `spec.md` and `plan.md` cross the Markdown review
  threshold. They remain cohesive temporal handoff contracts covering one
  workflow evolution; durable outcomes have been distilled into short product,
  architecture, capability and decision owners, so splitting the historical
  contracts would not reduce normal retrieval cost.

No orphan current-knowledge page, concentrated large capability owner,
placeholder owner, sensitive output or implementation-created shotgun surgery
was reported.

## Implementation notes

- Scoped knowledge checks filter findings to the explicitly inspected current
  pages, so auditing one active change does not surface unrelated repository
  debt.
- Repo-wide mode intentionally reports older incomplete disposition markers and
  leaves their semantic handling to the agent.
- No core planner, renderer, lifecycle, applier, state, CLI or TUI behavior
  changed.
