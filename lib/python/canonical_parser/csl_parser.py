"""
CSL Grammar Parser — Canonical Specification Language v1.0.0

Transforms a token stream into a typed Abstract Syntax Tree.

CSL Reference: Volume IV Chapters 6–17 (Grammar)
CORE: CORE-023-004
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from .lexer import CslLexer, SourceLocation, Token, TokenType
from .ast_nodes import (
    AstNode,
    BulletItemNode,
    BulletListNode,
    CodeBlockNode,
    DocumentNode,
    MetadataNode,
    ParagraphNode,
    SectionNode,
    SeparatorNode,
    SubsectionNode,
    TableNode,
    TableRowNode,
    TextNode,
)
from .diagnostics import Diagnostic, DiagnosticCategory, DiagnosticSeverity


_CANON_ID_RE = re.compile(r"(CANON-\d+)")
_CODE_FENCE_LANG_RE = re.compile(r"^```(\w*)$")


class CslParser:
    """
    CSL Grammar Parser.

    Builds a typed AST from a CSL token stream.

    Deterministic: equivalent inputs always produce equivalent ASTs.
    """

    def __init__(self) -> None:
        self._tokens: List[Token] = []
        self._pos: int = 0
        self._diagnostics: List[Diagnostic] = []

    @property
    def diagnostics(self) -> List[Diagnostic]:
        return list(self._diagnostics)

    def parse_file(self, path) -> DocumentNode:
        """Parse a CSL file into an AST DocumentNode."""
        path = Path(path)
        text = path.read_text(encoding="utf-8")
        return self.parse_text(text, source_name=str(path))

    def parse_text(self, text: str, source_name: str = "") -> DocumentNode:
        """Parse CSL source text into an AST DocumentNode."""
        self._diagnostics = []
        lexer = CslLexer(text, source_name=source_name)
        self._tokens = lexer.tokenize()
        self._pos = 0
        return self._parse_document(source_name)

    # ------------------------------------------------------------------
    # Internal parsing
    # ------------------------------------------------------------------

    def _peek(self) -> Token:
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]
        return Token(TokenType.EOF, "", SourceLocation(0, 0))

    def _advance(self) -> Token:
        tok = self._peek()
        if tok.token_type != TokenType.EOF:
            self._pos += 1
        return tok

    def _parse_document(self, source_name: str) -> DocumentNode:
        loc = self._peek().location
        doc = DocumentNode(
            node_type=None,  # set in __post_init__
            location=loc,
            source_path=source_name,
        )
        doc.__post_init__()

        # Top-level content: first H1 is the document title. Subsequent H1/H2
        # headings are treated as sections to preserve legacy canonical docs
        # that use both heading levels for section boundaries.
        seen_title = False
        while self._peek().token_type != TokenType.EOF:
            tok = self._peek()

            if tok.token_type == TokenType.HEADING1:
                self._advance()
                if not seen_title:
                    seen_title = True
                    doc.title = tok.value
                    # Attempt to extract CANON id from title
                    m = _CANON_ID_RE.search(tok.value)
                    if m:
                        doc.doc_id = m.group(1)
                else:
                    section = self._parse_section_from_heading(tok)
                    doc.add_child(section)
                continue

            if tok.token_type == TokenType.HEADING2:
                section = self._parse_section()
                doc.add_child(section)
                self._capture_document_metadata_from_section(doc, section)
                continue

            if tok.token_type == TokenType.METADATA:
                self._advance()
                meta = MetadataNode(
                    node_type=None,
                    location=tok.location,
                    key=tok.key,
                    value=tok.raw_value,
                    is_keyword=tok.is_keyword(),
                )
                meta.__post_init__()
                doc.add_child(meta)
                # Extract well-known metadata
                key = tok.key.lower()
                if key == "version":
                    doc.version = tok.raw_value
                elif key == "status":
                    doc.status = tok.raw_value
                continue

            if tok.token_type in (TokenType.SEPARATOR, TokenType.BLANK):
                self._advance()
                if tok.token_type == TokenType.SEPARATOR:
                    sep = SeparatorNode(node_type=None, location=tok.location)
                    sep.__post_init__()
                    doc.add_child(sep)
                continue

            # Everything else at top level is text
            self._advance()
            text_node = TextNode(node_type=None, location=tok.location, text=tok.value)
            text_node.__post_init__()
            doc.add_child(text_node)

        # Populate doc_id if not extracted from title
        if not doc.doc_id:
            m = _CANON_ID_RE.search(source_name)
            if m:
                doc.doc_id = m.group(1)

        if not doc.version:
            inferred = self._infer_version(source_name, doc.title)
            if inferred:
                doc.version = inferred

        return doc

    def _capture_document_metadata_from_section(self, doc: DocumentNode, section: SectionNode) -> None:
        heading = section.heading.strip().lower()
        if heading == "status" and not doc.status:
            value = self._extract_first_text_value(section)
            if value:
                doc.status = value
        elif heading == "version" and not doc.version:
            value = self._extract_first_text_value(section)
            if value:
                doc.version = value

    def _extract_first_text_value(self, section: SectionNode) -> str:
        for child in section.children:
            if isinstance(child, ParagraphNode) and child.text.strip():
                return child.text.strip()
            if isinstance(child, TextNode) and child.text.strip():
                return child.text.strip()
            if isinstance(child, BulletListNode):
                items = child.items()
                if items and items[0].text.strip():
                    return items[0].text.strip()
        return ""

    def _infer_version(self, source_name: str, title: str) -> str:
        for candidate in (source_name, title):
            m = re.search(r"v(\d+\.\d+(?:\.\d+)?)", candidate, re.IGNORECASE)
            if m:
                return m.group(1)
        return ""

    def _parse_section_from_heading(self, tok: Token) -> SectionNode:
        section = SectionNode(
            node_type=None,
            location=tok.location,
            heading=tok.value,
        )
        section.__post_init__()
        self._parse_section_body(section)
        return section

    def _parse_section(self) -> SectionNode:
        tok = self._advance()  # consume HEADING2
        return self._parse_section_from_heading(tok)

    def _parse_section_body(self, section: SectionNode) -> None:
        stop_tokens = (TokenType.HEADING1, TokenType.HEADING2, TokenType.EOF)

        current_bullet_list: Optional[BulletListNode] = None
        current_table: Optional[TableNode] = None
        current_paragraph_lines: List[str] = []
        paragraph_loc: Optional[SourceLocation] = None

        def _flush_paragraph() -> None:
            nonlocal current_paragraph_lines, paragraph_loc
            if current_paragraph_lines:
                para = ParagraphNode(
                    node_type=None,
                    location=paragraph_loc,
                    text="\n".join(current_paragraph_lines),
                )
                para.__post_init__()
                section.add_child(para)
            current_paragraph_lines = []
            paragraph_loc = None

        def _flush_bullet_list() -> None:
            nonlocal current_bullet_list
            if current_bullet_list is not None:
                section.add_child(current_bullet_list)
                current_bullet_list = None

        def _flush_table() -> None:
            nonlocal current_table
            if current_table is not None:
                section.add_child(current_table)
                current_table = None

        while self._peek().token_type not in stop_tokens:
            tok = self._peek()

            if tok.token_type == TokenType.HEADING3:
                _flush_paragraph()
                _flush_bullet_list()
                _flush_table()
                subsection = self._parse_subsection()
                section.add_child(subsection)
                continue

            if tok.token_type == TokenType.HEADING1:
                # H1 inside a section is unusual; treat as text
                self._advance()
                _flush_bullet_list()
                _flush_table()
                if not current_paragraph_lines:
                    paragraph_loc = tok.location
                current_paragraph_lines.append(f"# {tok.value}")
                continue

            if tok.token_type == TokenType.SEPARATOR:
                self._advance()
                _flush_paragraph()
                _flush_bullet_list()
                _flush_table()
                sep = SeparatorNode(node_type=None, location=tok.location)
                sep.__post_init__()
                section.add_child(sep)
                continue

            if tok.token_type == TokenType.BLANK:
                self._advance()
                _flush_paragraph()
                _flush_bullet_list()
                _flush_table()
                continue

            if tok.token_type == TokenType.BULLET:
                self._advance()
                _flush_paragraph()
                _flush_table()
                if current_bullet_list is None:
                    current_bullet_list = BulletListNode(node_type=None, location=tok.location)
                    current_bullet_list.__post_init__()
                item = BulletItemNode(node_type=None, location=tok.location, text=tok.value)
                item.__post_init__()
                current_bullet_list.add_child(item)
                continue

            if tok.token_type == TokenType.TABLE_SEP:
                self._advance()
                # separator after header row; already handled
                continue

            if tok.token_type == TokenType.TABLE_ROW:
                self._advance()
                _flush_paragraph()
                _flush_bullet_list()
                cells = [c.strip() for c in tok.value.strip("|").split("|")]
                if current_table is None:
                    current_table = TableNode(node_type=None, location=tok.location, headers=cells)
                    current_table.__post_init__()
                else:
                    row = TableRowNode(node_type=None, location=tok.location, cells=cells)
                    row.__post_init__()
                    current_table.add_child(row)
                continue

            if tok.token_type == TokenType.CODE_FENCE:
                self._advance()
                _flush_paragraph()
                _flush_bullet_list()
                _flush_table()
                code_node = self._parse_code_block(tok)
                section.add_child(code_node)
                continue

            if tok.token_type == TokenType.METADATA:
                self._advance()
                _flush_bullet_list()
                _flush_table()
                meta = MetadataNode(
                    node_type=None,
                    location=tok.location,
                    key=tok.key,
                    value=tok.raw_value,
                    is_keyword=tok.is_keyword(),
                )
                meta.__post_init__()
                section.add_child(meta)
                continue

            # Plain text
            self._advance()
            _flush_bullet_list()
            _flush_table()
            if not current_paragraph_lines:
                paragraph_loc = tok.location
            current_paragraph_lines.append(tok.value)

        _flush_paragraph()
        _flush_bullet_list()
        _flush_table()

    def _parse_subsection(self) -> SubsectionNode:
        tok = self._advance()  # consume HEADING3
        subsection = SubsectionNode(node_type=None, location=tok.location, heading=tok.value)
        subsection.__post_init__()

        while self._peek().token_type not in (TokenType.HEADING2, TokenType.HEADING3, TokenType.EOF):
            child_tok = self._peek()

            if child_tok.token_type in (TokenType.SEPARATOR, TokenType.BLANK):
                self._advance()
                continue

            if child_tok.token_type == TokenType.BULLET:
                self._advance()
                item = BulletItemNode(node_type=None, location=child_tok.location, text=child_tok.value)
                item.__post_init__()
                subsection.add_child(item)
                continue

            if child_tok.token_type == TokenType.TABLE_SEP:
                self._advance()
                continue

            if child_tok.token_type == TokenType.TABLE_ROW:
                self._advance()
                cells = [c.strip() for c in child_tok.value.strip("|").split("|")]
                row = TableRowNode(node_type=None, location=child_tok.location, cells=cells)
                row.__post_init__()
                subsection.add_child(row)
                continue

            if child_tok.token_type == TokenType.CODE_FENCE:
                self._advance()
                code_node = self._parse_code_block(child_tok)
                subsection.add_child(code_node)
                continue

            self._advance()
            text_node = TextNode(node_type=None, location=child_tok.location, text=child_tok.value)
            text_node.__post_init__()
            subsection.add_child(text_node)

        return subsection

    def _parse_code_block(self, fence_tok: Token) -> CodeBlockNode:
        lang_match = _CODE_FENCE_LANG_RE.match(fence_tok.value)
        language = lang_match.group(1) if lang_match else ""
        lines: List[str] = []

        while self._peek().token_type != TokenType.EOF:
            tok = self._advance()
            if tok.token_type == TokenType.CODE_FENCE:
                break
            lines.append(tok.value)

        code_node = CodeBlockNode(
            node_type=None,
            location=fence_tok.location,
            language=language,
            lines=lines,
        )
        code_node.__post_init__()
        return code_node
