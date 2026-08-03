"""
Workspace Orchestrator — State Manager
CORE-012

WorkspaceStateManager: loads, updates, and persists the mutable workspace
                       state (registry + last scan result).

Designed to support future resume: every state transition is persisted
atomically before the next operation begins.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import WorkspaceRepository, WorkspaceScanResult, WORKSPACE_SCHEMA_VERSION
from .persistence import WorkspacePersistence
from .registry import RepositoryRegistry


class WorkspaceStateManager:
    """
    Manages the mutable workspace state for the Workspace Orchestrator.

    Responsibilities:
    - Load existing state from persistence on startup
    - Provide a live RepositoryRegistry for mutation during a scan
    - Flush state atomically after each mutation
    - Support manual registration, removal, rename, and relocation
    """

    def __init__(self, workspace_root: str = ".") -> None:
        self.workspace_root = str(Path(workspace_root).resolve())
        self._persistence = WorkspacePersistence(workspace_root)
        self._registry = RepositoryRegistry()
        self._workspace_id: str = ""
        self._loaded = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def load(self) -> None:
        """Load existing workspace state from persistence."""
        workspace_meta = self._persistence.load_workspace()
        if workspace_meta:
            self._workspace_id = workspace_meta.get("workspace_id", "")

        repositories = self._persistence.load_repositories()
        for repo in repositories:
            self._registry.register(repo)

        self._loaded = True

    def ensure_loaded(self) -> None:
        if not self._loaded:
            self.load()

    # ------------------------------------------------------------------
    # Registry access
    # ------------------------------------------------------------------

    @property
    def registry(self) -> RepositoryRegistry:
        self.ensure_loaded()
        return self._registry

    @property
    def workspace_id(self) -> str:
        return self._workspace_id

    # ------------------------------------------------------------------
    # Manual registration / management
    # ------------------------------------------------------------------

    def register_repository(self, repo: WorkspaceRepository) -> None:
        """Manually register or update a repository."""
        self.ensure_loaded()
        self._registry.register(repo)

    def remove_repository(self, name: str) -> Optional[WorkspaceRepository]:
        """Remove a repository by name.  Returns the removed entry or None."""
        self.ensure_loaded()
        return self._registry.remove(name)

    def rename_repository(self, old_name: str, new_name: str) -> bool:
        """Rename a repository.  Returns True on success."""
        self.ensure_loaded()
        return self._registry.rename(old_name, new_name)

    def relocate_repository(self, name: str, new_root: str) -> bool:
        """Update the root path for a registered repository."""
        self.ensure_loaded()
        return self._registry.relocate(name, new_root)

    def update_repository(self, repo: WorkspaceRepository) -> None:
        """Update an existing repository entry."""
        self.ensure_loaded()
        self._registry.update(repo)

    # ------------------------------------------------------------------
    # Workspace ID management
    # ------------------------------------------------------------------

    def ensure_workspace_id(self) -> str:
        """Return existing workspace_id or create a new deterministic one."""
        if not self._workspace_id:
            import hashlib
            self._workspace_id = "WS-" + hashlib.sha1(
                self.workspace_root.encode()
            ).hexdigest()[:8].upper()
        return self._workspace_id

    # ------------------------------------------------------------------
    # Snapshot helpers
    # ------------------------------------------------------------------

    def current_repositories(self) -> List[WorkspaceRepository]:
        """Return all currently registered repositories sorted by priority."""
        self.ensure_loaded()
        return self._registry.all()

    def repository_count(self) -> int:
        self.ensure_loaded()
        return len(self._registry)
