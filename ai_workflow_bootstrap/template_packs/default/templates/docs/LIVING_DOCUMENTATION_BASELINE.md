# Living Documentation Baseline

[Project knowledge index](INDEX.md) ·
[Living-documentation policy](LIVING_DOCUMENTATION.md)

- Baseline status: `unestablished`
- Baseline evidence: _not established_

This project-owned inventory separates known historical closeout debt from new
debt after an explicit review. Bootstrap application never populates or marks
these entries reviewed. Establish the baseline only after inspecting the real
repository and recording exact evidence.

## Grandfathered closeout debt

| Change artifact | Debt status | Review evidence or rationale |
| --- | --- | --- |
| _None_ | — | — |

Entries here remain unresolved debt. They are exempt only from the prospective
closeout gate and are not declared correct, complete or semantically reviewed.
Every real row uses an existing direct `docs/changes/<change>` directory,
`unresolved` status and non-placeholder inventory evidence. Duplicate, unsafe,
missing or overlapping paths are invalid.

## Reviewed debt dispositions

| Change artifact | Disposition | Review evidence or rationale |
| --- | --- | --- |
| _None_ | — | — |

Move an entry out of grandfathered debt only after real review. Do not edit the
historical artifact merely to make a checker pass.
Reviewed rows use disposition `reviewed` with non-placeholder review evidence;
this records review of the exception and does not claim the historical artifact
was edited. `_None_ | — | —` is valid only as the sole row of an empty table.
