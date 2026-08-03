from __future__ import annotations

from lib.python.engineering_engine.knowledge_graph import (
    KnowledgeGraph,
)


class ScopeDetector:

    def __init__(self, root=None):
        self.root = root

    def detect(
        self,
        graph: KnowledgeGraph,
    ) -> list[str]:

        scope = []

        if graph.modules:
            scope.append("Runtime Modules")

        if graph.interfaces:
            scope.append("Runtime Interfaces")

        if graph.classes:
            scope.append("Python Components")

        if graph.functions:
            scope.append("Engineering Services")

        return sorted(scope)
