from __future__ import annotations

from lib.python.engineering_engine.knowledge_graph import KnowledgeGraph
from lib.python.engineering_engine.semantic_entities import (
    EntityType,
    SemanticEntity,
    SemanticRepository,
)


class SemanticExtractor:

    def extract(
        self,
        graph: KnowledgeGraph,
    ) -> SemanticRepository:

        repo = SemanticRepository()

        for module in sorted(graph.modules):
            repo.entities.append(
                SemanticEntity(
                    id=module,
                    type=EntityType.MODULE,
                    name=module,
                )
            )

        for cls in sorted(graph.classes):
            repo.entities.append(
                SemanticEntity(
                    id=f"class:{cls}",
                    type=EntityType.CLASS,
                    name=cls,
                )
            )

        for fn in sorted(graph.functions):
            repo.entities.append(
                SemanticEntity(
                    id=f"function:{fn}",
                    type=EntityType.FUNCTION,
                    name=fn,
                )
            )

        return repo
