# Implementation Plan: Navigable Living Knowledge v1

- Status: `completed`
- Approved spec: [spec.md](spec.md)
- Date: 2026-08-11
- Approved: 2026-08-11

## 1. Summary

Implement the approved three-layer living-knowledge contract in default pack
`0.7.0` without changing the generic lifecycle engine. The implementation will:

- strengthen generated hubs, authority and closeout guidance;
- add a protected seeded historical-baseline owner;
- extract shared deterministic documentation parsing;
- add a thin aggregate documentation command;
- separate blocking structural regressions from advisory maintainability
  signals;
- validate fresh, upgraded, evolved-seed and historical-debt repositories;
- close the change by updating the `ai_bootstrap` living owners only from
  passing implementation evidence.

This plan and [tasks.md](tasks.md) were explicitly approved together on
2026-08-11.

## 2. Relevant Existing Context

- Default pack `0.6.0` declares managed workflow/policy/check files and seeded
  living owners in `manifest.json`.
- `core.lifecycle.classify_rendered_file()` already preserves evolved or
  untracked seeds, including under `--force`, and safely advances untouched
  seeds with trusted provenance.
- Planner, applier and state modules are documentation-policy agnostic and have
  focused lifecycle/provenance tests. This boundary should remain unchanged.
- `check_links.py` owns relative file-link validation; `check_living_docs.py`
  owns a small set of blocking state/regression checks;
  `audit_repository.py` owns advisory repository-health collection.
- All three scripts parse overlapping Markdown, capability or closeout
  structures independently.
- The advisory audit currently accepts `follow-up` as a closeout disposition
  and reports capability concentration only when route and size thresholds are
  both crossed.
- Seven completed changes in this repository predate the current disposition
  marker. Existing notes acknowledge them, but no project-owned baseline is
  consumable by generated validation.
- `.ai-bootstrap/state.json` records the last local application as `0.5.1`,
  while the source pack is `0.6.0`. This is a compatibility fixture, not
  authorization to reapply or overwrite self-hosted knowledge implicitly.

## 3. Existing Conventions Found

- Folder structure: reusable outputs live under
  `ai_workflow_bootstrap/template_packs/default/templates/`; their output paths,
  groups and lifecycle are declared in the adjacent `manifest.json`.
- Naming style: generated Python scripts use snake_case, standard-library-only
  modules and direct `main(argv)` entry points; documentation uses kebab-case
  change directories and relative links.
- Error handling: invalid CLI/checker input produces concise stderr diagnostics
  and non-zero status; advisory audit findings retain exit status zero.
- Logging/output: deterministic, path-based stdout/stderr without file contents
  or sensitive values.
- Testing pattern: `unittest`, temporary repositories, direct subprocess
  execution of generated scripts and focused pure-function tests.
- Config pattern: JSON manifest plus generated Markdown owners; project
  knowledge is not stored in application-global configuration.
- External integration: none; Git is optional comparison evidence only.
- Persistence/data access: `.ai-bootstrap/state.json` owns applied provenance;
  seeded Markdown owns reviewed project knowledge.

## 4. Resolved Planning Decisions

### 4.1 Historical baseline format

Add seeded `docs/LIVING_DOCUMENTATION_BASELINE.md` with a constrained,
human-readable Markdown contract:

- `Baseline status: unestablished|established`;
- `Baseline evidence:` with a non-placeholder value when established;
- `Grandfathered closeout debt` table containing exact repository-relative
  change paths, debt status and review evidence/rationale;
- `Reviewed debt dispositions` table for entries deliberately removed from the
  prospective exception after real review.

The parser will consume only those fields/tables and will not interpret free
prose. A freshly generated file is `unestablished` with empty tables. Ordinary
bootstrap apply never discovers or populates historical rows. Audit/check
output may list candidate paths for a reviewer to copy deliberately.

The grandfather table, not a timestamp, defines the exception boundary. A
completed change not listed there must satisfy the current closeout contract.
Moving/removing an entry after review reduces outstanding debt without editing
the historical change artifact.

### 4.2 Shared parser ownership

Create managed
`.agents/skills/living-docs/scripts/documentation_contract.py`, sourced from the
equivalent template path. `living-docs` owns it because it defines navigation,
capability routing, headings, baseline and closeout syntax.

- `check_links.py` and `check_living_docs.py` import it locally.
- `audit_repository.py` resolves the sibling living-docs scripts directory from
  its own generated path and imports the same module.
- `check_docs.py` imports the two local checks and the advisory audit module
  through deterministic paths derived from `__file__`.
- Imports must work when a generated script is invoked from any current working
  directory with an explicit repository root.

No parser is copied and no subprocess chain is used to simulate shared
ownership. Each direct script entry point remains executable.

### 4.3 Link and fragment contract

- File-level relative Markdown links remain supported.
- Local fragments are validated against ATX Markdown headings using one
  documented standard-library normalization for the subset generated by the
  pack: percent-decoding, case-folding, whitespace-to-hyphen conversion,
  supported punctuation removal and deterministic duplicate suffixes.
- Existing simple fragments such as
  `#generated-maintainability-and-knowledge-audit` remain valid.
- Unsupported or unresolved local fragments produce an actionable diagnostic;
  external URLs and fragments remain outside repository validation.

Tests will protect the documented subset rather than claim byte-for-byte parity
with every Markdown renderer.

### 4.4 Closeout rationale contract

The deterministic checker accepts only:

- `updated`; or
- `no-update-needed` plus a non-empty rationale that is not one of the generated
  placeholder/reserved markers (`TODO`, `TBD`, `pending`, `reason required`,
  `no docs`, or template underscore placeholders).

It does not attempt semantic scoring of arbitrary prose. Reviewers remain
responsible for rejecting a formally non-empty but meaningless rationale.
`follow-up` is removed from closed-state grammar; unresolved work keeps the
change open.

### 4.5 Aggregate command modes

Add managed `.agents/skills/living-docs/scripts/check_docs.py`:

- default/repository mode: run blocking link, living-state, navigation,
  capability-route, baseline and completed-change checks;
- `--closeout docs/changes/<change>`: additionally require the selected change
  to have a valid final disposition even if its checklist is not otherwise
  recognizable as historical completion;
- optional advisory mode: include scoped maintainability findings without
  changing exit status solely for size/concentration;
- optional existing Git baseline argument remains delegated to the living-doc
  regression checker.

The command returns non-zero only for objective blocking issues or missing
required finding disposition in targeted closeout. Output includes stable code,
path, severity, evidence and expected remediation.

## 5. Proposed Changes

### 5.1 Shared deterministic contract and direct checkers

Create the shared module with pure/testable functions for:

- Markdown links and local target normalization;
- ATX headings and supported fragment resolution;
- capability table rows and authority-area route validation;
- knowledge graph reachability from canonical roots;
- knowledge status/placeholders;
- baseline fields and debt tables;
- change completion and living-document disposition;
- safe repository-relative path validation.

Refactor existing scripts to consume those functions while preserving their
public CLI purpose:

- `check_links.py`: blocking file/fragment links;
- `check_living_docs.py`: blocking current-state, route, navigation, baseline
  and closeout regressions;
- `audit_repository.py`: advisory size, independent concentration, mixed-owner
  structural signals and baseline-aware legacy debt candidates;
- `check_docs.py`: thin orchestration and consolidated diagnostics.

### 5.2 Generated knowledge policy and scaffolds

Update:

- `templates/docs/INDEX.md` to route the baseline owner and state the normal
  reading path;
- product/architecture READMEs to make hub-first behavior explicit without
  generating focused domain pages;
- `templates/docs/CAPABILITIES.md` to require correct-area owners and pertinent
  evidence/gaps;
- `templates/docs/GLOSSARY.md` to reinforce routing rather than duplicate fact
  ownership;
- `templates/docs/LIVING_DOCUMENTATION.md` with full baseline establishment,
  debt reduction, navigation and aggregate-check procedures;
- decision index/template only if implementation needs a concise link to the
  durable-rationale closeout rule; otherwise leave their already-correct
  contract unchanged.

Add `templates/docs/LIVING_DOCUMENTATION_BASELINE.md` as a generic empty
scaffold. Do not add product- or domain-specific focused pages.

### 5.3 Generated workflow integration

Update compactly:

- `templates/.agents/skills/living-docs/SKILL.md`: navigation/baseline/
  closeout ownership and aggregate validation;
- `templates/.agents/skills/maintainability-audit/SKILL.md`: independent signals
  and required finding disposition;
- `templates/.agents/skills/spec-driven/SKILL.md`: exact pre-spec, planning and
  targeted-closeout timing;
- `templates/docs/SPEC_DRIVEN.md`: detailed on-demand procedure only;
- `templates/docs/changes/_templates/spec.md`: potential owner paths and
  anticipated fact additions/changes/removals;
- `plan.md`: exact owner paths, shared-boundary decision and disposition;
- `tasks.md`: targeted closeout fields with `pending` initial state;
- `notes.md`: structured place for deviations and reviewed legacy/finding
  evidence when needed;
- `templates/AGENTS.md`: at most one concise always-loaded instruction needed to
  route non-trivial closeout to the aggregate check.

Do not duplicate detailed baseline syntax across always-loaded files.

### 5.4 Manifest and pack version

- Bump default pack to `0.7.0`.
- Declare the baseline scaffold as `seeded` in group `living-docs`.
- Declare `documentation_contract.py` and `check_docs.py` as `managed` in group
  `skill/living-docs`.
- Reuse existing directory declarations unless a new directory is actually
  required.
- Keep all existing lifecycles, obsolete migrations, project-owned paths and
  compositions unchanged.

### 5.5 Tests

Add `tests/test_documentation_contract.py` for pure parser contracts and
`tests/test_docs_checker.py` for aggregate CLI behavior. Refocus/extend:

- `test_living_docs_checker.py`: blocking navigation, authority, baseline and
  prospective closeout regressions;
- `test_maintainability_audit.py`: independent size/concentration signals,
  advisory exit behavior, baseline-aware debt and finding disposition;
- `test_template_pack.py`: `0.7.0`, manifest completeness/lifecycle, word
  budgets, generated file inventory and fresh direct execution;
- `test_planner.py` and `test_state.py`: missing baseline creation, evolved seed
  preservation, managed-only omission/provenance and `0.5.1` compatibility;
- `test_applier.py` only if an existing apply fixture is the smallest place to
  prove real apply/reapply behavior;
- `test_workflow.py` only if group selection changes (none is currently
  planned).

Use separate generated repository fixtures for fresh, clean upgrade,
evolved-seed upgrade and historical-debt adoption. Prefer public diagnostics,
exit status and preserved content over exact full-template string assertions.

### 5.6 Self-hosted documentation and user guide

After behavior passes:

- update root `README.md` generated-file/validation guidance;
- update `docs/product/README.md` with the verified workflow contract and create
  a focused product page only if the final responsibility is no longer cohesive
  in the hub;
- update `docs/architecture/README.md` with shared-parser/checker and baseline
  distribution boundaries, again splitting only on real responsibility;
- update `docs/INDEX.md` navigation if focused pages or baseline evidence are
  added;
- update `docs/CAPABILITIES.md` from `partial` to the evidence-supported final
  state and clear approved target/active change only after validation;
- remove the active roadmap item only after closeout;
- create/update a decision record if the final baseline/gate boundary warrants
  durable rationale;
- create the self-host baseline artifact by reviewed inventory rather than
  bootstrap inference. The seven known historical changes remain explicitly
  unresolved unless actually reviewed during this approved work.

Do not automatically reapply the bootstrap to this repository. Validate source
pack application in temporary repositories; update self-hosted managed copies
only if an explicit reviewed self-application step is added without risking
unrelated generated changes.

## 6. Module Boundaries

- Living-document structural contract owner:
  `templates/.agents/skills/living-docs/scripts/documentation_contract.py`.
- Blocking link adapter: `check_links.py`.
- Blocking semantic/structural regression adapter: `check_living_docs.py`.
- Aggregate adapter: `check_docs.py`.
- Advisory collection: `maintainability-audit/scripts/audit_repository.py`.
- Workflow timing/approval: generated `spec-driven` skill and guide.
- Policy/human explanation: generated `LIVING_DOCUMENTATION.md`.
- Distribution/lifecycle declaration: default `manifest.json`.
- Generic renderer/planner/applier/state: must not know Markdown, baseline or
  closeout semantics.
- CLI/TUI: must not gain documentation-check orchestration.

## 7. Architecture Locality

- Finding disposition from approved audit:
  - duplicated parsing: planned local refactor in shared contract module;
  - duplicated policy: reduce to authority-specific summaries and links;
  - `follow-up` grammar: safe local correction;
  - coupled concentration thresholds: local advisory-audit refactor;
  - historical debt: in-scope baseline capability;
  - brittle prose assertions: rewrite only affected tests;
  - large spec: accepted advisory observation;
  - large unrelated TUI: separate-spec candidate, untouched.
- Primary area: default pack documentation/skill/check templates.
- Files expected to change: files enumerated in sections 5.1–5.6 plus focused
  tests and approved change artifacts.
- Files that should not change: lifecycle, planner, applier, state, CLI and TUI
  unless a failing approved contract proves the plan assumption wrong.
- New boundary: one shared living-document structural contract module.
- Existing boundaries preserved: advisory versus blocking, generated versus
  project knowledge, managed versus seeded, current versus approved target.
- Shotgun-surgery control: every prose surface owns a different audience/timing;
  shared deterministic rules exist once in code and detailed baseline procedure
  exists once in policy.

## 8. Data / API / Interface Impact

- New generated file: `docs/LIVING_DOCUMENTATION_BASELINE.md` (`seeded`).
- New generated scripts: `documentation_contract.py` and `check_docs.py`
  (`managed`).
- New human/machine Markdown baseline fields/tables form a versioned generated
  contract; malformed input fails without mutation.
- Existing direct script CLIs remain supported.
- New aggregate CLI is repository-local and stack-independent.
- No product network API, persistence database or bootstrap core state schema
  change is planned.

## 9. Security / Privacy Impact

- No credentials, tokens, network calls or customer/runtime payloads.
- Shared path resolution must preserve repository containment and avoid
  following links outside the root.
- Sensitive/cache exclusions from the audit remain.
- Diagnostics emit paths, codes, counts and safe structural evidence only, not
  document contents.
- Baseline entries must be repository-relative `docs/changes/<change>` paths.

## 10. Dependency Impact

No dependency is added. `pathlib`, `re`, `urllib.parse`, `argparse`, `json`,
`dataclasses`, `subprocess` only for the existing optional Git comparison, and
other current standard-library facilities are sufficient.

## 11. Risks

- False blocking from Markdown fragment normalization: constrain and document
  the supported subset; test existing fragments.
- Baseline file becoming a hidden waiver list: require explicit established
  evidence, exact paths and visible unresolved status; never auto-populate it.
- Managed-only upgrade installs strict checks without seeded baseline: report
  `unestablished`, do not treat legacy debt as resolved or immediately fail all
  history.
- Cross-skill imports fail outside repository cwd: resolve from `__file__` and
  test invocation from another directory.
- Parser extraction changes existing direct commands: retain focused regression
  fixtures for exit status and diagnostics.
- Excessive prose duplication/context: enforce existing word budgets and keep
  detailed procedures in on-demand policy.
- Scope expansion into lifecycle/UI: stop and reconcile the approved plan if a
  generic engine change becomes necessary.

## 12. Validation Strategy

### 12.1 Focused contract tests

- Pure parser: links, headings/fragments, capability rows, baseline syntax,
  closeout statuses/rationales and repository-relative paths.
- Blocking checker: orphan owners, wrong-area/missing/change owner routes,
  incompatible placeholders, malformed baseline, new debt and targeted
  closeout.
- Advisory audit: independent size/concentration, legacy debt visibility,
  non-blocking thresholds and scoped finding disposition.
- Aggregator: composition, stable diagnostics, exit policy and operation from a
  non-repository cwd.

### 12.2 Generation/lifecycle fixtures

- Fresh Python and Rust repositories receive complete `0.7.0` surface.
- Existing clean `0.6.0` seed may update with trusted provenance.
- Evolved or untracked seeded owners remain byte-identical under normal,
  `--force` and reapply plans.
- Managed-only installs managed tools but not the seeded baseline.
- Historical-debt fixture remains usable only after explicit baseline
  establishment and rejects later unlisted debt.
- Legacy `0.5.1` state remains readable and grants no destructive authority.

### 12.3 Repository validation

- `python -m unittest discover -s tests -v`;
- `python -m compileall -q ai_workflow_bootstrap tests`;
- manifest JSON/load validation and pack version assertion;
- fresh generated direct execution of all three check commands and the audit;
- preview/dry-run/apply/reapply fixtures in temporary repositories;
- generated skills/frontmatter and context word budgets;
- proportional maintainability audit against changed code/docs;
- `python .agents/skills/living-docs/scripts/check_living_docs.py`;
- `python .agents/skills/living-docs/scripts/check_links.py`;
- source-template `check_docs.py` against this repository if local managed
  copies are intentionally not reapplied;
- `git diff --check` and final diff review.

Tests intentionally not added:

- no tests that require exact full policy/template prose;
- no heuristic semantic-truth scoring;
- no hard failure based only on lines, bytes or route count;
- no network, renderer-specific full-Markdown or downstream-repository tests.

## 13. Living Documentation Impact

- Product owners: `docs/product/README.md` and a focused workflow page only if
  final cohesion review warrants it.
- Architecture owners: `docs/architecture/README.md` and a focused checker/
  template-pack page only if warranted.
- Capability: preserve the existing two `verified` rows; the new navigable
  workflow row remains `partial` until implementation evidence supports
  promotion.
- Approved target/active change: already registered in `docs/CAPABILITIES.md`;
  clear only at validated closeout.
- Roadmap: active item already registered in `Now`; remove only at closeout.
- Baseline: create a reviewed self-host inventory without declaring the seven
  historical items resolved.
- Decision: evaluate the prospective-baseline and objective/advisory boundary;
  link the existing decision or create a superseding/additional record only if
  rationale materially changes.

## 14. Execution Steps

1. Re-read approved spec/plan/tasks and capture worktree state.
2. Add failing pure parser and generated-check contract tests.
3. Implement the shared living-document contract module.
4. Refactor direct link/living checks to use it without CLI regression.
5. Add baseline-aware blocking checks and aggregate command.
6. Refactor advisory audit to use shared rules and independent signals.
7. Update generated policy, hubs, workflow skills and change templates.
8. Add baseline/checker files and pack `0.7.0` declarations to manifest.
9. Add/complete fresh, upgrade, preservation, historical-debt and state
   compatibility fixtures.
10. Run focused tests and generated-script execution; correct only in-scope
    failures.
11. Run complete validation and proportional post-implementation audit.
12. Update self-host product/architecture/navigation/capability/roadmap/baseline
    and decision owners from evidence.
13. Fill closeout dispositions, validate links/diff and critically review the
    final boundary before reporting completion.

## 15. Rollback / Recovery

- Before implementation, rollback is deletion of unapproved plan/tasks only;
  no such action will be taken without user direction.
- During implementation, changes remain reviewable file-by-file; no destructive
  Git operation is used.
- Generated projects retain old managed tools until an explicit forced managed
  upgrade; evolved seeds remain protected.
- If `0.7.0` validation exposes a lifecycle requirement not expressible by
  current core contracts, stop and reconcile the spec/plan rather than patching
  around it.
- If the baseline parser proves too complex or ambiguous, keep strict checks
  unestablished and return to the approved format decision; never infer waivers.

## 16. Notes

- Planning audit inspected 35 relevant files. Its only encoded finding was the
  approved spec's 748-line size, accepted as a cohesive temporal contract.
- `audit_repository.py` (478 lines) and `test_template_pack.py` (491 lines) are
  close to source thresholds; implementation should extract shared behavior and
  place new contracts in focused test modules rather than append indiscriminately.
- This plan does not authorize implementation until the second approval gate.
