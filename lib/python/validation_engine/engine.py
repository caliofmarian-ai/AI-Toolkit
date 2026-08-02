from pathlib import Path

from .models import ValidationResult


class ValidationEngine:

    def __init__(self, root="."):

        self.root = Path(root).resolve()

    def validate(self):

        results = []

        required = [
            "docs/canonical",
            "development",
            "tests",
            "lib",
            "bin"
        ]

        for path in required:

            target = self.root / path

            results.append(
                ValidationResult(
                    identifier=f"VAL-{path.replace('/','_').upper()}",
                    target=path,
                    passed=target.exists(),
                    message="Present" if target.exists() else "Missing",
                    severity="ERROR" if not target.exists() else "INFO"
                )
            )

        return results

    def statistics(self):

        results = self.validate()

        return {
            "checks": len(results),
            "passed": sum(r.passed for r in results),
            "failed": sum(not r.passed for r in results)
        }
