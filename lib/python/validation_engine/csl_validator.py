from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List

from python.canonical_parser import CslLexer, CslParser, SemanticAnalyzer, TokenType
from python.canonical_entities import UniversalEngineeringModel


class ValidationCategory(str, Enum):
    LEXICAL = 'LEXICAL'
    SYNTAX = 'SYNTAX'
    SEMANTIC = 'SEMANTIC'
    RELATIONSHIP = 'RELATIONSHIP'
    CONSTRAINT = 'CONSTRAINT'
    DEPENDENCY = 'DEPENDENCY'
    GOVERNANCE = 'GOVERNANCE'
    SAFETY = 'SAFETY'


@dataclass
class ValidationFinding:
    category: ValidationCategory
    severity: str
    code: str
    message: str
    source_ref: str = ''
    passed: bool = True


@dataclass
class NormativeValidationResult:
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
        return [f for f in self.findings if f.severity == 'ERROR']
    def warnings(self) -> List[ValidationFinding]:
        return [f for f in self.findings if f.severity == 'WARNING']


class CslNormativeValidator:
    def __init__(self) -> None:
        self._parser = CslParser()
        self._analyzer = SemanticAnalyzer()
    def validate_text(self, text: str, source_ref: str = '') -> NormativeValidationResult:
        result = NormativeValidationResult(source_ref=source_ref)
        self._validate_lexical(text, source_ref, result)
        doc = self._parser.parse_text(text, source_name=source_ref)
        self._validate_syntax(source_ref, result)
        semantic = self._analyzer.analyze(doc)
        self._validate_semantic(semantic, source_ref, result)
        self._validate_relationships(semantic, source_ref, result)
        self._validate_constraints(semantic, source_ref, result)
        self._validate_dependencies(semantic, source_ref, result)
        self._validate_governance(semantic, source_ref, result)
        self._validate_safety(text, semantic, source_ref, result)
        return result
    def validate_file(self, path) -> NormativeValidationResult:
        path = Path(path)
        return self.validate_text(path.read_text(encoding='utf-8'), source_ref=str(path))
    def validate_uem(self, uem: UniversalEngineeringModel) -> NormativeValidationResult:
        result = NormativeValidationResult(source_ref='UEM')
        if len(uem) == 0:
            result.add(ValidationFinding(ValidationCategory.CONSTRAINT, 'WARNING', 'UEM-001', 'Universal Engineering Model contains no Engineering Objects', 'UEM', False))
        else:
            result.add(ValidationFinding(ValidationCategory.CONSTRAINT, 'INFO', 'UEM-002', f'UEM contains {len(uem)} Engineering Objects', 'UEM', True))
        stats = uem.statistics()
        result.add(ValidationFinding(ValidationCategory.SEMANTIC, 'INFO', 'UEM-003', f"UEM has {stats['total_relationships']} relationships across {stats['source_documents']} source documents", 'UEM', True))
        return result
    def _validate_lexical(self, text: str, source_ref: str, result: NormativeValidationResult) -> None:
        try:
            tokens = CslLexer(text, source_name=source_ref).tokenize()
            if not any(token.token_type == TokenType.KEYWORD for token in tokens):
                result.add(ValidationFinding(ValidationCategory.LEXICAL, 'ERROR', 'CSL-0001', 'No CSL declaration keyword found', source_ref, False))
            else:
                result.add(ValidationFinding(ValidationCategory.LEXICAL, 'INFO', 'LEX-OK', f'Lexical analysis: {len(tokens)} tokens, no lexical errors', source_ref, True))
        except ValueError as exc:
            code = 'CSL-0004' if 'Tab character' in str(exc) else 'CSL-0003' if 'Unterminated string' in str(exc) else 'CSL-0001'
            result.add(ValidationFinding(ValidationCategory.LEXICAL, 'ERROR', code, str(exc), source_ref, False))
    def _validate_syntax(self, source_ref: str, result: NormativeValidationResult) -> None:
        if self._parser.diagnostics:
            for diag in self._parser.diagnostics:
                result.add(ValidationFinding(ValidationCategory.SYNTAX, diag.severity.value, diag.code, diag.message, source_ref, diag.severity.value != 'ERROR'))
        else:
            result.add(ValidationFinding(ValidationCategory.SYNTAX, 'INFO', 'SYN-OK', 'Syntax analysis: AST constructed without errors', source_ref, True))
    def _validate_semantic(self, semantic, source_ref: str, result: NormativeValidationResult) -> None:
        had_error = False
        for diag in semantic.diagnostics:
            passed = diag.severity.value != 'ERROR'
            had_error = had_error or not passed
            result.add(ValidationFinding(ValidationCategory.SEMANTIC, diag.severity.value, diag.code, diag.message, source_ref, passed))
        if not had_error:
            result.add(ValidationFinding(ValidationCategory.SEMANTIC, 'INFO', 'SEM-OK', 'Semantic analysis: no semantic errors', source_ref, True))
    def _validate_relationships(self, semantic, source_ref: str, result: NormativeValidationResult) -> None:
        seen = set()
        duplicate = False
        for relationship in semantic.relationships:
            pair = (relationship['source'], relationship['relation_type'], relationship['target'])
            if pair in seen:
                duplicate = True
                result.add(ValidationFinding(ValidationCategory.RELATIONSHIP, 'WARNING', 'CSL-0205', f'Duplicate relationship detected: {pair}', source_ref, False))
            seen.add(pair)
        if not duplicate:
            result.add(ValidationFinding(ValidationCategory.RELATIONSHIP, 'INFO', 'REL-OK', f'Relationship validation: {len(semantic.relationships)} relationships found', source_ref, True))
    def _validate_constraints(self, semantic, source_ref: str, result: NormativeValidationResult) -> None:
        if not semantic.doc_id:
            result.add(ValidationFinding(ValidationCategory.CONSTRAINT, 'ERROR', 'CSL-0203', 'Document has no canonical identifier', source_ref, False))
        else:
            result.add(ValidationFinding(ValidationCategory.CONSTRAINT, 'INFO', 'CON-OK', f"Constraint validation: doc_id='{semantic.doc_id}' present", source_ref, True))
    def _validate_dependencies(self, semantic, source_ref: str, result: NormativeValidationResult) -> None:
        deps = [r for r in semantic.relationships if r['relation_type'] == 'depends_on']
        result.add(ValidationFinding(ValidationCategory.DEPENDENCY, 'INFO', 'DEP-OK', f'Dependency validation: {len(deps)} declared dependencies', source_ref, True))
    def _validate_governance(self, semantic, source_ref: str, result: NormativeValidationResult) -> None:
        if not semantic.status:
            result.add(ValidationFinding(ValidationCategory.GOVERNANCE, 'WARNING', 'CSL-0403', 'Document is missing governance status declaration', source_ref, False))
        else:
            result.add(ValidationFinding(ValidationCategory.GOVERNANCE, 'INFO', 'GOV-OK', f"Governance validation: status='{semantic.status}'", source_ref, True))
    def _validate_safety(self, text: str, semantic, source_ref: str, result: NormativeValidationResult) -> None:
        if '```' in text or '<script' in text.lower():
            result.add(ValidationFinding(ValidationCategory.SAFETY, 'WARNING', 'CSL-0400', 'Potential injection-style content detected in CSL source', source_ref, False))
        else:
            result.add(ValidationFinding(ValidationCategory.SAFETY, 'INFO', 'SAF-OK', 'Safety validation: no unsafe parsing or injection indicators detected', source_ref, True))
