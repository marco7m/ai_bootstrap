dev:
	cargo run

run:
	cargo run --release

clean-dev:
	cargo clean --profile dev

test:
	cargo test

lint:
	cargo clippy --all-targets --all-features -- -D warnings

typecheck:
	cargo check --all-targets --all-features
