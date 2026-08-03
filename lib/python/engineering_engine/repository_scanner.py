from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RepositoryModel:

    runtime_modules: list[str] = field(default_factory=list)

    runtime_interfaces: list[str] = field(default_factory=list)

    tests: list[str] = field(default_factory=list)

    entrypoints: list[str] = field(default_factory=list)

    canonical_documents: list[str] = field(default_factory=list)


class RepositoryScanner:

    def __init__(self, root: Path):
        self.root = root

    def scan(self) -> RepositoryModel:

        model = RepositoryModel()

        runtime = self.root / "lib/python/runtime"

        if runtime.exists():

            for file in runtime.rglob("*.py"):

                rel = str(file.relative_to(self.root))

                if "/interfaces/" in rel:
                    model.runtime_interfaces.append(rel)
                else:
                    model.runtime_modules.append(rel)

        tests = self.root / "tests"

        if tests.exists():

            for file in tests.rglob("*"):

                if file.is_file():
                    model.tests.append(str(file.relative_to(self.root)))

        bin_dir = self.root / "bin"

        if bin_dir.exists():

            for file in bin_dir.iterdir():

                if file.is_file():
                    model.entrypoints.append(str(file.relative_to(self.root)))

        canonical = self.root / "docs/canonical/v4"

        if canonical.exists():

            for file in canonical.glob("CANON-*.md"):

                model.canonical_documents.append(
                    str(file.relative_to(self.root))
                )

        model.runtime_modules.sort()
        model.runtime_interfaces.sort()
        model.tests.sort()
        model.entrypoints.sort()
        model.canonical_documents.sort()

        return model
