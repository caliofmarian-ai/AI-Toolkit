from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterator, List, Optional, Set


class EngObjectType(str, Enum):
    PROJECT = 'PROJECT'
    CAPABILITY = 'CAPABILITY'
    FEATURE = 'FEATURE'
    REQUIREMENT = 'REQUIREMENT'
    DECISION = 'DECISION'
    CONSTRAINT = 'CONSTRAINT'
    POLICY = 'POLICY'
    RULE = 'RULE'
    RISK = 'RISK'
    ISSUE = 'ISSUE'
    EPIC = 'EPIC'
    MILESTONE = 'MILESTONE'
    TASK = 'TASK'
    COMPONENT = 'COMPONENT'
    MODULE = 'MODULE'
    SERVICE = 'SERVICE'
    API = 'API'
    ENTITY = 'ENTITY'
    GENERATOR = 'GENERATOR'
    VALIDATOR = 'VALIDATOR'
    COMPILER = 'COMPILER'
    RUNTIME = 'RUNTIME'
    KNOWLEDGE = 'KNOWLEDGE'
    DOCUMENT = 'DOCUMENT'


class EngRelationType(str, Enum):
    IMPLEMENTS = 'IMPLEMENTS'
    CONTAINS = 'CONTAINS'
    DEPENDS_ON = 'DEPENDS_ON'
    EXTENDS = 'EXTENDS'
    REFERENCES = 'REFERENCES'
    REQUIRES = 'REQUIRES'
    OWNS = 'OWNS'
    APPROVES = 'APPROVES'
    TESTS = 'TESTS'
    VALIDATES = 'VALIDATES'
    GENERATES = 'GENERATES'
    DEPLOYS = 'DEPLOYS'
    PUBLISHES = 'PUBLISHES'
    CONSUMES = 'CONSUMES'
    SUPPORTS = 'SUPPORTS'
    BELONGS_TO = 'BELONGS_TO'


class EngVisibility(str, Enum):
    PUBLIC = 'PUBLIC'
    INTERNAL = 'INTERNAL'
    PROTECTED = 'PROTECTED'
    PRIVATE = 'PRIVATE'
    RESTRICTED = 'RESTRICTED'


@dataclass
class EngObject:
    obj_id: str
    obj_type: EngObjectType
    name: str
    version: str = '0.0.0'
    status: str = ''
    purpose: str = ''
    visibility: EngVisibility = EngVisibility.PUBLIC
    source_document: str = ''
    source_ref: str = ''
    properties: Dict[str, Any] = field(default_factory=dict)
    ast_ref: str = ''


@dataclass(frozen=True)
class EngRelationship:
    source_id: str
    target_id: str
    relation_type: EngRelationType
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    source_ref: str = ''


class UniversalEngineeringModel:
    def __init__(self):
        self._objects: Dict[str, EngObject] = {}
        self._relationships: List[EngRelationship] = []
        self._source_documents: Set[str] = set()
    def add_object(self, obj: EngObject):
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
    def add_relationship(self, rel: EngRelationship):
        self._relationships.append(rel)
    def all_relationships(self) -> List[EngRelationship]:
        return list(self._relationships)
    def relationships_of_type(self, relation_type: EngRelationType) -> List[EngRelationship]:
        return [r for r in self._relationships if r.relation_type == relation_type]
    def statistics(self) -> Dict[str, Any]:
        counts: Dict[str, int] = {}
        for obj in self._objects.values():
            counts[obj.obj_type.value] = counts.get(obj.obj_type.value, 0) + 1
        return {'total_objects': len(self._objects), 'total_relationships': len(self._relationships), 'source_documents': len(self._source_documents), 'object_type_counts': counts}
    def __len__(self):
        return len(self._objects)
    def __iter__(self) -> Iterator[EngObject]:
        return iter(self._objects.values())


class UemBuilder:
    def build(self, semantic_results: list) -> UniversalEngineeringModel:
        uem = UniversalEngineeringModel()
        for result in semantic_results:
            doc = EngObject(result.doc_id, EngObjectType.DOCUMENT, result.title or result.doc_id, result.version or '0.0.0', result.status, source_document=result.doc_id, source_ref=result.source_path, properties={'classification': result.classification})
            uem.add_object(doc)
            for entity in result.entities:
                obj_type = EngObjectType[entity['entity_type'].upper()] if entity['entity_type'].upper() in EngObjectType.__members__ else EngObjectType.ENTITY
                visibility_name = str(entity.get('visibility', 'Public')).upper()
                visibility = EngVisibility[visibility_name] if visibility_name in EngVisibility.__members__ else EngVisibility.PUBLIC
                uem.add_object(EngObject(entity['identifier'], obj_type, str(entity.get('name') or entity['identifier']), str(entity.get('version') or '0.0.0'), str(entity.get('status') or ''), visibility=visibility, source_document=result.doc_id, source_ref=result.source_path, properties=entity['properties'], ast_ref=entity['identifier']))
                uem.add_relationship(EngRelationship(result.doc_id, entity['identifier'], EngRelationType.CONTAINS, source_ref=result.source_path))
            for relationship in result.relationships:
                relation_name = relationship['relation_type'].upper()
                relation_type = EngRelationType[relation_name] if relation_name in EngRelationType.__members__ else EngRelationType.REFERENCES
                uem.add_relationship(EngRelationship(relationship['source'], relationship['target'], relation_type, metadata=relationship['attributes'], source_ref=result.source_path))
        return uem
