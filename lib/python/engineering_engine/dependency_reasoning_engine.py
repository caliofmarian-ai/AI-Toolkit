from __future__ import annotations

from collections import defaultdict

from lib.python.engineering_engine.semantic_entities import (
    SemanticRelationship,
    SemanticRepository,
)


class DependencyReasoningEngine:

    def __init__(self, repository: SemanticRepository):
        self.repository = repository

        self.forward = defaultdict(set)
        self.reverse = defaultdict(set)

        for rel in repository.relationships:

            if rel.relationship != "IMPORTS":
                continue

            self.forward[rel.source].add(rel.target)
            self.reverse[rel.target].add(rel.source)

    def dependencies_of(self, source: str) -> list[str]:

        return sorted(self.forward.get(source, set()))

    def dependents_of(self, target: str) -> list[str]:

        return sorted(self.reverse.get(target, set()))


    def transitive_dependencies_of(
        self,
        source: str,
    ) -> list[str]:

        visited = set()
        stack = [source]

        while stack:

            current = stack.pop()

            for dependency in self.forward.get(current, set()):

                if dependency in visited:
                    continue

                visited.add(dependency)
                stack.append(dependency)

        return sorted(visited)


    def transitive_dependents_of(
        self,
        target: str,
    ) -> list[str]:

        visited = set()
        stack = [target]

        while stack:

            current = stack.pop()

            for dependent in self.reverse.get(current, set()):

                if dependent in visited:
                    continue

                visited.add(dependent)
                stack.append(dependent)

        return sorted(visited)
