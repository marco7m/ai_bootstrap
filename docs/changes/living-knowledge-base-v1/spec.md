# Change Spec: Living Knowledge Base v1

## 1. Summary

Replace the bootstrap's placeholder living-docs scaffold with a reusable,
linked knowledge base that distinguishes product intent, technical
architecture, delivery status, roadmap, decisions and change history.

The generated documentation must help humans and AI agents understand a
project through progressive disclosure instead of requiring a monolithic
specification or repeated code exploration. Relative Markdown links are the
portable linking standard for this version.

## 2. Problem

The current living-docs templates name useful categories but do not define a
usable knowledge model. `PROJECT_SPEC.md`, `IMPLEMENTATION_STATUS.md`,
`WORKFLOW_MODULES.md` and `CANONICAL_DECISIONS.md` are isolated placeholders,
ownership between documents is unclear, and the generated workflow does not
connect approved intent to implementation and validation status.

As a result, a project can still require one large temporary specification or
repeated code reading to answer:

- what the product is and how it is expected to behave;
- how the architecture currently realizes that behavior;
- what is current, planned, partial, implemented or verified;
- why an important product or architecture decision was made;
- which change and evidence support a capability;
- what an agent should read first and what it should load only on demand.

Without explicit current-versus-target classification, an agent may also
mistake planned behavior for a current bug contract or treat an implementation
detail as intended product behavior.

## 3. Goal

Generate a compact, modular and navigable project knowledge base that:

- separates product (`what` and `why`) from architecture (`how`);
- provides one short entry point and on-demand navigation;
- connects capabilities to their product contract, architecture, lifecycle,
  active change and implementation evidence;
- records important decisions without turning change history into current
  truth;
- integrates living-document updates with spec approval, implementation and
  validation;
- remains portable across repositories, editors and AI coding agents;
- reduces long-term context discovery while keeping documents trustworthy.

## 4. Scope

- Redefine the default `living-docs` template-pack output around:
  - `docs/INDEX.md`;
  - `docs/AI_CONTEXT.md`;
  - `docs/LIVING_DOCUMENTATION.md`;
  - `docs/CAPABILITIES.md`;
  - `docs/product/README.md`;
  - `docs/architecture/README.md`;
  - `docs/decisions/README.md`;
  - `docs/decisions/_template.md`;
  - `docs/ROADMAP.md`;
  - `docs/IDEA_INBOX.md`;
  - `docs/GLOSSARY.md`.
- Use relative Markdown links as the generated cross-document link format.
- Define document ownership, authority, progressive reading and splitting
  rules in the living-documentation policy.
- Define the capability lifecycle vocabulary: `idea`, `planned`, `partial`,
  `implemented`, `verified`, `deprecated` and `rejected`.
- Make `CAPABILITIES.md` the owner of delivery status and the router between
  product, architecture, change artifacts and evidence.
- Keep `AI_CONTEXT.md` short and use it as a routing summary rather than a
  duplicate project specification.
- Teach the generated `living-docs` skill how to classify, read, create, split
  and update knowledge without transcribing conversations.
- Integrate the generated spec-driven workflow with the living-doc lifecycle:
  - approved intent becomes `planned`;
  - partial delivery becomes `partial`;
  - present code becomes `implemented` only when the implementation exists;
  - validated behavior becomes `verified` only after relevant evidence;
  - abandoned or superseded intent is updated explicitly.
- Add living-document impact and ownership prompts to generated change
  artifacts where they prevent documentation drift.
- Update generated agent instructions, workflow documentation, start guidance,
  public README and the bootstrap repository's relevant workflow documentation
  so they describe the same contract.
- Replace legacy living-doc outputs for fresh bootstrap applications without
  deleting them from repositories that already contain them.
- Remove the source repository's `docs/changes/` ignore rule so current and
  future spec/plan/task handoff artifacts are visible to Git and can be
  versioned normally.
- Add focused contract tests for generated file selection, core content and
  relative-link integrity.

## 5. Out of Scope

- Migrating `SPEC_V2.md` or any other existing project's large specification.
- Automatically deriving product or architecture truth from source code.
- Automatically deleting, renaming or rewriting legacy documents in an
  existing target repository.
- Automatically staging or committing change artifacts, or rewriting Git
  history for previously created artifacts.
- Adding a vector database, RAG pipeline, embeddings or external documentation
  service.
- Adding a diagram generator or requiring C4, arc42, Diataxis or ADR tooling.
- Adding a generic documentation linter to the production package.
- Adding Wikilink syntax or an alternate link-format configuration in v1.
- Changing CLI flags, TUI flows, bootstrap state schema, overwrite/backup
  behavior or workflow selection modes.
- Changing `bootstrap_sdd.py` behavior.
- Adding dependencies.

## 6. Users / Actors

- Project owners who need a readable description of product behavior,
  architecture, current delivery and future direction.
- AI coding agents that need fast, reliable project orientation before making
  or reviewing changes.
- Contributors joining an existing repository.
- Assistants or models taking over different spec, planning, implementation or
  validation phases.
- Bootstrap users applying only living docs or the recommended combined
  workflow to a new or existing repository.

## 7. Functional Requirements

1. A fresh bootstrap with living docs enabled must generate the core knowledge
   structure listed in Scope.
2. `docs/INDEX.md` must be the human and agent entry point and link to every
   core knowledge area using relative Markdown links.
3. `docs/AI_CONTEXT.md` must remain a compact routing summary and must tell an
   agent to load detail on demand rather than duplicate it.
4. `docs/product/README.md` must own product purpose, users, behaviors,
   invariants, boundaries, non-goals and links to product-system documents.
5. `docs/architecture/README.md` must own the current technical shape, module
   responsibilities, important flows, constraints and links to deeper
   architecture documents.
6. Product and architecture guidance must clearly distinguish current behavior
   from approved target behavior whenever both exist.
7. `docs/CAPABILITIES.md` must define and use a compact mapping containing at
   least capability, product contract, architecture, status, active change and
   evidence.
8. Status must use only `idea`, `planned`, `partial`, `implemented`, `verified`,
   `deprecated` or `rejected`.
9. `canonical` must describe document authority, not delivery status. Each
   durable fact must have one owning document; other documents link to it
   instead of maintaining competing copies.
10. `docs/decisions/README.md` must index durable decisions. The decision
    template must capture context, decision and consequences without requiring
    one file per trivial choice.
11. Change specs, plans and tasks must remain temporal delivery contracts. At
    completion, agents must distill durable facts into their living-doc owners
    rather than treating `docs/changes/` as the primary current-product view.
12. The generated workflow must require agents to register approved future
    behavior as `planned`, then update implementation and verification status
    only when the corresponding stage is supported by evidence.
13. The generated workflow must require a plan to identify affected living-doc
    owners and require tasks to update them after the relevant facts are known.
14. The generated living-docs skill must instruct agents to start from the
    index, read the smallest relevant document set, preserve single ownership,
    use relative links, split mixed or oversized documents, and flag conflicts
    between documentation and repository evidence.
15. Relative links between generated core documents must resolve in a freshly
    generated repository.
16. The living-docs-only and recommended modes must generate the new living
    structure and living-docs skill. Spec-driven-only mode must continue to
    exclude them.
17. Fresh generation must stop producing `docs/WORKFLOW_MODULES.md`,
    `docs/PROJECT_SPEC.md`, `docs/IMPLEMENTATION_STATUS.md` and
    `docs/CANONICAL_DECISIONS.md`; their responsibilities move to the new
    structure.
18. Applying the new pack to a repository that already has legacy files must
    not delete those files. Existing skip, force and backup behavior remains
    authoritative.
19. Optional detailed product or architecture documents must be proposed or
    created only when a real responsibility has enough content; the bootstrap
    must not create a large empty hierarchy.
20. README and repository workflow docs must accurately describe the generated
    knowledge base and its lifecycle.
21. The source repository's `.gitignore` must no longer ignore
    `docs/changes/`, while all unrelated ignore rules remain unchanged.
22. New change artifacts must appear in ordinary Git status/add flows without
    requiring `git add -f`; the bootstrap must not stage or commit them
    automatically.

## 8. Non-Functional Requirements

### Maintainability

- Prefer one fact owner plus links over mirrored prose.
- Keep always-read guidance short and stable.
- Keep the generated skill concise and procedural; do not add reference files,
  scripts or assets unless implementation proves they are necessary.
- Test behavioral contracts and generated structure, not full prose snapshots.

### Modularity / Architecture

- The default template pack owns generated file structure and content.
- The generated living-docs skill owns the reusable agent procedure.
- Generated spec-driven instructions own approval and delivery-stage behavior.
- The planner, applier, CLI, TUI and state modules remain independent of
  documentation semantics.

### Security / Privacy

- Templates must prohibit secrets, credentials, private message history,
  production data and other sensitive payloads in living docs.
- Evidence links must point to safe repository artifacts and must not encourage
  copying sensitive runtime payloads into documentation.
- No external service or network call is introduced.

### Reliability

- A planned capability must not be described as verified current behavior.
- `verified` requires explicit relevant validation evidence.
- If documentation and code/tests/runtime disagree, agents must surface the
  conflict and establish whether the implementation or documentation is stale
  before changing behavior.
- Existing non-destructive bootstrap semantics must be preserved.

### Performance

- No runtime performance impact.
- The reading model must reduce default context by loading only routing and
  task-relevant knowledge.

### Observability

- The capability map exposes delivery state, active change and evidence.
- Decision records preserve rationale and consequences.
- Bootstrap previews and state continue to expose generated files through the
  existing mechanisms.

### Simplicity

- Use Markdown files, relative links and the existing template-pack engine.
- Do not introduce a documentation framework, database or background process.
- Generate only foundational files; grow domain modules on demand.

## 9. User Flow / System Flow

1. A user applies the recommended or living-docs-only bootstrap.
2. The bootstrap generates a short index, foundational product and architecture
   pages, the capability map, decisions area, roadmap, inbox, glossary and the
   living-docs skill.
3. A human or agent starts from `docs/INDEX.md` or the compact AI router.
4. It follows relative links to only the product, architecture, capability or
   decision material relevant to the task.
5. A new idea remains non-canonical in the inbox.
6. After explicit spec approval, the intended capability becomes `planned` and
   links to its change contract.
7. The implementation plan identifies which living-doc owners will eventually
   change; the task checklist makes those updates explicit.
8. Implementation updates the capability only to the state supported by the
   repository.
9. Validation records safe evidence and promotes the capability to `verified`
   when the approved contract passes.
10. Durable product and architecture facts are distilled into their owning
    pages; change artifacts remain as history and handoff evidence.

## 10. Edge Cases

- A repository already contains one or more legacy living-doc files: the
  bootstrap creates missing new files under normal rules but does not remove
  legacy files.
- A new generated file already exists with user content: existing skip/force
  and backup behavior applies unchanged.
- A capability is partly delivered: it remains `partial`, with current and
  target behavior stated separately.
- Code exists but has not been validated: use `implemented`, not `verified`.
- A verified capability regresses: preserve the intended product contract,
  lower or annotate evidence/status as appropriate, and treat the mismatch as
  a bug or stale-document investigation.
- An approved change is abandoned: mark the capability `rejected` or restore
  the appropriate prior state instead of leaving it `planned` indefinitely.
- One document accumulates several unrelated systems: split it into focused
  pages and update its index rather than growing a new monolith.
- Two documents claim ownership of the same rule: select one owner, replace the
  duplicate with a relative link and note any unresolved conflict.
- Product behavior has no known implementation evidence yet: leave the
  evidence field empty or explicitly unavailable; do not invent a link.
- A relative link targets an optional page that does not exist: do not emit the
  link until the page is created.
- Removing the source ignore rule exposes other previously untracked change
  folders: inspect them before staging and never add unrelated artifacts
  automatically.

## 11. Constraints

- Follow the existing template-pack manifest and workflow groups.
- Preserve `recommended`, `spec-driven` and `living-docs` selection behavior.
- Preserve current planner/applier skip, force, backup and state semantics.
- Keep spec, plan and task artifacts versionable as the repository's cross-agent
  handoff contract.
- Keep generated files AI-agnostic and editor-portable.
- Use English in default templates, matching the current pack.
- Use relative Markdown links, not absolute filesystem links or Wikilinks.
- Do not require every document to be read for every task.
- Do not modify `bootstrap_sdd.py` for this change.

## 12. Assumptions

- Markdown-relative links provide sufficient navigation in GitHub, common
  editors and Obsidian.
- Project-specific domain decomposition cannot be known by the generic
  bootstrap and should grow from the foundational indexes.
- The bootstrap can safely change the fresh-install file set while preserving
  existing repositories through its current non-deletion behavior.
- A compact capability map is sufficient to route agents; it does not need to
  become a machine-readable database in v1.
- The current engine can create the required directories and render the new
  templates without production-code changes.

## 13. Acceptance Criteria

1. A dry-run of the recommended workflow includes every new core living-doc
   file and directory from Scope.
2. A living-docs-only dry-run includes the same living-doc structure and skill
   while excluding spec-driven artifacts.
3. A spec-driven-only dry-run excludes the living-doc structure and skill.
4. Fresh generation no longer includes the four superseded legacy living-doc
   outputs.
5. No bootstrap operation automatically deletes a pre-existing legacy file.
6. Generated core documents have clear, non-overlapping ownership and resolve
   their relative cross-links.
7. Product and architecture templates explicitly distinguish current and
   target state when necessary.
8. The capability template contains the approved lifecycle, routing columns
   and evidence guidance.
9. Generated AGENTS/workflow/skills/change templates implement the approved
   living-doc lifecycle and progressive-reading policy.
10. `AI_CONTEXT.md` remains a compact router rather than a duplicate product or
    architecture document.
11. Decision guidance captures context, decision and consequences and links
    decisions from an index.
12. Focused tests verify manifest integrity, workflow-mode selection, core
    knowledge contracts and relative-link resolution without snapshotting full
    documents.
13. README and relevant repository workflow documentation match the generated
    behavior.
14. No CLI, TUI, state schema, dependency or bootstrap runtime behavior changes.
15. The full unit-test suite, Python compilation check and diff/whitespace
    checks pass.
16. `.gitignore` no longer ignores `docs/changes/`, new change artifacts appear
    in normal Git status, and unrelated ignore behavior remains intact.

## 14. Open Questions

None. Relative Markdown links and non-destructive legacy handling were approved
before planning.
