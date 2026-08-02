from pathlib import Path


class TradingSignalsProfile:

    NAME = "Trading Signals Platform"

    CANONICAL_DIR = "docs/canonical"

    REQUIRED_CANONICAL = [
        "SYSTEM_ARCHITECTURE_MAP",
        "SYSTEM_INVARIANTS",
        "ALGO_SPEC",
        "SIGNAL_ENGINE_EXECUTION_SPEC",
        "SIGNAL_DISTRIBUTION_SPEC",
        "OBSERVABILITY_SPEC",
        "PERFORMANCE_ANALYTICS_SPEC",
    ]

    def inspect(self, repository):

        root = Path(repository)

        report = {
            "profile": self.NAME,
            "canonical_found": [],
            "canonical_missing": [],
        }

        canonical = root / self.CANONICAL_DIR

        if canonical.exists():

            files = [
                p.name
                for p in canonical.glob("*.md")
            ]

            for item in self.REQUIRED_CANONICAL:

                found = False

                for filename in files:

                    if item in filename:

                        report["canonical_found"].append(item)
                        found = True
                        break

                if not found:
                    report["canonical_missing"].append(item)

        else:

            report["canonical_missing"] = self.REQUIRED_CANONICAL.copy()

        return report
