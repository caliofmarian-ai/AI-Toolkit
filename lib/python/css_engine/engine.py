"""
CSS Engine — Canonical Specification Standard Execution Engine

Loads and validates canonical standards against CSS-000 through CSS-005.
Capabilities:
  - canonical standard loading
  - canonical standard validation
  - canonical metadata validation
  - version validation
  - cross-reference validation
  - canonical dependency validation
  - diagnostic generation
  - structured validation output
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


# Required header fields per CSS-001
_REQUIRED_HEADER_FIELDS = ("Version", "Status", "Classification", "Standard Family", "Identifier", "Owner")

# Required top-level sections per CSS-000 §6
_REQUIRED_SECTIONS = ("Purpose", "Scope", "Objectives")

# Valid status values per CSS-003
_VALID_STATUSES = frozenset(["Draft", "Normative", "Deprecated", "Superseded", "Archived", "Active"])

# Version pattern: semver
_VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")

# Normative keywords per CSS-003
_NORMATIVE_KEYWORDS = ("shall", "must", "may", "should", "will")


@dataclass
class CSSStandardRecord:
    """In-memory representation of a loaded CSS standard."""

    path: str
    identifier: str
    title: str
    version: str
    status: str
    classification: str
    standard_family: str
    owner: str
    sections: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    raw_text: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "identifier": self.identifier,
            "title": self.title,
            "version": self.version,
            "status": self.status,
            "classification": self.classification,
            "standard_family": self.standard_family,
            "owner": self.owner,
            "sections": self.sections,
            "dependencies": self.dependencies,
        }


@dataclass
class CSSDiagnostic:
    code: str
    message: str
    severity: str  # ERROR | WARNING | INFO
    path: str = ""

    def to_dict(self) -> Dict[str, str]:
        return {"code": self.code, "message": self.message, "severity": self.severity, "path": self.path}


@dataclass
class CSSValidationResult:
    """Structured output of CSS Engine validation for a single standard."""

    path: str
    identifier: str
    passed: bool
    diagnostics: List[CSSDiagnostic] = field(default_factory=list)

    @property
    def errors(self) -> List[CSSDiagnostic]:
        return [d for d in self.diagnostics if d.severity == "ERROR"]

    @property
    def warnings(self) -> List[CSSDiagnostic]:
        return [d for d in self.diagnostics if d.severity == "WARNING"]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "identifier": self.identifier,
            "passed": self.passed,
            "diagnostics": [d.to_dict() for d in self.diagnostics],
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
        }


class CSSEngine:
    """
    Executable CSS Engine.

    Loads canonical standard documents and validates them against
    the Canonical Specification Standard (CSS-000 through CSS-005).
    """

    def __init__(self, standards_root: Optional[str] = None) -> None:
        self._root = Path(standards_root).resolve() if standards_root else None
        self._records: Dict[str, CSSStandardRecord] = {}

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load(self, path: str) -> CSSStandardRecord:
        """Load a single canonical standard from a markdown file."""
        p = Path(path)
        text = p.read_text(encoding="utf-8")
        record = self._parse_standard(str(p), text)
        self._records[record.identifier] = record
        return record

    def load_directory(self, directory: str) -> List[CSSStandardRecord]:
        """Load all markdown files from a directory as canonical standards."""
        records: List[CSSStandardRecord] = []
        for md in sorted(Path(directory).rglob("*.md")):
            try:
                record = self.load(str(md))
                records.append(record)
            except Exception:
                pass
        return records

    def loaded_standards(self) -> List[CSSStandardRecord]:
        return list(self._records.values())

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self, record: CSSStandardRecord) -> CSSValidationResult:
        """Validate a CSSStandardRecord against CSS normative requirements."""
        diagnostics: List[CSSDiagnostic] = []

        self._validate_metadata(record, diagnostics)
        self._validate_version(record, diagnostics)
        self._validate_status(record, diagnostics)
        self._validate_required_sections(record, diagnostics)
        self._validate_normative_language(record, diagnostics)
        self._validate_cross_references(record, diagnostics)
        self._validate_dependencies(record, diagnostics)

        passed = all(d.severity != "ERROR" for d in diagnostics)
        return CSSValidationResult(path=record.path, identifier=record.identifier, passed=passed, diagnostics=diagnostics)

    def validate_all(self) -> List[CSSValidationResult]:
        """Validate every loaded standard."""
        return [self.validate(record) for record in self._records.values()]

    def diagnostics_report(self) -> Dict[str, Any]:
        """Return a structured diagnostics report across all loaded standards."""
        results = self.validate_all()
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        all_errors = [d.to_dict() for r in results for d in r.errors]
        all_warnings = [d.to_dict() for r in results for d in r.warnings]
        return {
            "total_standards": total,
            "passed": passed,
            "failed": total - passed,
            "total_errors": len(all_errors),
            "total_warnings": len(all_warnings),
            "results": [r.to_dict() for r in results],
        }

    # ------------------------------------------------------------------
    # Internal parsing
    # ------------------------------------------------------------------

    def _parse_standard(self, path: str, text: str) -> CSSStandardRecord:
        lines = text.splitlines()

        title = ""
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("# "):
                title = stripped[2:].strip()
                break

        def _extract_field(field_name: str) -> str:
            pattern = re.compile(rf"^\*\*{re.escape(field_name)}\*\*\s*[:\-]\s*(.+)$|^{re.escape(field_name)}:\s*(.+)$", re.IGNORECASE)
            for line in lines:
                m = pattern.match(line.strip())
                if m:
                    return (m.group(1) or m.group(2) or "").strip()
            return ""

        version = _extract_field("Version")
        status = _extract_field("Status")
        classification = _extract_field("Classification")
        standard_family = _extract_field("Standard Family")
        identifier = _extract_field("Identifier")
        owner = _extract_field("Owner")

        # Derive identifier from filename when not present in body
        if not identifier:
            identifier = Path(path).stem

        # Extract section headings (## level)
        sections = []
        for line in lines:
            m = re.match(r"^##\s+(.+)$", line.strip())
            if m:
                sections.append(m.group(1).strip())

        # Extract cross-reference mentions (e.g. CSS-001, CDM-003)
        dependencies = list(dict.fromkeys(re.findall(r"\b(?:CSS|CDM|CSL|CANON|AR|ADR|RFC)-\d+\b", text)))

        return CSSStandardRecord(
            path=path,
            identifier=identifier,
            title=title,
            version=version,
            status=status,
            classification=classification,
            standard_family=standard_family,
            owner=owner,
            sections=sections,
            dependencies=dependencies,
            raw_text=text,
        )

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    def _validate_metadata(self, record: CSSStandardRecord, diags: List[CSSDiagnostic]) -> None:
        for field_name in _REQUIRED_HEADER_FIELDS:
            value = getattr(record, field_name.lower().replace(" ", "_"), "") or ""
            if not value.strip():
                diags.append(CSSDiagnostic(
                    code="CSS-V001",
                    message=f"Required metadata field missing: {field_name}",
                    severity="ERROR",
                    path=record.path,
                ))

    def _validate_version(self, record: CSSStandardRecord, diags: List[CSSDiagnostic]) -> None:
        if record.version and not _VERSION_RE.match(record.version.strip()):
            diags.append(CSSDiagnostic(
                code="CSS-V002",
                message=f"Version '{record.version}' does not conform to semver (MAJOR.MINOR.PATCH)",
                severity="ERROR",
                path=record.path,
            ))

    def _validate_status(self, record: CSSStandardRecord, diags: List[CSSDiagnostic]) -> None:
        if record.status and record.status.strip() not in _VALID_STATUSES:
            diags.append(CSSDiagnostic(
                code="CSS-V003",
                message=f"Status '{record.status}' is not a valid canonical lifecycle status",
                severity="WARNING",
                path=record.path,
            ))

    def _validate_required_sections(self, record: CSSStandardRecord, diags: List[CSSDiagnostic]) -> None:
        section_text = " ".join(record.sections).lower()
        for required in _REQUIRED_SECTIONS:
            if required.lower() not in section_text:
                diags.append(CSSDiagnostic(
                    code="CSS-V004",
                    message=f"Required section missing: {required}",
                    severity="WARNING",
                    path=record.path,
                ))

    def _validate_normative_language(self, record: CSSStandardRecord, diags: List[CSSDiagnostic]) -> None:
        text_lower = record.raw_text.lower()
        has_normative = any(kw in text_lower for kw in _NORMATIVE_KEYWORDS)
        if not has_normative:
            diags.append(CSSDiagnostic(
                code="CSS-V005",
                message="No normative language (shall/must/may/should) detected",
                severity="WARNING",
                path=record.path,
            ))

    def _validate_cross_references(self, record: CSSStandardRecord, diags: List[CSSDiagnostic]) -> None:
        for dep in record.dependencies:
            if dep == record.identifier:
                diags.append(CSSDiagnostic(
                    code="CSS-V006",
                    message=f"Self-reference detected: {dep}",
                    severity="WARNING",
                    path=record.path,
                ))

    def _validate_dependencies(self, record: CSSStandardRecord, diags: List[CSSDiagnostic]) -> None:
        if len(record.dependencies) > 50:
            diags.append(CSSDiagnostic(
                code="CSS-V007",
                message=f"Excessive dependency count: {len(record.dependencies)} references found",
                severity="WARNING",
                path=record.path,
            ))

    def statistics(self) -> Dict[str, Any]:
        return {
            "loaded_standards": len(self._records),
            "identifiers": sorted(self._records.keys()),
        }
