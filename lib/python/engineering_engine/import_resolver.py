from __future__ import annotations

from pathlib import Path


class ImportResolver:

    def __init__(self, repository_root: Path):
        self.root = repository_root

        self.index = {}

        for file in (repository_root / "lib").rglob("*.py"):

            rel = file.relative_to(repository_root)

            module = ".".join(rel.with_suffix("").parts)

            self.index[module] = str(rel)

    def resolve(self, imported: str) -> str | None:

        if imported in self.index:
            return self.index[imported]

        for module, path in self.index.items():

            if module.endswith(imported):
                return path

        return None
