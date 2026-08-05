"""
CSL Abstract Syntax Tree — Canonical Specification Language v1.0.0

Typed, traversable AST nodes representing syntactic structure of CSL documents.

CSL Reference: Volume V Chapter 7 (Abstract Syntax Tree Construction)
CORE: CORE-023-004
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterator, List, Optional

from .lexer import SourceLocation


# ---------------------------------------------------------------------------
# Node types
# ---------------------------------------------------------------------------

class AstNodeType(str, Enum):
    DOCUMENT = "DOCUMENT"
    SECTION = "SECTION"
    SUBSECTION = "SUBSECTION"
    METADATA = "METADATA"
    PARAGRAPH = "PARAGRAPH"
    BULLET_LIST = "BULLET_LIST"
    BULLET_ITEM = "BULLET_ITEM"
    TABLE = "TABLE"
    TABLE_ROW = "TABLE_ROW"
    CODE_BLOCK = "CODE_BLOCK"
    SEPARATOR = "SEPARATOR"
    TEXT = "TEXT"


# ---------------------------------------------------------------------------
# Base node
# ---------------------------------------------------------------------------

@dataclass
class AstNode:
    """Base class for all CSL AST nodes."""

    node_type: AstNodeType
    location: SourceLocation
    children: List["AstNode"] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)

    def add_child(self, child: "AstNode") -> None:
        self.children.append(child)

    def iter_children(self) -> Iterator["AstNode"]:
        yield from self.children

    def find_all(self, node_type: AstNodeType) -> List["AstNode"]:
        result = []
        if self.node_type == node_type:
            result.append(self)
        for child in self.children:
            result.extend(child.find_all(node_type))
        return result

    def find_first(self, node_type: AstNodeType) -> Optional["AstNode"]:
        if self.node_type == node_type:
            return self
        for child in self.children:
            found = child.find_first(node_type)
            if found is not None:
                return found
        return None


# ---------------------------------------------------------------------------
# Concrete node types
# ---------------------------------------------------------------------------

@dataclass
class DocumentNode(AstNode):
    """Root node representing a complete CSL document."""

    source_path: str = ""
    # Metadata extracted from preamble
    doc_id: str = ""
    title: str = ""
    version: str = ""
    status: str = ""

    def __post_init__(self) -> None:
        self.node_type = AstNodeType.DOCUMENT

    def sections(self) -> List["SectionNode"]:
        return [c for c in self.children if isinstance(c, SectionNode)]

    def metadata_map(self) -> Dict[str, str]:
        result: Dict[str, str] = {}
        for child in self.children:
            if isinstance(child, MetadataNode):
                result[child.key.lower()] = child.value
        return result


@dataclass
class SectionNode(AstNode):
    """Represents a top-level section (## heading)."""

    heading: str = ""
    index: int = 0

    def __post_init__(self) -> None:
        self.node_type = AstNodeType.SECTION

    def subsections(self) -> List["SubsectionNode"]:
        return [c for c in self.children if isinstance(c, SubsectionNode)]

    def text_content(self) -> str:
        parts: List[str] = []
        for child in self.children:
            if isinstance(child, TextNode):
                parts.append(child.text)
            elif isinstance(child, ParagraphNode):
                parts.append(child.text)
            elif isinstance(child, BulletListNode):
                for item in child.children:
                    if isinstance(item, BulletItemNode):
                        parts.append(f"- {item.text}")
        return "\n".join(parts)


@dataclass
class SubsectionNode(AstNode):
    """Represents a subsection (### heading)."""

    heading: str = ""
    index: int = 0

    def __post_init__(self) -> None:
        self.node_type = AstNodeType.SUBSECTION


@dataclass
class MetadataNode(AstNode):
    """Represents a metadata key-value pair."""

    key: str = ""
    value: str = ""
    is_keyword: bool = False

    def __post_init__(self) -> None:
        self.node_type = AstNodeType.METADATA


@dataclass
class ParagraphNode(AstNode):
    """Represents a text paragraph."""

    text: str = ""

    def __post_init__(self) -> None:
        self.node_type = AstNodeType.PARAGRAPH


@dataclass
class TextNode(AstNode):
    """Represents a single text line."""

    text: str = ""

    def __post_init__(self) -> None:
        self.node_type = AstNodeType.TEXT


@dataclass
class BulletListNode(AstNode):
    """Represents a bullet list."""

    def __post_init__(self) -> None:
        self.node_type = AstNodeType.BULLET_LIST

    def items(self) -> List["BulletItemNode"]:
        return [c for c in self.children if isinstance(c, BulletItemNode)]


@dataclass
class BulletItemNode(AstNode):
    """Represents a single bullet item."""

    text: str = ""

    def __post_init__(self) -> None:
        self.node_type = AstNodeType.BULLET_ITEM


@dataclass
class TableNode(AstNode):
    """Represents a table."""

    headers: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.node_type = AstNodeType.TABLE

    def rows(self) -> List["TableRowNode"]:
        return [c for c in self.children if isinstance(c, TableRowNode)]


@dataclass
class TableRowNode(AstNode):
    """Represents a table data row."""

    cells: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.node_type = AstNodeType.TABLE_ROW


@dataclass
class CodeBlockNode(AstNode):
    """Represents a fenced code block."""

    language: str = ""
    lines: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.node_type = AstNodeType.CODE_BLOCK

    def content(self) -> str:
        return "\n".join(self.lines)


@dataclass
class SeparatorNode(AstNode):
    """Represents a --- separator."""

    def __post_init__(self) -> None:
        self.node_type = AstNodeType.SEPARATOR
