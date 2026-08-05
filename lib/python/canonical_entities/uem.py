"""
Universal Engineering Model — Canonical Specification Language v1.0.0

The UEM is the technology-independent semantic model produced by every conforming
CSL compiler. All Engineering Artifacts are generated from the UEM.

CSL Reference: Volume VI (Universal Engineering Model)
CORE: CORE-023-005
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterator, List, Optional, Set


# ---------------------------------------------------------------------------
# Engineering Object Types (Volume VI Chapter 4)
# ---------------------------------------------------------------------------

class EngObjectType(str, Enum):
    PROJECT = "PROJECT"
    CAPABILITY = "CAPABILITY"
    REQUIREMENT = "REQUIREMENT"
    POLICY = "POLICY"
    RULE = "RULE"
    CONSTRAINT = "CONSTRAINT"
    SERVICE = "SERVICE"
    INTERFACE = "INTERFACE"
    TEST = "TEST"
    DEPENDENCY = "DEPENDENCY"
    MODULE = "MODULE"
    COMPONENT = "COMPONENT"
    ENGINE = "ENGINE"
    DOCUMENT = "DOCUMENT"
    SECTION = "SECTION"
    BATCH = "BATCH"
    PARAMETER = "PARAMETER"
    CONFIGURATION = "CONFIGURATION"
    EVENT = "EVENT"
    STATE = "STATE"


# Engineering Relationship Types (Volume VI Chapter 6)
class EngRelationType(str, Enum):
    DEFINES = "DEFINES"
    CONTAINS = "CONTAINS"
    IMPLEMENTS = "IMPLEMENTS"
    REFERENCES = "REFERENCES"
    DEPENDS_ON = "DEPENDS_ON"
    EXTENDS = "EXTENDS"
    VALIDATES = "VALIDATES"
    TESTS = "TESTS"
    CONFIGURES = "CONFIGURES"
    PRODUCES = "PRODUCES"
    GOVERNS = "GOVERNS"


# Engineering Object Visibility (Volume VI Chapter 17)
class EngVisibility(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    PRIVATE = "PRIVATE"


# ---------------------------------------------------------------------------
# Engineering Object
# ---------------------------------------------------------------------------

@dataclass
class EngObject:
    """
    A single Engineering Object in the Universal Engineering Model.

    Engineering Objects are the fundamental units of engineering knowledge.
    They are technology-independent and implementation-independent.
    """

    obj_id: str
    obj_type: EngObjectType
    name: str
    version: str = "0.0.0"
    status: str = ""
    purpose: str = ""
    visibility: EngVisibility = EngVisibility.PUBLIC
    source_document: str = ""
    source_ref: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
    # Traceability: origin AST node id
    ast_ref: str = ""

    def __hash__(self) -> int:
        return hash(self.obj_id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EngObject) and self.obj_id == other.obj_id


# ---------------------------------------------------------------------------
# Engineering Relationship
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EngRelationship:
    """
    A semantic relationship between two Engineering Objects.

    Relationships express engineering necessity, dependency, implementation,
    validation, and governance connections.
    """

    source_id: str
    target_id: str
    relation_type: EngRelationType
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    source_ref: str = ""


# ---------------------------------------------------------------------------
# Universal Engineering Model
# ---------------------------------------------------------------------------

class UniversalEngineeringModel:
    """
    The Universal Engineering Model (UEM).

    The UEM is the canonical semantic representation produced by every
    conforming CSL compiler. It is the mandatory intermediate representation
    between Canonical Knowledge and Engineering Artifacts.

    CSL Reference: Volume VI — Fundamental Principle:
        Canonical Knowledge → UEM → Engineering Artifacts
    """

    def __init__(self) -> None:
        self._objects: Dict[str, EngObject] = {}
        self._relationships: List[EngRelationship] = []
        self._source_documents: Set[str] = set()

    # ------------------------------------------------------------------
    # Object operations
    # ------------------------------------------------------------------

    def add_object(self, obj: EngObject) -> None:
        """Add or replace an Engineering Object."""
        self._objects[obj.obj_id] = obj
        if obj.source_document:
            self._source_documents.add(obj.source_document)

    def get_object(self, obj_id: str) -> Optional[EngObject]:
        return self._objects.get(obj_id)

    def all_objects(self) -> List[EngObject]:
        return [self._objects[k] for k in sorted(self._objects)]

    def objects_by_type(self, obj_type: EngObjectType) -> List[EngObject]:
        return [o for o in self._objects.values() if o.obj_type == obj_type]

    def has_object(self, obj_id: str) -> bool:
        return obj_id in self._objects

    # ------------------------------------------------------------------
    # Relationship operations
    # ------------------------------------------------------------------

    def add_relationship(self, rel: EngRelationship) -> None:
        """Add an Engineering Relationship."""
        self._relationships.append(rel)

    def relationships_from(self, source_id: str) -> List[EngRelationship]:
        return [r for r in self._relationships if r.source_id == source_id]

    def relationships_to(self, target_id: str) -> List[EngRelationship]:
        return [r for r in self._relationships if r.target_id == target_id]

    def relationships_of_type(self, relation_type: EngRelationType) -> List[EngRelationship]:
        return [r for r in self._relationships if r.relation_type == relation_type]

    def all_relationships(self) -> List[EngRelationship]:
        return list(self._relationships)

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def dependency_graph(self) -> Dict[str, List[str]]:
        """Return dependency adjacency map: obj_id → [dep_obj_ids]."""
        graph: Dict[str, List[str]] = {obj_id: [] for obj_id in self._objects}
        for rel in self._relationships:
            if rel.relation_type == EngRelationType.DEPENDS_ON:
                if rel.source_id in graph:
                    graph[rel.source_id].append(rel.target_id)
        return graph

    def find_by_source_document(self, doc_id: str) -> List[EngObject]:
        return [o for o in self._objects.values() if o.source_document == doc_id]

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def statistics(self) -> Dict[str, Any]:
        type_counts: Dict[str, int] = {}
        for obj in self._objects.values():
            key = obj.obj_type.value
            type_counts[key] = type_counts.get(key, 0) + 1
        return {
            "total_objects": len(self._objects),
            "total_relationships": len(self._relationships),
            "source_documents": len(self._source_documents),
            "object_type_counts": type_counts,
        }

    def __len__(self) -> int:
        return len(self._objects)

    def __iter__(self) -> Iterator[EngObject]:
        return iter(self._objects.values())


# ---------------------------------------------------------------------------
# UEM Builder — converts SemanticResult objects into UEM
# ---------------------------------------------------------------------------

class UemBuilder:
    """
    Constructs the Universal Engineering Model from SemanticResult objects.

    CSL Reference: Volume V Chapter 9 (UEM Construction)
    """

    def build(self, semantic_results: list) -> UniversalEngineeringModel:
        """Build UEM from a list of SemanticResult objects."""
        uem = UniversalEngineeringModel()
        for result in semantic_results:
            self._add_document(uem, result)
        self._add_dependency_relationships(uem, semantic_results)
        return uem

    def _add_document(self, uem: UniversalEngineeringModel, result) -> None:
        doc_obj = EngObject(
            obj_id=result.doc_id,
            obj_type=EngObjectType.DOCUMENT,
            name=result.title,
            version=result.version,
            status=result.status,
            purpose=result.purpose,
            source_document=result.doc_id,
            source_ref=result.doc_id,
            properties={
                "objectives": result.objectives,
                "invariants": result.invariants,
                "scope_included": result.scope_included,
                "scope_excluded": result.scope_excluded,
            },
        )
        uem.add_object(doc_obj)

        for sec in result.sections:
            sec_obj = EngObject(
                obj_id=sec["id"],
                obj_type=EngObjectType.SECTION,
                name=sec["heading"],
                source_document=result.doc_id,
                source_ref=sec["id"],
                properties={
                    "content": sec["content"],
                    "bullets": sec["bullets"],
                    "metadata": sec["metadata"],
                },
            )
            uem.add_object(sec_obj)
            uem.add_relationship(EngRelationship(
                source_id=result.doc_id,
                target_id=sec["id"],
                relation_type=EngRelationType.CONTAINS,
                source_ref=result.doc_id,
            ))

    def _add_dependency_relationships(self, uem: UniversalEngineeringModel, semantic_results: list) -> None:
        for result in semantic_results:
            for dep in result.dependencies:
                if uem.has_object(dep):
                    uem.add_relationship(EngRelationship(
                        source_id=result.doc_id,
                        target_id=dep,
                        relation_type=EngRelationType.DEPENDS_ON,
                        source_ref=result.doc_id,
                    ))
