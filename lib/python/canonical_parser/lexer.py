"""
CSL Lexer — Canonical Specification Language v1.0.0

Transforms CSL source text into a deterministic token stream.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class TokenType(str, Enum):
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    TIMESTAMP = "TIMESTAMP"
    DURATION = "DURATION"
    VERSION = "VERSION"
    NULL = "NULL"
    COLON = "COLON"
    DASH = "DASH"
    COMMA = "COMMA"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    NEWLINE = "NEWLINE"
    INDENT = "INDENT"
    DEDENT = "DEDENT"
    COMMENT = "COMMENT"
    EOF = "EOF"


RESERVED_KEYWORDS = frozenset([
    "Project", "Capability", "Feature", "Requirement", "Decision", "Constraint",
    "Policy", "Rule", "Risk", "Issue", "Epic", "Milestone", "Task", "Component",
    "Module", "Service", "API", "Entity", "Relationship", "Generator", "Validator",
    "Compiler", "Runtime", "Knowledge", "Reference", "Approval", "Deployment",
    "Environment", "Provider", "Model", "Prompt",
])


@dataclass(frozen=True)
class SourceLocation:
    line: int
    column: int
    source: str = ""

    def __str__(self) -> str:
        return f"{self.source + ':' if self.source else ''}{self.line}:{self.column}"


@dataclass(frozen=True)
class Token:
    token_type: TokenType
    value: str
    location: SourceLocation


class CslLexer:
    def __init__(self, source: str, source_name: str = ""):
        self._source = source
        self._source_name = source_name
        self._indent_stack = [0]

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        lines = self._source.splitlines()
        for line_index, raw_line in enumerate(lines, start=1):
            indent_prefix = raw_line[: len(raw_line) - len(raw_line.lstrip(' '))]
            if '\t' in indent_prefix or raw_line.startswith('\t'):
                raise ValueError('Tab character used for indentation')
            if not raw_line.strip():
                tokens.append(Token(TokenType.NEWLINE, '', SourceLocation(line_index, 1, self._source_name)))
                continue
            indent = len(raw_line) - len(raw_line.lstrip(' '))
            if indent % 4 != 0:
                raise ValueError(f'Invalid indentation level at line {line_index}')
            tokens.extend(self._emit_indent_dedent(indent, line_index))
            content = raw_line[indent:]
            if content.startswith('#'):
                tokens.append(Token(TokenType.COMMENT, content[1:].strip(), SourceLocation(line_index, indent + 1, self._source_name)))
                tokens.append(Token(TokenType.NEWLINE, '', SourceLocation(line_index, len(raw_line) + 1, self._source_name)))
                continue
            tokens.extend(self._tokenize_content(content, line_index, indent + 1))
            tokens.append(Token(TokenType.NEWLINE, '', SourceLocation(line_index, len(raw_line) + 1, self._source_name)))
        while len(self._indent_stack) > 1:
            self._indent_stack.pop()
            tokens.append(Token(TokenType.DEDENT, '', SourceLocation(len(lines) + 1, 1, self._source_name)))
        tokens.append(Token(TokenType.EOF, '', SourceLocation(len(lines) + 1, 1, self._source_name)))
        return tokens

    def _emit_indent_dedent(self, indent: int, line: int) -> List[Token]:
        emitted: List[Token] = []
        if indent > self._indent_stack[-1]:
            self._indent_stack.append(indent)
            emitted.append(Token(TokenType.INDENT, '', SourceLocation(line, 1, self._source_name)))
        else:
            while indent < self._indent_stack[-1]:
                self._indent_stack.pop()
                emitted.append(Token(TokenType.DEDENT, '', SourceLocation(line, 1, self._source_name)))
            if indent != self._indent_stack[-1]:
                raise ValueError(f'Unmatched dedent at line {line}')
        return emitted

    def _tokenize_content(self, content: str, line: int, column_start: int) -> List[Token]:
        tokens: List[Token] = []
        i = 0
        while i < len(content):
            ch = content[i]
            col = column_start + i
            if ch == ' ':
                i += 1
                continue
            if ch == ':':
                tokens.append(Token(TokenType.COLON, ch, SourceLocation(line, col, self._source_name)))
                i += 1
                continue
            if ch == '-' and not (i + 1 < len(content) and content[i + 1].isalnum()):
                tokens.append(Token(TokenType.DASH, ch, SourceLocation(line, col, self._source_name)))
                i += 1
                continue
            if ch == ',':
                tokens.append(Token(TokenType.COMMA, ch, SourceLocation(line, col, self._source_name)))
                i += 1
                continue
            if ch == '[':
                tokens.append(Token(TokenType.LBRACKET, ch, SourceLocation(line, col, self._source_name)))
                i += 1
                continue
            if ch == ']':
                tokens.append(Token(TokenType.RBRACKET, ch, SourceLocation(line, col, self._source_name)))
                i += 1
                continue
            if ch == '{':
                tokens.append(Token(TokenType.LBRACE, ch, SourceLocation(line, col, self._source_name)))
                i += 1
                continue
            if ch == '}':
                tokens.append(Token(TokenType.RBRACE, ch, SourceLocation(line, col, self._source_name)))
                i += 1
                continue
            if ch == '"':
                value, i = self._read_string(content, i)
                tokens.append(Token(TokenType.STRING, value, SourceLocation(line, col, self._source_name)))
                continue
            value, i = self._read_word(content, i)
            tokens.append(self._classify_word(value, line, col))
        return tokens

    def _read_string(self, content: str, start: int):
        chars = []
        i = start + 1
        while i < len(content):
            ch = content[i]
            if ch == '"':
                return ''.join(chars), i + 1
            if ch == '\\':
                i += 1
                if i >= len(content):
                    break
                chars.append(content[i])
                i += 1
                continue
            chars.append(ch)
            i += 1
        raise ValueError('Unterminated string literal')

    def _read_word(self, content: str, start: int):
        i = start
        while i < len(content) and content[i] not in ' :,[]{}"':
            i += 1
        return content[start:i], i

    def _classify_word(self, value: str, line: int, column: int) -> Token:
        location = SourceLocation(line, column, self._source_name)
        if value in RESERVED_KEYWORDS:
            return Token(TokenType.KEYWORD, value, location)
        if value in {'true', 'false'}:
            return Token(TokenType.BOOLEAN, value, location)
        if value == 'null':
            return Token(TokenType.NULL, value, location)
        if self._is_version(value):
            return Token(TokenType.VERSION, value, location)
        if self._is_timestamp(value):
            return Token(TokenType.TIMESTAMP, value, location)
        if self._is_date(value):
            return Token(TokenType.DATE, value, location)
        if self._is_duration(value):
            return Token(TokenType.DURATION, value, location)
        if self._is_decimal(value):
            return Token(TokenType.DECIMAL, value, location)
        if self._is_integer(value):
            return Token(TokenType.INTEGER, value, location)
        if self._is_identifier(value):
            return Token(TokenType.IDENTIFIER, value, location)
        raise ValueError(f"Invalid token '{value}'")

    def _is_identifier(self, value: str) -> bool:
        return bool(value) and value[0].isalpha() and all(ch.isalnum() or ch in '-_' for ch in value)

    def _is_integer(self, value: str) -> bool:
        return value.isdigit() or (value.startswith('-') and value[1:].isdigit())

    def _is_decimal(self, value: str) -> bool:
        if value.count('.') != 1:
            return False
        left, right = value.split('.', 1)
        if left.startswith('-'):
            left = left[1:]
        return bool(left) and left.isdigit() and bool(right) and right.isdigit()

    def _is_version(self, value: str) -> bool:
        parts = value.split('.')
        return len(parts) == 3 and all(part.isdigit() for part in parts)

    def _is_date(self, value: str) -> bool:
        parts = value.split('-')
        return len(parts) == 3 and len(parts[0]) == 4 and all(part.isdigit() for part in parts)

    def _is_timestamp(self, value: str) -> bool:
        if 'T' not in value:
            return False
        date_part, time_part = value.split('T', 1)
        if time_part.endswith('Z'):
            time_part = time_part[:-1]
        parts = time_part.split(':')
        return self._is_date(date_part) and len(parts) == 3 and all(part.isdigit() and len(part) == 2 for part in parts)

    def _is_duration(self, value: str) -> bool:
        return len(value) > 1 and self._is_integer(value[:-1]) and value[-1] in 'dhms'
