"""
Workspace Index

Canonical in-memory representation of the repository.
Produced by a single filesystem traversal.
"""

from .models import WorkspaceFile, WorkspaceDirectory, WorkspaceStatistics, WorkspaceIndex
from .policy import RepositoryPolicy
from .builder import WorkspaceIndexBuilder
from .exporter import WorkspaceIndexExporter
from .incremental import (
    FileSnapshot,
    RepositorySnapshot,
    IndexDelta,
    IncrementalStats,
    IncrementalBuildResult,
    ChangeDetector,
    IncrementalWorkspaceIndex,
    CACHE_VERSION,
)

__all__ = [
    "WorkspaceFile",
    "WorkspaceDirectory",
    "WorkspaceStatistics",
    "WorkspaceIndex",
    "RepositoryPolicy",
    "WorkspaceIndexBuilder",
    "WorkspaceIndexExporter",
    "FileSnapshot",
    "RepositorySnapshot",
    "IndexDelta",
    "IncrementalStats",
    "IncrementalBuildResult",
    "ChangeDetector",
    "IncrementalWorkspaceIndex",
    "CACHE_VERSION",
]
