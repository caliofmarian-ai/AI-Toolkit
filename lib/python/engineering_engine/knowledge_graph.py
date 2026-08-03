from __future__ import annotations

from dataclasses import dataclass, field

from lib.python.engineering_engine.repository_model import (
    RepositoryKnowledge,
)


@dataclass(slots=True)
class KnowledgeGraph:

    modules: set[str] = field(default_factory=set)

    interfaces: set[str] = field(default_factory=set)

    classes: set[str] = field(default_factory=set)

    functions: set[str] = field(default_factory=set)

    imports: set[str] = field(default_factory=set)


class KnowledgeGraphBuilder:

    def build(
        self,
        knowledge: RepositoryKnowledge,
    ) -> KnowledgeGraph:

        graph = KnowledgeGraph()

        for path, module in knowledge.modules.items():

            graph.modules.add(path)

            if "/interfaces/" in path:
                graph.interfaces.add(path)

            graph.classes.update(module.classes)

            graph.functions.update(module.functions)

            graph.imports.update(module.imports)

        return graph
