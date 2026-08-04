from __future__ import annotations

from lib.python.engineering_engine.semantic_entities import (
    EntityType,
    SemanticRepository,
)


class SemanticClassifier:

    def classify(
        self,
        repository: SemanticRepository,
    ) -> SemanticRepository:

        for entity in repository.entities:

            name = entity.name

            if entity.type == EntityType.CLASS:

                if name.endswith("Engine"):
                    entity.type = EntityType.ENGINE

                elif name.endswith("Interface"):
                    entity.type = EntityType.INTERFACE

                elif name.endswith("Rule"):
                    entity.type = EntityType.RULE

                elif name.endswith("Batch"):
                    entity.type = EntityType.BATCH

        return repository
