from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
import subprocess


@dataclass
class ValidationResult:
    passed: int
    failed: int


class ValidationEngine:

    TESTS = [
        "tests/test_runtime_bootstrap.sh",
        "tests/test_runtime_health.sh",
        "tests/test_runtime_lifecycle.sh",
        "tests/test_runtime_scheduler.sh",
        "tests/test_runtime_shutdown.sh",
        "tests/test_runtime_webhooks.sh",
        "tests/test_runtime_telegram.sh",
    ]

    def __init__(self, root: Path):
        self.root = root

    def validate(self, core: str) -> ValidationResult:

        passed = 0
        failed = 0

        report = (
            self.root
            / "implementation-packages"
            / core
            / "validation-report.md"
        )

        report.parent.mkdir(parents=True, exist_ok=True)

        with report.open("w", encoding="utf-8") as md:

            md.write("# Validation Report\n\n")
            md.write(f"Generated: {datetime.now(UTC).isoformat()}\n\n")

            for test in self.TESTS:

                md.write(f"## {test}\n\n")

                result = subprocess.run(
                    ["bash", test],
                    cwd=self.root,
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    passed += 1
                    md.write("Status: PASSED\n\n")
                else:
                    failed += 1
                    md.write("Status: FAILED\n\n")

                md.write("```text\n")
                md.write(result.stdout)
                md.write(result.stderr)
                md.write("\n```\n\n")

            md.write("---\n\n")
            md.write(f"Passed: {passed}\n")
            md.write(f"Failed: {failed}\n")

        return ValidationResult(
            passed=passed,
            failed=failed,
        )
