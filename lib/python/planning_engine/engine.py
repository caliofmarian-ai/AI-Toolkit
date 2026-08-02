from .models import ExecutionPlan, PlanningTask

from python.repository_engine.engine import RepositoryEngine
from python.dependency_engine.engine import DependencyEngine
from python.validation_engine.engine import ValidationEngine


class PlanningEngine:

    def __init__(self, root="."):

        self.repository = RepositoryEngine(root)
        self.dependencies = DependencyEngine(root)
        self.validation = ValidationEngine(root)

    def build_plan(self):

        plan = ExecutionPlan(
            identifier="PLAN-001"
        )

        stats = self.repository.statistics()

        plan.tasks.append(
            PlanningTask(
                identifier="TASK-REPOSITORY",
                title=f"Inspect {stats['files']} files",
                priority="HIGH"
            )
        )

        deps = self.dependencies.statistics()

        plan.tasks.append(
            PlanningTask(
                identifier="TASK-DEPENDENCIES",
                title=f"Validate {deps['dependencies']} dependencies",
                priority="HIGH"
            )
        )

        validation = self.validation.statistics()

        plan.tasks.append(
            PlanningTask(
                identifier="TASK-VALIDATION",
                title=f"Execute {validation['checks']} validation checks",
                priority="HIGH"
            )
        )

        return plan
