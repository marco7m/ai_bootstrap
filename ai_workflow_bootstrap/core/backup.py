from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


def backup_path(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return path.with_suffix(path.suffix + f".bak-{timestamp}")


def create_backup(path: Path, *, dry_run: bool = False) -> Path:
    backup = backup_path(path)
    if not dry_run:
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
    return backup

