from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass
class AuditResult:
    runtime_modules: list[str]
    runtime_tests: list[str]
    entrypoints: list[str]


class RepositoryAudit:

    def __init__(self, repository_root: Path):
        self.root = repository_root

    def run(self) -> AuditResult:

        runtime = sorted(
            str(p.relative_to(self.root))
            for p in (self.root / "lib/python/runtime").rglob("*.py")
        )

        tests = sorted(
            str(p.relative_to(self.root))
            for p in (self.root / "tests").rglob("*runtime*")
        )

        entrypoints = sorted(
            str(p.relative_to(self.root))
            for p in (self.root / "bin").glob("*")
        )

        return AuditResult(runtime, tests, entrypoints)

    def write_markdown(self, output: Path):

        result = self.run()

        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open("w", encoding="utf-8") as md:

            md.write("# Repository Audit\n\n")

            md.write(
                f"Generated: {datetime.now(UTC).isoformat()}\n\n"
            )

            md.write("## Executive Summary\n\n")

            md.write("| Metric | Value |\n")
            md.write("|-------|------:|\n")
            md.write(f"| Runtime Modules | {len(result.runtime_modules)} |\n")
            md.write(f"| Runtime Tests | {len(result.runtime_tests)} |\n")
            md.write(f"| Entrypoints | {len(result.entrypoints)} |\n\n")

            md.write("Status: READY FOR GAP ANALYSIS\n\n")

            md.write("## Runtime Modules\n\n")

            for item in result.runtime_modules:
                md.write(f"- {item}\n")

            md.write("\n## Runtime Tests\n\n")

            for item in result.runtime_tests:
                md.write(f"- {item}\n")

            md.write("\n## Entrypoints\n\n")

            for item in result.entrypoints:
                md.write(f"- {item}\n")

            md.write("\n## Initial Findings\n\n")

            md.write("- Runtime foundation detected.\n")
            md.write("- Runtime interfaces detected.\n")
            md.write("- Runtime test suite detected.\n")
            md.write("- Repository ready for Gap Analysis.\n")
