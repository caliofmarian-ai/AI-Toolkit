"""
AI Control Center

Local Repository Provider

Canonical adapter over RepositoryEngine.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from repository_engine import RepositoryEngine

from .base import Provider


class LocalRepositoryProvider(Provider):

    def __init__(self, root: str | Path):

        self._root = Path(root).resolve()

        self._engine = RepositoryEngine(str(self._root))

    @property
    def provider_id(self) -> str:
        return "local_repository"

    @property
    def provider_name(self) -> str:
        return "Local Repository"

    def available(self) -> bool:
        return (self._root / ".git").exists()

    def inventory(self):

        return self._engine.discover()

    def statistics(self):

        return self._engine.statistics()

    def profile(self):

        return self._engine.profile()

    def summary(self) -> Dict[str, Any]:

        stats = self.statistics()

        return {

            "provider": self.provider_name,

            "root": str(self._root),

            "git": self.available(),

            "statistics": stats,

        }
