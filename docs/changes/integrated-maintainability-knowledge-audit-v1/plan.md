# Implementation Plan: Integrated Maintainability and Knowledge Audit v1

## 1. Summary

Add one standard-library advisory audit script to the generated
`maintainability-audit` skill, integrate its scoped use into the generated
specification/planning/closeout workflow, add an explicit closeout disposition
to the tasks template, and protect the generated behavior with focused
fixtures. Preserve the existing living-doc regression checker as the hard
semantic gate and increment the default pack to `0.6.0`.

## 2. Relevant Existing Context

- The default template pack is the source of downstream generated skills,
  managed workflow docs, `AGENTS.md` and change templates.
- The existing maintainability skill is advisory and already classifies safe
  cleanup, planned local refactor and separate-spec work, but it is primarily
  code-focused and has no reusable script.
- `spec-driven` already owns two approval gates and living-document impact, but
  only asks generally for maintainability inspection.
- `living-docs` owns knowledge navigation, current/target separation,
  distillation and the objective `check_living_docs.py`/`check_links.py`
  closeout gates.
- `check_living_docs.py` intentionally returns failure only for objective
  regressions. It must not become a heuristic size gate.
- `tests/test_template_pack.py` protects rendered workflow contracts, context
  budgets, manifest contents and fresh Python/Rust generation.
- `tests/test_living_docs_checker.py` protects the existing regression checker.
- This repository's `.agents` files are generated managed copies. Downstream
  behavior is changed in the template-pack sources, not by treating those
  copies as a second source of truth.

## 3. Existing Conventions Found

- Folder structure: default generated artifacts under
  `ai_workflow_bootstrap/template_packs/default/templates/`; standard-library
  tests under `tests/`; temporal contracts under `docs/changes/`.
- Naming style: kebab-case skill folders, snake_case Python helpers and
  behavior-named `unittest` methods.
- Error handling: validation scripts print concise deterministic diagnostics
  and return conventional process codes.
- Logging: scripts write human-readable results to standard output/error; no
  logging framework.
- Testing pattern: temporary repositories and semantic assertions rather than
  full generated-file snapshots.
- Config pattern: the manifest declares every generated managed file and
  directory.
- External integration pattern: none; generated checks are local.
- Persistence/data access pattern: no application persistence change.

## 4. Proposed Changes

### 4.1 Add the advisory repository audit

Create:

`templates/.agents/skills/maintainability-audit/scripts/audit_repository.py`

The command will accept a repository root and exactly one inspection mode:

- repeatable `--path <relative-path>` arguments for the normal scoped flow; or
- `--repo-wide` for an explicit full audit.

It will support deterministic text output and `--format json` for contract
tests and future integrations. A valid audit returns zero even when advisory
findings exist; malformed arguments or an unreadable root return a usage/error
code. Objective living-doc regressions remain the responsibility of
`check_living_docs.py`.

The script will emit sorted findings with a stable code, repository-relative
path, advisory/review level and compact evidence. It will never emit source or
document contents.

Initial signal codes:

- `large-file-review`: a source or Markdown file exceeds an advisory cohesion
  threshold;
- `knowledge-owner-concentration`: at least four capability product or
  architecture routes converge on the same Markdown owner and that owner also
  crosses the Markdown review threshold;
- `orphan-current-doc`: a current product, architecture or decision Markdown
  page is not reachable from the canonical living-document graph;
- `change-closeout-undispositioned`: a completed task checklist has no explicit
  living-document closeout disposition;
- `knowledge-owner-placeholder`: substantive project material exists while a
  required owner remains an initial placeholder.

Use documented internal defaults of 250 lines or 16 KiB for Markdown review and
500 lines or 32 KiB for recognized source files. Crossing either threshold is
evidence for review only. The agent may accept a cohesive file with rationale.

Repository-wide discovery will skip `.git`, `.ai-bootstrap`, dependency,
virtual-environment, build, cache and generated-artifact directories, binary
files and known sensitive local filenames. Scoped paths outside the repository
or inside excluded/sensitive areas will be rejected or skipped explicitly.

The current knowledge graph will start at `docs/INDEX.md` and follow
repository-relative Markdown links. Historical `docs/changes/`, templates and
idea/roadmap material are not treated as orphaned current product/architecture
owners. Capability concentration will normalize anchors to their owning file.

Completed-change detection will look for a checklist with no unchecked tasks
and require a `## Closeout Disposition` section with:

- living documentation: `updated`, `no-update-needed` with rationale, or
  `follow-up` with a link;
- maintainability: `resolved`, `accepted` with rationale, or `follow-up` with a
  link.

Only the living-document field controls the initial
`change-closeout-undispositioned` signal. The maintainability field is consumed
by agent guidance and left available for later deterministic expansion.

### 4.2 Expand maintainability-audit

Update the generated skill description and body so it:

- triggers for code or knowledge concentration, unclear ownership, large
  documents, orphan pages and incomplete closeout;
- runs the scoped audit for ordinary non-trivial work and repo-wide audit only
  when requested or justified by scoped evidence;
- inspects both implementation cohesion and knowledge retrieval cost;
- classifies each finding as safe local cleanup, planned local refactor,
  separate refactor spec or advisory observation;
- records evidence, risk, relation to the active change and disposition;
- treats deterministic output as a signal, not a semantic verdict;
- forbids broad refactors and automatic document splitting.

Keep the skill within its 300-word generated budget. The script owns detailed
thresholds and finding mechanics.

Validate the revised existing skill with the skill validation helper. No new
skill folder or UI metadata is introduced because this change updates the
existing generated skill shape.

### 4.3 Integrate the audit with spec-driven

Update the generated `spec-driven` skill, managed guide, `AGENTS.md` and change
templates with single-owner wording:

- `AGENTS.md`: compact trigger requiring proportional maintainability audit for
  non-trivial work when code or knowledge-health signals are present.
- `spec-driven/SKILL.md`: operational sequence at pre-spec, planning and
  closeout, plus the no-silent-scope-expansion routing rule.
- `docs/SPEC_DRIVEN.md`: detailed classification and approval-boundary
  rationale.
- spec template: record scoped audit findings, risk and required versus
  excluded dispositions.
- plan template: convert approved findings into local work and route
  separate-spec candidates.
- tasks template: run pre-plan and closeout audits and fill the structured
  closeout disposition.
- notes template: continue to record meaningful deviations; do not duplicate
  the disposition owner from tasks.

If a post-approval finding materially changes behavior, architecture or scope,
the workflow requires contract reconciliation and explicit approval. Unrelated
debt is never smuggled into the active change.

### 4.4 Strengthen living-doc guidance

Update the generated `living-docs` skill and managed policy so:

- indexes remain compact navigation hubs;
- focused pages are created for real product/architecture responsibilities
  when they reduce retrieval cost;
- size and repeated capability routing trigger a cohesion review rather than
  an automatic split;
- closeout checks for durable facts still trapped in specs/plans/tasks/notes;
- durable rationale is evaluated for an ADR without fabricating trivial
  decisions;
- the advisory audit complements, but does not replace, objective living-doc
  and link checks.

Do not change the seeded product/architecture/index templates merely to migrate
existing project knowledge. Managed skills/policy drive later reviewed
reorganization while lifecycle protection continues to preserve evolved seed
owners.

### 4.5 Register and version the generated surface

- Add the maintainability script directory/file to `manifest.json` under
  `skill/maintainability-audit` with managed lifecycle.
- Increment the default pack version from `0.5.1` to `0.6.0`; the new generated
  script and cross-workflow contract are a feature-level pack evolution.
- Update manifest/version and generated-surface tests.
- Do not change the tool distribution version or manifest schema.

### 4.6 Protect behavior with tests

Add `tests/test_maintainability_audit.py` with temporary repositories covering:

- explicit-scope requirement and deterministic ordering;
- large Markdown/source advisory findings and zero exit status;
- absence of the size finding below threshold;
- orphan current-doc detection and reachable-page success;
- capability concentration with anchors versus a small cohesive shared owner;
- completed tasks without disposition, accepted `updated`, and justified
  `no-update-needed`;
- sensitive/cache/generated path exclusion;
- JSON output containing evidence metadata but no file contents.

Extend `tests/test_template_pack.py` to prove:

- the new script is declared and rendered;
- the generated skills/guides/templates contain semantic anchors for the three
  audit boundaries, classifications and scope protection;
- existing two approval gates remain intact;
- context word budgets still pass;
- fresh Python and Rust projects receive the audit surface without changing
  conditional Rust behavior.

Keep existing living-doc checker tests unchanged except for additive assertions
that demonstrate its hard-failure contract remains separate.

## 5. Module Boundaries

- Maintainability audit script: objective, advisory signal collection only.
- `maintainability-audit` skill: semantic cohesion/risk interpretation and
  disposition.
- `spec-driven` skill/guide/templates: lifecycle timing, approved scope and
  routing.
- `living-docs` skill/policy: knowledge ownership, focused-page decisions and
  closeout distillation.
- Existing living-doc checker: hard objective regression detection.
- Manifest: generated file membership and pack version.
- Tests: public generated behavior and deterministic script contracts.
- Planner, renderer, applier, CLI, TUI, scanner, state and lifecycle modules
  must not learn maintainability heuristics.

## 6. Architecture Locality

- Primary owner: default template pack.
- Files expected to change:
  - default manifest;
  - generated `AGENTS.md`, three skill templates and two managed workflow
    guides;
  - spec/plan/tasks templates;
  - new generated maintainability audit script;
  - `tests/test_maintainability_audit.py`,
    `tests/test_template_pack.py` and narrowly related checker tests;
  - this repository's product, architecture, capabilities, roadmap and
    possibly one durable decision at closeout;
  - this change's tasks/notes.
- Files that should not change:
  - core planning/application/lifecycle modules;
  - CLI/TUI behavior;
  - project-owned instructions;
  - seeded downstream knowledge templates solely to force migration;
  - completed historical changes.
- New boundary: deterministic advisory repository-health scan inside the
  maintainability skill.
- Existing boundaries preserved: hard regression validation in living docs,
  semantic interpretation in skills and approval control in spec-driven.
- Why this is the smallest maintainable change: the template pack already owns
  every generated workflow surface and requires no runtime bootstrap feature.
- Are affected files conceptually related? Yes; they compose one generated
  workflow contract and its tests.
- Does this touch many files? Yes, intentionally across single-purpose workflow
  owners. Detailed prose will remain in the two managed guides; always-read
  surfaces receive only operational anchors.
- Refactor timing: no unrelated refactor before implementation. If shared test
  fixture creation becomes repetitive, extract only a test-local helper.

## 7. Data / API / Interface Impact

- New generated command-line script with path/repo-wide modes and text/JSON
  output.
- New structured closeout fields in generated `tasks.md`.
- Revised generated instruction contract and pack version `0.6.0`.
- No Python library API, bootstrap CLI, TUI, manifest schema or persisted-state
  schema change.

## 8. Security / Privacy Impact

- The script reads only recognized text/Markdown metadata needed for signals.
- It skips sensitive local filenames and common dependency/build/cache trees.
- Output contains only relative paths, counts, sizes, codes and dispositions,
  never source/doc contents or secret values.
- Paths are resolved and checked against the repository root to prevent escape.
- No network calls, telemetry or new credential handling.

## 9. Dependency Impact

No dependency is added. `argparse`, `json`, `pathlib`, `re` and other Python
standard-library facilities are sufficient. This avoids installation and
security impact in freshly generated repositories.

## 10. Risks

- Heuristic noise in old repositories: keep findings advisory, sorted and
  evidence-based; require agent judgment.
- Large historical change backlogs: exclude them from orphan analysis and
  report closeout findings individually only in explicit repo-wide mode or
  when their path is scoped.
- Markdown link parsing differences: support ordinary repository-relative
  inline links and defer exotic syntax to semantic review.
- Instruction duplication: assign detailed mechanics to the script and guides;
  keep skills/AGENTS operational and tested by word budget.
- False confidence: state explicitly that a clean scoped audit is not a
  repository-wide baseline.
- Silent scope growth: test semantic anchors requiring re-approval or separate
  spec routing.
- Applying pack `0.6.0` to evolved projects: managed workflow updates safely;
  seeded project knowledge remains preserved.

## 11. Validation Strategy

Develop contract-first: add focused failing audit fixtures and generated-output
assertions, implement the script and template contract, then run the complete
standard-library suite and fresh generation checks. Finish with skill,
manifest, living-doc and diff validation.

## 11.1 Test Strategy

- Contracts protected: deterministic advisory signals, sensitive output
  boundary, proportional workflow timing, approval-scope routing, closeout
  disposition and generated-surface completeness.
- Tests to add/update: audit subprocess/fixture tests, manifest rendering and
  semantic template assertions, additive hard-versus-advisory separation.
- Tests intentionally omitted: subjective automatic proof of “mixed
  responsibility,” LLM calls, exact prose snapshots, background watchers,
  stack-specific AST complexity and automatic document rewrites.
- Refactor resilience: tests assert codes, evidence metadata and generated
  public semantic anchors rather than private helper structure.

Validation commands:

1. `python -m unittest tests.test_maintainability_audit -v`
2. `python -m unittest tests.test_template_pack tests.test_living_docs_checker tests.test_workflow -v`
3. `python -m unittest discover -s tests -v`
4. `python -m compileall -q ai_workflow_bootstrap`
5. `python -m json.tool ai_workflow_bootstrap/template_packs/default/manifest.json`
6. Run the skill-creator `quick_validate.py` against the revised generated
   maintainability skill template.
7. Generate temporary Python and Rust repositories and execute the generated
   audit fixture in each.
8. `python .agents/skills/living-docs/scripts/check_living_docs.py --baseline-ref HEAD`
9. `python .agents/skills/living-docs/scripts/check_links.py`
10. `git diff --check`
11. Attempt `python -m build`; if optional packaging tooling is still absent,
    record that environment limitation without weakening the repository-native
    validation.

## 12. Living Documentation Impact

- Product owner: record the verified generated audit workflow after validation.
- Architecture owner: record script/skill/spec-driven/living-doc boundary and
  advisory versus hard-check separation.
- Capability: retain current `partial` evidence during implementation; promote
  to `verified` and clear target/active change only after all acceptance
  evidence passes.
- Roadmap: remove the active item at successful closeout.
- Decision: create one ADR if implementation confirms that objective
  regressions and advisory health signals are durable separate interfaces.
- Links/evidence: new script, change artifacts, tests and any ADR.
- No-update case: not applicable; generated public behavior changes.

## 13. Execution Steps

1. Re-read approved spec/plan and capture the pre-existing worktree boundary.
2. Add failing audit fixtures and generated-template assertions.
3. Implement the standalone advisory audit script and make focused tests pass.
4. Update maintainability, spec-driven and living-doc generated contracts
   without duplicating detailed mechanics.
5. Add structured closeout disposition to change templates.
6. Register the generated script and bump the pack to `0.6.0`.
7. Run focused and full tests, skill validation and fresh generated-project
   execution.
8. Review audit output on this repository and accept or route advisory findings
   without expanding this change.
9. Reconcile product, architecture, capability, roadmap and durable decision
   owners from validated evidence.
10. Fill closeout disposition, run final living-doc/link/diff checks and inspect
    the complete approved diff.

## 14. Rollback / Recovery

Before closeout, remove only the new generated audit template, manifest entry,
new tests and this change's workflow-template edits; restore the prior pack
version and leave seeded knowledge/current capability evidence intact. If the
advisory audit cannot meet signal quality or privacy criteria, keep the current
capability `partial`, retain the approved target and do not publish pack
`0.6.0`. No data migration, downstream write or persisted-state recovery is
required.

## 15. Notes

No implementation deviations are known at planning time.
