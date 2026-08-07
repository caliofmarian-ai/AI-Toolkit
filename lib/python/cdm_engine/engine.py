"""
CDM Engine — Canonical Document Model Execution Engine

Loads, parses, and materializes canonical documents into structured
CdmDocumentObject instances. Derives from CDM-000 through CDM-019.

Capabilities:
  - document loading
  - document parsing
  - header parsing
  - metadata extraction
  - canonical object materialization
  - dependency extraction
  - traceability extraction
  - provenance preservation
  - validation
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


# Required CDM header fields per CDM-001
_REQUIRED_METADATA = ("Version", "Status", "Classification", "Identifier", "Owner")

# Canonical document lifecycle states per CDM-003
_LIFECYCLE_STATES = frozenset(["Draft", "Normative", "Active", "Deprecated", "Superseded", "Archived"])

# Pattern to detect canonical references (CDM-002)
_CANONICAL_REF_RE = re.compile(r"\b([A-Z]{2,8}-\d{3,})\b")

# Traceability markers
_TRACE_MARKER_RE = re.compile(r"\b(TRACE|TRACKS|IMPLEMENTS|DERIVES-FROM|SUPERSEDES|DEPENDS-ON):\s*([A-Z]{2,8}-\d+)", re.IGNORECASE)


@dataclass
class CdmSection:
    """A section within a canonical document."""

    title: str
    level: int
    content: str
    subsections: List["CdmSection"] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "level": self.level,
            "content_length": len(self.content),
            "subsections": [s.to_dict() for s in self.subsections],
        }


@dataclass
class CdmTraceabilityLink:
    """A traceability relationship extracted from document text."""

    relation: str
    target: str
    source_context: str = ""

    def to_dict(self) -> Dict[str, str]:
        return {"relation": self.relation, "target": self.target}


@dataclass
class CdmDocumentObject:
    """
    Materialized canonical document object.

    Every field derives from CDM-000 through CDM-010.
    """

    path: str
    identifier: str
    title: str
    version: str
    status: str
    classification: str
    owner: str
    standard_family: str
    metadata: Dict[str, str] = field(default_factory=dict)
    sections: List[CdmSection] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    traceability: List[CdmTraceabilityLink] = field(default_factory=list)
    provenance: str = ""
    raw_text: str = ""

    @property
    def section_titles(self) -> List[str]:
        return [s.title for s in self.sections]

    def get_section(self, title: str) -> Optional[CdmSection]:
        for section in self.sections:
            if section.title.lower() == title.lower():
                return section
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "identifier": self.identifier,
            "title": self.title,
            "version": self.version,
            "status": self.status,
            "classification": self.classification,
            "owner": self.owner,
            "standard_family": self.standard_family,
            "metadata": self.metadata,
            "sections": [s.to_dict() for s in self.sections],
            "dependencies": self.dependencies,
            "traceability": [t.to_dict() for t in self.traceability],
            "provenance": self.provenance,
        }


@dataclass
class CdmValidationResult:
    """Result of CDM document validation."""

    path: str
    identifier: str
    passed: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "identifier": self.identifier,
            "passed": self.passed,
            "errors": self.errors,
            "warnings": self.warnings,
        }


class CdmEngine:
    """
    Executable CDM Engine.

    Loads canonical documents (markdown) and materializes them into
    structured CdmDocumentObject instances following the Canonical Document
    Model specification.
    """

    def __init__(self) -> None:
        self._documents: Dict[str, CdmDocumentObject] = {}

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load(self, path: str) -> CdmDocumentObject:
        """Load and materialize a single canonical document."""
        p = Path(path)
        text = p.read_text(encoding="utf-8")
        doc = self._materialize(str(p), text)
        self._documents[doc.identifier] = doc
        return doc

    def load_directory(self, directory: str) -> List[CdmDocumentObject]:
        """Load all markdown documents from a directory."""
        docs: List[CdmDocumentObject] = []
        for md in sorted(Path(directory).rglob("*.md")):
            try:
                docs.append(self.load(str(md)))
            except Exception:
                pass
        return docs

    def get(self, identifier: str) -> Optional[CdmDocumentObject]:
        return self._documents.get(identifier)

    def all_documents(self) -> List[CdmDocumentObject]:
        return list(self._documents.values())

    # ------------------------------------------------------------------
    # Parsing / Materialization
    # ------------------------------------------------------------------

    def _materialize(self, path: str, text: str) -> CdmDocumentObject:
        lines = text.splitlines()

        # Extract title from first H1
        title = ""
        for line in lines:
            if line.strip().startswith("# "):
                title = line.strip()[2:].strip()
                break

        # Extract header metadata (key: value lines)
        metadata = self._extract_metadata(lines)

        identifier = metadata.get("Identifier") or Path(path).stem
        version = metadata.get("Version", "")
        status = metadata.get("Status", "")
        classification = metadata.get("Classification", "")
        owner = metadata.get("Owner", "")
        standard_family = metadata.get("Standard Family", "")

        # Parse sections
        sections = self._parse_sections(lines)

        # Extract canonical dependencies / cross-references
        dependencies = list(dict.fromkeys(_CANONICAL_REF_RE.findall(text)))
        # Remove self-reference
        dependencies = [d for d in dependencies if d != identifier]

        # Extract traceability links
        traceability = [
            CdmTraceabilityLink(relation=m.group(1).upper(), target=m.group(2))
            for m in _TRACE_MARKER_RE.finditer(text)
        ]

        return CdmDocumentObject(
            path=path,
            identifier=identifier,
            title=title,
            version=version,
            status=status,
            classification=classification,
            owner=owner,
            standard_family=standard_family,
            metadata=metadata,
            sections=sections,
            dependencies=dependencies,
            traceability=traceability,
            provenance=path,
            raw_text=text,
        )

    def _extract_metadata(self, lines: List[str]) -> Dict[str, str]:
        """Extract key-value metadata from document header."""
        metadata: Dict[str, str] = {}
        kv_pattern = re.compile(r"^\*\*(.+?)\*\*\s*[:\-]\s*(.+)$|^([A-Za-z][A-Za-z ]+?):\s*(.+)$")
        in_header = True
        for line in lines:
            stripped = line.strip()
            # Stop parsing metadata after first empty line followed by section heading
            if stripped.startswith("## ") or stripped == "---":
                in_header = False
            if not in_header and stripped.startswith("## "):
                break
            m = kv_pattern.match(stripped)
            if m:
                if m.group(1):
                    metadata[m.group(1).strip()] = m.group(2).strip()
                elif m.group(3):
                    metadata[m.group(3).strip()] = m.group(4).strip()
        return metadata

    def _parse_sections(self, lines: List[str]) -> List[CdmSection]:
        """Parse markdown sections from document lines."""
        sections: List[CdmSection] = []
        current_level = 0
        current_title = ""
        current_content: List[str] = []

        def flush(title: str, level: int, content: List[str]) -> Optional[CdmSection]:
            if title:
                return CdmSection(title=title, level=level, content="\n".join(content).strip())
            return None

        for line in lines:
            m = re.match(r"^(#{1,6})\s+(.+)$", line)
            if m:
                level = len(m.group(1))
                title = m.group(2).strip()
                if level >= 2:
                    section = flush(current_title, current_level, current_content)
                    if section:
                        sections.append(section)
                    current_title = title
                    current_level = level
                    current_content = []
            else:
                if current_title:
                    current_content.append(line)

        section = flush(current_title, current_level, current_content)
        if section:
            sections.append(section)

        return sections

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self, doc: CdmDocumentObject) -> CdmValidationResult:
        """Validate a materialized document against CDM requirements."""
        errors: List[str] = []
        warnings: List[str] = []

        for field_name in _REQUIRED_METADATA:
            value = doc.metadata.get(field_name, "") or getattr(doc, field_name.lower().replace(" ", "_"), "")
            if not str(value).strip():
                errors.append(f"CDM-V001: Required metadata field missing: {field_name}")

        if not doc.title:
            errors.append("CDM-V002: Document title (H1) is missing")

        if doc.status and doc.status not in _LIFECYCLE_STATES:
            warnings.append(f"CDM-V003: Status '{doc.status}' is not a standard lifecycle state")

        if not doc.sections:
            warnings.append("CDM-V004: No sections found in document")

        passed = len(errors) == 0
        return CdmValidationResult(
            path=doc.path,
            identifier=doc.identifier,
            passed=passed,
            errors=errors,
            warnings=warnings,
        )

    def validate_all(self) -> List[CdmValidationResult]:
        return [self.validate(doc) for doc in self._documents.values()]

    def statistics(self) -> Dict[str, Any]:
        docs = self.all_documents()
        return {
            "total_documents": len(docs),
            "total_sections": sum(len(d.sections) for d in docs),
            "total_dependencies": sum(len(d.dependencies) for d in docs),
            "total_traceability_links": sum(len(d.traceability) for d in docs),
            "identifiers": sorted(self._documents.keys()),
        }
