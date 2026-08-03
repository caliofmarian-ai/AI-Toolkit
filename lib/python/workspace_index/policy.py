"""
Repository Policy

Single authority for repository inclusion and exclusion rules.

No engine may define its own ignore rules.
All filtering is delegated to RepositoryPolicy.
"""


class RepositoryPolicy:
    """
    Centralised authority for repository path filtering.

    Defines which directories, files, and extensions are excluded
    from analysis. No engine may implement its own filtering logic.
    """

    # Default directories excluded from all analysis
    DEFAULT_EXCLUDE_DIRS = frozenset([
        ".git",
        "__pycache__",
        "node_modules",
        ".node_modules",
        "venv",
        ".venv",
        "env",
        ".env",
        "build",
        "dist",
        ".cache",
        "cache",
        ".tox",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "htmlcov",
        ".eggs",
        "*.egg-info",
    ])

    # Default file extensions excluded from all analysis
    DEFAULT_EXCLUDE_EXTENSIONS = frozenset([
        ".pyc",
        ".pyo",
        ".pyd",
    ])

    def __init__(
        self,
        exclude_dirs=None,
        extra_exclude_dirs=None,
        exclude_extensions=None,
        extra_exclude_extensions=None,
    ):
        """
        Parameters
        ----------
        exclude_dirs:
            Full replacement for the default directory exclusion set.
            When None the DEFAULT_EXCLUDE_DIRS set is used.
        extra_exclude_dirs:
            Additional directories to exclude on top of the default set.
        exclude_extensions:
            Full replacement for the default extension exclusion set.
        extra_exclude_extensions:
            Additional extensions to exclude on top of the default set.
        """
        base_dirs = (
            frozenset(exclude_dirs)
            if exclude_dirs is not None
            else self.DEFAULT_EXCLUDE_DIRS
        )
        self._exclude_dirs = base_dirs | frozenset(extra_exclude_dirs or [])

        base_ext = (
            frozenset(exclude_extensions)
            if exclude_extensions is not None
            else self.DEFAULT_EXCLUDE_EXTENSIONS
        )
        self._exclude_extensions = base_ext | frozenset(extra_exclude_extensions or [])

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    @property
    def exclude_dirs(self):
        return self._exclude_dirs

    @property
    def exclude_extensions(self):
        return self._exclude_extensions

    def is_excluded_dir(self, name):
        """Return True if a directory with the given *name* should be excluded."""
        return name in self._exclude_dirs

    def is_excluded_file(self, name, extension):
        """Return True if a file should be excluded based on its extension."""
        return extension in self._exclude_extensions

    def should_prune(self, parts):
        """
        Return True if a path described by *parts* (a sequence of path
        components) should be excluded.

        Used by WorkspaceIndexBuilder during os.walk traversal.
        """
        return any(part in self._exclude_dirs for part in parts)
