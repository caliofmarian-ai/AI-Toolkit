"""
CSL Lexer — Canonical Specification Language v1.0.0

Transforms CSL source text into a deterministic token stream.

CSL Reference: Volume IV Chapters 4–5 (Tokens, Keywords)
CORE: CORE-023-004
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, List, Optional


# ---------------------------------------------------------------------------
# Token types
# ---------------------------------------------------------------------------

class TokenType(str, Enum):
    # Document structure
    HEADING1 = "HEADING1"        # # Title
    HEADING2 = "HEADING2"        # ## Section
    HEADING3 = "HEADING3"        # ### Subsection
    # Metadata key-value pairs
    METADATA = "METADATA"        # Key: Value
    # Bullet items
    BULLET = "BULLET"            # - item
    # Table rows
    TABLE_ROW = "TABLE_ROW"      # | col | col |
    TABLE_SEP = "TABLE_SEP"      # |---|---|
    # Code blocks
    CODE_FENCE = "CODE_FENCE"    # ```
    CODE_LINE = "CODE_LINE"      # line inside code fence
    # Block separators
    SEPARATOR = "SEPARATOR"      # ---
    # Plain text
    TEXT = "TEXT"
    # Empty line
    BLANK = "BLANK"
    # End of file
    EOF = "EOF"


# CSL reserved metadata keywords (Volume IV Chapter 5)
RESERVED_KEYWORDS = frozenset([
    "version",
    "status",
    "classification",
    "author",
    "date",
    "id",
    "title",
    "scope",
    "purpose",
    "objectives",
    "dependencies",
    "invariants",
    "constraints",
    "phase",
    "priority",
    "risk",
    "approval",
])


@dataclass(frozen=True)
class SourceLocation:
    """Source location for diagnostics traceability."""

    line: int
    column: int
    source: str = ""

    def __str__(self) -> str:
        if self.source:
            return f"{self.source}:{self.line}:{self.column}"
        return f"{self.line}:{self.column}"


@dataclass(frozen=True)
class Token:
    """Single CSL token."""

    token_type: TokenType
    value: str
    location: SourceLocation
    # For METADATA tokens: key and raw value
    key: str = ""
    raw_value: str = ""

    def is_keyword(self) -> bool:
        return self.token_type == TokenType.METADATA and self.key.lower() in RESERVED_KEYWORDS


# ---------------------------------------------------------------------------
# Lexer
# ---------------------------------------------------------------------------

_HEADING1_RE = re.compile(r"^# (.+)$")
_HEADING2_RE = re.compile(r"^## (.+)$")
_HEADING3_RE = re.compile(r"^### (.+)$")
_METADATA_RE = re.compile(r"^([A-Za-z][A-Za-z0-9 _-]*):\s*(.*)$")
_BULLET_RE = re.compile(r"^-\s+(.+)$")
_TABLE_ROW_RE = re.compile(r"^\|.+\|")
_TABLE_SEP_RE = re.compile(r"^\|[-| :]+\|")
_CODE_FENCE_RE = re.compile(r"^```")
_SEPARATOR_RE = re.compile(r"^---\s*$")


class CslLexer:
    """
    CSL Lexer: transforms source text into a token stream.

    Deterministic: identical inputs always produce identical token streams.
    Preserves source location for every token.
    """

    def __init__(self, source: str, source_name: str = ""):
        self._source = source
        self._source_name = source_name
        self._lines = source.splitlines()
        self._in_code_fence = False

    def tokenize(self) -> List[Token]:
        """Return the complete token list for the source."""
        return list(self._iter_tokens())

    def _iter_tokens(self) -> Iterator[Token]:
        for line_idx, raw_line in enumerate(self._lines):
            line_num = line_idx + 1
            line = raw_line.rstrip("\n\r")

            loc = SourceLocation(line=line_num, column=1, source=self._source_name)

            # Code fence toggle
            if _CODE_FENCE_RE.match(line):
                self._in_code_fence = not self._in_code_fence
                yield Token(TokenType.CODE_FENCE, line, loc)
                continue

            if self._in_code_fence:
                yield Token(TokenType.CODE_LINE, line, loc)
                continue

            # Blank line
            if not line.strip():
                yield Token(TokenType.BLANK, "", loc)
                continue

            # Separator
            if _SEPARATOR_RE.match(line):
                yield Token(TokenType.SEPARATOR, "---", loc)
                continue

            # Headings (most specific first)
            m = _HEADING3_RE.match(line)
            if m:
                yield Token(TokenType.HEADING3, m.group(1).strip(), loc)
                continue

            m = _HEADING2_RE.match(line)
            if m:
                yield Token(TokenType.HEADING2, m.group(1).strip(), loc)
                continue

            m = _HEADING1_RE.match(line)
            if m:
                yield Token(TokenType.HEADING1, m.group(1).strip(), loc)
                continue

            # Table separator (before row check)
            if _TABLE_SEP_RE.match(line):
                yield Token(TokenType.TABLE_SEP, line.strip(), loc)
                continue

            # Table row
            if _TABLE_ROW_RE.match(line):
                yield Token(TokenType.TABLE_ROW, line.strip(), loc)
                continue

            # Bullet
            m = _BULLET_RE.match(line)
            if m:
                yield Token(TokenType.BULLET, m.group(1).strip(), loc, key="", raw_value=m.group(1).strip())
                continue

            # Metadata key: value
            m = _METADATA_RE.match(line)
            if m:
                key = m.group(1).strip()
                raw_value = m.group(2).strip()
                yield Token(TokenType.METADATA, line.strip(), loc, key=key, raw_value=raw_value)
                continue

            # Plain text
            yield Token(TokenType.TEXT, line.strip(), loc)

        yield Token(TokenType.EOF, "", SourceLocation(line=len(self._lines) + 1, column=1, source=self._source_name))
