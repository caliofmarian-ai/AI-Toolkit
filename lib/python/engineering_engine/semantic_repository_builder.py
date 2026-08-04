from __future__ import annotations

from pathlib import Path

from lib.python.engineering_engine.repository_model import (
    RepositoryKnowledgeBuilder,
)
from lib.python.engineering_engine.knowledge_graph import (
    KnowledgeGraphBuilder,
)
from lib.python.engineering_engine.semantic_entities import (
    SemanticRepository,
)
from lib.python.engineering_engine.semantic_extractor import (
    SemanticExtractor,
)
from lib.python.engineering_engine.relationship_extractor import (
    RelationshipExtractor,
)


class SemanticRepositoryBuilder:

    def __init__(self, root: Path):
        self.root = root

    def build(self) -> SemanticRepository:

        knowledge = RepositoryKnowledgeBuilder(self.root).build()

        graph = KnowledgeGraphBuilder().build(knowledge)

        repository = SemanticExtractor().extract(graph)

        repository.relationships.extend(
            RelationshipExtractor().extract(knowledge)
        )

        return repository
