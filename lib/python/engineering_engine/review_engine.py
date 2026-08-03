from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from lib.python.engineering_engine.repository_model import RepositoryKnowledgeBuilder
from lib.python.engineering_engine.dependency_graph import DependencyGraphBuilder
from lib.python.engineering_engine.impact_analysis import ImpactAnalysis


@dataclass
class ReviewResult:
    target: str
    affected_modules: list[str]
    affected_tests: list[str]
    risk: str


class ReviewEngine:

    def __init__(self, root: Path):
        self.root = root

    def review(self, module: str) -> ReviewResult:

        knowledge = RepositoryKnowledgeBuilder(self.root).build()

        graph = DependencyGraphBuilder(self.root).build(knowledge)

        impact = ImpactAnalysis(graph).analyse(module)

        tests = []

        for test in (self.root / "tests").rglob("*"):

            if not test.is_file():
                continue

            name = test.name.lower()

            for affected in impact.affected:

                stem = Path(affected).stem.lower()

                if stem in name:
                    tests.append(str(test.relative_to(self.root)))

        count = len(impact.affected)

        if count == 0:
            risk = "LOW"
        elif count <= 5:
            risk = "MEDIUM"
        else:
            risk = "HIGH"

        return ReviewResult(
            target=module,
            affected_modules=sorted(impact.affected),
            affected_tests=sorted(set(tests)),
            risk=risk,
        )
