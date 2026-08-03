from __future__ import annotations

from pathlib import Path
from datetime import UTC, datetime


class ExecutionPackageGenerator:

    def __init__(self, root: Path):
        self.root = root

    def generate(
        self,
        core: str,
        batch: str,
        objective: str,
        affected_modules: list[str],
        suggested_tests: list[str],
        acceptance: list[str],
    ):

        package = self.root / "implementation-packages" / core
        package.mkdir(parents=True, exist_ok=True)

        output = package / f"{batch}-execution-package.md"

        with output.open("w", encoding="utf-8") as md:

            md.write("# Execution Package\n\n")

            md.write(f"Generated: {datetime.now(UTC).isoformat()}\n\n")

            md.write(f"CORE: {core}\n")
            md.write(f"BATCH: {batch}\n\n")

            md.write("## Objective\n\n")
            md.write(objective + "\n\n")

            md.write("## Affected Modules\n\n")
            if affected_modules:
                for module in affected_modules:
                    md.write(f"- {module}\n")
            else:
                md.write("- None\n")

            md.write("\n## Suggested Tests\n\n")
            if suggested_tests:
                for test in suggested_tests:
                    md.write(f"- {test}\n")
            else:
                md.write("- None\n")

            md.write("\n## Acceptance Criteria\n\n")
            for item in acceptance:
                md.write(f"- {item}\n")

            md.write("\n## Validation\n\n")
            md.write("- Repository builds successfully.\n")
            md.write("- Validation Engine passes.\n")
            md.write("- Review Engine passes.\n")
            md.write("- Canonical compliance preserved.\n")

            md.write("\n## Status\n\n")
            md.write("READY FOR EXECUTION\n")

        return output
