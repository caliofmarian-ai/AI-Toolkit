from __future__ import annotations

from dataclasses import dataclass

from lib.python.engineering_engine.dependency_reasoning_engine import (
    DependencyReasoningEngine,
)


@dataclass(slots=True)
class ImpactReport:

    target: str

    direct_dependencies: list[str]

    transitive_dependencies: list[str]

    direct_dependents: list[str]

    transitive_dependents: list[str]

    risk: str


class ImpactReasoningEngine:

    def __init__(
        self,
        dependency_engine: DependencyReasoningEngine,
    ):
        self.dependency_engine = dependency_engine

    def analyse(
        self,
        module: str,
    ) -> ImpactReport:

        direct_dependencies = self.dependency_engine.dependencies_of(module)

        transitive_dependencies = (
            self.dependency_engine.transitive_dependencies_of(module)
        )

        direct_dependents = self.dependency_engine.dependents_of(module)

        transitive_dependents = (
            self.dependency_engine.transitive_dependents_of(module)
        )

        score = (
            len(direct_dependencies)
            + len(transitive_dependencies)
            + (2 * len(direct_dependents))
            + (2 * len(transitive_dependents))
        )

        if score >= 40:
            risk = "HIGH"
        elif score >= 15:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        return ImpactReport(
            target=module,
            direct_dependencies=direct_dependencies,
            transitive_dependencies=transitive_dependencies,
            direct_dependents=direct_dependents,
            transitive_dependents=transitive_dependents,
            risk=risk,
        )
