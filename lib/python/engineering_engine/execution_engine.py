from __future__ import annotations

from pathlib import Path

from lib.python.engineering_engine.execution_package_generator import (
    ExecutionPackageGenerator,
)
from lib.python.engineering_engine.planning_engine import PlanningEngine


class ExecutionEngine:

    def __init__(self, root: Path):
        self.root = root
        self.planning = PlanningEngine(root)
        self.generator = ExecutionPackageGenerator(root)

    def generate(self, core: str):

        batches = self.planning.plan(core)

        generated = []

        for batch in batches:

            path = self.generator.generate(
                core=core,
                batch=batch.batch,
                objective=batch.objective,
                affected_modules=batch.affected_modules,
                suggested_tests=batch.suggested_tests,
                acceptance=[
                    "Validation Engine passes.",
                    "Review Engine passes.",
                    "Canonical compliance preserved.",
                ],
            )

            generated.append(path)

        return generated
