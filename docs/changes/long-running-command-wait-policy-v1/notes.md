# Notes: Long-running command wait policy v1

## Validation environment

- The repository's tests are standard-library `unittest` modules. The direct
  `pytest` command was unavailable because the configured asdf Python has no
  `pytest` installation, so all 14 test modules were executed explicitly with
  `python -m unittest`; all 92 tests passed.
- `python -m build` could not start because the environment has no `build`
  module. The local fallback `python -m pip wheel . --no-build-isolation
  --no-deps` also stopped during metadata generation because `bdist_wheel` is
  unavailable. No dependency was installed for this documentation/template
  change.
- Manifest JSON validation, both living-document checkers and `git diff
  --check` run without optional dependencies.

## Implementation notes

- The base template is the sole owner of the `300000 ms` target, repeated long
  wait and completion-only polling rule.
- The Rust fragment contains only Cargo classification examples and makes the
  launched program authoritative for `cargo run`.
- Pre-existing changes in `.ai-bootstrap/state.json` and
  `docs/LIVING_DOCUMENTATION.md` were not edited by this change.
