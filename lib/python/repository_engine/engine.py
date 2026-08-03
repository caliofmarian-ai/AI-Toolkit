from pathlib import Path

from .models import RepositoryItem


class RepositoryEngine:

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

        inventory = []

        for f in index.files:
            inventory.append(
                RepositoryItem(
                    path=f.path,
                    name=f.name,
                    item_type="file",
                    size=f.size,
                )
            )

        for d in index.directories:
            inventory.append(
                RepositoryItem(
                    path=d.path,
                    name=d.name,
                    item_type="directory",
                    size=0,
                )
            )

        return inventory

    def statistics(self):

        index = self._get_index()

        return {
            "items": index.statistics.total_files + index.statistics.total_directories,
            "files": index.statistics.total_files,
            "directories": index.statistics.total_directories,
        }
