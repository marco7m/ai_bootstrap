# Rust development workflow

[Architecture](README.md) · [Knowledge index](../INDEX.md)

Use the debug profile and its incremental cache throughout implementation and
validation. Clean development artifacts only after the final successful check;
do not clean between correction cycles.

## Commands

- `make dev` runs `cargo run` in the debug profile.
- `make test` runs the test suite.
- `make lint` runs Clippy for all targets and features with warnings denied.
- `make typecheck` checks all targets and features.
- `make clean-dev` runs `cargo clean --profile dev` after final validation.
- `make run` runs `cargo run --release` for daily use and lets Cargo rebuild only
  when the source changed.

`make clean-dev` removes Cargo's development/test profile artifacts while
preserving `target/release`. It must not delete databases, recordings, reports
or other user data. If the repository configures a non-default Cargo target
directory, document and ignore that project-specific directory separately.

## Optional release stripping

Binary applications may reduce release size when diagnostic symbols are not
needed:

```toml
[profile.release]
strip = "symbols"
```

This is opt-in. Keep symbols when they are useful for crash or production
diagnosis.
