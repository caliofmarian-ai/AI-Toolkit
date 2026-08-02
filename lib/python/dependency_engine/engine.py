import os
from pathlib import Path

from .models import Dependency


class DependencyEngine:

    def __init__(self, root=".", workspace_index=None):

        self.root = Path(root).resolve()
        self._workspace_index = workspace_index

    def _get_index(self):
        if self._workspace_index is not None:
            return self._workspace_index
        from python.workspace_index import WorkspaceIndexBuilder
        return WorkspaceIndexBuilder(self.root).build()

    def discover(self):

        index = self._get_index()

        dependencies = []

        for f in index.files:
            parent = os.path.dirname(f.path) or "."
            dependencies.append(
                Dependency(
                    source=parent,
                    target=f.path,
                    dependency_type="contains",
                )
            )

        return dependencies

    def statistics(self):

        deps = self.discover()

        return {
            "dependencies": len(deps),
            "directories": len(set(d.source for d in deps)),
            "files": len(set(d.target for d in deps)),
        }
