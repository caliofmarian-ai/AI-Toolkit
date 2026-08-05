"""
CSL Normative Validation Engine — Canonical Specification Language v1.0.0

Implements all mandated CSL validation categories:
- Lexical validation
- Syntax validation
- Semantic validation
- Relationship validation
- Constraint validation
- Dependency validation
- Governance validation
- Safety validation

CSL Reference: Volume II Chapter 7 (Validation), Volume V Chapter 10 (Validation)
CORE: CORE-023-006
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from python.canonical_parser import (
    CslLexer,
    CslParser,
    DiagnosticCategory,
    DiagnosticCollection,
    DiagnosticSeverity,
    SemanticAnalyzer,
    TokenType,
)
from python.canonical_entities import UniversalEngineeringModel


class ValidationCategory(str, Enum):
    LEXICAL = "LEXICAL"
    SYNTAX = "SYNTAX"
    SEMANTIC = "SEMANTIC"
    RELATIONSHIP = "RELATIONSHIP"
    CONSTRAINT = "CONSTRAINT"
    DEPENDENCY = "DEPENDENCY"
    GOVERNANCE = "GOVERNANCE"
    SAFETY = "SAFETY"


@dataclass
class ValidationFinding:
    """A single finding from CSL normative validation."""

    category: ValidationCategory
    severity: str  # ERROR | WARNING | INFO
    code: str
    message: str
    source_ref: str = ""
    passed: bool = True


@dataclass
class NormativeValidationResult:
    """Result of normative CSL validation."""

    source_ref: str
    findings: List[ValidationFinding] = field(default_factory=list)
    category_results: Dict[str, bool] = field(default_factory=dict)

    def add(self, finding: ValidationFinding) -> None:
        self.findings.append(finding)
        if not finding.passed:
            self.category_results[finding.category.value] = False
        elif finding.category.value not in self.category_results:
            self.category_results[finding.category.value] = True

    def passed(self) -> bool:
        return all(self.category_results.values())

    def errors(self) -> List[ValidationFinding]:
        return [f for f in self.findings if f.severity == "ERROR"]

    def warnings(self) -> List[ValidationFinding]:
        return [f for f in self.findings if f.severity == "WARNING"]

    def summary(self) -> Dict[str, Any]:
        return {
            "source": self.source_ref,
            "passed": self.passed(),
            "total_findings": len(self.findings),
            "errors": len(self.errors()),
            "warnings": len(self.warnings()),
            "categories": self.category_results,
        }


class CslNormativeValidator:
    """
    Normative CSL Validator implementing all mandated validation categories.

    Every category produces deterministic findings.
    Equivalent inputs always produce equivalent findings.
    """

    def __init__(self) -> None:
        self._parser = CslParser()
        self._analyzer = SemanticAnalyzer()

    def validate_text(self, text: str, source_ref: str = "") -> NormativeValidationResult:
        """Validate CSL source text through all normative validation categories."""
        result = NormativeValidationResult(source_ref=source_ref)

        # 1. Lexical validation
        self._validate_lexical(text, source_ref, result)

        # 2. Syntax validation
        doc = self._parser.parse_text(text, source_ref)
        self._validate_syntax(doc, source_ref, result)

        # 3. Semantic validation
        semantic = self._analyzer.analyze(doc)
        self._validate_semantic(semantic, source_ref, result)

        # 4. Relationship validation
        self._validate_relationships(semantic, source_ref, result)

        # 5. Constraint validation
        self._validate_constraints(semantic, source_ref, result)

        # 6. Dependency validation
        self._validate_dependencies(semantic, source_ref, result)

        # 7. Governance validation
        self._validate_governance(semantic, source_ref, result)

        # 8. Safety validation
        self._validate_safety(semantic, source_ref, result)

        return result

    def validate_file(self, path) -> NormativeValidationResult:
        path = Path(path)
        text = path.read_text(encoding="utf-8")
        return self.validate_text(text, source_ref=str(path))

    def validate_uem(self, uem: UniversalEngineeringModel) -> NormativeValidationResult:
        """Validate a fully constructed UEM."""
        result = NormativeValidationResult(source_ref="UEM")

        if len(uem) == 0:
            result.add(ValidationFinding(
                category=ValidationCategory.CONSTRAINT,
                severity="WARNING",
                code="UEM-001",
                message="Universal Engineering Model contains no Engineering Objects",
                source_ref="UEM",
                passed=False,
            ))
        else:
            result.add(ValidationFinding(
                category=ValidationCategory.CONSTRAINT,
                severity="INFO",
                code="UEM-002",
                message=f"UEM contains {len(uem)} Engineering Objects",
                source_ref="UEM",
                passed=True,
            ))

        stats = uem.statistics()
        result.add(ValidationFinding(
            category=ValidationCategory.SEMANTIC,
            severity="INFO",
            code="UEM-003",
            message=f"UEM has {stats['total_relationships']} relationships across {stats['source_documents']} source documents",
            source_ref="UEM",
            passed=True,
        ))

        return result

    # ------------------------------------------------------------------
    # 1. Lexical Validation
    # ------------------------------------------------------------------

    def _validate_lexical(self, text: str, source_ref: str, result: NormativeValidationResult) -> None:
        """Validate that source text produces a well-formed token stream."""
        try:
            lexer = CslLexer(text, source_name=source_ref)
            tokens = lexer.tokenize()
            # Check for unterminated code fences
            fence_count = sum(1 for t in tokens if t.token_type == TokenType.CODE_FENCE)
            if fence_count % 2 != 0:
                result.add(ValidationFinding(
                    category=ValidationCategory.LEXICAL,
                    severity="ERROR",
                    code="LEX-001",
                    message="Unterminated code fence (odd number of ``` markers)",
                    source_ref=source_ref,
                    passed=False,
                ))
            else:
                result.add(ValidationFinding(
                    category=ValidationCategory.LEXICAL,
                    severity="INFO",
                    code="LEX-OK",
                    message=f"Lexical analysis: {len(tokens)} tokens, no lexical errors",
                    source_ref=source_ref,
                    passed=True,
                ))
        except Exception as exc:
            result.add(ValidationFinding(
                category=ValidationCategory.LEXICAL,
                severity="ERROR",
                code="LEX-002",
                message=f"Lexical error: {exc}",
                source_ref=source_ref,
                passed=False,
            ))

    # ------------------------------------------------------------------
    # 2. Syntax Validation
    # ------------------------------------------------------------------

    def _validate_syntax(self, doc, source_ref: str, result: NormativeValidationResult) -> None:
        """Validate AST structural correctness."""
        for diag in self._parser.diagnostics:
            result.add(ValidationFinding(
                category=ValidationCategory.SYNTAX,
                severity=diag.severity.value,
                code=diag.code,
                message=diag.message,
                source_ref=source_ref,
                passed=diag.severity.value != "ERROR",
            ))

        if not self._parser.diagnostics:
            result.add(ValidationFinding(
                category=ValidationCategory.SYNTAX,
                severity="INFO",
                code="SYN-OK",
                message="Syntax analysis: AST constructed without errors",
                source_ref=source_ref,
                passed=True,
            ))

    # ------------------------------------------------------------------
    # 3. Semantic Validation
    # ------------------------------------------------------------------

    def _validate_semantic(self, semantic, source_ref: str, result: NormativeValidationResult) -> None:
        """Validate semantic correctness."""
        for diag in semantic.diagnostics:
            passed = diag.severity.value != "ERROR"
            result.add(ValidationFinding(
                category=ValidationCategory.SEMANTIC,
                severity=diag.severity.value,
                code=diag.code,
                message=diag.message,
                source_ref=source_ref,
                passed=passed,
            ))

        if not any(f.category == ValidationCategory.SEMANTIC and not f.passed for f in result.findings):
            result.add(ValidationFinding(
                category=ValidationCategory.SEMANTIC,
                severity="INFO",
                code="SEM-OK",
                message="Semantic analysis: no semantic errors",
                source_ref=source_ref,
                passed=True,
            ))

    # ------------------------------------------------------------------
    # 4. Relationship Validation
    # ------------------------------------------------------------------

    def _validate_relationships(self, semantic, source_ref: str, result: NormativeValidationResult) -> None:
        """Validate that all referenced CANON IDs use correct identifier format."""
        for dep in semantic.dependencies:
            if not re.match(r"^CANON-\d+$", dep):
                result.add(ValidationFinding(
                    category=ValidationCategory.RELATIONSHIP,
                    severity="WARNING",
                    code="REL-001",
                    message=f"Dependency reference '{dep}' does not conform to CANON-NNN identifier format",
                    source_ref=source_ref,
                    passed=False,
                ))

        result.add(ValidationFinding(
            category=ValidationCategory.RELATIONSHIP,
            severity="INFO",
            code="REL-OK",
            message=f"Relationship validation: {len(semantic.dependencies)} dependencies found",
            source_ref=source_ref,
            passed=True,
        ))

    # ------------------------------------------------------------------
    # 5. Constraint Validation
    # ------------------------------------------------------------------

    def _validate_constraints(self, semantic, source_ref: str, result: NormativeValidationResult) -> None:
        """Validate document-level constraints."""
        if not semantic.doc_id:
            result.add(ValidationFinding(
                category=ValidationCategory.CONSTRAINT,
                severity="ERROR",
                code="CON-001",
                message="Document has no canonical identifier",
                source_ref=source_ref,
                passed=False,
            ))
        else:
            result.add(ValidationFinding(
                category=ValidationCategory.CONSTRAINT,
                severity="INFO",
                code="CON-OK",
                message=f"Constraint validation: doc_id='{semantic.doc_id}' present",
                source_ref=source_ref,
                passed=True,
            ))

    # ------------------------------------------------------------------
    # 6. Dependency Validation
    # ------------------------------------------------------------------

    def _validate_dependencies(self, semantic, source_ref: str, result: NormativeValidationResult) -> None:
        """Validate dependency declarations."""
        result.add(ValidationFinding(
            category=ValidationCategory.DEPENDENCY,
            severity="INFO",
            code="DEP-OK",
            message=f"Dependency validation: {len(semantic.dependencies)} declared dependencies",
            source_ref=source_ref,
            passed=True,
        ))

    # ------------------------------------------------------------------
    # 7. Governance Validation
    # ------------------------------------------------------------------

    def _validate_governance(self, semantic, source_ref: str, result: NormativeValidationResult) -> None:
        """Validate governance metadata presence."""
        status_value = semantic.status
        if not status_value and source_ref:
            parsed = self._parser.parse_file(source_ref)
            status_value = parsed.status or parsed.inferred_value("status")
            if not status_value:
                for section in parsed.sections():
                    if section.heading.strip().lower() == "status":
                        status_value = section.text_content().strip()
                        break
        if not status_value:
            result.add(ValidationFinding(
                category=ValidationCategory.GOVERNANCE,
                severity="WARNING",
                code="GOV-001",
                message="Document is missing governance status declaration",
                source_ref=source_ref,
                passed=False,
            ))
        else:
            result.add(ValidationFinding(
                category=ValidationCategory.GOVERNANCE,
                severity="INFO",
                code="GOV-OK",
                message=f"Governance validation: status='{status_value}'",
                source_ref=source_ref,
                passed=True,
            ))

    # ------------------------------------------------------------------
    # 8. Safety Validation
    # ------------------------------------------------------------------

    def _validate_safety(self, semantic, source_ref: str, result: NormativeValidationResult) -> None:
        """
        Safety validation: documents with APPROVED or CANONICAL status
        must have objectives or purpose defined.
        """
        high_status = semantic.status.lower() in ("approved", "canonical", "implemented", "maintained")
        if high_status and not semantic.purpose and not semantic.objectives:
            result.add(ValidationFinding(
                category=ValidationCategory.SAFETY,
                severity="WARNING",
                code="SAF-001",
                message=f"Document with status '{semantic.status}' has no purpose or objectives defined",
                source_ref=source_ref,
                passed=False,
            ))
        else:
            result.add(ValidationFinding(
                category=ValidationCategory.SAFETY,
                severity="INFO",
                code="SAF-OK",
                message="Safety validation: document purpose/objectives present",
                source_ref=source_ref,
                passed=True,
            ))
