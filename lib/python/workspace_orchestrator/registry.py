"""
Workspace Orchestrator — Registry
CORE-012

WorkspaceRegistry: in-memory registry of known workspaces.
RepositoryRegistry: in-memory registry of repositories within a workspace.
"""

from pathlib import Path
from typing import Dict, Iterator, List, Optional

from .models import WorkspaceRepository


class RepositoryRegistry:
    """
    Registry for WorkspaceRepository instances within a single workspace.

    Provides lookup by name and root path.  All mutations are tracked for
    persistence by WorkspacePersistence.
    """

    def __init__(self) -> None:
        self._by_name: Dict[str, WorkspaceRepository] = {}
        self._by_root: Dict[str, WorkspaceRepository] = {}

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def register(self, repo: WorkspaceRepository) -> None:
        """Register or replace a repository entry."""
        self._by_name[repo.name] = repo
        self._by_root[str(Path(repo.repository_root).resolve())] = repo

    def remove(self, name: str) -> Optional[WorkspaceRepository]:
        """Remove a repository by name.  Returns the removed entry or None."""
        repo = self._by_name.pop(name, None)
        if repo is not None:
            root_key = str(Path(repo.repository_root).resolve())
            self._by_root.pop(root_key, None)
        return repo

    def rename(self, old_name: str, new_name: str) -> bool:
        """Rename a registered repository.  Returns True on success."""
        repo = self._by_name.pop(old_name, None)
        if repo is None:
            return False
        updated = WorkspaceRepository.from_dict({**repo.to_dict(), "name": new_name})
        self.register(updated)
        return True

    def relocate(self, name: str, new_root: str) -> bool:
        """Update the root path for a registered repository."""
        repo = self._by_name.get(name)
        if repo is None:
            return False
        old_key = str(Path(repo.repository_root).resolve())
        self._by_root.pop(old_key, None)
        updated = WorkspaceRepository.from_dict({**repo.to_dict(), "repository_root": new_root})
        self.register(updated)
        return True

    def update(self, repo: WorkspaceRepository) -> None:
        """Update an existing repository (full replacement by name)."""
        self.register(repo)

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(self, name: str) -> Optional[WorkspaceRepository]:
        return self._by_name.get(name)

    def get_by_root(self, root: str) -> Optional[WorkspaceRepository]:
        return self._by_root.get(str(Path(root).resolve()))

    def contains(self, name: str) -> bool:
        return name in self._by_name

    def all(self) -> List[WorkspaceRepository]:
        return sorted(self._by_name.values(), key=lambda r: r.priority)

    def names(self) -> List[str]:
        return sorted(self._by_name.keys())

    def __len__(self) -> int:
        return len(self._by_name)

    def __iter__(self) -> Iterator[WorkspaceRepository]:
        return iter(self.all())

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    def to_list(self) -> List[Dict]:
        return [r.to_dict() for r in self.all()]

    @classmethod
    def from_list(cls, items: List[Dict]) -> "RepositoryRegistry":
        registry = cls()
        for item in items:
            registry.register(WorkspaceRepository.from_dict(item))
        return registry


class WorkspaceRegistry:
    """
    Top-level registry tracking every workspace known to the AI CTO.

    Currently one workspace corresponds to a filesystem root directory that
    contains multiple git repositories.  Future versions may manage remote
    workspaces as well.
    """

    def __init__(self) -> None:
        self._workspaces: Dict[str, str] = {}   # workspace_id -> root path

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, workspace_id: str, root: str) -> None:
        self._workspaces[workspace_id] = str(Path(root).resolve())

    def remove(self, workspace_id: str) -> bool:
        return self._workspaces.pop(workspace_id, None) is not None

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get_root(self, workspace_id: str) -> Optional[str]:
        return self._workspaces.get(workspace_id)

    def workspace_ids(self) -> List[str]:
        return sorted(self._workspaces.keys())

    def __len__(self) -> int:
        return len(self._workspaces)

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, str]:
        return dict(sorted(self._workspaces.items()))

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "WorkspaceRegistry":
        registry = cls()
        for wid, root in data.items():
            registry.register(wid, root)
        return registry
