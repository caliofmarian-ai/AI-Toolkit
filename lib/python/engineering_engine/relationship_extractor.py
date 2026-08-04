from __future__ import annotations

from lib.python.engineering_engine.repository_model import (
    RepositoryKnowledge,
)
from lib.python.engineering_engine.semantic_entities import (
    SemanticRelationship,
)


class RelationshipExtractor:

    def extract(
        self,
        knowledge: RepositoryKnowledge,
    ) -> list[SemanticRelationship]:

        relationships = []

        for module_path, module in sorted(knowledge.modules.items()):

            source = module_path.replace("/", ".").removesuffix(".py")

            for imported in sorted(set(module.imports)):

                if not imported:
                    continue

                relationships.append(
                    SemanticRelationship(
                        source=source,
                        relationship="IMPORTS",
                        target=imported,
                    )
                )

        return relationships
