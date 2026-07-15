from __future__ import annotations

import hashlib
from dataclasses import dataclass

MANAGED = "managed"
SEEDED = "seeded"
PROJECT = "project"
COMPOSED = "composed"
MIGRATED = "migrated"

RENDERED_FILE_LIFECYCLES = frozenset({MANAGED, SEEDED})
WRITABLE_STATUSES = frozenset({"written", "updated", "overwritten", "reset"})
BLOCKING_STATUSES = frozenset({"conflict", "migration_required"})
RESET_CONFIRMATION = "RESET PROJECT KNOWLEDGE"


def content_hash(content: str) -> str:
    """Hash the exact UTF-8 text written by the bootstrap."""

    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def is_content_hash(value: object) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    return all(character in "0123456789abcdef" for character in value)


@dataclass(frozen=True)
class FileLifecycleDecision:
    status: str
    reason: str


def classify_rendered_file(
    *,
    lifecycle: str,
    exists: bool,
    current_hash: str | None,
    rendered_hash: str,
    prior_applied_hash: str | None,
    force: bool,
    reset_project_knowledge: bool,
) -> FileLifecycleDecision:
    if lifecycle not in RENDERED_FILE_LIFECYCLES:
        raise ValueError(f"Unsupported rendered-file lifecycle: {lifecycle}")

    if not exists:
        return FileLifecycleDecision("written", "missing")

    if current_hash == rendered_hash:
        return FileLifecycleDecision("unchanged", "matches rendered content")

    if lifecycle == MANAGED:
        if force:
            return FileLifecycleDecision("overwritten", "managed update requested")
        return FileLifecycleDecision("skipped", "managed file differs and force is disabled")

    if reset_project_knowledge:
        return FileLifecycleDecision("reset", "seeded knowledge reset explicitly requested")

    if is_content_hash(prior_applied_hash) and current_hash == prior_applied_hash:
        return FileLifecycleDecision("updated", "seed is unchanged since its last application")

    if is_content_hash(prior_applied_hash):
        return FileLifecycleDecision("preserved", "seeded content has project drift")
    return FileLifecycleDecision("preserved", "seeded content has no trusted applied provenance")
