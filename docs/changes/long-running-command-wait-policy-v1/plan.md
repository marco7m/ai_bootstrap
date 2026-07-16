# Implementation Plan: Long-running command wait policy v1

## 1. Summary

Extend the generated agent contract with one stack-independent process wait
policy and one small conditional Rust clarification. Keep the behavior entirely
declarative in the default template pack, protect it with rendered-output
contract tests, increment the pack version, and close out the durable product,
architecture and capability owners after validation.

## 2. Relevant Existing Context

- `templates/AGENTS.md` is the managed base instruction surface generated for
  every supported stack.
- The template already reserves `$stack_agent_instructions` for conditional
  stack guidance.
- `templates/fragments/rust-agents.md` is selected declaratively by the default
  manifest only when the detected stacks include Rust.
- `core.planner` renders the base template and matching fragments; it needs no
  new behavior for this change.
- `tests/test_template_pack.py` already renders Python and Rust profiles and
  checks conditional policy isolation plus an `AGENTS.md` word budget.
- The default pack is currently version `0.5.0`.

## 3. Existing Conventions Found

- Folder structure: generated policy in
  `ai_workflow_bootstrap/template_packs/default/templates/`; behavior contracts
  in `tests/`; durable knowledge in `docs/`.
- Naming style: descriptive Markdown headings and unittest method names that
  state the protected contract.
- Error handling: not applicable; this change adds instruction text, not a new
  runtime failure path.
- Logging: no logging change.
- Testing pattern: render plans for small temporary Python/Rust profiles and
  assert stable semantic anchors rather than full-file snapshots.
- Config pattern: stack-conditional context fragments are declared in
  `manifest.json`.
- External integration pattern: none.
- Persistence/data access pattern: no persistence change.

## 4. Proposed Changes

### 4.1 Add the generic wait policy

Add a compact `Long-running commands` section to the base `AGENTS.md` template.
It will require agents to classify process behavior before choosing a wait
cadence and, for finite non-interactive commands, use the longest supported
wait targeting up to `300000 ms`, repeat a long wait when necessary, and avoid
short polling or model rounds whose only purpose is checking completion.

The same section will explicitly route servers, TUIs, debuggers and programs
requiring input or prompt observation to a responsive polling cadence. The
wording will describe `300000 ms` as a target bounded by tool support so it
remains executable across agent platforms.

### 4.2 Add conditional Rust examples

Extend `fragments/rust-agents.md` with one bullet stating that ordinary
non-interactive `cargo build`, `cargo check`, `cargo test` and `cargo clippy`
invocations follow the generic finite-command rule. State that commands such as
`cargo run` must instead be classified from the behavior of the launched
program, preserving the exception for servers and interactive programs.

Do not repeat the timing and polling policy in the fragment; the base template
remains its single owner.

### 4.3 Protect the generated contract

Add focused assertions to the existing Rust/Python rendering test or a nearby
dedicated test:

- both rendered profiles contain the generic classification, long-wait target,
  completion-only polling prohibition and interactive exceptions;
- only the Rust profile contains the four Cargo examples;
- the Rust wording does not classify `cargo run` unconditionally;
- the existing word-budget test continues to pass.

Assertions will use individual semantic anchors, not an exact paragraph
snapshot. No test of terminal timing is added because the bootstrap generates
instructions and does not execute or supervise these commands.

### 4.4 Version and knowledge closeout

Increment the default template-pack version from `0.5.0` to `0.5.1` so the
managed instruction change has an explicit upgrade version. Update the
manifest-version assertion.

After implementation evidence exists:

- update `docs/product/README.md` with the verified generated wait-policy
  contract;
- update `docs/architecture/README.md` with base-template versus conditional-
  fragment ownership;
- update `docs/CAPABILITIES.md` evidence, remove the approved target and active
  change, and retain `verified` only if validation passes.

The root generated `AGENTS.md`, `.ai-bootstrap/state.json`, downstream
repositories, Rust lifecycle document and project-owned instructions remain
unchanged.

## 5. Module Boundaries

- Default base template owns stack-independent process classification and wait
  cadence.
- Rust context fragment owns only Rust command examples.
- Default manifest owns the pack version and existing fragment selection.
- Planner/renderer own generic composition and must not learn command-specific
  polling rules.
- Scanner, applier, CLI, TUI and state must not know about this policy.
- Tests protect rendered public output rather than template placement details.

## 6. Architecture Locality

- Primary module or owner: default template pack.
- Files expected to change:
  - `ai_workflow_bootstrap/template_packs/default/templates/AGENTS.md`;
  - `ai_workflow_bootstrap/template_packs/default/templates/fragments/rust-agents.md`;
  - `ai_workflow_bootstrap/template_packs/default/manifest.json`;
  - `tests/test_template_pack.py`;
  - `docs/product/README.md`, `docs/architecture/README.md` and
    `docs/CAPABILITIES.md` during closeout;
  - this change's `tasks.md` as work is completed.
- Files that should not be touched: runtime engine modules, root `AGENTS.md`,
  `AGENTS.project.md`, Rust lifecycle documentation, user-owned dirty files and
  unrelated change artifacts.
- New boundaries introduced: none.
- Existing boundaries preserved: generic base template plus declarative
  stack-specific fragments.
- Why this is the smallest maintainable change: existing rendering and
  conditional-selection mechanisms already provide the required behavior.
- Are the affected files all part of the same conceptual area? Yes; templates,
  their rendered-output contract test and their durable knowledge owners.
- Does this change require edits across unrelated areas? No.
- If yes, is that expected or a sign of weak boundaries? Not applicable.
- Should we refactor before, during, or after this change? No. Maintainability-
  audit triggers are absent because ownership is clear and the change is local.

## 7. Data / API / Interface Impact

The generated `AGENTS.md` text is the only public interface change. There is no
Python API, CLI option, manifest schema, persistence or filesystem-ownership
change. Pack version `0.5.1` identifies the changed managed output.

## 8. Security / Privacy Impact

- This does not touch credentials, tokens, user data, permissions, network
  calls or runtime logs.
- No command output is copied into generated instructions or tests.
- Existing rules excluding secrets and sensitive payloads remain unchanged.
- No external input handling is introduced.

## 9. Dependency Impact

No dependency is needed. Existing templates, planner fixtures, `unittest` tests
and documentation checkers are sufficient. There is no runtime, build-time or
development dependency impact.

## 10. Risks

- Overly absolute timing wording could be impossible for tools with lower wait
  caps; mitigate with “longest supported” plus the five-minute target.
- Command-name classification could mishandle interactive tests or programs;
  mitigate by making observed process behavior authoritative.
- Repeating the generic rule in the Rust fragment could drift; keep timing and
  polling wording only in the base template.
- Adding standing context could make `AGENTS.md` noisy; keep the section compact
  and preserve the existing word-budget check.
- Updating current evidence before validation could misstate capability status;
  perform knowledge closeout last.

## 11. Validation Strategy

Validate the smallest rendered contract first, then the complete repository and
living-document structure. Inspect the final diff to ensure only approved
owners changed and pre-existing dirty files were preserved.

## 11.1 Test Strategy

- Contract to protect: generic wait guidance appears for every stack; Cargo
  examples appear only for Rust; interactive exceptions and tool-cap tolerance
  remain explicit.
- Tests to add or update: focused semantic-anchor assertions on rendered Python
  and Rust `AGENTS.md`; manifest version assertion; existing context word
  budget.
- Tests intentionally not added: real sleeping processes, terminal-tool mocks,
  scheduler/model-round tests and exact full-paragraph snapshots.
- Why these tests should survive internal refactors: they assert generated
  public behavior and conditional output, not the helper or file that produced
  it.

Validation commands:

1. `pytest tests/test_template_pack.py`
2. `pytest`
3. `python -m build`
4. `python .agents/skills/living-docs/scripts/check_living_docs.py`
5. `python .agents/skills/living-docs/scripts/check_links.py`
6. `python -m json.tool ai_workflow_bootstrap/template_packs/default/manifest.json`
7. `git diff --check`

## 12. Living Documentation Impact

- Product fact owner(s) to update: `docs/product/README.md`.
- Architecture fact owner(s) to update: `docs/architecture/README.md`.
- Current state/evidence changes: retain `verified` and extend evidence only
  after rendered-contract and full-suite validation succeeds.
- Approved target/active-change changes: already registered after spec
  approval; clear both at successful closeout.
- Roadmap/decision changes: none; this is a local extension of the existing
  generated instruction contract and conditional-fragment architecture.
- Links/evidence to validate: capability links, change link and all living-doc
  relative links.
- Why no living-doc update is needed, if applicable: not applicable; generated
  public behavior and its architecture ownership change durably.

## 13. Execution Steps

1. Re-read the approved spec and this plan; confirm the dirty worktree boundary.
2. Add behavior-level rendered-output assertions and update the expected pack
   version so the unimplemented contract fails narrowly.
3. Add the generic base-template section and conditional Rust examples.
4. Increment the default pack version to `0.5.1`.
5. Run the focused template-pack test and adjust wording only within the
   approved contract and word budget.
6. Run the full validation set.
7. Update product, architecture and capability owners from the resulting
   evidence; close the task checklist.
8. Run documentation checks and final diff review again after closeout edits.

## 14. Rollback / Recovery

Before closeout, revert only this change's template, fragment, version, test and
documentation edits; do not touch pre-existing dirty files. If validation
fails, leave the capability's current verified evidence intact and keep the
approved target/active change open. No data migration or state recovery is
required because the bootstrap runtime and persisted schema are unchanged.

## 15. Notes

The plan intentionally does not enforce five-minute waiting in Python code. The
bootstrap's responsibility is to generate the standing agent instruction; tool
platforms retain control over actual maximum wait durations and model-turn
scheduling.
