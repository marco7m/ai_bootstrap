# Implementation Plan: Contract-First Proportional Workflow v1

- Status: `completed`
- Approved spec: [spec.md](spec.md)
- Spec approved: 2026-08-13
- Plan and tasks approved: 2026-08-13
- Classification: material behavioral novelty; high execution risk

## 1. Summary

Implement default template-pack `0.8.0` within its existing managed template
boundary. Behavioral novelty will determine whether a spec is needed; every
non-trivial implementation will retain approved `plan.md` and `tasks.md`.
Only genuinely trivial, unequivocal, low-risk work may use direct flow.

The existing artifact types and lifecycle engine are sufficient. Temporary
synthetic projects will prove fresh multi-stack delivery, `0.7.1` upgrade,
lifecycle preservation and a non-trivial repair directory containing
plan/tasks/notes without `spec.md`.

This plan and [tasks.md](tasks.md) were explicitly approved together on
2026-08-13.

## 2. Current Evidence and Conventions

- Pack version is `0.7.1`.
- Generated `AGENTS.md`, `spec-driven/SKILL.md` and `docs/SPEC_DRIVEN.md`
  currently route every non-trivial task through a new spec.
- Current counts versus approved budgets are 656/800, 266/300 and 669/1000
  words respectively.
- `START_PROMPT.md` also implies a universal spec-first route.
- Plan/tasks/notes templates do not fully represent a repair without spec.
- Generated link/living/aggregate checkers and the auditor are currently keyed
  by change directory or `tasks.md`; inspection found no general `spec.md`
  requirement. Protect that behavior with tests before considering code edits.
- Template-pack files are managed; living owners are seeded/project knowledge;
  `AGENTS.project.md` is project-owned.
- Temporary generation tests already use `build_plan`, `apply_plan` and
  synthetic `RepoProfile` instances.

The scoped source audit found `large-file-review` only for
`tests/test_template_pack.py` (510 lines), so scenario coverage will go in a
focused test module. The artifact audit also flagged this spec and an earlier
verbose plan draft. The approved spec remains one cohesive temporal contract;
this plan was rewritten by delta to resolve its own concentration finding.

## 3. Template Changes

### Compact routing surfaces

- `templates/AGENTS.md`: replace the universal spec route with authority-first
  classification, the unconditional non-trivial plan/tasks gate, the
  spec-on-novelty/ambiguity rule and the narrow trivial direct-flow exception.
  Link details to the guide and remain within 800 words.
- `templates/.agents/skills/spec-driven/SKILL.md`: in at most 300 words, route
  authority discovery, internal novelty/risk reasoning, concise material
  disclosure, applicable gates, implementation, validation and closeout.
- `templates/docs/START_PROMPT.md`: make spec approval conditional while keeping
  plan/tasks approval mandatory for every non-trivial implementation.

These files will carry invariants and links, not duplicate the full matrix.

### Detailed on-demand owner

Rewrite `templates/docs/SPEC_DRIVEN.md` within 1000 words as the single owner of
the approved route matrix and examples. It will cover:

- adaptable authority versus evidence;
- two-axis reasoning without numeric scoring or trivial-response ceremony;
- six routes and disguised product-change signals;
- the unconditional second gate for non-trivial implementation;
- active/historical change reconciliation;
- the no-spec repair directory contract;
- progressive disclosure, compact handoff, stop conditions and proportional
  validation.

Examples remain stack- and domain-neutral.

### Existing artifact templates

- `templates/docs/changes/_templates/plan.md`: begin with either an approved
  spec or an existing contract authority. A no-spec repair declares novelty
  `none` and records reproduction, cause, boundary, risks, regression and
  validation without copying the contract.
- `templates/docs/changes/_templates/tasks.md`: reread the applicable authority,
  explicitly confirm plan/tasks approval and stop if novelty or conflict
  appears; do not assume a spec exists.
- `templates/docs/changes/_templates/notes.md`: identify its optional,
  non-empty evidence/deviation/limitation/validation/closeout role.
- Leave spec/open-question/decision templates unchanged unless a focused
  failure proves a missing approved contract and triggers reconciliation.

No artifact type, routing engine or mandatory classification record is added.

## 4. Checks, Version and Lifecycle

- Add regression fixtures proving a complete plan/tasks/notes repair directory
  without spec passes generated link and closeout checks, while pending tasks,
  broken links and invalid dispositions still fail.
- Leave `check_docs.py`, `check_living_docs.py`, `check_links.py`,
  `documentation_contract.py` and the auditor unchanged if current behavior
  passes. A discovered grammar requirement is a stop/reapproval condition.
- Change only `manifest.json` version from `0.7.1` to `0.8.0`; preserve groups,
  lifecycle classes, project-owned paths, compositions and obsolete migrations.
- Do not change renderer, scanner, workflow selection, lifecycle, planner,
  applier, state, CLI or TUI without focused evidence and renewed approval.
- Do not synchronize root generated workflow copies or repair the stale root
  `.agents` installation; reusable template sources are authoritative here.

## 5. Test and Compatibility Design

Create `tests/test_spec_driven_workflow.py` so route scenarios do not enlarge
the manifest inventory suite. Protect the outcomes in spec acceptance criteria
1–13 through stable markers and generated artifacts, not whole paragraphs or an
LLM integration harness. In particular, prove:

- spec presence/absence is decided by novelty/ambiguity;
- every non-trivial route has approved plan/tasks;
- direct flow requires trivial + unequivocal + low risk;
- material classification is normally one sentence and creates no file;
- no-spec repair plan/tasks/notes have their approved roles;
- read-only/trivial routes create no empty change directory;
- handoffs are compact and validation comes from local stack/instructions.

Keep version, inventory, frontmatter and word-budget assertions in
`tests/test_template_pack.py`, changing only concise anchors there.

Temporary compatibility fixtures will:

1. Freshly generate Python and Rust projects with all skills and execute their
   no-spec repair documentation checks.
2. Generate a Node or Go profile and verify stack-neutral routing/local command
   detection without installing dependencies.
3. Model `0.7.1` prior state with old managed content, evolved seeded owners and
   `AGENTS.project.md`; exercise preview, managed update, managed-only and
   reapply.
4. Assert managed guidance updates, seeded/project-owned bytes remain intact,
   state becomes `0.8.0`, and no unexpected conflict or `migration_required`
   appears.
5. Validate the no-spec format using delivered fresh and upgraded content, not
   source assertions alone.

## 6. Boundaries and Impact

- Policy remains in managed templates; detailed routing remains in generated
  `docs/SPEC_DRIVEN.md`; durable current truth remains in living owners.
- Generated checkers validate links/tasks/closeout but do not decide product
  novelty.
- Existing lifecycle/state schema and public checker CLI remain unchanged.
- A focused test module is the only planned local structural improvement.
- No dependency, credential, network call, customer payload or real downstream
  is involved. Fixtures are synthetic and temporary.
- Pack output behavior and version change; application APIs and persistence do
  not.

Stop before new dependencies, artifact types, checker grammar, core changes,
expanded permissions, destructive actions or unrelated refactors.

## 7. Validation Strategy

Run in ascending cost; do not repeat expensive gates without relevant changes:

1. `git diff --check` and focused route/template-budget tests.
2. Focused checker plus lifecycle/state/planner/applier tests for the no-spec
   format and `0.7.1` upgrade.
3. `python -m compileall -q ai_workflow_bootstrap tests`, removing only
   untracked caches proven to be created by this run.
4. Manifest, frontmatter, relative-link and source/generated aggregate checks.
5. Fresh Python/Rust/Node-or-Go generation and delivered-content checks.
6. Temporary upgrade, managed-only, seed/project-owned preservation, reapply
   and no-spec closeout checks.
7. Full `pytest -q` and `python -m unittest discover -s tests -q` after inputs
   stabilize.
8. Scoped post-change audit, targeted closeout and critical diff review.

The review must look specifically for gate weakening, disguised product change,
classification ceremony, duplicated guidance, budget overflow, stack leakage,
brittle prose assertions and lifecycle changes. Deterministic temporary-project
evidence will not be called real downstream agent validation.

## 8. Living Documentation

After implementation evidence exists:

- add the approved target/active change to `docs/CAPABILITIES.md` without
  replacing verified current evidence, then update evidence and clear it only
  at successful closeout;
- update `docs/product/README.md` by delta with authority-first routing, the
  unconditional second gate and the no-spec repair shape;
- update `docs/architecture/README.md` by delta with compact/on-demand ownership
  and unchanged lifecycle/checker boundaries;
- create no focused owner or ADR unless a real responsibility/rationale boundary
  is proven and reconciled;
- do not rewrite historical changes, baseline inventory or root generated
  workflow copies.

Use the installed targeted closeout only if compatible. If root self-host drift
prevents it, run the candidate source checker read-only and report that
limitation rather than mutating the installed skill.

## 9. Execution Order

1. Re-read approved artifacts, capture worktree, confirm second approval and
   register the approved target.
2. Add focused failing route, second-gate, classification and no-spec contracts.
3. Rewrite compact surfaces and detailed guide within approved budgets.
4. Adapt plan/tasks/notes templates without adding artifacts.
5. Prove current tasks-based checker behavior; stop if checker code is needed.
6. Bump the pack to `0.8.0` and add fresh/upgrade multi-stack fixtures.
7. Run focused through full validation in the ordered ladder.
8. Re-audit and critically review the exact diff.
9. Distill supported durable facts, complete closeout and stop without commit.

## 10. Recovery and Approval Gate

Before this second approval, only spec/plan/tasks exist. Implementation remains
source-local and reviewable; temporary projects are disposable. No staging,
commit, force application, knowledge reset or destructive Git operation is
authorized. Preserve unrelated work and remove only proven run-generated
untracked artifacts.

Approval must cover this plan and [tasks.md](tasks.md) together. It authorizes
only the template sources, focused tests, temporary fixtures and living-owner
closeout described above. Any stopped boundary returns to approval.
