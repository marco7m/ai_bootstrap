# Implementation Plan: Living Docs Downstream Compatibility v1

- Status: `completed`
- Approved spec: [spec.md](spec.md)
- Date: 2026-08-11
- Approved: 2026-08-11

## 1. Summary

Implement pack `0.7.1` as a project-agnostic repair inside the existing
generated documentation-validation boundary. The work will:

- correct canonical GitHub-style fragments without accepting downstream-specific
  aliases;
- replace first-column-only baseline parsing with constrained typed rows;
- add a formal, shared maintainability closeout grammar and reconcile it with
  the auditor's stable public findings;
- preserve direct checkers, seeded knowledge, managed-only behavior and old
  state;
- prove the contracts in generic fresh/upgrade/debt/downstream-shaped fixtures;
- use the real downstream only as read-only acceptance evidence.

This plan and [tasks.md](tasks.md) were explicitly approved together on
2026-08-11.

## 2. Relevant Current Context

- `documentation_contract.py` already owns Markdown links, fragments,
  capability rows, baseline sets and living-document closeout grammar.
- `check_links.py` and `check_living_docs.py` consume that owner directly.
- `audit_repository.py` imports the same contract, so fragment and baseline
  parsing need no second implementation.
- `check_docs.py` still parses maintainability text independently and accepts
  any value except four placeholders.
- `_table_paths()` validates only the first cell and loses duplicates by
  constructing a set.
- `heading_slug()` removes punctuation before collapsing whitespace, producing
  one hyphen for ` — ` instead of two.
- Default pack `0.7.0` already distributes the parser/checkers as `managed` and
  the baseline as `seeded`; generic lifecycle changes are unnecessary.
- The capability is now honestly `implemented`, with this approved target and
  active change registered. Internal tests remain useful evidence but no longer
  claim complete downstream verification.

## 3. Planning Audit and Dispositions

The scoped planning audit inspected 14 affected files and reported only:

- this approved spec at 580 lines;
- `tests/test_template_pack.py` at 510 lines.

Both are advisory size signals. The spec is a cohesive temporal contract and
will not be split. `test_template_pack.py` will receive only pack inventory and
version assertions; behavioral cases go to focused parser/checker modules.

Manual findings from the approved spec retain these dispositions:

| Finding | Plan disposition |
| --- | --- |
| Maintainability grammar parsed in `check_docs.py` | Planned local refactor: move grammar/data parsing to `documentation_contract.py` |
| Baseline rows reduced prematurely to sets | Planned local refactor: typed ordered rows with row-specific errors before exposing exact sets |
| Fragment/baseline/closeout fixtures are too synthetic | Planned local refactor: public generic generated-repository fixtures |
| Complete renderer parity | Separate-spec only if later evidence requires it |
| Downstream owner size/concentration | Advisory observation owned downstream; no change here |

No broad refactor precedes implementation.

## 4. Resolved Technical Design

### 4.1 Canonical fragment subset

Keep fragment construction in `documentation_contract.py` and implement the
approved subset as a small deterministic character pipeline:

1. extract visible text from supported inline Markdown links and remove
   supported emphasis markers;
2. trim the heading's outer whitespace and case-fold it;
3. replace each ordinary ASCII space independently with `-`;
4. preserve authored `-` and Unicode alphanumeric characters;
5. remove supported punctuation and other whitespace without coalescing the
   hyphens already produced;
6. generate duplicate suffixes in document order (`base`, `base-1`, `base-2`);
7. percent-decode an incoming fragment once and compare exactly.

No normalization removes diacritics or transliterates Unicode. Diagnostics may
show the expected canonical anchor. The implementation will not import a full
Markdown renderer or add a dependency.

Tests will separate em-dash spacing, consecutive ordinary spaces, authored
hyphens, Unicode, percent-encoding, duplicates and inline links instead of
combining them in one happy-path test.

### 4.2 Typed baseline rows

Add a small immutable row representation in `documentation_contract.py` with
path, value, evidence and source row. Parse each exact three-cell table before
building `Baseline.grandfathered` and `Baseline.reviewed` sets.

Validation order:

1. require the exact section and table header;
2. parse the `_None_ | — | —` sentinel and reject it beside real rows;
3. reject missing/extra cells and placeholders;
4. require `unresolved` in grandfathered rows and `reviewed` in reviewed rows;
5. reject percent-encoded, absolute, non-canonical, nested, empty, `.`/`..` or
   trailing-separator path spellings;
6. resolve against the repository inferred from the canonical baseline path and
   require an existing non-symlink direct directory under `docs/changes/`;
7. detect duplicates before conversion to sets and reject cross-table overlap;
8. reject real rows in an `unestablished` baseline.

`parse_baseline()` remains the one public owner used by living checks and the
auditor. Existing callers continue to pass the baseline path; no adapter
re-parses table cells.

### 4.3 Maintainability Markdown contract

Replace the ambiguous single free-text field in the generated tasks template
with two constrained human-readable tables under closeout:

```markdown
### Maintainability audit scope

| Repository-relative path |
| --- |
| `src/example.py` |

### Maintainability finding dispositions

| Finding code | Path | Disposition | Rationale or reference |
| --- | --- | --- | --- |
| `large-file-review` | `src/example.py` | accepted | Cohesive public boundary |
```

For a clean scoped audit, the disposition table uses the sole sentinel row:

```markdown
| _None_ | — | no-findings | Scoped audit returned no findings |
```

Rules:

- scope contains at least one safe existing repository-relative file/directory;
- each non-sentinel row identifies one stable auditor `(code, path)` tuple;
- `accepted` requires non-placeholder rationale and a current matching finding;
- `separate-spec` requires a current matching finding and safe existing spec
  reference;
- `resolved` requires an identified tuple absent from the current rerun;
- `no-findings` is valid only as the sole sentinel when the rerun is empty;
- duplicate tuples, unknown dispositions, missing current findings and
  undispositioned current findings fail;
- threshold meaning stays inside the auditor and reviewer; reconciliation sees
  only its public code/path/scope results.

The pure Markdown grammar belongs in `documentation_contract.py`. Audit
execution and tuple reconciliation belong in `check_docs.py` because it is the
aggregate adapter. `check_docs.py` will run the scoped auditor during every
targeted closeout; `--advisory` controls reporting outside targeted closeout,
not whether the closeout contract is enforced.

Historical completed tasks are not rewritten. Repository-wide prospective
living-document validation remains governed by the baseline. The stricter
maintainability contract applies when a change is explicitly targeted for
closeout using the repaired managed checker.

### 4.4 Project-agnostic fixture boundary

Create test helpers that generate neutral repositories and generic headings
such as reliability qualification, Unicode interaction, repeated sections and
linked visible text. Fixtures must not copy the downstream repository, use its
name, encode game-domain terms or depend on its directory layout beyond the
public `docs/` contract.

The real downstream is used once at closeout by running the candidate source
checker read-only with `PYTHONDONTWRITEBYTECODE=1`. Expected evidence is:

- prior false positives for canonical double-hyphen anchors disappear;
- the known accent-folded non-canonical link remains a genuine actionable
  failure with its expected Unicode anchor;
- no file, state or bytecode is written downstream.

This real check tests classification, not a requirement that unrelated
downstream debt vanish.

### 4.5 Pack and lifecycle compatibility

- Change `manifest.json` version from `0.7.0` to `0.7.1`.
- Keep the parser, checkers, policies and skills `managed`.
- Keep the baseline and current knowledge owners `seeded`.
- Do not change manifest lifecycle/group classifications or add files unless
  implementation proves the approved tables need a new managed helper; the
  default design does not.
- Exercise old state with `0.7.0` provenance, managed-only, evolved seeds,
  preview/dry-run/apply/reapply and existing legacy-state coverage.
- Do not touch generic lifecycle, planner, applier, state, CLI or TUI source.

## 5. Proposed File Changes

### Shared source and adapters

- `templates/.agents/skills/living-docs/scripts/documentation_contract.py`:
  canonical fragments, typed baseline rows and maintainability grammar.
- `check_links.py`: preserve direct CLI and improve canonical-fragment
  diagnostics only through shared results.
- `check_living_docs.py`: consume stricter baseline results; no table parsing.
- `check_docs.py`: remove regex grammar, run declared scope and reconcile stable
  tuples.
- `audit_repository.py`: retain advisory ownership and expose no new semantic
  verdict; no source cleanup was substantiated by direct inspection.

### Managed policy and templates

- `templates/docs/LIVING_DOCUMENTATION.md`: document the exact supported
  fragment/baseline/closeout subset once for humans.
- `templates/docs/LIVING_DOCUMENTATION_BASELINE.md`: make allowed row values and
  evidence requirements explicit without establishing a baseline.
- `templates/docs/changes/_templates/tasks.md`: add the two maintainability
  tables with pending placeholders that cannot accidentally close the gate.
- generated `living-docs`, `maintainability-audit` and `spec-driven` skills:
  concise routing to their owners and timing; no repeated full grammar.
- `templates/docs/SPEC_DRIVEN.md`: detailed closeout procedure only if needed.
- `manifest.json`: version `0.7.1`, no lifecycle changes.

`AGENTS.md`, spec/plan templates, product/architecture scaffolds and unrelated
decision templates remain unchanged unless a focused failing acceptance test
proves a missing instruction. Such evidence requires plan reconciliation before
expansion.

### Tests

- `tests/test_documentation_contract.py`: pure fragment, baseline-row and
  maintainability-table grammar.
- `tests/test_docs_checker.py`: generic generated repository, direct/aggregate
  execution from another cwd, stable tuple reconciliation and neutral
  downstream-shaped fixture.
- `tests/test_living_docs_checker.py`: malformed/stale baseline integration and
  exact grandfathering.
- `tests/test_maintainability_audit.py`: shared parser integration, stable
  findings, advisory thresholds and cleanup regression coverage.
- `tests/test_template_pack.py`: `0.7.1`, manifest inventory/lifecycle,
  templates, direct generated scripts and context budgets; no large behavioral
  fixture additions.
- `tests/test_planner.py`, `tests/test_state.py` and `tests/test_applier.py` only
  where their existing public fixtures are the smallest proof of `0.7.0` state,
  managed-only and seed preservation. No production core changes are planned.

### Living owners at implementation closeout

- distill final product behavior into
  `docs/product/living-documentation-workflow.md`;
- distill final boundaries into
  `docs/architecture/documentation-validation.md`;
- reconcile hubs only if links/approved-target text changes;
- update `docs/LIVING_DOCUMENTATION.md` and self-host baseline syntax without
  changing its established inventory semantics;
- promote the capability to `verified` and clear target/change only after all
  evidence passes;
- remove the roadmap item only at that closeout;
- update decisions 0001/0002 only if durable rationale changes. The current
  expectation is no new decision because this repair enforces their existing
  boundaries.

## 6. Architecture Locality

- Shared grammar remains in one generated living-docs module.
- Link/living/aggregate/audit adapters retain separate blocking, orchestration
  and advisory responsibilities.
- Templates describe human input but do not become parser implementations.
- Test fixtures exercise public commands and generated repositories, not
  private regex details.
- Core lifecycle and UI remain unaware of documentation semantics.

Expected result: a focused change in the existing validation boundary, not
shotgun surgery. If implementation needs a new core lifecycle or renderer
dependency, stop and reconcile the approved spec/plan.

## 7. Security, Privacy and Dependency Impact

- No external dependency, network call or runtime renderer.
- Canonical path checks reject encoded traversal and symlink escape before an
  entry can grant baseline or audit scope authority.
- Diagnostics emit stable paths/codes and expected anchors, not document
  contents or sensitive rationale.
- Real downstream validation is read-only, uses no bytecode, and records only
  sanitized counts/classifications in closeout notes.

## 8. Validation Strategy

### Focused red/green contracts

1. Fragment unit cases and public link checker fixture.
2. Baseline grammar matrix and aggregate prospective-gate fixture.
3. Maintainability grammar matrix and actual scoped-audit reconciliation.
4. Generated fresh/upgrade/debt/downstream-shaped fixtures.
5. Pack/state/managed-only preservation checks.

### Complete validation

- focused unittest/pytest modules during implementation;
- `pytest -q` and `python -m unittest discover -s tests -q`;
- `python -m compileall -q ai_workflow_bootstrap tests` with no retained
  generated cache artifacts;
- manifest load/version/inventory and generated skill/frontmatter budgets;
- source and freshly generated aggregate/direct checkers from another cwd;
- fresh apply/reapply and proportional `0.7.0` upgrade/managed-only/evolved-seed
  dry-run and real temporary-repository application;
- read-only candidate source checker against the established downstream, with
  before/after status equality;
- proportional post-implementation maintainability audit;
- living owner/link checks and targeted closeout;
- `git diff --check` and critical final diff review.

No test may assert that structural checks prove semantic truth or that all
downstream documentation is healthy.

## 9. Risks and Mitigations

- **Anchor overreach:** constrain the supported subset and keep invalid Unicode
  folding blocking.
- **Baseline waiver expansion:** validate complete rows and existing canonical
  paths before exposing sets.
- **Closeout bureaucracy:** reconcile stable tuples only; do not judge prose or
  thresholds semantically.
- **Fixture overfitting:** neutral names/data and public repository contracts;
  real project only as external read-only evidence.
- **Patch-version incompatibility:** preserve CLIs/lifecycle and treat stricter
  malformed-input rejection as restoration of the `0.7.0` approved contract.
- **Test concentration:** keep manifest assertions small and behavior in
  focused modules.
- **Hidden lifecycle expansion:** stop if any production core file becomes
  necessary.

## 10. Execution Order

1. Re-read approved spec/plan/tasks and capture both worktree states.
2. Add failing fragment and generic public-checker contracts.
3. Implement canonical fragment normalization and diagnostics.
4. Add failing baseline grammar/integration contracts.
5. Implement typed baseline rows and safe existence/duplicate validation.
6. Add failing maintainability grammar/reconciliation contracts.
7. Implement shared tables and aggregate scoped reconciliation.
8. Update managed policies/templates/skills and pack version.
9. Add/complete fresh, upgrade, debt and neutral downstream-shaped fixtures.
10. Run focused and complete internal validation.
11. Run candidate source checker read-only against the real downstream and
    classify expected residual genuine debt without editing it.
12. Run post-change audit, reconcile durable owners/capability/roadmap and
    targeted closeout.
13. Inspect final diff for scope, duplication, hidden semantic thresholds,
    lifecycle leakage and project-specific fixtures.

## 11. Rollback / Recovery

- Before plan/tasks approval, no implementation exists to roll back.
- During implementation, every change remains file-local and reviewable; no
  destructive Git operation is used.
- Temporary generated repositories are disposable and never replace source.
- Downstream validation makes no write, so no downstream recovery is expected.
- If a patch-version or contract conflict appears, stop and return to approval
  rather than adding aliases or migrations silently.

## 12. Approval Gate

Approval must cover this plan and [tasks.md](tasks.md) together. Approval allows
implementation and validation only within the approved project-agnostic
boundary; it does not authorize downstream edits, commits, staging or unrelated
cleanup.
