from __future__ import annotations

from dataclasses import dataclass, field

from lib.python.engineering_engine.dependency_graph import DependencyGraph


@dataclass
class ImpactReport:
    target: str
    affected: set[str] = field(default_factory=set)


class ImpactAnalysis:

    def __init__(self, graph: DependencyGraph):
        self.graph = graph

    def analyse(self, module: str) -> ImpactReport:

        report = ImpactReport(target=module)

        reverse = {}

        for source, deps in self.graph.graph.items():
            for dep in deps:
                reverse.setdefault(dep, set()).add(source)

        stack = list(reverse.get(module, set()))

        while stack:

            current = stack.pop()

            if current in report.affected:
                continue

            report.affected.add(current)

            stack.extend(reverse.get(current, set()))

        return report
