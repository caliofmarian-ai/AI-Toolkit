"""
Workspace Index Exporter

Serialization helpers for WorkspaceIndex.
"""

import json
from pathlib import Path


class WorkspaceIndexExporter:
    """Serialises a WorkspaceIndex to JSON."""

    @staticmethod
    def to_dict(index):
        stats = index.statistics
        return {
            "repository_name": index.repository_name,
            "repository_root": index.repository_root,
            "created_at": index.created_at,
            "statistics": {
                "total_files": stats.total_files,
                "total_directories": stats.total_directories,
                "ignored_files": stats.ignored_files,
                "ignored_directories": stats.ignored_directories,
                "scan_duration": stats.scan_duration,
                "files_per_second": stats.files_per_second,
            },
            "files": [
                {
                    "path": f.path,
                    "name": f.name,
                    "size": f.size,
                    "extension": f.extension,
                }
                for f in index.files
            ],
            "directories": [
                {"path": d.path, "name": d.name}
                for d in index.directories
            ],
            "ignored_files": [
                {
                    "path": f.path,
                    "name": f.name,
                    "size": f.size,
                    "extension": f.extension,
                }
                for f in index.ignored_files
            ],
            "ignored_dirs": [
                {"path": d.path, "name": d.name}
                for d in index.ignored_dirs
            ],
            "extension_histogram": index.extension_histogram(),
        }

    @staticmethod
    def export(index, filename):
        data = WorkspaceIndexExporter.to_dict(index)
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return data
