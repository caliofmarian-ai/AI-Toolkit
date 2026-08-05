"""
CSL Diagnostics — Canonical Specification Language v1.0.0

Deterministic diagnostic contract for all CSL subsystems.

CSL Reference: Volume V Chapter 13 (Diagnostics)
CORE: CORE-023-004
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from .lexer import SourceLocation


class DiagnosticSeverity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    HINT = "HINT"


class DiagnosticCategory(str, Enum):
    LEXICAL = "LEXICAL"
    SYNTAX = "SYNTAX"
    SEMANTIC = "SEMANTIC"
    RELATIONSHIP = "RELATIONSHIP"
    CONSTRAINT = "CONSTRAINT"
    DEPENDENCY = "DEPENDENCY"
    GOVERNANCE = "GOVERNANCE"
    SAFETY = "SAFETY"
    GENERAL = "GENERAL"


@dataclass(frozen=True)
class Diagnostic:
    """A single CSL diagnostic message."""

    severity: DiagnosticSeverity
    category: DiagnosticCategory
    code: str
    message: str
    source_ref: str = ""
    location: Optional[SourceLocation] = None

    def is_error(self) -> bool:
        return self.severity == DiagnosticSeverity.ERROR

    def is_warning(self) -> bool:
        return self.severity == DiagnosticSeverity.WARNING

    def __str__(self) -> str:
        loc = str(self.location) if self.location else self.source_ref
        return f"[{self.severity.value}][{self.category.value}][{self.code}] {self.message} ({loc})"


@dataclass
class DiagnosticCollection:
    """Collection of diagnostics from a compilation pass."""

    _items: List[Diagnostic] = field(default_factory=list)

    def add(self, diagnostic: Diagnostic) -> None:
        self._items.append(diagnostic)

    def error(self, code: str, message: str, category: DiagnosticCategory = DiagnosticCategory.GENERAL,
              source_ref: str = "", location: Optional[SourceLocation] = None) -> None:
        self.add(Diagnostic(DiagnosticSeverity.ERROR, category, code, message, source_ref, location))

    def warning(self, code: str, message: str, category: DiagnosticCategory = DiagnosticCategory.GENERAL,
                source_ref: str = "", location: Optional[SourceLocation] = None) -> None:
        self.add(Diagnostic(DiagnosticSeverity.WARNING, category, code, message, source_ref, location))

    def info(self, code: str, message: str, category: DiagnosticCategory = DiagnosticCategory.GENERAL,
             source_ref: str = "", location: Optional[SourceLocation] = None) -> None:
        self.add(Diagnostic(DiagnosticSeverity.INFO, category, code, message, source_ref, location))

    def all(self) -> List[Diagnostic]:
        return list(self._items)

    def errors(self) -> List[Diagnostic]:
        return [d for d in self._items if d.is_error()]

    def warnings(self) -> List[Diagnostic]:
        return [d for d in self._items if d.is_warning()]

    def has_errors(self) -> bool:
        return any(d.is_error() for d in self._items)

    def count(self) -> int:
        return len(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)
