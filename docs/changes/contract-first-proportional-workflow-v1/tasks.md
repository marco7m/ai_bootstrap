# Tasks: Contract-First Proportional Workflow v1

- Status: `completed`
- Approved spec: [spec.md](spec.md)
- Implementation authority after second gate: [plan.md](plan.md) and this
  checklist together

## Approval and preservation

- [x] Re-read the approved spec, plan and this checklist before implementation.
- [x] Capture `git status --short`; preserve unrelated work and confirm no real
      downstream is in scope.
- [x] Confirm this plan and tasks were explicitly approved together before any
      template, test, manifest or living-owner implementation edit.
- [x] Record the approved target/active change without replacing current
      capability state or evidence.
- [x] Stop and request reconciliation if implementation needs a new artifact
      type, dependency, checker grammar, core module or expanded permission.

## Focused routing contracts

- [x] Add a focused workflow test module rather than expanding the already-large
      manifest suite with the scenario matrix.
- [x] Protect feature/new-contract spec approval followed by the separate
      plan/tasks approval gate.
- [x] Protect the invariant that every non-trivial clear-contract repair uses
      approved plan/tasks despite behavioral novelty `none`.
- [x] Protect direct flow only for work that is simultaneously trivial,
      unequivocal and low risk.
- [x] Cover ambiguous/conflicting bugs, active P0/P1 reconciliation, closed
      historical specs, behavior-preserving refactors and disguised product
      changes.
- [x] Cover read-only diagnosis, repositories without structured living docs
      and a validation example outside Rust/Python assumptions.
- [x] Cover compact handoff and internal-by-default classification with a
      one-sentence material disclosure and no mandatory report/file.
- [x] Assert stable route outcomes and artifact markers rather than complete
      paragraphs or downstream-domain examples.

## Compact and detailed generated guidance

- [x] Rewrite the workflow section of template `AGENTS.md`; keep it at or below
      800 words and route detail to the on-demand guide.
- [x] Rewrite the generated `spec-driven` skill at or below 300 words around
      authority, two-axis reasoning, route selection, applicable gates,
      implementation, validation and closeout.
- [x] Update `START_PROMPT.md` so spec approval is conditional on novelty/
      ambiguity while plan/tasks approval remains mandatory for every
      non-trivial implementation.
- [x] Rewrite `docs/SPEC_DRIVEN.md` at or below 1000 words as the single owner of
      the six routes, second-gate invariant, no-spec repair shape, progressive
      disclosure, handoff, stop conditions and validation ladder.
- [x] Confirm compact surfaces do not duplicate the route matrix and generic
      guidance contains no project- or stack-specific rule.

## Existing artifact contract

- [x] Update the plan template to begin with either approved spec or existing
      contract authority and a behavioral-novelty declaration.
- [x] Ensure a no-spec repair plan records authority, novelty `none`,
      reproduction, cause, repair boundary, risks, regression and validation.
- [x] Update the tasks template to reread the applicable authority, preserve the
      explicit second gate and stop if novelty or authority conflict emerges.
- [x] Update the notes template to record non-empty repair evidence, deviations,
      limitations, validation and closeout.
- [x] Add no new template/artifact type; leave spec/open-question/decision
      templates unchanged unless a focused failure triggers reconciliation.

## No-spec documentation checks

- [x] Add a generated fixture at `docs/changes/<repair>/` with plan/tasks and
      closeout notes but no `spec.md`.
- [x] Prove complete no-spec repair artifacts pass link, living-document,
      maintainability and aggregate closeout checks.
- [x] Prove pending tasks, broken links and invalid closeout still fail; do not
      weaken existing gates.
- [x] Confirm trivial bugs and read-only investigations require no empty change
      directory, spec or notes artifact.
- [x] Leave checker/auditor sources unchanged if current tasks-based behavior
      passes; stop for plan reconciliation if their grammar must change.

## Pack and lifecycle compatibility

- [x] Change only the default manifest version from `0.7.1` to `0.8.0` and
      update focused version assertions.
- [x] Preserve every manifest group, lifecycle, project-owned path,
      composition, obsolete migration and state schema.
- [x] Freshly generate temporary Python and Rust projects with skills; verify
      delivered content, word budgets, manifest and no-spec repair checks.
- [x] Generate a temporary Node or Go profile; verify generic routing and
      locally detected validation commands without installing dependencies.
- [x] Build a synthetic prior `0.7.1` state and test preview, managed update,
      managed-only and reapply behavior.
- [x] Prove managed instructions update, evolved seeded and project-owned files
      remain byte-identical, state becomes `0.8.0`, and no unexpected
      `migration_required` or conflict appears.
- [x] Validate the no-spec repair format using the content actually delivered
      after fresh generation and upgrade, not source assertions alone.

## Validation and critical review

- [x] Run `git diff --check` and focused workflow/template budget tests.
- [x] Run focused docs-checker, living-doc, audit, planner, lifecycle, state and
      applier tests justified by the changed contracts.
- [x] Run `python -m compileall -q ai_workflow_bootstrap tests`; identify caches
      before removing only untracked artifacts created by this run.
- [x] Validate manifest references, skill frontmatter, relative links and source
      plus generated aggregate documentation commands.
- [x] Run fresh multi-stack and `0.7.1` upgrade/reapply/managed-only temporary
      compatibility fixtures.
- [x] Run full `pytest -q` and
      `python -m unittest discover -s tests -q` once relevant inputs stabilize.
- [x] Run the proportional post-implementation maintainability audit over the
      exact changed source, tests and living owners; disposition every finding.
- [x] Critically review the diff for second-gate weakening, disguised product
      changes, repeated classification ceremony, duplicated guidance, budget
      overflow, stack leakage, brittle prose assertions and lifecycle changes.
- [x] Confirm no real downstream, root generated workflow copy, historical
      change, baseline inventory or unrelated worktree file was modified.

## Living knowledge and closeout

- [x] Update `docs/product/README.md` by delta with validated authority-first
      routing, unconditional non-trivial plan/tasks gate and no-spec repair
      artifact behavior.
- [x] Update `docs/architecture/README.md` by delta with compact versus
      on-demand ownership and unchanged lifecycle/checker boundaries.
- [x] Update `docs/CAPABILITIES.md` current evidence only after validation,
      then clear approved target/active change at successful closeout.
- [x] Create no new focused owner or ADR unless a real responsibility/rationale
      boundary is proven and reconciled.
- [x] Record validation commands/results, meaningful limitations and any
      unavailable gate without claiming it passed.
- [x] Run relative-link and targeted closeout checks using the installed checker
      when compatible or the reusable candidate source read-only when self-host
      drift prevents that command; report the distinction.
- [x] Complete the closeout tables below, close every checklist item supported
      by evidence and summarize without committing.

## Closeout Disposition

- Living documentation: `updated`
- Living documentation rationale: `updated product, architecture and capability owners by delta with the validated pack 0.8.0 routing and artifact contract`
- Durable facts added/changed/removed: `added authority-first two-axis routing, the unconditional non-trivial plan/tasks gate and the no-spec repair shape; changed default pack evidence from 0.7.1 to 0.8.0; removed the generated implication that every non-trivial task requires a new spec`

### Maintainability audit scope

| Repository-relative path |
| --- |
| `ai_workflow_bootstrap/template_packs/default/manifest.json` |
| `ai_workflow_bootstrap/template_packs/default/templates/AGENTS.md` |
| `ai_workflow_bootstrap/template_packs/default/templates/.agents/skills/spec-driven/SKILL.md` |
| `ai_workflow_bootstrap/template_packs/default/templates/docs/SPEC_DRIVEN.md` |
| `ai_workflow_bootstrap/template_packs/default/templates/docs/START_PROMPT.md` |
| `ai_workflow_bootstrap/template_packs/default/templates/docs/changes/_templates/plan.md` |
| `ai_workflow_bootstrap/template_packs/default/templates/docs/changes/_templates/tasks.md` |
| `ai_workflow_bootstrap/template_packs/default/templates/docs/changes/_templates/notes.md` |
| `tests/test_spec_driven_workflow.py` |
| `tests/test_template_pack.py` |
| `tests/test_maintainability_audit.py` |
| `tests/test_state.py` |
| `docs/product/README.md` |
| `docs/architecture/README.md` |
| `docs/CAPABILITIES.md` |
| `docs/changes/contract-first-proportional-workflow-v1` |

### Maintainability finding dispositions

| Finding code | Path | Disposition | Rationale or reference |
| --- | --- | --- | --- |
| `large-file-review` | `tests/test_template_pack.py` | accepted | Existing cohesive manifest, inventory and budget suite; route scenarios live in the new focused workflow module |
| `large-file-review` | `docs/changes/contract-first-proportional-workflow-v1/spec.md` | accepted | Cohesive approved temporal contract for a broad reusable workflow; not a current knowledge owner |
