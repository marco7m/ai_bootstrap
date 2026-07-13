# Tasks: Living Knowledge Base v1

- [x] Re-read the approved spec and plan before implementation.
- [x] Confirm the worktree state and preserve unrelated user changes.
- [x] Update the default template-pack version and manifest with the approved
      living-doc directories and files.
- [x] Stop fresh generation of the four superseded legacy living-doc outputs
      without adding any deletion behavior for existing repositories.
- [x] Add `docs/INDEX.md` as the compact navigation owner with valid relative
      links to every core knowledge area.
- [x] Add `docs/CAPABILITIES.md` with the approved lifecycle, product,
      architecture, change and evidence mapping.
- [x] Add the foundational product, architecture and decision indexes plus the
      minimal decision template.
- [x] Rewrite AI context, living-documentation policy, roadmap, idea inbox and
      glossary templates around routing, ownership and progressive disclosure.
- [x] Ensure product and architecture guidance separates current behavior from
      approved target behavior.
- [x] Expand the generated `living-docs` skill with concise project-orientation,
      ownership, lifecycle, link and conflict-resolution instructions.
- [x] Integrate living-document impact and lifecycle rules into generated
      AGENTS, spec-driven workflow, start guidance and relevant skills.
- [x] Add concrete living-document ownership and update prompts to generated
      spec, plan and task templates without weakening either approval gate.
- [x] Update README and the bootstrap repository's relevant workflow guidance
      to match the new generated structure and non-destructive legacy policy.
- [x] Remove only the `docs/changes/` entry from the source `.gitignore` so
      change artifacts are versionable through ordinary Git workflows.
- [x] Inspect newly visible change paths and avoid staging unrelated artifacts.
- [x] Update template-pack and planner tests for recommended,
      living-docs-only and spec-driven-only generated file contracts.
- [x] Add a focused test that generated core relative Markdown links resolve in
      a temporary applied repository.
- [x] Add only narrow content assertions for ownership, lifecycle,
      current/target separation and evidence; do not snapshot full prose.
- [x] Confirm no production engine, CLI, TUI, state-schema, dependency or
      `bootstrap_sdd.py` changes were introduced.
- [x] Run `python3 -m unittest discover -s tests -v`.
- [x] Run `python3 -m compileall -q ai_workflow_bootstrap` and
      `git diff --check`.
- [x] Inspect the final diff for broken links, sensitive data, conceptual
      locality and unintended legacy deletion behavior.
- [x] Validate every acceptance criterion and mark completed tasks.
- [x] Record meaningful deviations in `notes.md` and summarize the final result.
- [x] Confirm change artifacts no longer require `git add -f` and that no
      automatic staging or commit behavior was added.
