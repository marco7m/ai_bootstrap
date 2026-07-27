# Change Spec: Integrated Maintainability and Knowledge Audit v1

## 1. Summary

Evolve the generated `spec-driven + living-docs` workflow so non-trivial
changes receive a proportional maintainability audit of both code and project
knowledge. Deterministic checks will surface objective signals; the
`maintainability-audit` skill will interpret and prioritize them; `spec-driven`
will route in-scope work without silently expanding an approved contract; and
`living-docs` will preserve compact, linked, current knowledge at closeout.

## 2. Problem

The current bootstrap provides useful ownership, capability and regression
contracts, but it does not reliably drive projects toward a small-page,
wiki-like knowledge base as they evolve.

The generated maintainability skill focuses primarily on source files,
functions and tests. The spec-driven templates ask about maintainability and
living-document impact, but they do not establish when a scoped audit occurs,
how its findings are prioritized or what happens when a finding is outside the
approved change. The living-doc checker intentionally catches only objective
regressions, so it can pass while product or architecture knowledge accumulates
in large central owners, focused pages remain absent, durable decisions are not
extracted, or current understanding still depends on large historical change
artifacts.

Consequently, agents may keep appending to a few owner files even when real
responsibility boundaries already justify focused pages. Manual development is
also only reconciled when a later agent deliberately inspects the affected
area; no generated workflow tells that agent how to detect and route the
resulting documentation debt.

## 3. Goal

Generate a reusable workflow that:

- performs lightweight, scoped maintainability inspection before specifying,
  planning and closing non-trivial work;
- treats source maintainability and knowledge maintainability as two views of
  the same audit;
- detects objective repository and documentation health signals without
  pretending that size alone proves a defect;
- classifies findings by risk and appropriate remediation boundary;
- includes related findings in the current contract when appropriate and
  routes unrelated or broad work to a separately approved spec;
- incrementally evolves living docs toward compact, linked pages owned by real
  product, architecture, capability and decision responsibilities;
- reduces the amount of source and historical change material future humans
  and agents must read.

## 4. Scope

### 4.1 Generated maintainability audit

- Expand the generated `maintainability-audit` skill to cover both code and
  project knowledge.
- Make its triggering description include large or concentrated living
  documents, unclear knowledge ownership, missing focused pages, orphaned
  documentation and change artifacts that still carry current truth.
- Require each finding to include evidence, risk, relation to the current
  change and one remediation class:
  - safe local cleanup;
  - planned local refactor;
  - separate refactor spec;
  - advisory observation requiring no immediate change.
- Keep file length and byte size as review signals rather than hard
  correctness ceilings.

### 4.2 Deterministic health signals

- Add a reusable, stack-independent audit surface for cheap objective signals
  that can run on an explicitly scoped path set and, when deliberately
  requested, across a repository.
- At minimum, support evidence-backed signals for:
  - unusually large source or Markdown files;
  - living-document pages not reachable from the documented knowledge graph;
  - excessive concentration of distinct capability or architecture
    responsibilities in one large owner;
  - current capability routing that repeatedly depends on a large central
    owner instead of focused pages;
  - completed change artifacts that appear not to have completed their
    living-document closeout;
  - missing or placeholder knowledge ownership where substantive project
    material exists.
- Produce stable, concise, path-based output suitable for humans and agents.
- Do not print file contents, secrets, credentials, provider payloads or other
  sensitive data.
- Keep the existing living-document regression checker's hard-failure contract
  distinct from advisory maintainability signals. A size signal alone must not
  make the objective regression checker fail.

### 4.3 Spec-driven integration

- Before drafting a spec, inspect the smallest relevant area and use the audit
  when maintainability or knowledge-health triggers are present.
- After spec approval and before finalizing plan/tasks, use audit findings to
  choose module/knowledge owners and the smallest maintainable implementation
  boundary.
- At closeout, inspect the implemented diff and affected living-document
  owners for new or unresolved findings.
- Require the spec and plan to state the disposition of relevant findings.
- Preserve both approval gates. Findings discovered after approval must not
  silently expand the approved scope:
  - a necessary, small and directly related cleanup may remain local and be
    recorded;
  - a material in-scope change requires explicit contract reconciliation;
  - unrelated or broad refactoring is recorded as a separate-spec candidate;
  - an advisory signal may be accepted with rationale.

### 4.4 Living-document evolution

- Strengthen generated guidance so foundational index pages remain navigation
  hubs and detailed responsibilities migrate to focused product or
  architecture pages when cohesion warrants it.
- Require closeout to ask whether durable facts remain only in change-local
  specs, plans, tasks or notes.
- Require durable architectural/product rationale to be evaluated for a
  decision record without creating ADRs for trivial or reversible details.
- Preserve the one-fact/one-owner rule, current-versus-target separation and
  evidence requirements.
- Keep pages discoverable through relative links from the appropriate index,
  capability or decision owner.

### 4.5 Reusable bootstrap surface

- Update the default template pack, generated skills, workflow guidance,
  change templates and relevant managed agent instructions.
- Update this repository's canonical product, architecture, capability and
  decision owners at closeout.
- Increment the default template-pack version because generated managed
  behavior changes.
- Add contract tests and fresh generated-project validation for the revised
  workflow.

## 5. Out of Scope

- Automatically rewriting, splitting or deleting project documentation without
  agent judgment and normal approval boundaries.
- Running a background daemon, watcher, hosted service or automatic LLM call
  after every manual edit.
- Treating line count, byte size, heading count or number of files as an
  unconditional failure.
- Fully baselining an existing downstream repository during bootstrap
  application.
- Automatically inferring product intent solely from code.
- Reorganizing `text-online-mmorpg` as part of this repository change; it will
  receive the new generated workflow through a later bootstrap application and
  its own reviewed audit.
- Adding stack-specific AST analyzers, third-party complexity services or new
  runtime dependencies in this version.
- Replacing the existing spec, plan and tasks approval gates.

## 6. Users / Actors

- Project owners applying or upgrading `ai-workflow-bootstrap`.
- Agents specifying, planning, implementing and closing non-trivial changes.
- Human contributors whose manual changes are later reviewed by an agent.
- Future humans and agents navigating generated living documentation.
- The deterministic audit and living-document validation scripts.

## 7. Functional Requirements

1. The generated maintainability skill must explicitly audit code and living
   knowledge and must trigger on both implementation and documentation
   maintainability signals.
2. A non-trivial workflow must perform proportional inspection at specification,
   planning and closeout boundaries without requiring a full-repository audit
   for every change.
3. Findings must carry path-based evidence, risk and disposition, and must
   distinguish current-scope cleanup from separately approved refactoring.
4. Generated instructions must forbid silent expansion of an approved spec or
   plan in response to an audit finding.
5. Deterministic signals must be reproducible, concise and stable enough for
   contract testing.
6. The audit must distinguish blocking correctness/regression findings from
   advisory cohesion and size findings.
7. A large but cohesive file must be permitted when the audit records why
   splitting would not improve ownership or future retrieval.
8. A small file may still be reported when it mixes responsibilities, has
   unclear ownership or creates shotgun surgery.
9. Knowledge-graph checks must use repository-relative Markdown ownership and
   links rather than requiring external services.
10. Closeout must evaluate whether current truth has been distilled from
    temporal change artifacts into product, architecture, capability, roadmap
    or decision owners.
11. The generated workflow must tell agents how to handle manual uncommitted
    changes without assuming they were produced under the current spec.
12. Existing lifecycle-aware protection of evolved seeded documents must remain
    unchanged.
13. Existing generated Python and Rust workflows, conditional Rust guidance and
    project-owned path protection must remain compatible.

## 8. Non-Functional Requirements

### Modularity / Architecture

- Keep deterministic signal collection separate from semantic prioritization
  and scope decisions.
- Keep skills concise; repeated deterministic logic belongs in scripts.
- Preserve template-pack ownership as the source of downstream generated
  behavior.
- Do not duplicate detailed workflow prose across `AGENTS.md`, skills and
  documentation guides.

### Security / Privacy

- Ignore repository metadata, build/cache directories, binaries and known
  sensitive local files where applicable.
- Emit paths, measurements and finding codes, never file contents or secret
  values.
- Do not add network access or transmit repository material.

### Reliability

- Preserve the existing objective regression checks and link validation.
- Produce deterministic ordering and stable finding identifiers.
- Handle missing Git metadata, incomplete scaffolds and repositories with no
  source files without crashing.
- Avoid classifying an advisory signal as a blocker solely because a threshold
  was crossed.

### Performance

- The normal scoped audit must remain cheap enough to use during an ordinary
  non-trivial change.
- Full-repository scanning must be explicit and must skip common generated,
  cache and dependency trees.

### Observability

- Report the inspected scope, evidence, finding kind and whether the result is
  blocking or advisory.
- Make a clean result distinguish “no signals in inspected scope” from “area
  not inspected”.

### Simplicity

- Prefer standard-library implementation and repository-relative Markdown
  analysis.
- Avoid configuration machinery until a demonstrated project need requires
  configurable policy.
- Keep the common agent workflow short; detailed rationale belongs in
  on-demand guidance.

## 9. Maintainability Impact

- Does this change make future changes easier or harder? Easier: it makes
  documentation and code entropy visible at the points where scope can still be
  controlled and reduces future context retrieval.
- Touched architecture: default template-pack skills, managed workflow
  guidance, living-document validation/audit scripts, change templates and
  their contract tests.
- Potential entropy: overlapping instructions across four workflow owners,
  noisy heuristic findings and accidental conversion of advisory thresholds
  into rigid policy.
- Refactor needed before coding: none established; planning must inspect whether
  signal collection belongs beside the maintainability skill or the existing
  living-doc scripts while preserving the separation required above.
- Refactor scope: local to the default template pack and its tests unless
  planning evidence establishes a reusable core abstraction is necessary.

## 10. Living Documentation Impact

- Product fact owner(s): `docs/product/README.md`.
- Architecture fact owner(s): `docs/architecture/README.md`.
- Current capability state/evidence affected: bootstrap file application and
  upgrade remains currently verified; after approval this change adds an
  approved workflow-evolution target without replacing that evidence.
- Approved target and active change:
  `docs/changes/integrated-maintainability-knowledge-audit-v1/spec.md` after
  explicit approval.
- Roadmap or durable decisions affected: evaluate a durable decision for the
  hard-regression versus advisory-health boundary; roadmap entry is needed only
  while this approved outcome is active.
- Documents intentionally unchanged: existing completed change artifacts,
  project-owned instructions and downstream project knowledge.

## 11. User Flow / System Flow

1. An agent starts a non-trivial task and reads the repository knowledge index
   and relevant capability.
2. The agent inspects the smallest affected code and knowledge area.
3. Cheap deterministic checks surface objective maintainability and
   documentation-health signals for that scope.
4. The maintainability skill evaluates cohesion and ownership, assigns risk and
   disposition, and reports whether broader inspection is justified.
5. The spec records related required outcomes and explicit exclusions.
6. After spec approval, planning converts in-scope findings into concrete steps
   and routes broad or unrelated findings to separate-spec candidates.
7. After plan/tasks approval, implementation stays within that contract.
8. Closeout audits the diff and affected owners, distills durable facts,
   records justified advisory debt and runs objective regression/link checks.
9. A later manual change follows the same flow when an agent next inspects its
   diff; bootstrap itself does not silently rewrite documentation.

## 12. Edge Cases

- A long canonical vision document is cohesive and intentionally read only on
  demand.
- A short index page mixes navigation, architecture detail and product
  requirements.
- Many capabilities legitimately share one small overview page.
- Many capabilities point into different anchors of a central owner that has
  become costly to navigate.
- A Markdown page is intentionally historical and reachable only through a
  change artifact.
- A completed tasks checklist has an explicit, justified “no living-doc update”
  disposition.
- The repository has no Git history, has a dirty worktree or contains manual
  changes unrelated to the active spec.
- A seeded knowledge base is still a scaffold and therefore lacks focused
  pages.
- A file exceeds an advisory threshold because of generated data, a schema or a
  cohesive reference table.
- A finding appears only after implementation and would materially change the
  approved interface or architecture.
- A project has no durable decisions yet; absence alone must not fabricate an
  ADR.
- Paths contain spaces, non-ASCII characters or Markdown anchors.

## 13. Constraints

- Follow the repository's two explicit approval gates.
- Use only repository-local, safe evidence; do not infer intent from source
  alone.
- Preserve existing managed/seeded/project/composed lifecycle semantics.
- Keep generated skills within their established word budgets unless an
  explicitly justified budget adjustment is approved.
- Use Python standard-library facilities for deterministic scripts.
- The generated output must remain useful across supported stacks.
- Do not mutate or commit downstream repositories during validation.

## 14. Assumptions

- Most maintainability decisions require agent judgment; deterministic tooling
  should collect signals rather than replace that judgment.
- Repository-relative links and scoped filesystem evidence are sufficient for
  the first version.
- Existing projects will apply the newer managed workflow and then review their
  protected seeded knowledge under the new audit.
- A future CI or editor integration can invoke the deterministic surface, but
  such integration is not required for this version.

## 15. Acceptance Criteria

1. A freshly generated project instructs agents to audit both implementation
   and knowledge maintainability at proportional spec, planning and closeout
   boundaries.
2. The generated maintainability skill classifies findings into safe local
   cleanup, planned local refactor, separate refactor spec or advisory
   observation, with evidence and risk.
3. Generated spec/plan/tasks guidance records finding disposition and forbids
   silent expansion of approved scope.
4. A deterministic audit fixture reports an oversized living-document owner as
   an advisory review signal with stable path-based evidence and does not fail
   solely because of size.
5. A deterministic audit fixture detects an orphaned current-knowledge page or
   equivalent broken knowledge-graph ownership signal.
6. A fixture with multiple capability routes concentrated in a large central
   owner produces a review signal, while a small cohesive shared owner does not
   produce the same concentration signal.
7. A completed-change fixture with no durable closeout disposition produces a
   review signal; an explicitly justified no-update disposition does not.
8. Existing objective living-document regressions continue to return failure,
   while advisory health signals remain distinguishable and non-blocking.
9. Large cohesive/reference files can be explicitly accepted without requiring
   an automatic split or separate spec.
10. Audit output is deterministic, contains no file contents and safely skips
    common caches, generated artifacts and sensitive local paths.
11. Existing template-pack lifecycle, CLI/TUI, Python generation, Rust
    generation, project-owned path and two-approval-gate tests continue to
    pass.
12. New contract tests cover the revised skills, workflow templates,
    deterministic audit behavior and fresh generated-project surface.
13. Generated always-read instructions and triggered skills remain within
    reviewed context budgets.
14. The default template-pack version is incremented and its manifest/tests
    agree.
15. This repository's current product, architecture, capability, roadmap and
    decision owners are reconciled at closeout with links validated.

## 16. Open Questions

None blocking spec approval. Planning must choose the smallest script ownership
that satisfies the required separation between objective regression gates,
advisory signal collection and semantic prioritization.
