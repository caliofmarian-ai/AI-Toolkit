from __future__ import annotations

from pathlib import Path

from lib.python.engineering_engine.repository_model import (
    RepositoryKnowledgeBuilder,
)


class ScopeDetector:

    def __init__(self, root: Path):
        self.root = root

    def detect(self) -> list[str]:

        knowledge = RepositoryKnowledgeBuilder(self.root).build()

        scope = []

        if knowledge.modules:
            scope.append("Runtime Modules")

        has_interfaces = any(
            "/interfaces/" in module
            for module in knowledge.modules
        )

        if has_interfaces:
            scope.append("Runtime Interfaces")

        has_classes = any(
            info.classes
            for info in knowledge.modules.values()
        )

        if has_classes:
            scope.append("Python Components")

        has_functions = any(
            info.functions
            for info in knowledge.modules.values()
        )

        if has_functions:
            scope.append("Engineering Services")

        return sorted(set(scope))
