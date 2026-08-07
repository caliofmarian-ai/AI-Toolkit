"""
CSL Engine — Canonical Specification Language Execution Engine

Wraps the canonical_parser (Lexer, Parser, AST Builder, SemanticAnalyzer)
into a single executable engine interface.

Capabilities:
  - Lexing (tokenization)
  - Parsing (AST construction)
  - Semantic Analysis
  - Validation
  - Compiler Interface (structured output)

The implementation derives directly from the canonical EBNF and the
existing CslLexer / CslParser / SemanticAnalyzer in canonical_parser.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from python.canonical_parser import (
    CslLexer,
    CslParser,
    Diagnostic,
    DiagnosticSeverity,
    SemanticAnalyzer,
    SemanticResult,
    Token,
)
from python.canonical_parser.ast_nodes import DocumentNode


@dataclass
class CslExecutionResult:
    """Full result from executing the CSL pipeline on a source text."""

    source_name: str
    tokens: List[Token] = field(default_factory=list)
    ast: Optional[DocumentNode] = None
    semantic: Optional[SemanticResult] = None
    diagnostics: List[Diagnostic] = field(default_factory=list)
    valid: bool = False

    @property
    def errors(self) -> List[Diagnostic]:
        return [d for d in self.diagnostics if d.severity == DiagnosticSeverity.ERROR]

    @property
    def warnings(self) -> List[Diagnostic]:
        return [d for d in self.diagnostics if d.severity == DiagnosticSeverity.WARNING]

    def to_dict(self) -> Dict[str, Any]:
        entities = []
        relationships = []
        if self.semantic:
            entities = self.semantic.entities
            relationships = self.semantic.relationships

        return {
            "source_name": self.source_name,
            "valid": self.valid,
            "token_count": len(self.tokens),
            "entity_count": len(entities),
            "relationship_count": len(relationships),
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "diagnostics": [
                {
                    "code": d.code,
                    "message": d.message,
                    "severity": d.severity.value if hasattr(d.severity, "value") else str(d.severity),
                    "category": d.category.value if hasattr(d.category, "value") else str(d.category),
                }
                for d in self.diagnostics
            ],
            "entities": entities,
            "relationships": relationships,
        }


@dataclass
class CslCompileResult:
    """Structured compiler output — the canonical representation of a CSL document."""

    source_name: str
    identifier: str
    title: str
    version: str
    status: str
    entities: List[Dict[str, Any]] = field(default_factory=list)
    relationships: List[Dict[str, Any]] = field(default_factory=list)
    valid: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_name": self.source_name,
            "identifier": self.identifier,
            "title": self.title,
            "version": self.version,
            "status": self.status,
            "entities": self.entities,
            "relationships": self.relationships,
            "valid": self.valid,
        }


class CslEngine:
    """
    Executable CSL Engine.

    Provides a unified interface over:
      Lexer → Parser → AST → SemanticAnalyzer → Validator → CompilerInterface
    """

    def __init__(self) -> None:
        self._analyzer = SemanticAnalyzer()
        self._results: Dict[str, CslExecutionResult] = {}

    # ------------------------------------------------------------------
    # Core pipeline
    # ------------------------------------------------------------------

    def execute(self, text: str, source_name: str = "<inline>") -> CslExecutionResult:
        """Run the full CSL pipeline on a source text string."""
        result = CslExecutionResult(source_name=source_name)

        # Step 1: Lex
        lexer = CslLexer(text, source_name=source_name)
        try:
            result.tokens = lexer.tokenize()
        except Exception as exc:
            from python.canonical_parser import DiagnosticCategory
            from python.canonical_parser.diagnostics import Diagnostic as D
            result.diagnostics.append(D(
                code="CSL-L001",
                message=f"Lexer error: {exc}",
                severity=DiagnosticSeverity.ERROR,
                category=DiagnosticCategory.SYNTAX,
                source_path=source_name,
            ))
            return result

        # Step 2: Parse — a fresh parser instance per execution avoids state bleeding
        parser = CslParser()
        try:
            doc = parser.parse_text(text, source_name)
            result.ast = doc
            result.diagnostics.extend(parser.diagnostics)
        except Exception as exc:
            from python.canonical_parser import DiagnosticCategory
            from python.canonical_parser.diagnostics import Diagnostic as D
            result.diagnostics.append(D(
                code="CSL-P001",
                message=f"Parser error: {exc}",
                severity=DiagnosticSeverity.ERROR,
                category=DiagnosticCategory.SYNTAX,
                source_path=source_name,
            ))
            return result

        # Step 3: Semantic analysis
        try:
            semantic = self._analyzer.analyze(doc)
            result.semantic = semantic
            result.diagnostics.extend(semantic.diagnostics.all())
        except Exception as exc:
            from python.canonical_parser import DiagnosticCategory
            from python.canonical_parser.diagnostics import Diagnostic as D
            result.diagnostics.append(D(
                code="CSL-S001",
                message=f"Semantic analysis error: {exc}",
                severity=DiagnosticSeverity.ERROR,
                category=DiagnosticCategory.SEMANTIC,
                source_path=source_name,
            ))
            return result

        result.valid = all(
            d.severity != DiagnosticSeverity.ERROR for d in result.diagnostics
        )

        self._results[source_name] = result
        return result

    def execute_file(self, path: str) -> CslExecutionResult:
        """Execute the CSL pipeline on a file."""
        text = Path(path).read_text(encoding="utf-8")
        return self.execute(text, source_name=path)

    def execute_directory(self, directory: str) -> List[CslExecutionResult]:
        """Execute the CSL pipeline on all .csl files in a directory."""
        results: List[CslExecutionResult] = []
        for csl_file in sorted(Path(directory).rglob("*.csl")):
            results.append(self.execute_file(str(csl_file)))
        return results

    # ------------------------------------------------------------------
    # Compiler interface
    # ------------------------------------------------------------------

    def compile(self, text: str, source_name: str = "<inline>") -> CslCompileResult:
        """Compile CSL source text into a structured canonical representation."""
        execution = self.execute(text, source_name)
        semantic = execution.semantic

        identifier = ""
        title = ""
        version = ""
        status = ""

        if semantic:
            identifier = semantic.doc_id
            title = semantic.title or ""
            version = semantic.version or ""
            status = semantic.status or ""

        return CslCompileResult(
            source_name=source_name,
            identifier=identifier,
            title=title,
            version=version,
            status=status,
            entities=semantic.entities if semantic else [],
            relationships=semantic.relationships if semantic else [],
            valid=execution.valid,
        )

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self, text: str, source_name: str = "<inline>") -> bool:
        """Return True if the CSL source is valid with no errors."""
        result = self.execute(text, source_name)
        return result.valid

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def statistics(self) -> Dict[str, Any]:
        return {
            "executed_sources": len(self._results),
            "valid_sources": sum(1 for r in self._results.values() if r.valid),
            "sources": list(self._results.keys()),
        }
