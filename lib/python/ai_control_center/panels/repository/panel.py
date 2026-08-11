"""
AI Control Center

Repository Panel

Unified Repository View
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class RepositoryPanel:

    root: Path

    @classmethod
    def discover(cls, path: str | Path) -> "RepositoryPanel":
        return cls(Path(path).resolve())

    @property
    def name(self) -> str:
        return self.root.name

    @property
    def path(self) -> str:
        return str(self.root)

    @property
    def git_repository(self) -> bool:
        return (self.root / ".git").exists()

    def summary(self) -> dict:

        return {
            "name": self.name,
            "path": self.path,
            "git_repository": self.git_repository,
        }
