---
name: living-docs
description: Navigate and maintain linked project knowledge for product behavior, architecture, current capability state, approved targets, roadmap and durable decisions. Use for project orientation, expected-versus-current behavior questions, documentation updates, change closeout, baselining or bug-contract investigation.
---

1. Start at `docs/INDEX.md`; read only the relevant capability, product, architecture, roadmap or decision pages.
2. Treat `scaffold` as unestablished and `incomplete` as partial. Mark `baselined` only after product intent and architecture are reviewed against evidence.
3. Keep product intent (`what/why`) separate from architecture (`how`). Separate current behavior from approved targets.
4. Give each durable fact one owner and replace duplicate prose with relative Markdown links. Keep indexes as compact navigation hubs.
5. In `docs/CAPABILITIES.md`, preserve current state/evidence when adding an approved target and active change. Never use planned work as current evidence.
6. Keep unapproved ideas in `IDEA_INBOX.md`; remove rejected or superseded history from the active map after preserving any useful disposition/decision.
7. Treat change artifacts as temporal contracts. At closeout, distill durable facts into their owners and evaluate durable rationale for a decision record.
8. When docs conflict with evidence or an owner looks regenerated/downgraded, inspect `.ai-bootstrap/state.json` and Git/evidence. Restore its established boundary before narrow closeout.
9. Preserve capabilities unless explicitly disposed. Recover still-valid prior facts plus supported increments; never blindly restore or promote unsupported prose to `verified`.
10. At closeout account for facts added, changed and removed; every removal needs disposition. Review retrieval cost when pages grow or many capabilities route to one owner. Split only for real responsibilities; size alone is advisory.
11. Use the maintainability audit for orphan, concentration and closeout signals. It complements rather than replaces semantic review.
12. After structural/recovery changes run `python .agents/skills/living-docs/scripts/check_living_docs.py` and `python .agents/skills/living-docs/scripts/check_links.py`.
13. Never store sensitive payloads. Summarize owners, current/target changes, evidence, accepted findings and gaps.
