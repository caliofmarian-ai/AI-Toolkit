from python.discovery_engine.engine import DiscoveryEngine


class TradingSignalsProfile:

    NAME = "Trading Signals Platform"

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

        discovery = DiscoveryEngine(repository)

        discovered = list(
            discovery.discover_canonical_documents().keys()
        )

        report = {
            "profile": self.NAME,
            "canonical_found": [],
            "canonical_missing": [],
        }

        for required in self.REQUIRED_CANONICAL:

            found = False

            for document in discovered:

                if required in document:

                    report["canonical_found"].append(required)
                    found = True
                    break

            if not found:
                report["canonical_missing"].append(required)

        return report
