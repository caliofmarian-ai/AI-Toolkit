from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from lib.python.engineering_engine.repository_model import RepositoryKnowledge
from lib.python.engineering_engine.import_resolver import ImportResolver


@dataclass
class DependencyGraph:
    graph: dict[str, set[str]] = field(default_factory=dict)


class DependencyGraphBuilder:

    def __init__(self, root: Path):
        self.resolver = ImportResolver(root)

    def build(self, knowledge: RepositoryKnowledge) -> DependencyGraph:

        graph = DependencyGraph()

        for module_path, module in knowledge.modules.items():

            graph.graph[module_path] = set()

            for imported in module.imports:

                resolved = self.resolver.resolve(imported)

                if resolved is None:
                    continue

                if resolved == module_path:
                    continue

                graph.graph[module_path].add(resolved)

        return graph
