# Change Spec: Contract-First Proportional Workflow v1

- Status: `approved`
- Approved: 2026-08-13
- Approval scope: pack `0.8.0`, existing artifact types, current context budgets,
  and the reconciled non-trivial implementation gate and repair-artifact
  contract below.

## 1. Summary

Evolve the reusable default template-pack so an agent classifies work before
creating change artifacts. The generated workflow must separate behavioral
novelty from execution risk, locate existing authority first, and select the
smallest sufficient combination of specification, planning, approvals,
context, documentation and validation.

The workflow remains one integrated `spec-driven + living-docs` workflow with
two explicit approval gates whenever a new or reconciled specification and a
non-trivial implementation plan are required. Every non-trivial implementation
retains the plan/tasks approval gate even when no new spec is needed. Using
`spec-driven` will no longer imply that every non-trivial task creates a new
product specification.

This change is itself classified as:

- behavioral novelty: **material**, because it changes generated agent routing,
  artifact creation and approval behavior;
- execution risk: **high**, because managed instructions are distributed to
  repositories of different stacks and maturity, and an incorrect route could
  either weaken a gate or create recurring documentation and validation cost.

## 2. Problem

The current default pack is `0.7.1`. Its generated `AGENTS.md` says that every
non-trivial task creates `docs/changes/<change>/spec.md`; the generated
`spec-driven` skill repeats that path; and `docs/SPEC_DRIVEN.md` describes one
non-trivial route centered on a new spec. This correctly preserves approval
discipline but conflates two independent questions:

1. Does the work need controlled scope, approval, planning and validation?
2. Does the work introduce a behavioral or architectural decision that needs a
   new or reconciled specification?

As a result, a complex repair whose expected behavior is already authoritative
can be made to re-specify the product. The repeated contract then propagates
through spec, plan, tasks and closeout, consumes context, obscures the actual
delta and makes handoff harder. Conversely, simply suppressing the spec based
on a “bug” label could weaken gates for risky repairs or hide product changes
presented as bugs.

The source inspection also found these relevant conditions:

- the always-read `AGENTS.md` and skill already have explicit word budgets;
- the detailed on-demand guide is the appropriate owner for a routing matrix
  and examples;
- lifecycle already distinguishes managed, seeded and project-owned files, so
  the workflow change should not require a parallel lifecycle mechanism;
- existing tests protect the two gates and generated surfaces, but several
  assert literal prose rather than complete routing outcomes;
- the scoped maintainability audit found only `large-file-review` for
  `tests/test_template_pack.py` (510 lines), an advisory cohesion signal;
- this checkout's installed `.agents` state predates the current pack and lacks
  the generated audit script, while the reusable template source contains it.
  That self-hosting drift is evidence to preserve, not authority for broadening
  this change.

## 3. Goal

Make the generated workflow safe and efficient across domains, languages,
stacks and documentation maturity by ensuring that agents:

- discover authority and classify work before creating artifacts;
- distinguish contract novelty from execution risk;
- preserve necessary approvals without inventing product decisions;
- use progressive context disclosure and compact handoffs;
- update artifacts and durable knowledge by delta;
- select proportionate validation from repository evidence and affected
  boundaries;
- finish one vertical change before opening incidental work;
- remain usable when structured living documentation is absent.

## 4. Scope

### Required source contract

Update the reusable sources, subject to the approved implementation plan:

- `ai_workflow_bootstrap/template_packs/default/templates/AGENTS.md`;
- `ai_workflow_bootstrap/template_packs/default/templates/.agents/skills/spec-driven/SKILL.md`;
- `ai_workflow_bootstrap/template_packs/default/templates/docs/SPEC_DRIVEN.md`.

The always-read files must remain compact routing surfaces. Detailed route
definitions, examples, artifact budgets and validation guidance belong in the
on-demand guide.

### Conditional source contract

Inspect and change only when required to deliver or validate the approved
behavior:

- `templates/docs/START_PROMPT.md`;
- templates for spec, plan, tasks and notes;
- the generated `living-docs` and `maintainability-audit` skills;
- the default manifest and pack version;
- tests that own template content, generation, lifecycle and temporary-project
  compatibility.

Prefer existing artifacts and lifecycle categories. Do not introduce a repair
document type, routing engine or checker unless implementation evidence proves
that concise guidance and existing spec/plan/tasks/notes owners are
insufficient.

### Validation scope

Validate source contracts, generated output, upgrade behavior and two distinct
temporary stack profiles. Use only temporary projects; downstream repositories
are excluded even as writable fixtures.

## 5. Out of Scope

- Editing, applying, or validating by mutation against any real downstream
  project.
- Encoding rules specific to `DraftCorrectionOutput`, `InvalidOpeningCue`,
  `opening_cues`, games, providers, Rust, Python or another domain/stack.
- Replacing `spec-driven + living-docs` with competing workflows.
- Redesigning bootstrap lifecycle, planner, applier, state, CLI or TUI unless a
  concrete compatibility defect makes a narrow change necessary and that
  scope is explicitly reconciled before implementation.
- Creating a mandatory work diary, context-map document, repair-spec type or
  permanent artifact for trivial/read-only work.
- Rewriting closed historical changes to reflect the new workflow.
- Refactoring large tests solely because an advisory size threshold fired.
- Adding dependencies, committing, staging, force-applying, resetting project
  knowledge or performing destructive Git operations.

## 6. Users / Actors

- Agents executing features, repairs, refactors, maintenance and investigations
  in generated repositories.
- Project owners who approve behavioral contracts and implementation plans.
- Maintainers applying or upgrading the default template-pack.
- A later agent or session resuming approved work from repository artifacts.
- Repositories with rich living docs and repositories whose only authorities
  are README files, ADRs, tickets, schemas, tests, APIs, configuration, code or
  user-supplied external documentation.

## 7. Functional Requirements

### 7.1 Authority-first orientation

1. Before creating an artifact or reading broad repository context, the agent
   must read local instructions, start at the compact knowledge hub when one
   exists, locate the relevant contract/capability/active change, and follow
   only links needed for the next decision.
2. The workflow must distinguish authority from evidence. Its adaptable
   preference is current product contract, approved decisions, current
   architecture, capability owner, approved active change, public contracts and
   invariants, with code/runtime as current implementation evidence and
   historical changes as context rather than the sole current owner.
3. The workflow must degrade gracefully when these document categories do not
   exist and use the best available README, ADR, ticket, schema, test, API,
   configuration, code or supplied external contract.
4. Conflicts among docs, tests, code and runtime must be surfaced. Current code
   is not automatically the intended contract.

### 7.2 Two-axis classification

5. Before selecting a route or artifact, the agent must reason about two
   independent axes:
   - behavioral novelty: none, partial or material;
   - execution risk: reasoned from affected responsibilities, persistence,
     interfaces/consumers, security/privacy, concurrency/idempotency,
     dependencies, reversibility, blast radius, deterministic regression and
     required real environments.
6. The generated workflow must not impose a numeric score or a standard report
   block. The agent exposes a concise evidence-based classification when it
   determines artifact creation, an approval gate, scope expansion or material
   validation; normally one sentence is sufficient. Trivial tasks, questions,
   explanations and simple investigations need not print it.
7. No file, report or permanent map is created merely to record classification.
   Execution risk determines the depth of an already-required non-trivial plan
   and its validation, not whether the second gate exists. Material behavioral
   novelty requires a new or explicitly reconciled spec even when the code diff
   appears small.

### 7.3 Work routes

8. The detailed guide must define and distinguish these routes:
   - **new behavior or contract change:** new spec, explicit approval, plan and
     tasks, second approval, then implementation;
   - **bug restoring a clear existing contract:** cite authority, preserve or
     add proportional regression evidence and diagnose; a non-trivial repair
     requires plan and tasks plus explicit approval before the narrow repair,
     while a truly trivial low-risk repair may use the direct flow; validate
     against the existing contract without a new product spec;
   - **ambiguous bug or authority conflict:** do not guess; create or reconcile
     a spec and obtain approval before planning;
   - **behavior-preserving refactor or maintenance:** no automatic product spec;
     every non-trivial implementation still uses plan, tasks, explicit approval
     and proportional audit/validation, adding a spec only for changed
     responsibility/boundary/contract or another relevant decision;
   - **trivial unequivocal work:** direct or explicitly compressed flow,
     proportional validation, no empty temporal artifacts, and preservation of
     any approval the user explicitly required;
   - **read-only investigation/diagnosis:** locate authority, reproduce safely,
     explain cause and recommend a route without inferring implementation
     authorization.
9. “Bug” labeling must not bypass novelty detection. A new observable result,
   relaxed validation, fallback, retry/cost increase, authority source,
   compatibility rule, persisted data, access/privacy behavior or choice among
   plausible outcomes requires reconciliation/spec approval.

### 7.4 Approval and stop behavior

10. A new or reconciled spec requires explicit approval before plan/tasks.
11. Every non-trivial implementation requires proportional `plan.md` and
    `tasks.md` plus their own explicit approval before implementation, including
    every clear-contract repair whose behavioral novelty is `none`. Spec
    approval and silence are not implementation approval.
12. Omitting a new product spec never omits the second gate for non-trivial
    work. Only work that is genuinely trivial, unequivocal and low risk may use
    a direct/compressed implementation flow. There is no intermediate
    “proportional risk” route that permits non-trivial implementation without
    approved plan/tasks. An already-approved active plan satisfies this rule
    only while it still covers the same repair approach, scope, risk and
    acceptance criteria; otherwise it must be reconciled and reapproved.
13. The agent must stop on a new behavioral decision, material scope/risk or
    approach change, authority conflict, destructive action/new permission, or
    required P0/P1 playtest stop.
14. The agent should not stop merely to ask something discoverable through safe
    read-only inspection or for a local decision that does not change approved
    behavior or scope.

### 7.5 Active and historical change routing

15. A defect within an active approved change must preserve evidence and be
    reconciled into its existing plan/checklist when it implements the same
    contract. A new spec is not automatic.
16. Material changes to the active contract, approach, risk, scope or acceptance
    criteria must trigger the corresponding reconciliation and renewed
    approval.
17. A closed historical change must not be silently reopened or rewritten. A
    repair may link to its relevant contract and use an existing plan/tasks/notes
    artifact or a narrow repair record only when planning, approval or
    traceability requires it. It must not duplicate the original specification.

### 7.6 Repair artifacts without a new specification

18. A standalone non-trivial clear-contract repair that is not already covered
    by suitable active artifacts uses
    `docs/changes/<repair>/plan.md`, `tasks.md` and, during implementation and
    closeout, `notes.md`; the directory intentionally has no `spec.md`.
19. Its `plan.md` must begin by linking the existing authority being restored
    and explicitly state that the repair introduces no behavioral novelty. It
    records the reproduced defect, diagnosed cause, repair boundary, risks,
    regression and validation strategy without copying the existing contract.
20. Its `tasks.md` is the concrete checklist approved at the second gate.
    `notes.md` records material evidence, deviations, limitations and closeout;
    it is created only when implementation or closeout has such content.
21. If planning or implementation discovers a behavioral decision, authority
    conflict or material contract expansion, stop and create or reconcile a
    spec before continuing. Obtain spec approval and then approval of the
    reconciled plan/tasks.
22. Generated tools and documentation checks must accept a valid change
    directory with plan/tasks/notes and no spec. They must not weaken normal
    task, link, audit or closeout checks for that format.
23. Do not create a repair directory for a trivial bug or read-only
    investigation. Their direct result or diagnosis is sufficient unless the
    route later becomes non-trivial implementation work.

### 7.7 Progressive context and compact handoff

24. Generated guidance must direct agents to search terms/links first, open
    only necessary sections/files, deepen context only when the next decision
    depends on it, and avoid rereading unchanged sources without a concrete
    reason.
25. Requirements must be linked rather than copied across spec, plan, tasks,
    notes and closeout. The active working map consists of objective, authority,
    active change, relevant files, pending decision, remaining gates, evidence
    and blockers, represented by existing artifacts whenever possible rather
    than a mandatory new diary.
26. A handoff must compactly identify approved objective, authorities, current
    state, next concrete task, expected files, prohibitions, completed/pending
    validation and worktree/evidence to preserve. It must not contain a
    conversation transcript, duplicated rationale, irrelevant file inventory or
    raw tool output when a reproducible summary suffices.
27. Resumption must begin from active artifacts and status, not reconstruction
    of the entire conversation or historical archive.

### 7.8 Artifact and knowledge budgets

28. Each artifact must retain one purpose: spec = what/why, plan = how, tasks =
    verifiable sequence, notes = deviations/evidence/limits/results, living
    owners = current durable truth, decision = durable rationale among material
    alternatives.
29. Artifacts must use the minimum detail sufficient for decision, handoff,
    implementation and verification, with links and deltas relative to existing
    authority. No rigid line/token quota is introduced for individual changes.
30. Empty specs/plans/notes, duplicated requirements, conversation archives and
    transient facts without future value are prohibited. Repair specs, when
    genuinely needed, cover only the unresolved delta.
31. Closeout must update living owners only for supported durable changes,
    preserve current capability evidence until superseded by validation, and
    avoid restating facts already owned elsewhere.

### 7.9 Completion-oriented planning

32. The workflow must favor one vertical change/repair and one concrete next
    action at a time. Broad parallel roadmaps and incidental refactors/bugs do
    not enter scope unless they block acceptance, violate essential
    security/correctness or are inseparable from the repair.
33. External gates that cannot run remain honestly pending; unavailable runtime
    is neither a pass nor by itself proof that local implementation failed.

### 7.10 Proportional validation

34. Validation must follow a risk-based ladder: quick pure checks, focused
    regression/contract test, affected boundary integration, persistence or
    migration checks, relevant consumers/compatibility, proportional
    lint/type/format checks, broad suite when blast radius or closeout requires
    it, and real runtime/hardware/provider/playtest when it is an acceptance
    gate.
35. Agents must fail fast on cheap checks and must not rerun an expensive gate
    when no relevant input changed. Commands come from detected stack and local
    instructions, not a hard-coded language/tool assumption.
36. Validation reports must distinguish deterministic checks from real
    environment evidence, record reproducible commands/evidence, and preserve
    unavailable gates as pending.

## 8. Non-Functional Requirements

### Modularity / Architecture

- Preserve one integrated generated workflow. `AGENTS.md` and the
  `spec-driven` skill own compact routing; `docs/SPEC_DRIVEN.md` owns the
  detailed matrix and examples; `living-docs` continues to own durable
  knowledge; maintainability audit remains advisory evidence.
- Keep workflow policy in template sources, not generic lifecycle/planner/
  applier/state modules, unless a reusable lifecycle defect is independently
  proven and reconciled.
- Avoid shotgun edits across all templates. Change optional templates/skills
  only when they have a distinct contract to carry.

### Security / Privacy

- Do not weaken approval for security, authorization, privacy, destructive or
  permission-expanding work.
- Do not include secrets, private messages, production/customer payloads or
  sensitive tool output in artifacts, fixtures or handoffs.
- Temporary compatibility fixtures must use synthetic data.

### Reliability

- Route selection must preserve both false-negative safety (no material product
  change disguised as a repair) and false-positive efficiency (no new product
  spec for a clear-contract repair).
- Managed updates must preserve seeded and project-owned content under existing
  lifecycle rules and must not introduce unexpected `migration_required`.
- Existing explicit user approvals remain authoritative even when a route would
  otherwise be compressed.

### Performance

- Do not permanently expand always-loaded context without an explicit benefit.
- Keep the generated skill within its existing 300-word budget and generated
  `AGENTS.md` within its existing 800-word budget unless approval explicitly
  reconciles a demonstrated insufficiency.
- Keep detailed guidance on demand; reduce expected reads and repeated prose.

### Observability

- Material routing decisions must be auditable through a short statement of
  authority, classification, selected route, required gates and pending
  real-environment validation. Do not require a standardized section for
  trivial interactions or spend recurring tokens announcing an obvious route.
- Compatibility validation must make file lifecycle decisions and unexpected
  migration/conflict statuses visible.

### Simplicity

- Prefer prose contracts and behavior-oriented tests over a new routing DSL,
  numeric risk engine or mandatory artifact type.
- Use existing links, owners, templates and checkers before adding machinery.

## 9. Maintainability Impact

- Scoped audit evidence: the reusable generated audit inspected 12 candidate
  files covering compact guidance, detailed guidance, artifact templates and
  their principal tests.
- Findings and risk: one advisory `large-file-review` at
  `tests/test_template_pack.py` (`lines=510`, `bytes=23678`); no finding in the
  workflow sources or artifact-template directory.
- Required in-scope disposition: keep new scenario assertions organized around
  public routing outcomes; split or extract test helpers only if the approved
  implementation would otherwise worsen cohesion.
- Separate-spec or advisory disposition: the absent installed audit script and
  stale self-host state are retained as advisory self-hosting drift unless they
  block required validation. A broad self-bootstrap repair is out of scope.
- Does this change make future changes easier or harder? Easier if the route
  matrix has one detailed owner and compact surfaces only link/route to it;
  harder if the same matrix is duplicated across files or frozen through many
  exact prose assertions.
- Touched architecture: managed default-pack workflow templates, manifest
  version metadata and behavior-oriented template/generation compatibility
  tests.
- Potential entropy: divergent route descriptions, new artifact taxonomy,
  literal-prose test brittleness and stack-specific validation leakage.
- Refactor needed before coding: none established.
- Refactor scope: at most a local test organization improvement justified by
  the implementation; no separate refactor is approved by this spec.

## 10. Living Documentation Impact

- Product fact owner(s): `docs/product/README.md`, potentially a focused workflow
  owner only if planning proves the durable routing contract is too cohesive and
  detailed for the current product hub.
- Architecture fact owner(s): `docs/architecture/README.md` for the compact
  managed-routing versus on-demand-guide boundary.
- Potential exact owner paths, when known: `docs/product/README.md`,
  `docs/architecture/README.md`, `docs/CAPABILITIES.md`.
- Durable facts expected to be added: authority-first/two-axis route selection,
  clear-contract repair without automatic spec, progressive disclosure and
  proportional validation as generated behavior.
- Durable facts expected to change: the current generated workflow contract and
  pack evidence/version after validation.
- Durable facts expected to be removed and required disposition: remove the
  durable implication that every non-trivial task creates a spec; supersede it
  with classification-based routing rather than deleting approval discipline.
- Current capability state/evidence affected: “Bootstrap file application and
  upgrade” generated workflow behavior; current verified evidence remains until
  implementation and validation support replacement.
- Approved target and active change: after explicit spec approval, link this
  change as the approved target/active change without replacing current state.
- Roadmap or durable decisions affected: no roadmap/ADR required unless planning
  discovers a durable alternative with material consequences not already owned
  by this spec.
- Documents intentionally unchanged before approval: all living owners. In this
  first gate, only this temporal spec is created.

## 11. User Flow / System Flow

1. Read repository-local instructions and compact knowledge index if present.
2. Locate the narrow existing authority and active change, then inspect minimum
   supporting tests/code/runtime evidence.
3. Reason about behavioral novelty and execution risk; state the classification
   briefly only when it affects a material routing, gate, scope or validation
   decision.
4. Choose one of the six work routes and the smallest sufficient artifacts,
   gates, context and validation.
5. If a new/reconciled behavioral contract is needed, create only the spec and
   stop for approval.
6. If the contract is already clear, every non-trivial implementation still
   creates or reuses plan/tasks and stops for their explicit approval without
   manufacturing a product spec; only genuinely trivial, unequivocal low-risk
   work proceeds directly.
7. Implement only after applicable approval, preserving evidence and existing
   owners.
8. Validate from cheap/focused checks toward broader/real gates as justified.
9. Close the vertical slice by delta, distill only durable current facts and
   leave unavailable external gates visibly pending.
10. Hand off using approved artifacts and compact status rather than the
    conversation transcript.

## 12. Edge Cases

- A one-line code change introduces material observable behavior: it still
  requires a spec.
- A broad/high-risk repair restores an exact existing contract: it requires a
  detailed plan, tasks, second approval and broad validation without a new
  product spec.
- A test contradicts an approved product contract: the conflict is investigated
  rather than treating the test as automatic authority.
- Only code/runtime documents current behavior and no intent source exists: an
  ambiguity that affects behavior is specified rather than guessed.
- A bug is found during an active approved change: reconcile the existing
  artifacts if it is the same contract; reapprove only the materially changed
  gate.
- A repair points to a closed spec: link to it without rewriting history and
  create only the narrowest needed current record.
- A user explicitly requests read-only diagnosis: do not implement or infer
  permission from the diagnosis route.
- A user explicitly requests a compressed low-risk flow: preserve hard safety,
  permission and behavioral-novelty gates.
- An external provider/hardware/playtest is unavailable: retain the gate as
  pending and report local evidence separately.
- A repository has no `docs/INDEX.md`, Python, Rust, test suite or build command:
  use available authorities and detected/local commands; do not fabricate
  structure or commands.
- Managed workflow files in an upgraded project have local drift: existing
  lifecycle behavior must skip/preserve or explicitly update as designed, never
  conceal the conflict with force or reset seeded knowledge.

## 13. Constraints

- Work only in `/home/marco/slapy/projetos/ai_bootstrap` and `/tmp` fixtures.
- Do not alter real downstream projects.
- Correct template-pack sources, not generated downstream copies.
- Create no `plan.md` or `tasks.md` before explicit approval of this spec.
- After approval, create plan and tasks and stop again for explicit approval.
- Do not commit, stage, use `--force`, reset knowledge or overwrite unrelated
  local work.
- Preserve existing managed/seeded/project-owned semantics and one integrated
  workflow.
- Choose the next pack version consistently. Because this changes the generated
  behavioral contract rather than repairing `0.7.1` implementation, the
  proposed target is `0.8.0`; implementation evidence may challenge that choice
  only through explicit reconciliation.
- Treat the motivating downstream failure solely as a generic routing test.

## 14. Assumptions

- Existing prose templates and behavior-oriented tests can express the routing
  contract without a runtime classifier or new dependency.
- Existing plan/tasks/notes artifacts can represent a narrow repair when an
  audit trail is needed; no new artifact category is presumed necessary.
- The default pack's current lifecycle can update managed guidance while
  preserving seeded and project-owned content.
- Python and Rust temporary profiles exercise the available distinct stack
  rendering paths; they do not make the workflow stack-specific.
- Full source-suite and generated-project validation are available locally; real
  downstream mutation is neither needed nor permitted.

## 15. Acceptance Criteria

### Routing scenarios

1. A non-trivial feature route requires a new spec, explicit approval, plan and
   tasks, second explicit approval, then implementation.
2. A complex clear-contract bug locates and cites authority, preserves/adds a
   regression, creates no new product spec, and always requires proportional
   `plan.md`, `tasks.md` and their explicit approval before its non-trivial
   implementation, even when behavioral novelty is `none`.
3. Only a genuinely trivial, unequivocal and low-risk clear-contract bug uses a
   compressed flow; it creates no empty temporal artifact and receives focused
   regression/local validation.
4. A bug without a contract or with conflicting authority requires a new or
   reconciled spec and cannot be implemented before approval.
5. A P0/P1 found in an active change preserves evidence and required stop
   behavior, reconciles into the active scope for the same contract, and creates
   a new spec only for material novelty.
6. A repair tied to a closed historical spec does not rewrite history, links to
   the contract and creates only a narrow current record when necessary.
7. A behavior-preserving refactor does not automatically create a product spec
   and uses proportional audit/planning/validation.
8. A product change labeled as a bug is detected through novelty signals and
   requires specification/reconciliation.
9. A read-only investigation diagnoses and recommends a route without
   implementing or inferring write authorization.
10. A repository without structured living docs uses available README/tests/
    schemas/tickets/code and does not fail solely due to missing
    `docs/INDEX.md`.
11. A non-Rust/non-Python scenario in the guidance derives validation from
    local stack/instructions and contains no incorrect stack command. Temporary
    executable generation still covers at least two supported distinct stack
    profiles.
12. A handoff fixture or contract assertion proves that another agent can resume
    from compact active artifacts/status without receiving the conversation.
13. A standalone non-trivial clear-contract repair is represented consistently
    by `docs/changes/<repair>/plan.md` and `tasks.md`, followed by `notes.md` when
    evidence or closeout exists, without `spec.md`; its plan links the restored
    authority, declares no behavioral novelty and records reproduction, cause,
    boundary, risks, regression and validation. Fresh generation, `0.7.1`
    upgrade and documentation-check fixtures accept this format, while trivial
    bugs and read-only investigations create no repair directory.

### Distribution and compatibility

14. The required three template sources express a consistent contract; the
    detailed matrix has one owner and is not duplicated verbatim into always-read
    guidance.
15. `AGENTS.md` and the `spec-driven` skill stay within their existing 800- and
    300-word budgets. The detailed guide remains within its current 1000-word
    budget unless the approved plan demonstrates that the complete matrix
    cannot remain clear within it and reconciles a replacement budget before
    implementation.
16. No new artifact type, dependency or core lifecycle change is introduced
    without explicit evidence and approval reconciliation.
17. The pack version advances consistently from confirmed `0.7.1` to proposed
    `0.8.0`; manifest and version assertions agree.
18. Fresh temporary Python and Rust projects receive the intended generated
    content and select stack-appropriate commands/fragments.
19. A temporary upgrade fixture from `0.7.1` proves managed updates, reapply and
    managed-only behavior while preserving evolved seeded and project-owned
    files and producing no unexpected `migration_required`.
20. Manifest references, generated skill frontmatter, relative documentation
    links and aggregate documentation checks pass.

### Validation and closeout

21. Focused contract tests cover the routing and repair-artifact scenarios at behavior level
    without depending primarily on whole-paragraph literal matches.
22. Validation runs in ascending cost: focused template/routing tests, relevant
    generation/lifecycle tests, compileall or equivalent, documentation/link
    checks, full `ai_bootstrap` suite, and temporary fresh/upgrade projects.
23. Expensive validations are not repeated unless relevant inputs changed;
    commands and results are recorded reproducibly.
24. A critical post-implementation review checks for weakened gates, hidden
    product changes, duplicated guidance, stack assumptions, lifecycle
    regression, excessive always-read context and tests coupled to wording.
25. Closeout updates durable product/architecture/capability owners by delta,
    records pack evidence honestly, closes the approved checklist and leaves any
    unavailable gate pending rather than calling it passed.
26. `git diff --check` passes, no downstream file is changed, unrelated worktree
    content is preserved and no commit is created.

## 16. Open Questions

None currently block approval. The proposed `0.8.0` version, existing artifact
set and current word budgets are explicit spec decisions. If planning or
implementation evidence shows one is insufficient, stop and reconcile the
affected decision before proceeding.
