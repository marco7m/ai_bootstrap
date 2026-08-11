# Tasks: Navigable Living Knowledge v1

- Status: `completed`

## Approval and baseline

- [x] Re-read the approved spec and approved plan before implementation.
- [x] Capture `git status --short` and preserve all unrelated/pre-existing work.
- [x] Confirm the current capability evidence remains unchanged and the approved
      target/active roadmap item still point to this change.
- [x] Re-run the scoped planning audit if repository state changed materially.

## Contract-first tests

- [x] Add `tests/test_documentation_contract.py` for links, ATX fragments,
      capability routes, baseline tables, closeout grammar and safe paths.
- [x] Add `tests/test_docs_checker.py` for repository and targeted-closeout
      aggregation, stable diagnostics, exit policy and non-repository cwd.
- [x] Add failing blocking-check fixtures for orphan owners, missing/wrong-area/
      change-artifact capability owners, incompatible placeholders, malformed
      baseline, invalid new closeout and unlisted post-baseline debt.
- [x] Add advisory fixtures proving size and route concentration are independent,
      never fail solely by threshold and require closeout disposition when
      relevant to the targeted change.
- [x] Add distinct generation/upgrade fixtures for fresh, clean existing,
      evolved-seed, historical-debt and legacy `0.5.1` state repositories.

## Shared documentation contract and checks

- [x] Add the managed `documentation_contract.py` template with one source for
      link, heading, route, reachability, baseline and closeout parsing.
- [x] Refactor `check_links.py` to use shared file/fragment validation while
      preserving its direct CLI.
- [x] Refactor `check_living_docs.py` to use shared current-state and capability
      parsing and add objective navigation/baseline/prospective-closeout gates.
- [x] Add thin `check_docs.py` repository and `--closeout` modes without copied
      parsing or subprocess-only composition.
- [x] Refactor `audit_repository.py` to import the shared contract, split size
      from concentration, report baseline-aware debt and keep advisory exit zero.
- [x] Remove `follow-up` from valid closed living-document dispositions and
      reject only objective placeholder/generic rationale markers.

## Generated workflow and pack

- [x] Add the empty human-readable
      `templates/docs/LIVING_DOCUMENTATION_BASELINE.md` scaffold.
- [x] Update INDEX, product/architecture hubs, CAPABILITIES, GLOSSARY and living-
      documentation policy templates with navigation, authority and baseline
      contracts; leave decision templates unchanged unless durable-rationale
      routing genuinely needs a concise adjustment.
- [x] Update generated living-docs, maintainability-audit and spec-driven skills
      with their distinct responsibilities and concise timing.
- [x] Update spec, plan, tasks and notes templates with exact owner/fact and
      closeout dispositions; update `docs/SPEC_DRIVEN.md` only for detailed
      procedure that does not belong in always-loaded skills.
- [x] Update generated `AGENTS.md` only if one concise aggregate-closeout route
      is necessary and keep all context word budgets.
- [x] Declare the seeded baseline and managed shared/aggregate scripts in
      `manifest.json`; bump the default pack to `0.7.0` without changing existing
      lifecycles, obsolete migrations, compositions or project-owned paths.

## Lifecycle and compatibility validation

- [x] Prove fresh Python and Rust generation includes the complete `0.7.0`
      documentation surface and no domain-specific focused pages.
- [x] Prove preview, dry-run, apply and reapply preserve evolved/untracked seeded
      owners and safely update only managed or trusted untouched-seed paths.
- [x] Prove `--managed-only` installs managed checks but does not create or
      falsely establish the seeded baseline.
- [x] Prove an explicitly established legacy inventory keeps known historical
      debt visible, permits reduction after review and rejects new unlisted debt.
- [x] Prove legacy `0.5.1` state remains readable and grants no overwrite or
      inferred-baseline authority.
- [x] Confirm no core lifecycle, planner, applier, state, CLI or TUI change is
      needed; stop for contract reconciliation if this assumption fails.

## Validation and self-host closeout

- [x] Run focused parser/checker/audit/template/lifecycle tests and generated
      scripts from temporary repositories and another cwd.
- [x] Run `python -m unittest discover -s tests -v`.
- [x] Run `python -m compileall -q ai_workflow_bootstrap tests`.
- [x] Validate manifest loading, pack version, generated skill frontmatter and
      always-loaded word budgets.
- [x] Run the proportional audit against the implemented diff and affected
      knowledge owners; disposition every finding without silent scope expansion.
- [x] Update root README and self-host product/architecture/navigation owners
      only from implemented and validated behavior, creating focused pages only
      for real responsibilities.
- [x] Establish the self-host baseline through reviewed evidence; keep the seven
      known historical closeouts explicitly unresolved unless actually reviewed.
- [x] Promote the navigable workflow capability and clear its approved target/
      active change only when implementation evidence supports the final state.
- [x] Remove the roadmap item only after durable owners and capability evidence
      are reconciled.
- [x] Reuse or add a durable decision only if final baseline/gate rationale must
      survive this change.
- [x] Run direct living-doc/link checks, the source aggregate checker against
      this repository, and `git diff --check`.
- [x] Critically inspect the final diff for parser/policy duplication, brittle
      prose tests, hidden hard thresholds, historical rewrites, sensitive output,
      lifecycle leakage and shotgun surgery.
- [x] Validate every approved acceptance criterion and record meaningful
      deviations in `notes.md` only if implementation creates them.
- [x] Confirm no downstream repository, historical change artifact or evolved
      seeded owner was automatically rewritten.

## Closeout Disposition

- Living documentation: `updated`
- Living documentation rationale: focused product and architecture owners,
  navigation, policy, baseline, capability, roadmap and durable decision were
  reconciled with the validated implementation.
- Durable facts added/changed/removed: added the three-layer navigation,
  explicit prospective baseline and aggregate-check contracts; changed closeout
  and audit authority; removed `follow-up` as a valid closed disposition.
- Maintainability findings: `accepted` — the root README remains a cohesive user
  guide; spec and plan remain cohesive temporal contracts; manifest assertions
  stay in `test_template_pack.py` while behavioral contracts live in focused
  test modules. No concentration, orphan owner, parser duplication or shotgun
  surgery finding remains.
