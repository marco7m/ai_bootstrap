# Tasks: Living Docs Downstream Compatibility v1

- Status: `completed`

## Approval and preservation

- [x] Re-read approved `spec.md`, `plan.md` and this file before implementation.
- [x] Capture `git status --short` in `ai_bootstrap` and the read-only downstream;
      preserve every pre-existing change.
- [x] Confirm plan and tasks were explicitly approved together.
- [x] Confirm capability remains `implemented` with the approved target active.

## Contract-first fragments

- [x] Add focused tests for em-dash spacing, consecutive spaces, authored
      hyphens, Unicode, percent-encoding, duplicates and Markdown links inside
      headings.
- [x] Add a generic generated-repository fixture proving canonical fragments
      pass and diacritic-folded/transliterated aliases fail with the expected
      anchor.
- [x] Implement the canonical fragment subset once in
      `documentation_contract.py`.
- [x] Preserve direct link/living checker execution from another cwd and
      repository containment failures.

## Contract-first baseline

- [x] Add pure tests for exact headers/cells, sentinels, allowed values,
      placeholders, canonical paths, existing directories, symlinks, encoded
      traversal, duplicates and cross-table overlap.
- [x] Add aggregate fixtures proving valid exact grandfathering and rejecting
      malformed established/unestablished inventory.
- [x] Implement typed ordered baseline rows before exposing exact path sets.
- [x] Confirm no baseline is created, established, populated, removed or
      reclassified automatically.

## Contract-first maintainability closeout

- [x] Add pure tests for audit-scope and disposition tables, including all four
      values and malformed/duplicate rows.
- [x] Add aggregate tests using real stable auditor findings for accepted,
      separate-spec, resolved, no-findings, missing and stale dispositions.
- [x] Move maintainability grammar ownership from `check_docs.py` to
      `documentation_contract.py`.
- [x] Reconcile each current `(code, path)` tuple against the declared scope
      without importing threshold semantics.
- [x] Keep size/concentration advisory and require formal disposition only at
      targeted closeout.

## Templates, pack and compatibility

- [x] Update managed living-document policy, baseline guidance, tasks template
      and three skills without duplicating the full grammar.
- [x] Bump only the default pack version to `0.7.1`; preserve manifest groups,
      lifecycles, project-owned paths, compositions and obsolete migrations.
- [x] Add neutral fresh, clean-upgrade, historical-debt and established-
      downstream-shaped fixtures with no project/domain-specific names or data.
- [x] Prove `0.7.0` state readability, managed-only behavior and evolved seeded
      owner preservation through existing public lifecycle fixtures.
- [x] Confirm lifecycle, planner, applier, state, CLI and TUI production source
      remain unchanged; stop for approval reconciliation if evidence differs.

## Validation and closeout

- [x] Run focused parser/checker/audit/template/lifecycle tests.
- [x] Run full pytest and unittest suites plus `compileall` without retained
      cache artifacts.
- [x] Validate manifest/version, generated inventory, skills/frontmatter and
      context budgets.
- [x] Run source and generated aggregate/direct commands from another cwd.
- [x] Run proportional temporary fresh apply/reapply and `0.7.0` upgrade,
      managed-only and evolved-seed checks.
- [x] Run the candidate source checker against the real downstream read-only
      with bytecode disabled; confirm identical before/after status and record
      only sanitized classification evidence.
- [x] Confirm generic canonical double-hyphen links pass and the candidate
      checker correctly classifies the current downstream's evolved
      non-canonical links without adding a project-specific alias.
- [x] Run the proportional post-implementation maintainability audit and
      disposition every relevant finding without scope expansion.
- [x] Update product/architecture workflow owners and policy from validated
      behavior; reassess decisions 0001/0002 without creating unnecessary ADRs.
- [x] Promote capability to `verified`, clear target/change and remove roadmap
      item only if all approved evidence supports it.
- [x] Run living-document/link/targeted-closeout checks and `git diff --check`.
- [x] Critically inspect the final diff for parser duplication, project-specific
      fixtures, hidden aliases, semantic thresholds, seed mutation, lifecycle
      leakage, brittle prose assertions and unrelated changes.
- [x] Confirm no downstream file, historical change, baseline inventory or
      evolved seeded owner was rewritten.

## Closeout Disposition

- Living documentation: `updated`
- Living documentation rationale: `updated the focused product, architecture and policy owners with the validated project-agnostic fragment, baseline and maintainability contracts`
- Durable facts added/changed/removed: `added exact canonical fragment, typed baseline-row and scoped finding-reconciliation contracts; changed pack evidence from 0.7.0 to 0.7.1; removed permissive first-column/free-text acceptance and no durable capability`

### Maintainability audit scope

| Repository-relative path |
| --- |
| `ai_workflow_bootstrap/template_packs/default/manifest.json` |
| `ai_workflow_bootstrap/template_packs/default/templates/.agents/skills/living-docs` |
| `ai_workflow_bootstrap/template_packs/default/templates/.agents/skills/maintainability-audit/SKILL.md` |
| `ai_workflow_bootstrap/template_packs/default/templates/.agents/skills/spec-driven/SKILL.md` |
| `ai_workflow_bootstrap/template_packs/default/templates/docs/LIVING_DOCUMENTATION.md` |
| `ai_workflow_bootstrap/template_packs/default/templates/docs/LIVING_DOCUMENTATION_BASELINE.md` |
| `ai_workflow_bootstrap/template_packs/default/templates/docs/SPEC_DRIVEN.md` |
| `ai_workflow_bootstrap/template_packs/default/templates/docs/changes/_templates/tasks.md` |
| `tests/test_documentation_contract.py` |
| `tests/test_docs_checker.py` |
| `tests/test_maintainability_audit.py` |
| `tests/test_template_pack.py` |
| `tests/test_state.py` |
| `docs/product/living-documentation-workflow.md` |
| `docs/architecture/documentation-validation.md` |
| `docs/LIVING_DOCUMENTATION.md` |
| `docs/CAPABILITIES.md` |
| `docs/ROADMAP.md` |
| `docs/changes/living-docs-downstream-compatibility-v1` |

### Maintainability finding dispositions

| Finding code | Path | Disposition | Rationale or reference |
| --- | --- | --- | --- |
| `large-file-review` | `ai_workflow_bootstrap/template_packs/default/templates/.agents/skills/living-docs/scripts/documentation_contract.py` | accepted | Cohesive single owner for the shared deterministic contract; adapters and behavioral tests remain separate |
| `large-file-review` | `docs/changes/living-docs-downstream-compatibility-v1/plan.md` | accepted | Cohesive temporal implementation contract, not a current fact owner |
| `large-file-review` | `docs/changes/living-docs-downstream-compatibility-v1/spec.md` | accepted | Cohesive approved temporal behavior contract, not a current fact owner |
| `large-file-review` | `tests/test_template_pack.py` | accepted | Existing cohesive manifest/inventory suite; new behavioral contracts remain in focused parser and checker modules |
