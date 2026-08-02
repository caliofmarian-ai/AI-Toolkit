from pathlib import Path

from .models import Dependency


class DependencyEngine:

    def __init__(self, root="."):

        self.root = Path(root).resolve()

    def discover(self):

        dependencies = []

        for file in self.root.rglob("*"):

            if not file.is_file():
                continue

            if ".git" in file.parts:
                continue

            if "__pycache__" in file.parts:
                continue

            parent = str(file.parent.relative_to(self.root))

            dependencies.append(
                Dependency(
                    source=parent if parent else ".",
                    target=str(file.relative_to(self.root)),
                    dependency_type="contains"
                )
            )

        return dependencies

    def statistics(self):

        deps = self.discover()

        return {
            "dependencies": len(deps),
            "directories": len(set(d.source for d in deps)),
            "files": len(set(d.target for d in deps))
        }
