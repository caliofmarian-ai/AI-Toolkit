from __future__ import annotations

from dataclasses import dataclass

from lib.python.engineering_engine.semantic_repository_builder import (
    SemanticRepositoryBuilder,
)
from lib.python.engineering_engine.dependency_reasoning_engine import (
    DependencyReasoningEngine,
)
from lib.python.engineering_engine.impact_reasoning_engine import (
    ImpactReasoningEngine,
)
from lib.python.engineering_engine.recommendation_engine import (
    RecommendationEngine,
)
from lib.python.engineering_engine.execution_plan_engine import (
    ExecutionPlanEngine,
)
from lib.python.engineering_engine.validation_plan_engine import (
    ValidationPlanEngine,
)


@dataclass(slots=True)
class EngineeringWorkflowResult:

    impact: object

    recommendation: object

    execution: object

    validation: object


class EngineeringWorkflowEngine:

    def __init__(self, root):
        self.root = root

    def analyse(
        self,
        module: str,
    ) -> EngineeringWorkflowResult:

        repository = SemanticRepositoryBuilder(
            self.root
        ).build()

        dependency = DependencyReasoningEngine(
            repository
        )

        impact = ImpactReasoningEngine(
            dependency
        ).analyse(module)

        recommendation = RecommendationEngine().generate(
            impact
        )

        execution = ExecutionPlanEngine().build(
            recommendation
        )

        validation = ValidationPlanEngine().build(
            execution
        )

        return EngineeringWorkflowResult(
            impact=impact,
            recommendation=recommendation,
            execution=execution,
            validation=validation,
        )
