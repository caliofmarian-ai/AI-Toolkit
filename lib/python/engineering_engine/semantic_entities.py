from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class EntityType(str, Enum):

    REPOSITORY = "repository"
    MODULE = "module"
    ENGINE = "engine"
    CLASS = "class"
    FUNCTION = "function"
    INTERFACE = "interface"
    CAPABILITY = "capability"
    ARTIFACT = "artifact"
    CANON = "canon"
    RULE = "rule"
    BATCH = "batch"


@dataclass(slots=True)
class SemanticEntity:

    id: str

    type: EntityType

    name: str

    attributes: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class SemanticRelationship:

    source: str

    relationship: str

    target: str


@dataclass(slots=True)
class SemanticRepository:

    entities: list[SemanticEntity] = field(default_factory=list)

    relationships: list[SemanticRelationship] = field(default_factory=list)
