# Change Spec: Living Knowledge Base v1.1

## 1. Summary

Refine the v1 living knowledge base so the mandatory AI context is materially
smaller, every workflow fact has one source, capability state can represent a
verified current system and a planned evolution simultaneously, and freshly
generated documentation explicitly distinguishes an empty scaffold from a
trusted baseline.

This change also simplifies overwrite semantics. Explicit overwrite consent is
destructive: the bootstrap may replace declared generated files and remove
known superseded bootstrap files without creating backups. Recovery is the
user's Git responsibility.

This spec supersedes conflicting requirements in the
[v1 spec](../living-knowledge-base-v1/spec.md), especially the single capability
status, mandatory `AI_CONTEXT.md`, non-destructive legacy retention and backup
behavior.

## 2. Problem

The v1 knowledge structure is sound, but its surrounding workflow spends more
context than the project memory it is meant to optimize:

- generated `AGENTS.md` is about 1,985 words and is normally loaded
  automatically;
- it requires `docs/SPEC_DRIVEN.md`, about 2,368 additional words, for every
  non-trivial task;
- `SPEC_DRIVEN.md` embeds copies of templates that already have independent
  files;
- `AI_CONTEXT.md` repeats routing and stack facts already owned by the index and
  architecture;
- there is no enforceable context-size budget.

The capability table also uses one lifecycle status for two different facts.
A current capability may be verified while its next approved evolution is
planned, but one `Status` cell cannot express both without misleading an agent.

Finally, a fresh scaffold can look authoritative before anyone has populated or
reviewed it. When applying a new pack to an existing project, obsolete generated
documents may coexist with the new owners and create competing truth. The
existing backup system adds code, CLI surface and extra files even after the
user explicitly chose overwrite.

## 3. Goal

- Make the smallest normal orientation path cheap enough to read routinely.
- Preserve the two explicit spec-driven approval gates with one source for each
  workflow rule and artifact template.
- Represent current implementation truth separately from approved future work.
- Make documentation coverage explicit as `scaffold`, `incomplete` or
  `baselined`.
- Keep active maps compact as projects and their histories grow.
- Make relative-link validation deterministic and reusable.
- Make overwrite behavior simple, previewable and explicitly destructive.

## 4. Scope

### 4.1 Context and ownership reduction

- Reduce generated `AGENTS.md` to mandatory repository policy, approval gates,
  safety rules and navigation pointers.
- Stop requiring a full read of `docs/SPEC_DRIVEN.md` for every non-trivial
  task. The spec-driven skill becomes the concise operational procedure;
  `SPEC_DRIVEN.md` remains on-demand reference material.
- Remove embedded spec, plan, task and decision templates from
  `SPEC_DRIVEN.md`. The files under `docs/changes/_templates/` are their only
  owners.
- Keep the standalone change templates concise and complete enough to work
  without copied prose in the workflow guide.
- Update `START_PROMPT.md` and generated skills so they do not recreate the
  mandatory-read chain.
- Add loose word-budget contract tests for always-read/routing artifacts.

### 4.2 Entry point and baseline state

- Make `docs/INDEX.md` the only living-knowledge entry point.
- Stop generating `docs/AI_CONTEXT.md`; its routing belongs to the index and its
  detected technical facts belong to architecture.
- Add a compact knowledge status to the index:
  - `scaffold`: generated structure has not been populated and must not be
    treated as complete project truth;
  - `incomplete`: useful knowledge exists but known coverage gaps remain;
  - `baselined`: product intent and current architecture were reviewed against
    stated evidence.
- Add a baseline evidence field, normally a Git revision plus any relevant
  validation reference.
- Teach agents that code can establish current implementation but cannot alone
  establish intended product behavior; unresolved intent must be surfaced.

### 4.3 Capability model

- Replace the single status with separate current and future fields.
- The active capability map contains:
  - capability;
  - product contract;
  - architecture;
  - current state;
  - current evidence;
  - approved target;
  - active change.
- Current state uses only `unknown`, `absent`, `partial`, `implemented`,
  `verified` or `deprecated`.
- `verified` requires relevant safe evidence; `implemented` means the current
  implementation exists but is not yet fully validated.
- Approved future work is represented in `Approved target` and `Active change`
  without lowering or replacing the current state.
- Unapproved ideas stay in `IDEA_INBOX.md`; rejected or superseded intent keeps
  only a compact disposition or durable decision and does not remain in the
  active capability map indefinitely.
- The roadmap contains only approved outcomes and links their capability/change.

### 4.4 Deterministic maintenance

- Generate a standard-library-only link checker with the living-docs skill.
- The checker validates relative Markdown links in living knowledge, ignores
  external URLs and anchors, and avoids treating fenced examples as links.
- The generated skill runs the checker after structural/link changes rather
  than asking an agent to reason manually about every path.
- Add focused tests for the script and generated link contract.

### 4.5 Destructive overwrite and legacy cleanup

- Explicit CLI `--force` and the TUI overwrite selection authorize replacing
  differing declared generated files without backups.
- Remove automatic backup creation, the `--no-backup` option, backup-specific
  planner/applier state and obsolete backup code/tests/documentation.
- Existing `.bak-*` files are not searched for or deleted.
- Without overwrite consent, existing differing files remain skipped and no
  file is deleted.
- With overwrite consent and living docs enabled, preview and application may
  remove only this known superseded bootstrap set when present:
  - `docs/WORKFLOW_MODULES.md`;
  - `docs/PROJECT_SPEC.md`;
  - `docs/IMPLEMENTATION_STATUS.md`;
  - `docs/CANONICAL_DECISIONS.md`;
  - `docs/AI_CONTEXT.md`.
- Legacy deletion must appear explicitly in dry-run/TUI preview and final
  results before/after application; it must never be a hidden side effect.
- Spec-driven-only mode must not delete living-doc files.
- The bootstrap does not verify Git cleanliness or create a commit. Selecting
  overwrite is the user's confirmation that recovery is available through Git
  or is otherwise unnecessary.
- Source template files may be replaced or deleted normally; Git is their only
  recovery mechanism.

### 4.6 Documentation and versioning

- Update generated docs, README and repository workflow guidance to the new
  reading path, status model and overwrite policy.
- Increment the default template-pack version for the changed output contract.
- Keep CLI/TUI workflow choices and `.ai-bootstrap/state.json` format stable
  except for removal of internal backup-only fields that are not required in
  serialized state.

## 5. Out of Scope

- Populating or migrating the actual product knowledge of `text-online-mmorpg`.
- Automatically inferring intended product behavior from code.
- Deleting arbitrary or user-selected documentation paths.
- Deleting legacy files without explicit overwrite consent.
- Creating backup copies, Git commits, branches or stashes.
- Requiring a clean Git worktree before overwrite.
- Adding embeddings, RAG, a database or external documentation service.
- Supporting Wikilinks.
- Building a general Markdown parser or documentation framework.
- Automatically measuring API billing tokens with a provider tokenizer.

## 6. Users / Actors

- Project owners applying or updating the bootstrap.
- AI agents loading repository policy and task-relevant product/architecture
  knowledge.
- Contributors distinguishing current behavior from approved future work.
- Users explicitly selecting overwrite in CLI or TUI.

## 7. Functional Requirements

1. Fresh recommended and living-docs-only generation must use `INDEX.md` as the
   sole knowledge entry point and must not generate `AI_CONTEXT.md`.
2. The generated index must start as `scaffold` and explain that placeholders
   are not established project truth.
3. Agents must not promote the knowledge base to `baselined` without reviewing
   product intent, current architecture and stated evidence.
4. Generated `AGENTS.md` must preserve both approval gates without requiring
   `SPEC_DRIVEN.md` to be read on every non-trivial task.
5. `SPEC_DRIVEN.md` must point to standalone artifact templates and must not
   embed copies of them.
6. The spec-driven and living-docs skills must route to the smallest relevant
   context and preserve current/target separation.
7. The capability map must expose current state/evidence and approved
   target/change independently.
8. Approving a spec must add or update the approved target and active change;
   it must not replace a valid current state.
9. Implementation and validation may update current state only when repository
   and evidence support the transition.
10. Ideas and rejected history must not cause unbounded growth of the active
    capability map.
11. Roadmap entries must be approved outcomes, ordered and linked to their
    capability or active change.
12. The generated link checker must return success for the fresh core docs and
    failure for a broken local relative link.
13. Without overwrite consent, existing differing files must be skipped and
    known legacy files must remain untouched.
14. With overwrite consent, differing generated files must be replaced without
    `.bak` creation.
15. With overwrite consent and living docs enabled, known legacy files must be
    shown as deletions in preview and removed during application.
16. No mode may delete files outside the explicit known legacy set.
17. Spec-driven-only overwrite must not remove living-doc legacy files.
18. CLI help, TUI labels, README and result messages must describe destructive
    overwrite accurately and must not promise backups.
19. The obsolete `--no-backup` interface and backup implementation must be
    removed.
20. Existing generated workflow selection, dry-run behavior, overwrite opt-in
    and state recording must otherwise continue to work.

## 8. Non-Functional Requirements

### Token efficiency

- Generated `AGENTS.md` must contain at most 800 whitespace-delimited words.
- Generated `docs/SPEC_DRIVEN.md` must contain at most 1,000 words.
- Generated `docs/INDEX.md` must contain at most 250 words.
- Each generated operational skill must contain at most 300 words.
- Tests use word counts as a stable tokenizer-independent proxy, not exact API
  token counts.
- Core policy must not be duplicated merely to make each document standalone.

### Maintainability

- One workflow fact and one artifact template have one owner.
- Link validation is deterministic, dependency-free and separated from prose.
- Deletion behavior uses an explicit allowlist and a visible plan result.
- Do not retain dead backup parameters, flags, messages or tests.

### Reliability

- A verified current capability remains visible when a planned evolution is
  added.
- Scaffold documentation is never silently treated as complete.
- Dry-run and real apply must plan the same overwrite/deletion operations.
- Failed or skipped writes must not trigger unrelated deletions.

### Security / Privacy

- Existing prohibitions on secrets, private messages and sensitive runtime or
  production data remain.
- The link checker performs local filesystem reads only and does not follow
  external URLs.
- Destructive cleanup is restricted to project-relative allowlisted paths.

### Compatibility

- Removing `--no-backup` is an intentional CLI breaking change approved by this
  spec.
- Removing `AI_CONTEXT.md` is an intentional generated-output change.
- Existing user-created backup files and Git history remain untouched.

### Simplicity

- Prefer short Markdown, relative links and standard-library code.
- Do not add a migration framework or generic deletion configuration for this
  fixed legacy set.

## 9. User Flow / System Flow

### Fresh project

1. User applies recommended or living-docs-only mode.
2. Bootstrap creates the compact knowledge structure with status `scaffold`.
3. An agent starts at the index and gathers product intent plus implementation
   evidence.
4. After explicit review, it marks coverage `incomplete` or `baselined` and
   records baseline evidence.
5. Later changes update current and approved-target columns independently.

### Existing project without overwrite

1. Preview reports differing generated files as skipped.
2. No generated file is replaced and no legacy file is deleted.

### Existing project with overwrite

1. User explicitly selects `--force` or TUI overwrite.
2. Preview lists replacements and each allowlisted legacy deletion.
3. User confirms the TUI preview, or the CLI force invocation serves as direct
   confirmation.
4. Bootstrap replaces declared files and deletes listed obsolete files without
   creating backups.
5. Final results and state reflect the new generated set; Git remains the
   recovery mechanism.

## 10. Edge Cases

- A current capability is verified and has a planned v2: retain `verified` as
  current, describe v2 under approved target and link its active change.
- No current implementation exists: use `absent`, not `planned`, as current.
- Current behavior is not yet understood: use `unknown`; do not infer absence.
- A legacy file exists but living docs are disabled: preserve it.
- A legacy path is a directory or non-regular file: refuse that deletion and
  report it rather than recursively deleting it.
- A known legacy file is untracked or modified: explicit overwrite still
  authorizes deletion; no backup or Git check is performed.
- One write fails: surface the failure and do not claim successful cleanup or
  complete state. Exact ordering will be chosen in the implementation plan to
  minimize partial destructive results.
- The link checker encounters an external URL, anchor, fenced example or
  missing optional document not linked by the core: ignore non-local targets
  and report only actual emitted local broken links.
- An existing invocation passes `--no-backup`: parsing fails as an unsupported
  option after this breaking change.

## 11. Constraints

- Follow the current manifest/template-pack architecture.
- Preserve relative Markdown links.
- Preserve explicit spec approval and plan/tasks approval.
- Preserve `recommended`, `spec-driven` and `living-docs-only` selection.
- Do not stage or commit files automatically.
- Do not modify unrelated visible `docs/changes/` artifacts.
- Do not add dependencies.

## 12. Assumptions

- The user's statement that Git is the recovery mechanism authorizes removal
  of the backup feature rather than merely changing its default.
- Selecting overwrite authorizes deletion of the fixed superseded bootstrap
  paths when the corresponding living-doc workflow is enabled.
- `INDEX.md`, not `AI_CONTEXT.md`, is the intended long-term entry point.
- Word count is an acceptable regression proxy for context cost.

## 13. Acceptance Criteria

- All functional requirements are protected by focused contract tests or a
  documented validation check.
- The word budgets pass and the mandatory path no longer loads the full
  workflow manual.
- Standalone change templates are the only template definitions.
- A test demonstrates `verified current + planned target` without ambiguity.
- A test demonstrates scaffold generation and baseline guidance.
- The generated link checker passes valid docs and rejects a broken relative
  link.
- Tests demonstrate preserve-without-overwrite and visible-delete-with-overwrite.
- Forced overwrite produces no backup file.
- No backup flag, implementation, promise or stale test remains.
- Recommended, living-docs-only and spec-driven-only contracts still pass.
- README and generated instructions match actual behavior.
- Full unit tests, compile validation and diff checks pass.

## 14. Open Questions

None. Approval of this spec confirms the intentional removal of backups,
`--no-backup`, `AI_CONTEXT.md` and non-destructive retention of the known legacy
files when overwrite is explicitly selected.
