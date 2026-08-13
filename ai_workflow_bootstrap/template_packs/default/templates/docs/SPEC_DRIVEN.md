# Spec-Driven Workflow

This is detailed on-demand guidance. The `spec-driven` skill is the normal
operational entry point; `living-docs` owns durable current knowledge.

## Authority and classification before artifacts

Read local instructions, then start at `docs/INDEX.md` or another compact hub
when present. Locate the relevant current product contract, approved decision,
architecture, capability and active change; follow only links needed for the
next decision. Without structured living docs, use the best available README,
ADR, ticket, schema, API, invariant test, configuration, code or user-supplied
contract. Code/runtime proves what exists, not automatically what is intended.
Surface conflicts instead of choosing silently.

Reason about two independent axes:

- behavioral novelty: `none`, `partial` or `material`;
- execution risk: affected responsibilities, persistence, interfaces,
  security/privacy, concurrency, dependencies, reversibility, blast radius,
  deterministic regression and required real environments.

Do not use a numeric score. Expose the classification when it changes artifacts,
approval, scope or material validation; one sentence normally suffices. Do not
print a standard classification block for trivial questions or explanations,
and do not create a file merely to record it. Risk changes plan and validation
depth; it never removes the gate for non-trivial implementation.

## Routes

### New behavior or contract change

Create [spec.md](changes/_templates/spec.md), obtain explicit approval, create
[plan.md](changes/_templates/plan.md) and [tasks.md](changes/_templates/tasks.md),
obtain explicit approval of both, then implement.

### Clear-contract bug

Cite the authority, reproduce the defect proportionally and diagnose its cause.
A non-trivial repair uses approved plan/tasks but no new product spec. A truly
trivial, unequivocal, low-risk repair may flow directly with focused regression
and validation.

### Ambiguous bug or authority conflict

Do not guess. Preserve current behavior as evidence, create or reconcile a spec,
and obtain both gates before implementation.

### Behavior-preserving refactor or maintenance

Do not create a product spec automatically. Every non-trivial implementation
still needs approved plan/tasks and proportional audit/validation. Specify any
new responsibility, boundary, public contract or material decision.

### Trivial unequivocal work

Use direct/compressed flow only when work is also low risk. Create no empty
temporal artifacts; respect any approval explicitly required by the user.

### Read-only investigation

Locate authority, reproduce safely, explain cause and recommend a route. Do not
infer implementation permission or create change artifacts for a simple
diagnosis.

A “bug” becomes contract work when it adds an observable result, relaxed
validation, fallback, retry/cost, authority source, compatibility rule,
persisted data, access/privacy change or a choice among plausible behaviors.

## Gates and repair without a new spec

Every non-trivial implementation requires proportional plan/tasks and explicit
approval before coding, even with novelty `none`. Spec approval never approves
implementation; silence approves neither gate.

A standalone repair not covered by active artifacts uses
`docs/changes/<repair>/plan.md`, `tasks.md` and later [notes.md](changes/_templates/notes.md)
when evidence exists. It intentionally has no `spec.md`. The plan begins with a
link to the existing authority, declares novelty `none`, and records
Reproduction, Diagnosed cause, Repair boundary, risks, regression and
validation. Tasks are the approved checklist; notes hold material evidence,
deviations, limitations and closeout. If a new behavioral decision or conflict
appears, stop, create/reconcile a spec, approve it, then reapprove plan/tasks.

For a defect inside an active approved change, preserve evidence and reconcile
the existing plan/tasks when contract, approach, scope, risk and acceptance
remain covered. Reapprove material changes. Never silently rewrite a closed
historical change; link its contract and create only the narrow current repair
record when needed.

## Progressive context and artifacts

Search terms and links before opening whole files. Deepen context only for the
next decision; do not reread unchanged material without cause. Keep a compact
working map—objective, authority, active change, files, pending decision, gates,
evidence and blockers—inside existing artifacts when possible, never a mandatory
diary.

Each artifact answers one question: spec = what/why; plan = how; tasks = ordered
verification; notes = deviations/evidence/limits/result; living owners = current
durable truth; decisions = durable rationale among material alternatives. Link
instead of copying requirements. Prefer deltas; create no empty spec, plan or
notes and do not archive conversations.

## Maintainability, validation and stops

Audit proportionally when ownership is unclear, files are large, tests are
brittle or a small concept is scattered. Findings are advisory evidence:
perform safe local cleanup, plan an in-scope refactor, route separate work to an
approved spec, or accept the observation with rationale. Never expand approved
scope silently.

Validate in ascending cost: quick pure checks; focused regression/contract;
affected boundary integration; persistence/migration; relevant consumers;
proportional format/lint/type checks; broad suite when blast radius or closeout
requires it; real runtime/hardware/provider/playtest when it is an acceptance
gate. Use local stack instructions, fail fast, and do not repeat expensive gates
when relevant inputs are unchanged. Separate deterministic from real evidence;
leave unavailable external gates pending.

Stop for a new decision, authority conflict, material scope/risk/approach
change, destructive action/new permission or required P0/P1 playtest stop. Keep
incidental debt out unless it blocks acceptance, essential safety/correctness or
is inseparable from the repair.

## Compact handoff and closeout

A compact handoff contains only approved objective, authority links, current
state, next task, expected files, prohibitions, completed/pending validation and
worktree/evidence to preserve. Exclude transcripts, duplicated rationale,
irrelevant inventories and raw output when a reproducible summary suffices.
Resume from active artifacts and status, not the whole history.

At closeout account for durable facts added, changed and removed; update each
living owner once and preserve capability evidence until validation supports a
new state. Record exact audit scope and formal finding dispositions in tasks.
Run `check_docs.py . --closeout docs/changes/<change> --advisory`; only `updated`
or justified `no-update-needed` closes living docs. Validate links, close the
checklist and report behavior, evidence, pending gates and limitations.
