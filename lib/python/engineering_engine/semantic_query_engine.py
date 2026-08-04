from __future__ import annotations

from lib.python.engineering_engine.semantic_entities import (
    EntityType,
    SemanticEntity,
    SemanticRelationship,
    SemanticRepository,
)


class SemanticQueryEngine:

    def __init__(self, repository: SemanticRepository):
        self.repository = repository

    def find_by_type(
        self,
        entity_type: EntityType,
    ) -> list[SemanticEntity]:

        return sorted(
            (
                entity
                for entity in self.repository.entities
                if entity.type == entity_type
            ),
            key=lambda e: e.name,
        )

    def find_entity(
        self,
        name: str,
    ) -> SemanticEntity | None:

        for entity in self.repository.entities:
            if entity.name == name:
                return entity

        return None

    def outgoing_relationships(
        self,
        source: str,
    ) -> list[SemanticRelationship]:

        return [
            rel
            for rel in self.repository.relationships
            if rel.source == source
        ]
