# Change Spec: Living Docs Downstream Compatibility v1

- Status: `completed`
- Change: `living-docs-downstream-compatibility-v1`
- Date: 2026-08-11
- Approved: 2026-08-11

## 1. Summary

Repair three project-agnostic compatibility and gate-integrity defects exposed
when default pack `0.7.0` was applied to its first established downstream:

1. supported heading fragments diverge from GitHub-style section anchors and
   reject real links around punctuation and adjacent spaces;
2. the historical-debt baseline accepts malformed rows as waivers because it
   validates only their first column;
3. targeted closeout accepts arbitrary maintainability text and does not
   objectively reconcile recorded dispositions with advisory findings.

The repair will retain one shared standard-library documentation contract,
preserve direct checker entry points and lifecycle boundaries, and add generic
representative fixtures. It will not rewrite downstream documentation, infer a
baseline, or turn advisory thresholds into semantic verdicts.

This specification was explicitly approved on 2026-08-11 after removing a
proposed downstream-specific fragment alias. Approval authorizes planning, not
implementation; plan and tasks require their own explicit approval.

## 2. Problem and Reproduction Evidence

Internal green tests are not sufficient compatibility evidence. Pack `0.7.0`
has 118 passing tests and its self-host aggregate check passes, but its fixtures
do not represent the first real downstream's anchor convention, malformed
baseline rows or disposition bypasses.

### 2.1 Finding 1: fragment normalization rejects downstream links

The source owner is:

`ai_workflow_bootstrap/template_packs/default/templates/.agents/skills/living-docs/scripts/documentation_contract.py`

`heading_slug()` removes punctuation and then collapses adjacent whitespace.
The reproduced results are:

```text
Integrated reliability qualification — 2026-08-07
-> integrated-reliability-qualification-2026-08-07

Parte 4 — Actor, Controller e interfaces de interação
-> parte-4-actor-controller-e-interfaces-de-interação
```

The downstream links use two hyphens where a space, removed em dash and another
space occur. The [GitHub section-link rules](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#section-links)
replace each space with a hyphen and remove other punctuation; they do not
collapse the two surviving space-derived hyphens. GitHub also preserves allowed
UTF-8 characters, so the downstream `interacao` fragment is not the canonical
GitHub anchor for the heading containing `interação`.

Read-only execution in `/home/marco/slapy/projetos/text-online-mmorpg`, with
`PYTHONDONTWRITEBYTECODE=1`, reproduced:

- six `broken-fragment` diagnostics across `docs/CAPABILITIES.md`,
  `docs/ROADMAP.md`, `docs/decisions/README.md`,
  `docs/decisions/0001-controller-neutral-decision-activation.md`,
  `docs/product/VISION.md` and two playtest/change notes;
- one additional `capability-route` diagnostic for the same incompatible
  `VISION.md` route already reported as a broken fragment;
- three distinct target anchors underlying those seven blocking diagnostics.

The original classification of seven independent `broken-fragment` failures is
therefore adjusted: there are six broken-link occurrences plus one structurally
duplicated route failure. The em-dash behavior is a checker false positive for
GitHub-compatible double-hyphen links. The accent-folded `interacao` link is
legacy downstream debt relative to the GitHub renderer and must not be silently
declared canonical or accepted by a compatibility alias.

Severity: **high compatibility risk**. A managed upgrade makes the new aggregate
gate unusable on established documents, while an over-broad compatibility rule
could falsely certify links that the renderer does not provide.

### 2.2 Finding 2: malformed baseline rows authorize waivers

The affected functions are `_table_paths()` and `parse_baseline()`, together
with the seeded baseline template and checker tests. Reproduction with an
existing `docs/changes/old` directory and this established row:

```markdown
| `docs/changes/old` | banana | |
```

returned:

```text
grandfathered = ['docs/changes/old']
errors = ()
```

The parser ignores status, evidence, column count and duplicates. It also
deduplicates rows through a set before it could report duplicate inventory.
The living checker later verifies existence, but the parser does not own a
complete row grammar and the aggregate gate accepts the malformed waiver.
Cross-table overlap is already rejected and must remain rejected.

Severity: **high gate-integrity risk**. A typo or arbitrary value can exempt a
completed historical change from the prospective closeout contract without the
review evidence required by the approved `navigable-living-knowledge-v1` spec
and baseline decision.

### 2.3 Finding 3: maintainability disposition is permissive and unreconciled

`check_docs.py::_maintainability_closeout_problem()` rejects only empty,
`pending`, `todo` and `tbd`. A tasks file containing:

```markdown
- Maintainability findings: `banana`
```

reproduced `None` as the closeout problem, so an unknown value closes that part
of the gate.

The aggregate checker also runs the auditor in advisory mode and prints its
stable `level`, `code`, `path` and evidence, but validates maintainability text
independently. It does not prove that a current finding received any
disposition. A targeted self-host run reported large-file findings for the
completed spec and plan and passed; that particular accepted outcome may be
reasonable, but the checker cannot establish the relationship.

Severity: **high workflow-integrity risk**. Arbitrary text can close a required
gate, and relevant findings can disappear from the handoff without an objective
accounting boundary. This is not a claim that size itself should block closeout.

## 3. Goal

Deliver a backward-compatible pack repair in which:

- fragment validation implements and documents a small GitHub-compatible ATX
  subset used by generated and established documents;
- invalid legacy fragment differences remain visible and are migrated by their
  owning project rather than hidden, accepted or rewritten automatically;
- every established baseline row is structurally valid, safe, reviewed and
  unambiguous before it can affect prospective gating;
- targeted closeout recognizes only explicit maintainability dispositions and
  accounts for current stable auditor findings without interpreting arbitrary
  prose or converting thresholds into verdicts;
- realistic fixtures prove fresh-project, clean-upgrade, historical-debt and
  downstream compatibility separately;
- managed updates preserve seeded owners and old state under existing lifecycle
  rules.

## 4. Scope

### 4.1 Shared fragment contract

Document and implement in `documentation_contract.py` a supported ATX-heading
subset with these rules:

- remove supported inline Markdown formatting while retaining visible text,
  including Markdown links inside headings;
- case-fold letters;
- replace each ordinary space with one hyphen without collapsing adjacent
  space-derived or authored hyphens;
- remove supported punctuation, including an em dash, without first collapsing
  its surrounding spaces;
- retain supported Unicode characters in the canonical anchor;
- strip leading/trailing whitespace before anchor construction;
- append `-1`, `-2`, and so on for duplicate canonical headings in document
  order;
- percent-decode incoming URI fragments before exact comparison;
- validate only the documented subset, not every Markdown renderer.

GitHub-style canonical anchors are the reference. Double-hyphen links for
headings containing ` — ` are canonical and must pass. A fragment that differs
from canonical through diacritic removal, transliteration or fuzzy matching
remains invalid. The checker may report the expected canonical fragment, but it
must not accept an anchor the renderer does not generate or mutate its owner.

Malformed, ambiguous or unrelated fragments remain blocking. File containment,
symlink handling and existing direct `check_links.py` and
`check_living_docs.py` commands remain supported.

### 4.2 Baseline grammar

Keep the baseline human-readable Markdown. Each data row has exactly three
cells under the exact expected header. `_None_ | — | —` remains an empty-table
sentinel and is valid only when it is the table's sole data row.

Every real path in either table must:

- be canonical repository-relative POSIX form `docs/changes/<change>` with one
  non-empty direct change-directory name;
- contain no absolute prefix, `.`/`..`, empty component, trailing separator or
  percent-encoded traversal;
- resolve within the repository to an existing, non-symlink directory;
- appear once across the entire baseline after normalization.

Grandfathered closeout debt rows have the exact form:

```markdown
| `docs/changes/<change>` | unresolved | <inventory evidence or rationale> |
```

`unresolved` is the only allowed debt status. Evidence/rationale must be
non-empty and must not normalize to a placeholder such as `—`, `todo`, `tbd`,
`pending`, `not reviewed`, `reason required` or a generated underscore prompt.

Reviewed debt disposition rows use `reviewed` as the only v1 disposition and
require non-placeholder review evidence/rationale. `reviewed` means only that a
real reviewer removed or reclassified the baseline exception with recorded
evidence; it does not claim that the historical artifact itself was edited or
that all of its semantics are current. More detailed disposition values require
a later approved contract rather than ad hoc acceptance.

Duplicate rows, normalized aliases of the same path and any overlap between the
grandfathered and reviewed tables are blocking. An `unestablished` baseline may
contain only empty sentinels. An `established` baseline requires non-placeholder
baseline evidence and full validation of every row. Validation never rewrites,
removes, reclassifies or establishes inventory.

### 4.3 Maintainability closeout grammar and reconciliation

The shared contract, not `check_docs.py`, must own the deterministic grammar.
The allowed dispositions are:

- `resolved`, tied to identified findings that no longer occur in the rerun;
- `accepted`, tied to identified current findings and a non-placeholder
  rationale;
- `separate-spec`, tied to identified current findings and an existing safe
  repository reference, normally `docs/changes/<change>/spec.md`;
- `no-findings`, with a non-empty explicit inspected scope and only when the
  current audit of that scope returns no findings.

Unknown values fail. `accepted` without rationale, `separate-spec` without a
reference and `no-findings` without inspected scope fail. Placeholder prose
does not satisfy a required field. `resolved` cannot hide a finding still
returned for the same scope.

Objective reconciliation is limited to the auditor's stable public tuple of
finding code and path plus its reported inspected scope. The aggregate checker
must account for each relevant current tuple exactly once or fail targeted
closeout. It must not import private threshold logic, score rationale quality,
infer code cohesion or require a refactor merely because a threshold fired.
Manual findings may be recorded in the same human-readable disposition surface,
but remain reviewer assertions rather than facts the checker pretends to prove.

The exact Markdown layout is an implementation-plan decision, provided it is
constrained, readable, preserves old historical artifacts, avoids duplicated
parsing and supports more than one finding without ambiguous free prose.

### 4.4 Distribution and compatibility

- Change the reusable source in the default template pack, not only generated
  copies.
- Proposed release: pack `0.7.1`. The stricter behavior restores the approved
  `0.7.0` contract that malformed baseline and closeout input must fail; no
  promised lifecycle or CLI interface is removed.
- Update managed scripts, skills, policies and change templates only where the
  repaired contract requires it.
- Preserve all seeded owners and never establish or populate a downstream
  baseline automatically.
- Preserve `--managed-only`: it may update managed tooling but cannot create or
  establish the seeded baseline.
- Keep old state readable and preserve existing provenance/overwrite rules.
- Do not change lifecycle, planner, applier, state, CLI or TUI unless new
  evidence demonstrates a generic compatibility defect and the approved spec
  is reconciled first.
- Do not add an external dependency unless planning demonstrates that the
  documented standard-library subset is insufficient and records maintenance
  and security impact.

## 5. Out of Scope

- Reorganizing any downstream documentation or product code.
- Establishing its baseline or automatically editing its links.
- Treating an invalid legacy renderer fragment as canonical without a visible
  migration diagnostic.
- Deleting, rewriting or retrofitting historical changes.
- Automatically creating domain pages or inferring domain truth.
- Implementing complete GitHub/GitLab/CommonMark renderer parity.
- Replacing constrained Markdown with JSON or another opaque format without a
  demonstrated insufficiency.
- Making size, line count, byte count or route concentration blocking by itself.
- Semantically judging all maintainability rationale prose.
- Fixing unrelated `ai_bootstrap` debt.
- Committing, staging, resetting, cleaning or destructively changing files.

## 6. Users / Actors

- Maintainers releasing and applying template-pack repairs.
- Existing projects upgrading managed documentation tooling.
- Humans and agents establishing/reviewing historical-debt baselines.
- Contributors closing spec-driven changes with maintainability evidence.
- Reviewers distinguishing structural proof from advisory judgment.

## 7. Functional Requirements

1. Real headings containing ` — ` generate canonical double-hyphen fragments.
2. Authored and space-derived consecutive hyphens are preserved as documented.
3. Supported Unicode remains in canonical anchors.
4. Duplicate headings receive deterministic zero-based suffix behavior matching
   GitHub's first-unsuffixed, then `-1`, `-2` convention.
5. Markdown links inside headings contribute visible link text, not their URL.
6. Percent-encoded fragments are decoded safely before canonical comparison.
7. Invalid fragments and paths outside the repository remain blocking.
8. Diacritic removal, transliteration and fuzzy matching do not turn a
   non-rendered fragment into a valid fragment.
9. Baseline tables validate exact columns, allowed values, safe existing paths,
   evidence, duplicates, sentinels and cross-table overlap.
10. Only `unresolved` grandfather rows and `reviewed` reviewed-disposition rows
    are accepted in v1.
11. Baseline entries grandfather only their exact listed paths.
12. Baseline review never implies that a historical artifact was edited.
13. Maintainability closeout accepts only the four named dispositions with
    their required rationale/reference/scope.
14. Relevant current auditor findings cannot disappear without an identified
    disposition.
15. Advisory thresholds remain non-blocking and do not become semantic
    judgments.
16. Direct checker entry points and aggregate execution from another current
    working directory remain supported.
17. New and managed-only projects retain an unestablished baseline unless a
    reviewer explicitly establishes it.

## 8. Non-Functional Requirements

### Modularity / Architecture

- `documentation_contract.py` remains the single deterministic owner for
  fragment, baseline and closeout grammar.
- `check_links.py`, `check_living_docs.py`, `check_docs.py` and
  `audit_repository.py` remain thin authority-specific consumers.
- Stable audit output is the only coupling used for objective reconciliation;
  aggregate code does not copy auditor thresholds or internals.
- Core bootstrap lifecycle and user-interface layers remain policy-agnostic.

### Security / Privacy

- Resolve and contain paths against the repository root, rejecting symlink and
  encoded traversal.
- Emit paths, codes, scope and safe structural evidence, not document contents,
  secrets or sensitive downstream payloads.
- Use no network at runtime.

### Reliability

- Equal input produces deterministic anchors, row errors, findings and exit
  status.
- Malformed input fails without mutation.
- Diagnostics distinguish canonical success from blocking failure and may
  suggest the expected canonical fragment without accepting an invalid alias.
- Internal fixtures cannot substitute for the representative downstream
  fixture and read-only candidate validation.

### Performance

- Validation remains bounded to selected Markdown/workflow and audit scope.
- No full renderer or repository-wide scan is added to ordinary direct checks.

### Observability

- Diagnostics distinguish canonical fragment success, legacy compatibility,
  broken fragment, malformed baseline and undispositioned maintainability.
- Baseline errors identify table and row without echoing sensitive prose.
- Maintainability output identifies inspected scope and each stable finding
  tuple requiring disposition.

### Simplicity / Dependencies

- Prefer Python standard library and constrained Markdown over a new parser or
  opaque data format.
- Do not generalize beyond documented downstream and generated contracts.

## 9. Maintainability Impact

### 9.1 Audit evidence

The proportional generated audit inspected 13 affected parser, checker, auditor,
template, manifest and test files. Its sole encoded signal was:

- `tests/test_template_pack.py`: `large-file-review` at 510 lines.

This advisory threshold does not prove mixed responsibility. Manual review of
the same surfaces found the following.

### 9.2 Findings and proposed dispositions

| Finding | Risk | Classification | Proposed disposition |
| --- | --- | --- | --- |
| `check_docs.py` independently parses maintainability disposition | High | Refactor within this repair | Move deterministic grammar to `documentation_contract.py`; keep aggregate orchestration thin |
| `_table_paths()` discards row semantics and set-deduplicates evidence | High | Refactor within this repair | Parse typed constrained rows once, preserve row/duplicate diagnostics and share them with blocking/advisory consumers |
| Fragment test combines Unicode, duplicate and inline-link happy paths but omits renderer edge cases | High | Refactor within this repair | Split contract cases and add generic representative fixtures through public checker behavior |
| Baseline tests use synthetic text without existing change paths and cover only a valid row | High | Refactor within this repair | Add malformed-value/evidence/path/duplicate/overlap tests plus aggregate fixture tests |
| Closeout tests accept free prose `no-findings in scoped audit` without reconciling audit output | High | Refactor within this repair | Test every formal disposition and finding/scope reconciliation through the aggregate CLI |
| `tests/test_template_pack.py` exceeds the source line threshold | Low | Advisory observation | Add behavioral contracts to focused checker/parser modules; split only if a real manifest responsibility emerges |
| Full renderer parity would greatly expand parser ownership | Medium | Separate spec | Keep this repair to the explicit GitHub-compatible subset; require new evidence and approval for broader parity |
| Downstream product/knowledge concentration findings | Low for this repair | Advisory observation | Do not reorganize downstream owners; thresholds remain consultative and downstream-owned |

The earlier apparent duplicate auditor call/return came from overlapping output
ranges, not source duplication, and is removed from the finding set. No
pre-implementation broad refactor is required. The shared contract is still
the correct cohesive owner. Parser/disposition typing and realistic fixtures
are local to this repair; lifecycle/UI expansion is not justified.

## 10. Living Documentation Impact

### Durable owners affected after approval and implementation

- Product: `docs/product/living-documentation-workflow.md` and its hub
  `docs/product/README.md` only as needed to route the repaired contract.
- Architecture: `docs/architecture/documentation-validation.md` and its hub
  `docs/architecture/README.md` only as needed to route the repaired boundary.
- Capability: `docs/CAPABILITIES.md`, specifically “Navigable
  living-documentation workflow”.
- Navigation/policy: `docs/INDEX.md` only if routes change, and
  `docs/LIVING_DOCUMENTATION.md` for the documented fragment, baseline and
  closeout grammar.
- Roadmap: `docs/ROADMAP.md` after approval to order the active repair.
- Decisions: reassess
  `docs/decisions/0001-separate-advisory-health-from-regression-gates.md` and
  `0002-use-an-explicit-prospective-documentation-baseline.md`; update or add a
  decision only if durable rationale changes rather than merely being enforced.
- Root usage guidance: `README.md` only if the public validation/upgrade command
  changes.

The current capability state `verified` is not supported by the reproduced real
downstream gate failure. After spec approval, the proposed honest repair-time
state is `implemented`: the capability exists and internal validation passes,
but compatibility is not fully validated. Preserve the internal 118-test
evidence while adding the downstream limitation, approved target and active
change. Promote to `verified` only after all repair criteria pass, including a
candidate checker run read-only against at least one established downstream (or
an explicitly authorized equivalent) without making that repository a product
dependency or treating a synthetic fixture alone as proof.

Spec approval alone does not alter current capability evidence, baseline,
manifest or version; those changes remain gated by the approved plan/tasks and
validated implementation, except for registering this approved target and
active change in their living owners.

## 11. System Flows

### Fragment validation

1. Parse a supported ATX heading outside fenced code.
2. Remove supported inline markup while retaining visible text.
3. Produce its canonical GitHub-style anchor and ordered duplicate aliases.
4. Percent-decode the requested fragment and compare canonically.
5. Fail non-canonical aliases with source, target and expected canonical
   fragment.

### Baseline validation

1. Parse status/evidence and locate both exact tables.
2. Validate header, sentinel and exactly three cells per data row.
3. Validate allowed status/disposition, evidence and canonical safe path.
4. Resolve each path against the repository and confirm an existing non-symlink
   change directory.
5. Reject duplicate normalized paths and cross-table overlap.
6. Only then expose exact grandfathered/reviewed sets to downstream checks.

### Targeted maintainability closeout

1. Read the declared inspected scope and formal dispositions.
2. Run the advisory auditor over that scope.
3. Match current stable finding code/path tuples to declared dispositions.
4. Reject unknown/missing/malformed dispositions or unresolved mismatches.
5. Keep threshold findings advisory; acceptance with rationale remains valid.
6. Report the scope and accounted/unaccounted findings without claiming
   semantic correctness.

## 12. Edge Cases

- Two ordinary spaces, an authored hyphen, and spaces around removed punctuation
  produce distinct consecutive-hyphen cases and must not be globally collapsed.
- Unicode canonical fragments and their percent-encoded forms compare equally.
- Unicode diacritic-folded and unrelated ASCII approximations fail; diagnostics
  may show the canonical Unicode fragment.
- Duplicate headings after markup removal share the same base and receive
  ordered suffixes.
- An empty or markup-only heading creates no fragment.
- A Markdown link in a heading retains only visible link text.
- Baseline rows with too few/many cells, escaped/encoded traversal, missing
  directory, symlink, duplicate, trailing slash or placeholder evidence fail.
- `_None_` combined with a real row fails rather than being ignored.
- The same path spelled differently cannot evade duplicate/overlap checks.
- `accepted` with generic placeholder prose fails formal validation; meaningful
  prose quality beyond placeholders remains reviewer-owned.
- A finding can be accepted without refactoring when rationale is present.
- `resolved` fails while the same stable finding remains in the rerun.
- A changed auditor threshold may change findings but not retroactively rewrite
  historical artifacts; current targeted closeout uses current evidence.
- Missing/unestablished baseline remains observable and does not invent legacy
  waivers.

## 13. Constraints and Assumptions

- Follow both explicit spec-driven approval gates.
- Preserve all pre-existing worktree changes and downstream state.
- Source fixes live in the template pack; generated copies are validation
  outputs, not alternate owners.
- Existing seeded lifecycle and old-state compatibility are assumed sufficient
  until contrary evidence appears.
- GitHub section-anchor rules are the renderer reference for the supported
  subset. Real downstream evidence selected the cases, but no repository name,
  layout or invalid local convention enters the reusable contract.
- No commit, stage, reset, cleanup or destructive operation.

## 14. Acceptance Criteria

1. Representative headings containing an em dash produce double-hyphen
   canonical anchors; canonical Unicode preservation is documented.
2. Unicode, percent-encoded Unicode, duplicates, inline Markdown links,
   authored hyphens and consecutive spaces/hyphens have focused tests.
3. Invalid and unsupported fragments continue to fail actionably.
4. Absolute, escaping, symlinked and otherwise outside-repository paths remain
   rejected.
5. The aggregate checker passes generic representative fixtures for canonical
   downstream-shaped links; a separate fixture proves that an accent-folded
   non-canonical link remains blocking and reports the expected anchor.
6. Direct `check_links.py`, `check_living_docs.py` and `check_docs.py` commands
   execute from a different current working directory.
7. An established baseline row with an unknown debt status fails.
8. Empty or placeholder row rationale/evidence fails.
9. Missing, unsafe, non-canonical, symlinked, duplicate or overlapping baseline
   paths fail.
10. A valid baseline grandfathers only exact listed existing paths and does not
    edit historical artifacts.
11. Reviewed rows accept only `reviewed` with real evidence and make no claim
    that the historical artifact was updated.
12. Unknown maintainability disposition fails.
13. `accepted` without non-placeholder rationale fails.
14. `separate-spec` without a safe existing reference fails.
15. `no-findings` without explicit inspected scope, or with current findings in
    that scope, fails.
16. Size/concentration findings remain non-blocking solely by threshold and may
    be formally accepted with rationale.
17. Targeted closeout fails until every relevant current stable finding tuple
    has one valid disposition.
18. A fresh project receives an unestablished empty baseline.
19. `--managed-only` neither creates nor establishes the seeded baseline.
20. Evolved seeded owners remain byte-preserved under applicable preview,
    dry-run, apply, force and reapply paths.
21. Separate project-agnostic fixtures cover fresh project, clean upgrade,
    established historical debt and an established downstream documentation
    shape without importing its name, files or domain.
22. Old pack state remains readable and grants no new overwrite, baseline or
    migration authority.
23. Source-template and generated direct/aggregate checkers agree on the shared
    contract without copied fragment, table or disposition parsing.
24. The capability is represented as `implemented` during repair and is
    promoted to `verified` only after read-only downstream candidate validation
    plus all relevant internal evidence passes.
25. Product, architecture, capability, policy, roadmap and any warranted
    decision owner are reconciled only at approved implementation closeout.
26. Focused tests, full suite, `compileall`, manifest/version validation,
    aggregate and direct checkers, proportional dry-run/apply/reapply/state
    checks, `git diff --check` and final maintainability review pass.
27. No external dependency, downstream rewrite, automatic baseline, historical
    debt hiding, semantic-threshold verdict or unrelated core/UI change is
    introduced.

## 15. Resolved Approval Decisions and Open Questions

Approved decisions:

- pack `0.7.1` is the compatible repair target unless implementation evidence
  proves that a documented valid public input or interface must be removed;
- GitHub-compatible canonical fragments remain exact, with no accent-folding,
  transliteration or downstream-specific alias;
- real downstream material is reproduction/acceptance evidence only; permanent
  fixtures and implementation remain project-agnostic;
- baseline vocabulary is `unresolved` and `reviewed`;
- maintainability reconciliation uses stable finding code/path and inspected
  scope without importing threshold semantics;
- lifecycle, planner, applier, state, CLI and TUI remain unchanged absent new
  approved evidence.

No material spec question remains open. Planning must select the smallest
human-readable Markdown layout for multiple maintainability dispositions while
preserving the approved grammar and direct-entry-point compatibility.
