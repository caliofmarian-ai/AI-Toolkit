from __future__ import annotations

from dataclasses import dataclass, field

from lib.python.engineering_engine.execution_plan_engine import (
    ExecutionPlan,
)


@dataclass(slots=True)
class ValidationPlan:

    target: str

    risk: str

    checks: list[str] = field(default_factory=list)


class ValidationPlanEngine:

    def build(
        self,
        plan: ExecutionPlan,
    ) -> ValidationPlan:

        checks = [
            "Python compilation passes",
            "No import errors",
        ]

        if plan.risk == "HIGH":
            checks.extend([
                "Regression suite passes",
                "Impact analysis reviewed",
                "Architecture validation passes",
                "Manual engineering review completed",
            ])

        elif plan.risk == "MEDIUM":
            checks.extend([
                "Affected tests pass",
                "Dependency validation passes",
            ])

        else:
            checks.extend([
                "Local tests pass",
            ])

        return ValidationPlan(
            target=plan.target,
            risk=plan.risk,
            checks=checks,
        )
