"""
Workspace Index — Data Models

Immutable data model for the canonical repository representation.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkspaceFile:
    """Immutable representation of a single repository file."""

    path: str
    name: str
    size: int
    extension: str


@dataclass(frozen=True)
class WorkspaceDirectory:
    """Immutable representation of a single repository directory."""

    path: str
    name: str


@dataclass(frozen=True)
class WorkspaceStatistics:
    """Performance and coverage metrics collected during a single traversal."""

    total_files: int
    total_directories: int
    ignored_files: int
    ignored_directories: int
    scan_duration: float
    files_per_second: float


class WorkspaceIndex:
    """
    Canonical immutable in-memory representation of a repository.

    Created exclusively by WorkspaceIndexBuilder.
    Read-only after construction — mutation raises AttributeError.
    """

    def __init__(
        self,
        repository_name,
        repository_root,
        files,
        directories,
        ignored_files,
        ignored_dirs,
        statistics,
        created_at,
    ):
        object.__setattr__(self, "_repository_name", repository_name)
        object.__setattr__(self, "_repository_root", str(repository_root))
        object.__setattr__(self, "_files", tuple(files))
        object.__setattr__(self, "_directories", tuple(directories))
        object.__setattr__(self, "_ignored_files", tuple(ignored_files))
        object.__setattr__(self, "_ignored_dirs", tuple(ignored_dirs))
        object.__setattr__(self, "_statistics", statistics)
        object.__setattr__(self, "_created_at", created_at)
        object.__setattr__(self, "_locked", True)

    def __setattr__(self, name, value):
        if getattr(self, "_locked", False):
            raise AttributeError(
                "WorkspaceIndex is immutable and cannot be modified after construction."
            )
        object.__setattr__(self, name, value)

    # -------------------------------------------------------------------------
    # Repository identity
    # -------------------------------------------------------------------------

    @property
    def repository_name(self):
        return self._repository_name

    @property
    def repository_root(self):
        return self._repository_root

    @property
    def created_at(self):
        return self._created_at

    # -------------------------------------------------------------------------
    # Filesystem collections
    # -------------------------------------------------------------------------

    @property
    def files(self):
        return self._files

    @property
    def directories(self):
        return self._directories

    @property
    def ignored_files(self):
        return self._ignored_files

    @property
    def ignored_dirs(self):
        return self._ignored_dirs

    @property
    def statistics(self):
        return self._statistics

    # -------------------------------------------------------------------------
    # Categorized file views (no new I/O)
    # -------------------------------------------------------------------------

    def files_by_extension(self, *extensions):
        """Return all files whose extension matches any of the given extensions."""
        ext_set = set(extensions)
        return tuple(f for f in self._files if f.extension in ext_set)

    def python_files(self):
        return self.files_by_extension(".py")

    def markdown_files(self):
        return self.files_by_extension(".md")

    def shell_scripts(self):
        return self.files_by_extension(".sh")

    def json_files(self):
        return self.files_by_extension(".json")

    def yaml_files(self):
        return self.files_by_extension(".yml", ".yaml")

    def test_files(self):
        return tuple(f for f in self._files if f.name.startswith("test_"))

    def canonical_documents(self):
        return tuple(
            f for f in self.markdown_files()
            if "canonical" in f.path.replace("\\", "/")
        )

    def files_matching(self, predicate):
        """Return all files for which predicate(WorkspaceFile) is True."""
        return tuple(f for f in self._files if predicate(f))

    # -------------------------------------------------------------------------
    # Statistics helpers
    # -------------------------------------------------------------------------

    def extension_histogram(self):
        """Return a dict mapping file extension → count."""
        histogram = {}
        for f in self._files:
            key = f.extension if f.extension else "(no ext)"
            histogram[key] = histogram.get(key, 0) + 1
        return histogram

    def largest_directories(self, top_n=10):
        """Return the top_n directories by contained file count."""
        counts = {}
        for f in self._files:
            import os
            parent = os.path.dirname(f.path) or "."
            counts[parent] = counts.get(parent, 0) + 1
        return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_n]

    # -------------------------------------------------------------------------
    # Representation
    # -------------------------------------------------------------------------

    def __repr__(self):
        return (
            f"WorkspaceIndex("
            f"repository={self._repository_name!r}, "
            f"files={len(self._files)}, "
            f"directories={len(self._directories)})"
        )
