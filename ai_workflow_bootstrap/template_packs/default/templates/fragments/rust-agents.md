## Rust development lifecycle

- Follow [the Rust development workflow](docs/architecture/rust-development.md).
  Keep debug/test caches during implementation cycles and run `make clean-dev`
  only after the final successful validation; keep the release artifact.
- Ordinary non-interactive `cargo build`, `cargo check`, `cargo test` and
  `cargo clippy` invocations follow the long-running command policy. Classify
  `cargo run` by the launched program rather than by the Cargo command itself.
