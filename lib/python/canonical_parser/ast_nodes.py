from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional

from .lexer import SourceLocation


class AstNodeType(str, Enum):
    DOCUMENT = 'DOCUMENT'
    HEADER_FIELD = 'HEADER_FIELD'
    ENTITY = 'ENTITY'
    RELATIONSHIP = 'RELATIONSHIP'
    ATTRIBUTE = 'ATTRIBUTE'
    SCALAR = 'SCALAR'
    LIST = 'LIST'
    MAP = 'MAP'


@dataclass
class AstNode:
    node_type: AstNodeType
    location: SourceLocation


@dataclass
class ScalarValueNode(AstNode):
    value_type: str = ''
    value: Any = None
    def __post_init__(self):
        self.node_type = AstNodeType.SCALAR


@dataclass
class ListValueNode(AstNode):
    items: List[AstNode] = field(default_factory=list)
    def __post_init__(self):
        self.node_type = AstNodeType.LIST


@dataclass
class MapEntryNode:
    key: str
    value: AstNode


@dataclass
class MapValueNode(AstNode):
    entries: List[MapEntryNode] = field(default_factory=list)
    def __post_init__(self):
        self.node_type = AstNodeType.MAP


@dataclass
class AttributeNode(AstNode):
    name: str = ''
    value: Optional[AstNode] = None
    def __post_init__(self):
        self.node_type = AstNodeType.ATTRIBUTE


@dataclass
class EntityNode(AstNode):
    entity_type: str = ''
    attributes: List[AttributeNode] = field(default_factory=list)
    children: List['EntityNode'] = field(default_factory=list)
    def __post_init__(self):
        self.node_type = AstNodeType.ENTITY
    def get_attribute(self, name: str) -> Optional[AttributeNode]:
        return next((a for a in self.attributes if a.name == name), None)


@dataclass
class RelationshipNode(AstNode):
    source: str = ''
    relation_type: str = ''
    target: str = ''
    attributes: List[AttributeNode] = field(default_factory=list)
    def __post_init__(self):
        self.node_type = AstNodeType.RELATIONSHIP


@dataclass
class HeaderFieldNode(AstNode):
    name: str = ''
    value: Optional[AstNode] = None
    def __post_init__(self):
        self.node_type = AstNodeType.HEADER_FIELD


@dataclass
class DocumentNode(AstNode):
    source_path: str = ''
    source_text: str = ''
    header_fields: List[HeaderFieldNode] = field(default_factory=list)
    declarations: List[AstNode] = field(default_factory=list)
    def __post_init__(self):
        self.node_type = AstNodeType.DOCUMENT
    def header_value(self, name: str) -> str:
        for field in self.header_fields:
            if field.name == name and isinstance(field.value, ScalarValueNode):
                return str(field.value.value)
        return ''
    @property
    def title(self) -> str:
        return self.header_value('Title')
    @property
    def version(self) -> str:
        return self.header_value('Version')
    @property
    def status(self) -> str:
        return self.header_value('Status')
    @property
    def classification(self) -> str:
        return self.header_value('Classification')
    @property
    def doc_type(self) -> str:
        for item in self.declarations:
            if isinstance(item, EntityNode):
                return item.entity_type
        return ''
    def entities(self) -> List[EntityNode]:
        return [item for item in self.declarations if isinstance(item, EntityNode)]
    def relationships(self) -> List[RelationshipNode]:
        return [item for item in self.declarations if isinstance(item, RelationshipNode)]
