# Change Spec: Long-running command wait policy v1

## 1. Summary

Add generated agent guidance that distinguishes finite, non-interactive commands
from interactive or persistent processes. Agents should wait in long intervals
for finite work instead of repeatedly polling the terminal, while retaining
short polling when timely interaction is actually required.

## 2. Problem

Long compilations and validation commands can run for several minutes. Agents
currently receive no generated guidance about terminal wait cadence, so an
agent may repeatedly request process output at short intervals and create model
rounds whose only purpose is to learn that the command is still running.

This is especially visible with Rust commands such as `cargo build`, `cargo
check`, `cargo test` and `cargo clippy`, but the underlying problem applies to
any long-running, finite, non-interactive command. The opposite case also
matters: servers, TUIs, debuggers and other interactive programs need prompt
observation or input and must not inherit a long blind wait.

## 3. Goal

Generate a concise, tool-tolerant execution policy that minimizes unnecessary
terminal polling and model rounds for finite commands without reducing the
agent's ability to interact with live processes.

## 4. Scope

- Add a generic long-running command policy to the managed `AGENTS.md`
  template.
- Extend the conditional Rust agent fragment to identify ordinary non-
  interactive invocations of `cargo build`, `cargo check`, `cargo test` and
  `cargo clippy` as concrete examples of the generic policy.
- Add contract tests for generic generation, Rust-specific generation and
  non-Rust isolation.
- At closeout, update the durable product/capability knowledge that owns the
  generated instruction surface.

## 5. Out of Scope

- Changing the Codex terminal tool, API polling implementation, model scheduler
  or billing behavior.
- Detecting process interactivity automatically in bootstrap runtime code.
- Executing or supervising user-project commands from the bootstrap.
- Applying the bootstrap to downstream repositories as part of this change.
- Prescribing a fixed wait cadence for interactive or persistent processes.

## 6. Users / Actors

- Project owners generating agent instructions with `ai-workflow-bootstrap`.
- Coding agents running builds, tests, linters and other terminal commands in
  generated repositories.
- Developers who need responsive interaction with servers, TUIs and debuggers.

## 7. Functional Requirements

1. Generated `AGENTS.md` tells agents to classify a launched command before
   choosing a wait cadence:
   - finite and non-interactive; or
   - interactive, persistent, input-sensitive or otherwise requiring prompt
     observation.
2. For a finite, non-interactive command expected to take time, the generated
   guidance tells the agent to:
   - use the longest supported initial wait, targeting up to `300000 ms`;
   - avoid short-interval terminal polling;
   - if the process is still running, use another long wait;
   - avoid creating model rounds solely to check whether the process finished.
3. The wording must remain valid when an agent tool imposes a wait limit lower
   than `300000 ms`: the agent uses the longest supported wait rather than
   repeatedly requesting short waits.
4. The generic policy must explicitly exclude servers, TUIs, debuggers and
   programs that require interactive input or prompt observation.
5. For detected Rust projects, generated instructions must explicitly state
   that ordinary non-interactive `cargo build`, `cargo check`, `cargo test` and
   `cargo clippy` executions follow the finite-command policy.
6. The Rust examples must not classify all Cargo processes as non-interactive;
   in particular, an application launched through Cargo may be a server, TUI,
   debugger target or other persistent/interactive program.
7. Non-Rust projects receive the generic policy but no Rust-specific examples.

## 8. Non-Functional Requirements

### Modularity / Architecture

- The managed base `AGENTS.md` template owns the stack-independent decision
  rule.
- The existing Rust context fragment owns only Rust-specific examples and
  classification guidance.
- No scanner, planner, renderer or applier behavior changes are needed.

### Security / Privacy

- The guidance must not request storing or exposing command output, credentials
  or sensitive payloads.

### Reliability

- The rule must depend on process behavior, not command-name matching alone.
- Explicit exceptions must prevent long waits from making interactive sessions
  unusable.

### Performance

- The generated policy should reduce short terminal checks and model turns that
  perform no useful work while a finite process remains active.
- The policy must not promise that every tool can wait exactly `300000 ms`.

### Observability

- Normal compiler/test output remains available when the long wait returns.
- The change adds no runtime telemetry.

### Simplicity

- Keep the generated wording short enough to remain useful as standing agent
  context.
- Prefer one generic rule plus conditional examples over duplicating the full
  rule per stack.

## 9. Maintainability Impact

- Does this change make future changes easier or harder? Easier: it establishes
  one generic owner for wait cadence and keeps stack-specific classification in
  existing context fragments.
- Touched architecture: default template pack and its contract tests.
- Potential entropy: duplicated timing rules in stack fragments or brittle
  tests that assert the entire paragraph verbatim.
- Refactor needed before coding: no.
- Refactor scope: none.

## 10. Living Documentation Impact

- Product fact owner(s): `docs/product/README.md` for the generated agent-
  instruction contract.
- Architecture fact owner(s): `docs/architecture/README.md` for base-template
  versus conditional-fragment ownership.
- Current capability state/evidence affected: bootstrap file application and
  upgrade remains the current verified capability until implementation and
  validation provide new evidence.
- Approved target and active change: after spec approval, add this target and
  change link to `docs/CAPABILITIES.md` without replacing current state.
- Roadmap or durable decisions affected: no roadmap ordering or separate
  durable decision is currently required.
- Documents intentionally unchanged: Rust development lifecycle documentation,
  because it owns artifact and command lifecycle rather than agent polling.

## 11. User Flow / System Flow

1. The bootstrap renders `AGENTS.md` for a target repository.
2. Every generated repository receives the generic process-classification and
   wait-cadence rule.
3. A detected Rust repository also receives Cargo examples through the existing
   Rust context fragment.
4. Before running or waiting on a process, the agent classifies its interaction
   needs.
5. The agent waits in long intervals for finite non-interactive work, or uses a
   responsive cadence for interactive/persistent work.

## 12. Edge Cases

- A normally finite test command can prompt for input; actual observed or
  expected interactivity overrides its usual classification.
- A command can be quiet for a long time without being hung; silence alone does
  not justify short polling.
- A command launched through `cargo run` can be finite, persistent or
  interactive and must be classified by the launched program.
- A terminal tool may cap its initial execution wait below five minutes; the
  longest supported wait satisfies the intent.
- A process that exceeds the first long wait receives another long wait unless
  evidence indicates that interaction or diagnosis is needed.

## 13. Constraints

- `AGENTS.md` remains bootstrap-managed and within its tested word budget.
- `AGENTS.project.md` remains project-owned and is neither created nor changed.
- Existing uncommitted changes in `.ai-bootstrap/state.json` and
  `docs/LIVING_DOCUMENTATION.md` must remain untouched.
- Implementation must not add dependencies.

## 14. Assumptions

- Agents consuming `AGENTS.md` can choose among tool-supported wait durations.
- A behavioral instruction is the appropriate bootstrap boundary; exact
  enforcement belongs to the agent/tool platform and is outside this product.
- Five minutes is a target maximum for one finite-command wait, not a required
  delay after a process has already completed.

## 15. Acceptance Criteria

1. Generated instructions for every stack contain a concise rule to use the
   longest supported wait, targeting up to `300000 ms`, for long-running finite
   non-interactive commands.
2. Those instructions prohibit short-interval polling and model rounds used
   only to check completion, and direct another long wait when needed.
3. The generic rule clearly exempts servers, TUIs, debuggers and programs that
   require input or prompt observation.
4. Rust generation explicitly applies the rule to ordinary non-interactive
   `cargo build`, `cargo check`, `cargo test` and `cargo clippy` executions.
5. Non-Rust generation contains no Cargo-specific wording.
6. Contract tests protect the generic rule, Rust conditional behavior and the
   existing `AGENTS.md` word budget without coupling to a full paragraph.
7. The relevant test suite and living-document checks pass.
8. No unrelated files or user-owned dirty changes are modified.

## 16. Open Questions

None. The specification resolves the main design choice by using a generic
behavioral rule with conditional Rust examples.
