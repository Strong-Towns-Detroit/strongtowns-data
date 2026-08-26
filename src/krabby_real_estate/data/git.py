"""Producer Git-state capture and promotion guard."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GitState:
    commit: str | None
    clean: bool


def git_state(repository: Path) -> GitState:
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        check=False,
        capture_output=True,
        text=True,
    )
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repository,
        check=False,
        capture_output=True,
        text=True,
    )
    return GitState(
        commit=commit.stdout.strip() if commit.returncode == 0 else None,
        clean=status.returncode == 0 and not status.stdout.strip(),
    )
