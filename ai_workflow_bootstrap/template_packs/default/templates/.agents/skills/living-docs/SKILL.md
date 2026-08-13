---
name: living-docs
description: Navigate and maintain linked product, architecture, capability, decision and baseline knowledge. Use for orientation, documentation updates, closeout, baselining or bug-contract investigation.
---

1. Start at `docs/INDEX.md`; follow only relevant capability, product, architecture, roadmap or decision links.
2. Treat `scaffold` as unestablished and `incomplete` as partial. Mark `baselined` only after product intent, architecture, routes and evidence are reviewably navigable.
3. Keep product (`what/why`) separate from architecture (`how`), and current behavior separate from approved targets.
4. Give each durable fact one owner. Keep INDEX and area READMEs as compact hubs; split only for real responsibilities, never size alone.
5. Preserve current capability state/evidence when adding an approved target and active change. Never use planned work as current evidence.
6. Keep unapproved ideas in `IDEA_INBOX.md`; preserve useful disposition/rationale before removing rejected or superseded items.
7. Treat changes as temporal contracts, never the only current owner. At closeout distill durable facts and evaluate lasting rationale for a decision.
8. If docs conflict with evidence or look regenerated/downgraded, inspect `.ai-bootstrap/state.json` and Git/evidence before recovery.
9. Preserve capabilities unless explicitly disposed. Recover still-valid facts plus supported increments; never promote unsupported prose to `verified`.
10. Account for facts added, changed and removed; every removal needs disposition.
11. Keep `docs/LIVING_DOCUMENTATION_BASELINE.md` unestablished until reviewed. Grandfather only exact existing `docs/changes/<change>` rows with `unresolved` and real evidence; reviewed rows use `reviewed`. Never infer or rewrite debt.
12. Use the maintainability audit for independent size/concentration and cohesion review. Thresholds are advisory.
13. At closeout record explicit maintainability scope and per-finding dispositions, then run `python .agents/skills/living-docs/scripts/check_docs.py . --closeout docs/changes/<change> --advisory`; only `updated` or justified `no-update-needed` closes living docs.
14. Never store sensitive payloads. Summarize owners, current/target changes, evidence, findings and gaps.
