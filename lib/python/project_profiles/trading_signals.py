from pathlib import Path
from python.discovery_engine.engine import DiscoveryEngine


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

        discovery = DiscoveryEngine(root)

        files = list(
            discovery.discover_canonical_documents().keys()
        )

            for item in self.REQUIRED_CANONICAL:

                found = False

                for filename in files:

                    if item in filename:

                        report["canonical_found"].append(item)
                        found = True
                        break

                if not found:
                    report["canonical_missing"].append(item)

        return report
