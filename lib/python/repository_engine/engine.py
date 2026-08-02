from pathlib import Path

from .models import RepositoryItem


class RepositoryEngine:

    def __init__(self, root="."):

        self.root = Path(root).resolve()

    def discover(self):

        inventory = []

        for item in self.root.rglob("*"):

            if ".git" in item.parts:
                continue

            if "__pycache__" in item.parts:
                continue

            inventory.append(
                RepositoryItem(
                    path=str(item.relative_to(self.root)),
                    name=item.name,
                    item_type="directory" if item.is_dir() else "file",
                    size=item.stat().st_size if item.is_file() else 0,
                )
            )

        return inventory

    def statistics(self):

        inventory = self.discover()

        return {
            "items": len(inventory),
            "files": sum(1 for i in inventory if i.item_type == "file"),
            "directories": sum(1 for i in inventory if i.item_type == "directory"),
        }
