# Change Spec: Navigable Living Knowledge v1

- Status: `completed`
- Change: `navigable-living-knowledge-v1`
- Date: 2026-08-11
- Approved: 2026-08-11

## 1. Summary

Evolve the reusable default template pack so generated and upgraded projects
maintain three distinct documentation layers:

1. compact navigation from `docs/INDEX.md` through area hubs;
2. focused, linked owners for current product and architecture knowledge;
3. temporal evidence and history under `docs/changes/`.

The change makes navigability, baseline quality and organic closeout explicit
workflow outcomes. It adds objective regression gates where repository
structure can be checked safely, keeps semantic quality and concentration as
review responsibilities, and introduces a conservative project-owned baseline
for pre-existing closeout debt. It does not infer domain truth, rewrite evolved
owners or retroactively declare historical artifacts reviewed.

This specification is approved. It does not approve a plan or implementation;
those remain subject to the second explicit workflow gate.

## 2. Problem

The default pack already separates product, architecture, capabilities,
roadmap, decisions and changes, and pack `0.6.0` already tells agents to keep
READMEs compact, create focused owners for real responsibilities and distill
durable facts at closeout. The implemented gates do not yet make those outcomes
reliable:

- the generated product and architecture READMEs are both hubs and default
  detail owners, so continued appending remains the path of least resistance;
- `check_links.py` validates file targets outside `docs/changes/`, but it does
  not validate knowledge routes, owner authority or closeout artifacts;
- `check_living_docs.py` catches a small set of objective regressions, but not
  orphan focused owners, invalid capability owner routes, new undispositioned
  closeouts or baseline debt growth;
- `audit_repository.py` reports orphans, a combined size/concentration signal
  and completed changes without a recognized disposition, but findings remain
  advisory and its closeout grammar still accepts `follow-up`;
- concentration is currently reported only when route count and file-size
  thresholds are both crossed, which can miss a small mixed owner or many
  capability routes before the file becomes large;
- multiple scripts independently parse Markdown links, capability rows and
  closeout text, increasing drift risk as contracts become stricter;
- generated spec, plan and task artifacts do not yet carry enough exact owner
  and fact-disposition information to make closeout mechanically reviewable;
- there is no project-owned cutoff/inventory that distinguishes historical
  closeout debt from debt created after adoption of a stricter workflow.

The current repository demonstrates the migration problem. Seven completed
changes predate the `0.6.0` closeout marker and have no living-document
disposition. The completed `integrated-maintainability-knowledge-audit-v1`
change recorded these as accepted legacy advisory evidence, but no durable,
machine-readable project baseline prevents the backlog from growing. The
repository's `.ai-bootstrap/state.json` also records its last self-application
as pack `0.5.1`, while the source pack is `0.6.0`; therefore migration tests
must cover managed-policy advancement without treating preserved seeded owners
as stale scaffolds.

## 3. Goal

Generate a living-documentation workflow in which:

- a human or agent can start at `docs/INDEX.md` and discover current product
  behavior, architecture, capability state, evidence, decisions and known
  limitations without using `docs/changes/` as the normal reading path;
- product and architecture READMEs act primarily as compact area hubs while
  focused pages emerge only for real responsibilities;
- every durable fact has one current owner, with current state, approved target
  and aspiration kept distinct;
- change artifacts remain temporal contracts and evidence, not surrogate
  current documentation;
- a change cannot close with absent, pending or unjustified living-document
  disposition under the applicable post-baseline contract;
- existing historical debt stays visible and reducible without making an
  upgraded project immediately unusable;
- deterministic checks prove only objective structure and workflow invariants,
  while semantic truth, cohesion and completeness remain explicit review work;
- future humans and agents need less broad context to find or update one fact.

## 4. Scope

### 4.1 Navigation and current-knowledge structure

Revise the generated living-document policy, skill and scaffolds to establish:

- `docs/INDEX.md` as the canonical entry point and coverage-status owner;
- `docs/product/README.md` and `docs/architecture/README.md` as compact hubs
  that may temporarily own small cohesive baseline content but must route
  mature responsibilities to focused pages;
- organic focused pages based on a real capability, domain, flow, subsystem or
  cross-cutting responsibility, without a fixed domain taxonomy or empty-page
  generation;
- relative reachability from the index graph to every focused current owner;
- capability rows that route product contract and current architecture to the
  correct authority areas and link pertinent safe evidence;
- explicit unknowns and incomplete coverage rather than inferred intent;
- structural prevention of a change artifact being the only declared product
  or architecture owner of a current capability.

The pack must not require a separate page because a threshold was crossed.
Size, route count and mixed-content signals trigger review; cohesion and owner
responsibility determine whether a split is appropriate.

### 4.2 Authority model

Generated policy must keep these owners non-overlapping:

| Concern | Durable owner |
| --- | --- |
| Product purpose, what/why, expected behavior and rules | `docs/product/` |
| Current components, flows, persistence, integrations and operation | `docs/architecture/` |
| Current state, evidence, approved target and active change | `docs/CAPABILITIES.md` |
| Approved ordered outcomes only | `docs/ROADMAP.md` |
| Rationale and consequences that must outlive a change | `docs/decisions/` |
| Navigation, coverage status and baseline evidence | `docs/INDEX.md` |
| Stable cross-project terminology routing to its fact owner | `docs/GLOSSARY.md` |
| Temporal handoff, local decisions, notes and evidence | `docs/changes/` |

Cross-links may summarize context but must not create a second authoritative
copy. An approved target must not replace current behavior or evidence, and an
aspiration without approval must remain outside the current/approved contract.

### 4.3 Baselining and historical debt

Keep the existing coverage progression, but strengthen its meaning:

- `scaffold`: generated navigation and placeholders; no claim of project truth;
- `incomplete`: reviewed useful knowledge exists, known gaps are explicit and
  the normal reading path works for the covered responsibilities;
- `baselined`: a reviewer can navigate the documented current product and
  architecture, capability routes and evidence for the declared scope, with
  unknowns and exclusions stated. It does not mean exhaustive or permanently
  true.

Code, tests, safe runtime evidence and historical changes may support a
baseline. Code alone cannot establish product intent. Promotion must reconcile
conflicts, reject superseded designs, preserve unknowns and record the reviewed
scope/evidence rather than copying every historical artifact.

Add a seeded project-knowledge artifact at
`docs/LIVING_DOCUMENTATION_BASELINE.md`. Its generated state is an
unestablished scaffold; after review or editing it is protected by the existing
`seeded` lifecycle exactly like other evolved knowledge owners. It owns:

- the baseline status and evidence/cutoff contract used by documentation
  checks;
- an explicit inventory of pre-existing closeout debt that is grandfathered
  only from the prospective gate, not declared correct or reviewed;
- per-entry status sufficient to show unresolved, reduced or deliberately
  reviewed debt without editing the historical artifact;
- the rule that any completed change absent from that reviewed legacy inventory
  must satisfy the current closeout contract.

The bootstrap may generate the empty artifact and a read-only report or proposed
inventory, but ordinary apply must not populate debt entries, infer their
semantic disposition or mark them reviewed. A project without an established
baseline receives actionable setup guidance; strict historical enforcement is
not silently enabled. A fresh project establishes an empty legacy inventory as
part of its initial reviewed workflow baseline.

### 4.4 Organic change closeout

Strengthen generated spec, plan, task and note templates so that:

- every spec names potentially affected product, architecture, capability,
  roadmap, decision and navigation owners, including exact paths when already
  known;
- a spec distinguishes facts expected to be added, changed or removed from
  implementation details that belong in the later plan;
- plan and tasks record exact paths once discovery makes them known;
- closeout accounts for durable facts added, changed and removed, with explicit
  owner/disposition for each removal;
- living-document disposition is exactly `updated` or `no-update-needed`;
- `no-update-needed` requires a change-specific non-empty rationale;
- `pending`, `follow-up`, an absent field or generic rationale is not a valid
  closeout;
- unresolved documentation work prevents that change from being called closed;
  it is not converted into a valid disposition merely by linking a follow-up;
- capability current state/evidence advances only after implementation and
  relevant validation support it;
- durable rationale is promoted to a decision record when it must survive the
  change, without producing ADRs for trivial or easily reversible choices.

A targeted closeout mode must reject pending/absent disposition for the active
change. Repository-wide validation may ignore genuinely active, unchecked
changes, but must reject any newly completed change that is neither compliant
nor explicitly present in the established legacy-debt inventory.

### 4.5 Maintainability audit

Evolve the generated advisory audit and skill to report independent,
actionable signals for:

- many capability routes converging on one owner, independently of size;
- large current owners, independently of route count;
- likely mixed hub/detail responsibility using only conservative structural
  evidence;
- current owner pages unreachable from the canonical navigation graph;
- invalid or authority-incompatible capability routes;
- closeout debt relative to an established baseline;
- structurally detectable reliance on change artifacts for current capability
  ownership.

The audit must continue to return advisory findings rather than fail solely on
thresholds. Relevant findings must receive one workflow disposition:

- safe local cleanup;
- planned local refactor within this change;
- separate refactor spec;
- advisory observation with rationale.

The audit must not claim to detect semantically current prose trapped in changes
from keyword similarity, embeddings or another fragile content heuristic.
Outside objective route violations, this remains a guided human/agent review.

### 4.6 Validation surface

Add a stack-independent generated entry point at
`.agents/skills/living-docs/scripts/check_docs.py`. It is a thin aggregator,
not a fourth implementation of parsing rules. It must compose the existing
link and living-document checks, the objective portion of closeout/baseline
validation and advisory audit output where requested.

Shared Markdown-link, capability-route and closeout parsing must have one small
standard-library source used by the relevant scripts. The implementation plan
will select the lowest-complexity module boundary after validating standalone
generated-script execution; subprocess orchestration or copied parsers are not
acceptable substitutes for shared ownership.

Blocking checks are limited to objective contracts:

- broken/out-of-repository relative links and invalid supported fragments;
- focused current owners orphaned from the canonical graph;
- missing, malformed or authority-incompatible capability owner routes;
- invalid capability states and current/target regression invariants;
- placeholders incompatible with `incomplete` or `baselined` status;
- malformed baseline inventory;
- invalid closeout for a targeted change or new completed change after the
  baseline;
- disappearance or downgrade of protected current knowledge when an explicit
  comparison baseline is supplied.

Consultative output includes size, concentration, possible mixed ownership,
legacy debt and possible semantic truth trapped in changes. The aggregator must
not fail because a file exceeded a size/route threshold, and must not claim to
prove semantic completeness or veracity. Diagnostics must include path,
problem, severity and expected disposition/remediation.

`check_links.py` may retain its deliberately narrow responsibility if shared
parsing and the aggregator cover the broader contract. Existing direct command
compatibility must be preserved.

### 4.7 Template pack, lifecycle and migration

- Bump the default pack from `0.6.0` to `0.7.0`; the change adds backward-
  compatible workflow capability and generated artifacts without redefining
  lifecycle semantics or removing existing interfaces.
- Keep policies, skills and executable checks `managed` so explicit managed
  upgrades distribute the current workflow.
- Keep index, capability, product, architecture, roadmap, glossary and decision
  owners `seeded`.
- Add the baseline artifact as `seeded`, because the bootstrap creates its
  scaffold but reviewed content belongs to the project thereafter.
- Do not introduce a new lifecycle unless implementation planning proves the
  existing `managed`, `seeded`, `project`, `composed` and `migrated` contracts
  cannot express an approved requirement.
- Preserve evolved/untracked seeded owners on normal apply and `--force`;
  update only untouched seeds with trusted applied-content provenance.
- `--managed-only` may distribute policy/checker changes without touching
  owners, but must not pretend a missing baseline artifact is established.
- Preview, dry-run, apply and reapplication must distinguish managed updates,
  a newly offered baseline scaffold and preserved evolved knowledge.
- No migration may invent domain pages, facts, closeout dispositions or legacy
  review results.
- Existing obsolete-file migration behavior remains guarded; this change does
  not repurpose it for semantic Markdown migration.

Core lifecycle, planner, applier and state modules are compatibility surfaces,
not presumed implementation targets. They change only if the approved plan
demonstrates a missing generic contract. The default design uses existing
seeded protection and keeps documentation semantics out of core application.

### 4.8 Tests and self-hosting

Add focused contract tests for generated output, direct scripts and integrated
validation. Separate fixtures must cover:

- a fresh project with scaffold knowledge and empty historical debt;
- an existing clean project adopting `0.7.0`;
- an existing project with reviewed/evolved seeded owners;
- an existing project with known historical closeout debt;
- the self-host shape where state records `0.5.1` while a later source pack is
  applied conservatively.

Generation, preview, dry-run, real apply in temporary repositories,
reapplication, state provenance, manifest classification and managed-only
behavior must be covered where pertinent. Tests should assert public output and
workflow invariants rather than duplicate full prose or freeze parser internals.

At implementation closeout, update the `ai_bootstrap` living owners from
validated behavior, create focused product/architecture pages if their real
responsibilities now justify them, update navigation and capability evidence,
and record a durable decision only if the final rationale must outlive this
change. Run a critical post-implementation maintainability review before
declaring completion.

## 5. Out of Scope

- Reorganizing living documentation in downstream repositories now.
- Changing downstream product code or behavior.
- Automatically migrating content without semantic review.
- Deleting, compacting or rewriting `docs/changes/` history.
- Turning every change artifact into a living page.
- Retrofitting dispositions into historical tasks without reviewing them.
- Imposing Diátaxis, C4 or another external taxonomy.
- Requiring a separate page solely because of line count, byte count or route
  count.
- Claiming deterministic checks prove semantic truth, completeness or currency.
- Inferring product intent solely from implementation.
- Adding embeddings, a database, network service or third-party dependency.
- Changing secrets, credentials, private messages, production/customer data or
  sensitive payloads.
- Committing, staging, resetting or cleaning repository changes.

## 6. Users / Actors

- Project owners generating or upgrading a workflow.
- Humans and agents navigating and maintaining current project knowledge.
- Contributors specifying, implementing, validating and closing changes.
- Template-pack maintainers evolving lifecycle-safe reusable artifacts.
- Reviewers assessing baseline coverage, historical debt and durable decisions.

## 7. Functional Requirements

1. `docs/INDEX.md` remains the generated starting point and routes every
   canonical knowledge area.
2. Product and architecture READMEs explicitly operate as compact hubs and may
   retain detail only while it is one cohesive baseline responsibility.
3. Focused current owners are created only in response to reviewed project
   responsibilities; the bootstrap generates no domain-specific empty pages.
4. Every focused current owner is reachable by relative links from the
   canonical knowledge graph.
5. Every non-placeholder significant capability supplies valid product and
   architecture owner routes in their respective authority areas and safe
   pertinent evidence or an explicit evidence gap.
6. A change artifact cannot serve as the declared product or architecture owner
   of a current capability.
7. Product, architecture, capability, roadmap, decision, index and change
   authority remain separated as defined in section 4.2.
8. Current state/evidence, approved target and unapproved aspiration remain
   distinguishable.
9. Unknown facts and incomplete coverage remain explicit and are never filled
   from implementation evidence alone.
10. Coverage promotion follows the reviewed `scaffold` → `incomplete` →
    `baselined` semantics in section 4.3.
11. The generated baseline artifact starts unestablished and cannot grandfather
    historical debt until a reviewer records an explicit inventory/evidence.
12. Grandfathered debt remains visible as unresolved debt, can be reduced
    progressively and cannot grow implicitly.
13. Historical artifacts are not edited or marked reviewed by bootstrap
    application or deterministic checks.
14. Specs identify potentially affected durable owners and anticipated fact
    additions, changes and removals.
15. Plans/tasks record exact owner paths when known and closeout accounts for
    durable fact disposition.
16. Valid living-document closeout is `updated` or justified
    `no-update-needed`; `pending`, `follow-up`, absence and generic rationale are
    invalid for closure.
17. Capability current state/evidence advances only after implementation and
    relevant evidence exist.
18. Durable non-trivial rationale is evaluated for a decision owner.
19. Advisory audit signals separate size, route concentration and mixed-owner
    review rather than making size a prerequisite for concentration.
20. Each relevant audit finding receives one of the four dispositions in
    section 4.5 without silent scope expansion.
21. Deterministic detection of change-only current knowledge is limited to safe
    structural proxies; semantic suspicion is advisory.
22. `check_docs.py` composes existing checks through shared parsing/validation
    ownership and supports repository and targeted-closeout use.
23. Direct `check_links.py` and `check_living_docs.py` entry points remain
    compatible unless an explicitly documented migration is approved later.
24. Blocking and consultative findings follow section 4.6 and produce
    actionable path-based diagnostics.
25. New projects, upgraded clean projects and upgraded debt-bearing projects
    receive distinct, safe behavior.
26. Managed artifacts update only under existing consent rules; evolved seeded
    owners remain preserved.
27. No apply mode invents domain content, a baseline inventory or historical
    review result.
28. Pack version and state provenance accurately identify `0.7.0` application.

## 8. Non-Functional Requirements

### Modularity / Architecture

- Documentation semantics stay in generated skills/policies/checks, not in the
  generic planner/applier unless a reusable lifecycle gap is proven.
- Shared deterministic parsing has one cohesive owner and remains importable in
  freshly generated repositories.
- The aggregator composes checks and does not duplicate their rules.
- Skills divide responsibility: `living-docs` owns navigation, fact authority,
  baselining and distillation; `maintainability-audit` owns advisory signals and
  finding classification; `spec-driven` owns timing, approvals and closeout.

### Security / Privacy

- Checks inspect only repository-relative, non-sensitive paths and never emit
  file contents or secret values.
- Existing path traversal, symlink and sensitive-path protections remain.
- No network access or external service is needed.

### Reliability

- Outputs are deterministic for equal repository state and arguments.
- A malformed baseline fails actionably but does not authorize rewrite or
  deletion.
- Historical debt gating is prospective after explicit establishment, never
  inferred from timestamps alone.
- Existing direct check commands and lifecycle-safe reapplication continue to
  work.

### Performance

- Default validation remains repository-local, standard-library-only and
  bounded to Markdown/workflow artifacts required for the selected mode.
- Repo-wide advisory scanning remains explicit.

### Observability

- Every diagnostic includes path, stable problem code/category, blocking or
  consultative level, evidence safe to print and expected remediation or
  disposition.
- Summaries distinguish inspected scope from claims not evaluated.

### Simplicity

- No external dependency is added; existing standard-library mechanisms are
  sufficient.
- Always-loaded `AGENTS.md` and skill text remain concise; detailed examples and
  baseline procedure live in on-demand policy/help.
- The workflow adds no universal domain folder taxonomy.

## 9. Maintainability Impact

### 9.1 Scoped audit evidence

The generated pack auditor was run read-only against 38 relevant files:

```text
python ai_workflow_bootstrap/template_packs/default/templates/.agents/skills/maintainability-audit/scripts/audit_repository.py . \
  --path ai_workflow_bootstrap/template_packs/default/templates/docs \
  --path ai_workflow_bootstrap/template_packs/default/templates/.agents/skills \
  --path ai_workflow_bootstrap/template_packs/default/manifest.json \
  --path ai_workflow_bootstrap/core/lifecycle.py \
  --path ai_workflow_bootstrap/core/template_pack.py \
  --path ai_workflow_bootstrap/core/planner.py \
  --path ai_workflow_bootstrap/core/applier.py \
  --path ai_workflow_bootstrap/core/state.py \
  --path tests/test_lifecycle.py \
  --path tests/test_template_pack.py \
  --path tests/test_planner.py \
  --path tests/test_applier.py \
  --path tests/test_state.py \
  --path tests/test_living_docs_checker.py \
  --path tests/test_maintainability_audit.py --format json
```

It returned no encoded advisory finding. That clean scoped result does not
cover semantic ownership or prove repository-wide health. Manual inspection of
the same surfaces and existing historical audit evidence produced the findings
below.

### 9.2 Findings and dispositions

| Finding | Risk | Evidence | Disposition |
| --- | --- | --- | --- |
| Link, capability and closeout parsing is distributed across three scripts | Medium | `check_links.py`, `check_living_docs.py` and `audit_repository.py` each own overlapping Markdown/workflow parsing | Refactoring within this change: establish one small shared deterministic parsing boundary and thin entry points |
| Policy rules repeat across `AGENTS.md`, three skills, two policy guides and four change templates | Medium | The same hub, closeout and audit concepts appear with slightly different accepted values and timing | Refactoring within this change: define an authority matrix and keep always-loaded text terse; do not attempt to generate all prose from one source |
| Existing closeout grammar accepts `follow-up`, contrary to the requested closed-state contract | High | `_valid_living_disposition()` accepts `updated`, justified `no-update-needed` and justified `follow-up` | Cleanup local seguro within the approved implementation: narrow the closeout contract and update focused tests/templates together |
| Concentration requires both four routes and a large owner | Medium | `_concentration_findings()` gates on route count and `_is_large()` | Refactoring within this change: emit independent advisory signals and keep thresholds non-blocking |
| Current deterministic gates do not consume a historical-debt baseline | High | Seven completed pre-`0.6.0` changes have no disposition; only notes record their legacy status | Refactoring within this change: add the protected baseline artifact and prospective gate; do not modify those changes |
| Tests contain exact prose assertions across generated policies | Medium | `test_generated_workflow_integrates_audit_without_silent_scope_expansion` checks many literal fragments | Refactoring within this change: retain small rendering smoke assertions, move behavioral contracts to generated-repository fixtures and parser/check outcomes |
| Existing lifecycle boundary already protects evolved seeded owners | Low | Pure lifecycle matrix, planner provenance and application preflight are independently tested | Advisory observation: preserve this boundary and avoid documentation logic in core |
| Product and architecture owners in this repository remain central but currently small/cohesive for two capabilities | Low | Both capability rows route to the two READMEs; the index honestly marks coverage `incomplete` | Advisory observation: self-host closeout must reassess real focused owners, but this spec does not prescribe a split |
| `ai_workflow_bootstrap/tui.py` was previously recorded as a large unrelated source file | Low for this change | Existing completed audit notes route it as pre-existing debt | Separate spec if product work later requires a TUI refactor; no expansion here |

No broad pre-implementation refactor is required. The shared parser boundary,
closeout grammar correction and contract-focused test adjustment are directly
within this change. TUI/source modularization remains outside it.

### 9.3 Expected maintainability result

The change should reduce future context and shotgun surgery by giving shared
structural rules one implementation owner, making owner routes discoverable,
and ensuring every completed change either distills facts or explains why no
living owner changed. It must not centralize semantic policy in a large generic
checker: deterministic structure, advisory evidence and human/agent judgment
remain separate responsibilities.

## 10. Living Documentation Impact

### Product fact owners affected after approval/implementation

- `docs/product/README.md`: generated workflow contract and approved target;
- focused product owner(s) selected during planning only if a real navigable-
  knowledge responsibility warrants extraction.

### Architecture fact owners affected after approval/implementation

- `docs/architecture/README.md`: current template-pack, lifecycle and generated
  validation boundaries;
- focused architecture owner(s) selected during planning if shared parsing,
  generated checks or template-pack migration becomes its own durable boundary.

### Capability, navigation and policy owners affected

- `docs/CAPABILITIES.md`: current state/evidence remains unchanged until
  implementation validates the approved target; after spec approval it may
  record the target and active change under repository workflow;
- `docs/INDEX.md`: navigation/coverage only if focused owners or baseline
  evidence change at closeout;
- `docs/LIVING_DOCUMENTATION.md`: self-host policy when the managed template is
  applied/updated;
- `docs/GLOSSARY.md`: only if final implementation introduces stable terms that
  need disambiguation;
- `docs/ROADMAP.md`: only after approval, if the user orders this outcome;
- `docs/decisions/README.md` and a decision record: only if final blocking-versus-
  advisory, baseline or parser-boundary rationale needs durable ownership.

### Reusable generated owners affected

- default pack `living-docs`, `maintainability-audit` and `spec-driven` skills;
- `docs/LIVING_DOCUMENTATION.md`, `docs/INDEX.md`, product/architecture hubs,
  `docs/CAPABILITIES.md`, `docs/GLOSSARY.md` and decision templates;
- spec, plan, tasks and notes templates, plus `docs/SPEC_DRIVEN.md` only where
  workflow timing/details cannot remain solely in the skill;
- living-doc checks, advisory audit, new thin aggregator and shared parser;
- `manifest.json` classifications/version and relevant generated directories;
- lifecycle/application/state code only if planning proves a generic gap;
- generation, checker, audit, lifecycle, planner/applier/state and migration
  tests affected by the final design.

### Intentionally unchanged in this round

This draft does not update any living owner, capability target, roadmap,
decision, manifest, skill, template, script, code or test. It creates only this
temporal spec and awaits explicit approval.

## 11. User Flow / System Flow

### Fresh project

1. Bootstrap creates navigation hubs, current-owner scaffolds, managed policies
   and checks, and an unestablished empty baseline artifact.
2. A reviewer uses repository evidence and known product intent to mark useful
   coverage `incomplete` or a reviewed scope `baselined`.
3. Focused pages are created only as real responsibilities are documented and
   are linked from hubs/capabilities.
4. Each later change identifies affected owners, implements under both approval
   gates and passes targeted closeout validation.

### Existing clean project

1. Preview/dry-run shows managed workflow updates, a missing seeded baseline
   scaffold if applicable, and preservation of evolved seeds.
2. Apply updates only authorized managed/untouched-seed paths.
3. A reviewer establishes an empty or explicit legacy inventory from current
   repository evidence.
4. Prospective checks reject later closeout debt.

### Existing project with historical debt

1. Bootstrap preserves all evolved owners and historical changes.
2. Audit reports candidate legacy debt without changing it.
3. A reviewer records exact grandfathered paths as unresolved in the baseline
   artifact and states evidence/scope.
4. Repository validation passes with visible legacy advisory debt but rejects
   completed changes not in that inventory and lacking valid disposition.
5. Later review may reduce the inventory without rewriting history.

### Change closeout

1. The spec and approved plan/tasks identify exact durable owners.
2. Implementation and evidence determine whether current capability state may
   advance.
3. Durable facts are updated or explicitly judged unaffected; removals receive
   disposition; lasting rationale is evaluated for a decision.
4. The targeted aggregator validates links, routes, baseline and closeout, and
   presents advisory concentration findings for disposition.
5. Only `updated` or justified `no-update-needed` closes living documentation.

## 12. Edge Cases

- Repository is not a Git repository: baseline inventory and lifecycle still
  work; Git comparison is unavailable and reported, not fabricated.
- Existing project has no baseline artifact: tools report setup required and do
  not silently grandfather or fail the whole historical backlog.
- Baseline artifact exists but is malformed: validation fails actionably and
  never rewrites it.
- Historical change lacks tasks, uses an older template or has unchecked tasks:
  it is reported according to explicit inventory/status rules, not guessed
  closed from directory age.
- Active new change legitimately has `pending`: ordinary work may continue;
  targeted closeout fails until disposition is valid.
- `no-update-needed` uses boilerplate such as “no docs”: targeted closeout
  rejects a rationale that does not identify why durable owners are unaffected.
- Capability links to a valid file in the wrong authority area or to a change:
  route validation fails even though the file exists.
- Capability uses a heading fragment: validate it only under a documented,
  deterministic Markdown-anchor contract; unsupported ambiguous fragments get
  actionable guidance rather than silent success.
- Focused owner is linked only from another focused owner: it is valid if the
  whole route remains reachable from a canonical hub.
- One cohesive owner serves many capabilities: audit reports concentration;
  documented advisory disposition may retain it.
- One short owner mixes unrelated responsibilities: semantic audit may require
  separation even without a size signal.
- `--managed-only` upgrades tools but omits the seeded baseline: strict
  prospective enforcement remains unestablished and is reported clearly.
- Existing seed has missing/unusable provenance: preserve it conservatively.
- A baseline inventory path later disappears: report stale debt metadata for
  review; do not infer resolution.
- Sensitive or generated dependency paths are encountered: skip them without
  emitting contents.

## 13. Constraints

- Follow both explicit approval gates; this draft authorizes no plan or code.
- Preserve current lifecycle semantics and evolved seeded knowledge.
- Standard library only unless a later approved spec demonstrates necessity.
- Keep generated workflow vendor-neutral and stack-independent.
- Preserve direct script entry points and bounded output.
- Do not use automatic semantic migration or rewrite historical changes.
- No commit, stage, reset, cleanup or destructive Git/filesystem action.

## 14. Assumptions

- The existing `seeded` lifecycle is sufficient for a generated baseline
  scaffold that becomes protected project knowledge after review.
- Capability rows remain the canonical machine-readable routing surface.
- Exact legacy path inventories are more reliable than a timestamp-only cutoff
  because older change artifacts have inconsistent completion metadata.
- Projects may adopt managed tooling before establishing a baseline; tools must
  represent that state honestly.
- The current accepted decision separating advisory health from blocking
  regressions remains valid and should be extended, not reversed.

## 15. Acceptance Criteria

1. A fresh generated Python project contains understandable linked scaffolding,
   `Knowledge status: scaffold`, an unestablished empty baseline artifact and no
   domain-specific empty pages.
2. A fresh generated project can run the direct checks and aggregator with the
   standard library only.
3. Product and architecture scaffolds teach hub behavior, authority separation,
   focused-page triggers and explicit unknowns.
4. A generated focused owner disconnected from canonical navigation is detected
   with path and expected route.
5. A capability with a missing, wrong-area or change-artifact product/
   architecture owner is detected.
6. A valid capability route to focused product/architecture owners passes and
   remains reachable from `docs/INDEX.md`.
7. A current capability cannot use only historical change material as its
   declared current contract/architecture.
8. `incomplete`/`baselined` knowledge with incompatible seed placeholders is
   rejected; `scaffold` remains valid without pretending completeness.
9. A targeted closeout with absent or `pending` living disposition fails.
10. `follow-up` is not accepted as a closed living-document disposition.
11. `no-update-needed` without a change-specific rationale fails; a justified
    case passes.
12. A completed new change after baseline with no valid disposition fails
    repository validation.
13. An explicitly inventoried historical closeout remains visible as advisory
    debt without making the project unusable or declaring it resolved.
14. Removing one reviewed legacy-debt entry reduces the baseline count without
    modifying the historical artifact.
15. Adding unlisted debt after baseline is rejected.
16. Concentrated routing and large-owner signals are independent, actionable and
    advisory; neither fails solely because a threshold was crossed.
17. Relevant advisory findings require recorded workflow disposition at
    targeted closeout, while a justified cohesive owner may remain unsplit.
18. Deterministic checks do not claim semantic detection of current truth in
    changes beyond safe structural route violations.
19. `check_docs.py` composes shared rules without copied link/capability/closeout
    parsing and reports inspected scope.
20. Existing direct link and living-regression check commands still work.
21. A new project, clean existing project and historical-debt project have
    separate fixtures and expected outcomes.
22. A project with evolved seeded index/product/architecture/capability owners
    preserves them under preview, dry-run, apply, `--force` and reapplication as
    applicable.
23. Managed policies/checks update under existing consent, while managed-only
    adoption does not falsely establish the seeded baseline.
24. Manifest validation proves the baseline lifecycle, generated script paths,
    groups and pack version `0.7.0`.
25. Migration/state tests cover prior pack provenance, including the repository's
    `0.5.1`-state to `0.7.0` compatibility shape.
26. Current capability state/evidence is not replaced by the approved target
    before implementation evidence exists.
27. Generated `AGENTS.md` and skills stay within existing reviewed context
    budgets; detailed policy remains on demand.
28. No external dependency, domain taxonomy, automatic fact invention or
    sensitive output is introduced.
29. The `ai_bootstrap` product, architecture, navigation, capability and any
    warranted decision owners are updated only at implementation closeout from
    validated behavior.
30. Focused tests, manifest validation, fresh generation, preview/dry-run/apply/
    reapply checks, direct/aggregate document checks, link checks,
    `git diff --check` and the relevant complete suite pass.
31. A post-implementation critical review re-runs the proportional audit,
    verifies finding dispositions and confirms no new shotgun surgery, parser
    duplication or owner concentration was hidden.

## 16. Open Questions

These questions materially affect the implementation plan and remain open for
approval or later planning evidence:

1. What minimal syntax should `docs/LIVING_DOCUMENTATION_BASELINE.md` use so
   exact legacy paths/statuses are deterministic without turning a human owner
   into an opaque data file: a constrained Markdown table, a fenced structured
   block, or a small paired machine-readable artifact? The approved principles
   are seeded protection, explicit review and no timestamp-only cutoff.
2. Should supported Markdown fragments be validated using a deliberately small
   explicit-anchor convention, or should capability owner routes be file-level
   only? Reimplementing every renderer's implicit slug rules would be fragile.
3. Can the shared parsing boundary be a single generated Python module imported
   by all three scripts while preserving their direct execution in every
   generated layout, or is a small package/init adjustment required? This must
   be proven during planning before selecting paths.
4. What objective rule rejects generic `no-update-needed` rationale without
   pretending to judge prose quality? At minimum empty/placeholder/known generic
   values are invalid; broader semantic judgment may need to remain a reviewer
   responsibility.

The following design questions are resolved by this draft rather than left
open: closeout gates are prospective after an explicit path inventory; the
baseline owner is a protected seeded project-knowledge document; the aggregator
is a thin new script over shared rules; size/concentration remain advisory;
semantic “truth trapped in changes” is not guessed; hubs are enforced through
navigation/authority contracts rather than a universal taxonomy; the proposed
pack version is `0.7.0`; and existing projects adopt the workflow through
managed updates plus an explicitly reviewed seeded baseline.
