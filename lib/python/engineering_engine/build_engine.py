from __future__ import annotations

from pathlib import Path

from lib.python.engineering_engine.repository_audit import RepositoryAudit
from lib.python.engineering_engine.gap_analysis import GapAnalysis
from lib.python.engineering_engine.ip_generator import (
    ImplementationPackageGenerator,
)
from lib.python.engineering_engine.validation_engine import ValidationEngine


class BuildEngine:

    def __init__(self, root: Path):
        self.root = root

    def build(self, core: str):

        package = self.root / "implementation-packages" / core
        package.mkdir(parents=True, exist_ok=True)

        print()
        print("========================================")
        print("ENGINEERING BUILD")
        print("========================================")

        print("[1/5] Repository Audit")
        RepositoryAudit(self.root).write_markdown(
            package / "repository-audit.md"
        )

        print("[2/5] Gap Analysis")
        GapAnalysis(self.root).write_markdown(
            package / "gap-analysis.md"
        )

        print("[3/5] Implementation Package")
        ImplementationPackageGenerator(self.root).generate(core)

        print("[4/5] Validation")
        ValidationEngine(self.root).validate(core)

        print("[5/5] Complete")

        print()
        print("Artifacts:")
        for file in sorted(package.glob("*")):
            print(" -", file.name)

        print()
        print("ENGINEERING BUILD COMPLETE")
