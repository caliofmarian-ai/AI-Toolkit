"""
Workspace Index Builder

Sole authority for filesystem traversal.

Only WorkspaceIndexBuilder may call os.walk() / Path.rglob() / glob().
All other components consume the resulting WorkspaceIndex.
"""

import os
import time
from pathlib import Path

from .models import WorkspaceFile, WorkspaceDirectory, WorkspaceStatistics, WorkspaceIndex
from .policy import RepositoryPolicy


class WorkspaceIndexBuilder:
    """
    Performs exactly one filesystem traversal and produces an immutable
    WorkspaceIndex.

    Usage
    -----
    builder = WorkspaceIndexBuilder(root=".", policy=RepositoryPolicy())
    index   = builder.build()
    """

    def __init__(self, root=".", policy=None):
        self.root = Path(root).resolve()
        self.policy = policy if policy is not None else RepositoryPolicy()

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def build(self):
        """
        Traverse the repository exactly once and return an immutable
        WorkspaceIndex containing all discovered files and directories.
        """
        started = time.perf_counter()

        files = []
        directories = []
        ignored_files = []
        ignored_dirs = []

        for dirpath, dirnames, filenames in os.walk(str(self.root), topdown=True):

            current_dir = Path(dirpath)
            current_rel = current_dir.relative_to(self.root)
            current_parts = current_rel.parts

            # Prune excluded directories so os.walk never descends into them.
            # Partition dirnames into kept and excluded in-place.
            kept = []
            for d in dirnames:
                if self.policy.is_excluded_dir(d) or self.policy.should_prune(current_parts + (d,)):
                    rel = str(current_rel / d) if str(current_rel) != "." else d
                    ignored_dirs.append(
                        WorkspaceDirectory(
                            path=rel,
                            name=d,
                        )
                    )
                else:
                    kept.append(d)
            dirnames[:] = kept

            # Record the current directory itself (skip the root)
            if str(current_rel) != ".":
                directories.append(
                    WorkspaceDirectory(
                        path=str(current_rel),
                        name=current_dir.name,
                    )
                )

            # Record files
            for filename in filenames:
                file_path = current_dir / filename
                ext = file_path.suffix

                if self.policy.is_excluded_file(filename, ext):
                    rel = str(current_rel / filename) if str(current_rel) != "." else filename
                    ignored_files.append(
                        WorkspaceFile(
                            path=rel,
                            name=filename,
                            size=0,
                            extension=ext,
                        )
                    )
                    continue

                try:
                    size = file_path.stat().st_size
                except OSError:
                    size = 0

                rel = str(current_rel / filename) if str(current_rel) != "." else filename
                files.append(
                    WorkspaceFile(
                        path=rel,
                        name=filename,
                        size=size,
                        extension=ext,
                    )
                )

        elapsed = time.perf_counter() - started
        files_per_second = len(files) / elapsed if elapsed > 0 else float(len(files))

        statistics = WorkspaceStatistics(
            total_files=len(files),
            total_directories=len(directories),
            ignored_files=len(ignored_files),
            ignored_directories=len(ignored_dirs),
            scan_duration=round(elapsed, 6),
            files_per_second=round(files_per_second, 2),
        )

        return WorkspaceIndex(
            repository_name=self.root.name,
            repository_root=str(self.root),
            files=files,
            directories=directories,
            ignored_files=ignored_files,
            ignored_dirs=ignored_dirs,
            statistics=statistics,
            created_at=time.time(),
        )
