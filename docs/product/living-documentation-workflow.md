# Navigable Living-Documentation Workflow

[Product hub](README.md) · [Capabilities](../CAPABILITIES.md) ·
[Architecture](../architecture/documentation-validation.md) ·
[Knowledge index](../INDEX.md)

## Product contract

Generated projects maintain three distinct knowledge layers:

1. `docs/INDEX.md` and compact area hubs provide the normal navigation path;
2. focused product and architecture owners explain current knowledge;
3. `docs/changes/` preserves temporal handoff, evidence and history.

Focused pages emerge only for real responsibilities. The workflow does not
generate domain-specific empty pages or require a split solely because of file
size. Every focused current owner remains reachable from the index graph, and a
capability routes its product contract under `docs/product/` and current
architecture under `docs/architecture/`.

## Coverage and historical debt

Knowledge progresses from generated `scaffold`, through reviewed but explicitly
`incomplete` coverage, to a navigable `baselined` scope backed by stated
evidence. Code may establish current implementation but cannot alone establish
product intent.

`docs/LIVING_DOCUMENTATION_BASELINE.md` is a seed-once project owner. It starts
unestablished. After real repository review it records exact grandfathered
historical closeout paths and evidence. Those entries remain visible unresolved
debt; they are exempt only from the prospective gate and are never populated or
declared reviewed by bootstrap application.

Established grandfather rows use an existing direct `docs/changes/<change>`
path, `unresolved` and real inventory evidence. Reviewed exception rows use
`reviewed` and real review evidence without implying the historical artifact was
edited. Malformed, missing, unsafe, duplicate or overlapping rows cannot grant
an exception.

## Change closeout

A targeted closeout accepts living documentation only as:

- `updated`; or
- `no-update-needed` with a change-specific rationale.

`pending`, `follow-up`, absence and objective placeholder rationales keep the
change open. Closeout accounts for facts added, changed and removed, evaluates
lasting rationale for a decision record, and advances capability state only
when implementation and evidence support it.

The aggregate command validates objective links, routes, reachability, baseline
and closeout invariants. Size, capability concentration and semantic cohesion
remain advisory review signals. Deterministic checks do not claim to prove
truth, completeness or currency.

Targeted closeout declares explicit audit-scope paths and accounts for every
current stable finding code/path as accepted with rationale, routed to a
separate spec, or resolved after disappearance. `no-findings` is valid only for
a currently clean declared scope. Thresholds remain advisory rather than
becoming semantic verdicts.

Supported local ATX fragments follow the documented GitHub-style subset: one
hyphen per ordinary space, punctuation removal without collapsing those
hyphens, Unicode preservation, percent-decoding, visible inline-link text and
ordered duplicate suffixes. Diacritic folding and transliteration are not
accepted as renderer anchors.

## Compatibility

Managed policies and checks advance under existing update consent. Evolved or
untracked seeded knowledge remains preserved during ordinary apply and
`--force`; managed-only application does not create or falsely establish the
seeded baseline. No migration invents domain facts or rewrites historical
changes.

Pack `0.7.1` repairs these structural contracts without changing lifecycle or
making any downstream repository part of the reusable behavior or fixtures.
