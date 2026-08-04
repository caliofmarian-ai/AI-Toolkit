from __future__ import annotations

from dataclasses import dataclass, field

from lib.python.engineering_engine.impact_reasoning_engine import (
    ImpactReport,
)


@dataclass(slots=True)
class RecommendationReport:

    target: str

    risk: str

    recommendations: list[str] = field(default_factory=list)


class RecommendationEngine:

    def generate(
        self,
        report: ImpactReport,
    ) -> RecommendationReport:

        recommendations = []

        if report.risk == "HIGH":

            recommendations.extend([
                "Run complete regression test suite.",
                "Review all transitive dependents.",
                "Perform full validation before merge.",
                "Require engineering review.",
            ])

        elif report.risk == "MEDIUM":

            recommendations.extend([
                "Run affected module tests.",
                "Review direct dependents.",
                "Validate impacted interfaces.",
            ])

        else:

            recommendations.extend([
                "Run local unit tests.",
                "Verify module behaviour.",
            ])

        return RecommendationReport(
            target=report.target,
            risk=report.risk,
            recommendations=recommendations,
        )
