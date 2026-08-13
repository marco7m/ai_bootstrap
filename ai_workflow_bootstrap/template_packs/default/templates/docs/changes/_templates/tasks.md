# Tasks: <title>

- [ ] Re-read the applicable approved spec or existing authority and the plan
- [ ] Confirm plan and tasks were explicitly approved before non-trivial implementation
- [ ] Stop if behavioral novelty, authority conflict or material contract expansion appears
- [ ] Inspect relevant code paths and conventions
- [ ] Run the proportional scoped maintainability audit and disposition findings
- [ ] Confirm module ownership and boundaries
- [ ] Check maintainability triggers before implementation
- [ ] Confirm tests protect behavior contracts, not implementation details
- [ ] Identify product, architecture, capability, roadmap and decision owners affected by the approved change
- [ ] Register an approved target/active change when a spec changed the target; preserve current state/evidence
- [ ] Replace these generic items with concrete, ordered, checkable tasks
- [ ] Add only the tests justified by the spec and plan
- [ ] Leave out fragile tests that only freeze implementation details
- [ ] Keep touched files cohesive and avoid mixed responsibilities
- [ ] Apply Level 1 refactors where useful
- [ ] Document Level 2/3 refactor needs instead of hiding debt
- [ ] Validate acceptance criteria
- [ ] Update current capability state/evidence only when implementation and validation support it
- [ ] Distill durable facts into their living-doc owners and validate relative links
- [ ] Account for durable facts added, changed and removed; disposition every removal
- [ ] Check whether changed files are conceptually related
- [ ] Document architecture smell if the change is unexpectedly scattered
- [ ] Update docs if behavior, config, commands, or architecture changed
- [ ] Confirm touched area is at least as maintainable as before
- [ ] Run `python .agents/skills/living-docs/scripts/check_docs.py . --closeout docs/changes/<change> --advisory`
- [ ] Summarize final result

## Closeout Disposition

- Living documentation: `pending`
- Living documentation rationale: `pending`
- Durable facts added/changed/removed: `pending`

### Maintainability audit scope

| Repository-relative path |
| --- |
| _Pending approved implementation paths_ |

### Maintainability finding dispositions

| Finding code | Path | Disposition | Rationale or reference |
| --- | --- | --- | --- |
| _Pending_ | — | pending | Pending implementation and scoped audit |
