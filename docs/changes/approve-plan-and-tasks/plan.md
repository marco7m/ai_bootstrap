# Implementation Plan: Approval gate for plan and tasks

## 1. Summary

Update the repository's workflow instructions and their generated-template counterparts to add an explicit approval gate after planning, using the persisted change artifacts as the handoff contract between AI models.

## 2. Relevant Existing Context

- Repository-local guidance: `AGENTS.md`, `docs/SPEC_DRIVEN.md`, `docs/START_PROMPT.md`, and `.agents/skills/spec-driven/SKILL.md`.
- Generated-project guidance: matching files under `ai_workflow_bootstrap/template_packs/default/templates/`.
- `README.md` contains the concise public workflow sequence.
- The bootstrap engine copies template content; it does not interpret approval stages.

## 3. Existing Conventions Found

- Folder structure: source templates mirror the workflow docs generated for target repositories.
- Naming style: short imperative workflow rules and ordered lists.
- Testing pattern: focused `unittest` coverage for template presence and selected behavior; no tests currently assert full instructional prose.
- Config, persistence, external integrations: not involved.

## 4. Proposed Changes

1. Replace each short workflow sequence with the new plan/tasks approval stage.
2. Add a dedicated rule: implementation requires explicit approval of both `plan.md` and `tasks.md` after they are drafted.
3. Add concise handoff instructions allowing different assistants/models to own spec, planning, and implementation by reading the approved artifacts and current repository state.
4. Update README and start prompts to communicate the two approval moments.
5. Add focused text-presence tests only for the generated template artifacts that enforce the new contract.

## 5. Module Boundaries

- Documentation and skill files own workflow policy.
- Template files own what newly bootstrapped repositories receive.
- The Python engine, CLI, TUI, and state modules must not change because they do not enforce this conversational policy.

## 6. Architecture Locality Check

The affected files are distributed across source docs and their template mirrors, which is expected because they intentionally represent the same workflow at two layers. No architecture refactor is needed.

## 7. Data / API / Interface Impact

Generated instructions change. There is no runtime API, CLI, TUI, persistent-state, or file-selection change.

## 8. Security / Privacy Impact

No credentials, prompts, model identity, private conversations, or additional logs are introduced. Persisted change artifacts contain only the project documentation users already choose to create.

## 9. Dependency Impact

None.

## 10. Risks

- Source and template wording could drift.
- Overly rigid wording could block an explicitly requested fast path.
- An assistant could mistake spec approval for plan/tasks approval; the rules and tests must distinguish them.

## 11. Validation Strategy

- Add tests that load the generated `AGENTS.md`, `docs/SPEC_DRIVEN.md`, start prompt, and spec-driven skill templates and assert they contain the second-approval and artifact-handoff contract.
- Run the full `unittest` suite and a whitespace/diff check.

Do not snapshot full documents: prose snapshots would be brittle and would not add confidence beyond the contract phrases.

## 12. Execution Steps

1. Update repository-local instructions, skill, and README.
2. Mirror the rules in generated templates and prompts.
3. Add focused template-contract tests.
4. Run validation and confirm that no Python runtime modules changed.

## 13. Rollback / Recovery

Revert the documentation/template change. No migration or runtime recovery is required.

## 14. Notes

Artifact-based handoff is deliberately model-agnostic: it enables model changes without collecting or depending on model metadata.
