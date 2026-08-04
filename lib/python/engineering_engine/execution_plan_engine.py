from __future__ import annotations

from dataclasses import dataclass, field

from lib.python.engineering_engine.recommendation_engine import (
    RecommendationReport,
)


@dataclass(slots=True)
class ExecutionPlan:

    target: str

    risk: str

    phases: list[str] = field(default_factory=list)


class ExecutionPlanEngine:

    def build(
        self,
        report: RecommendationReport,
    ) -> ExecutionPlan:

        phases = [
            "Review impacted modules",
            "Implement required changes",
        ]

        if report.risk == "HIGH":
            phases.extend([
                "Run complete regression suite",
                "Execute full validation",
                "Engineering review",
                "Approve merge",
            ])

        elif report.risk == "MEDIUM":
            phases.extend([
                "Run affected tests",
                "Validate interfaces",
                "Approve merge",
            ])

        else:
            phases.extend([
                "Run local tests",
                "Approve merge",
            ])

        return ExecutionPlan(
            target=report.target,
            risk=report.risk,
            phases=phases,
        )
