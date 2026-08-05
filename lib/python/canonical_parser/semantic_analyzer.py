"""
CSL Semantic Analyzer — Canonical Specification Language v1.0.0

Assigns engineering meaning to AST nodes.
Produces semantic annotations and semantic diagnostics.

CSL Reference: Volume III (Semantic Model), Volume V Chapter 8 (Semantic Analysis)
CORE: CORE-023-005
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .ast_nodes import (
    AstNodeType,
    BulletItemNode,
    BulletListNode,
    DocumentNode,
    MetadataNode,
    SectionNode,
)
from .diagnostics import (
    Diagnostic,
    DiagnosticCategory,
    DiagnosticCollection,
    DiagnosticSeverity,
)
from .lexer import SourceLocation


_CANON_REF_RE = re.compile(r"(CANON-\d+)")
_VERSION_RE = re.compile(r"^\d+\.\d+(\.\d+)?$")


@dataclass(frozen=True)
class SemanticAnnotation:
    """Semantic annotation for an AST node."""

    node_id: str
    semantic_type: str
    properties: Dict[str, object] = field(default_factory=dict)
    canonical_refs: List[str] = field(default_factory=list)
    source_ref: str = ""


@dataclass
class SemanticResult:
    """Output of semantic analysis for one document."""

    doc_id: str
    title: str
    version: str
    status: str
    purpose: str = ""
    objectives: List[str] = field(default_factory=list)
    scope_included: List[str] = field(default_factory=list)
    scope_excluded: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    invariants: List[str] = field(default_factory=list)
    sections: List[Dict] = field(default_factory=list)
    annotations: List[SemanticAnnotation] = field(default_factory=list)
    diagnostics: DiagnosticCollection = field(default_factory=DiagnosticCollection)


class SemanticAnalyzer:
    """
    CSL Semantic Analyzer.

    Takes a DocumentNode (AST) and produces a SemanticResult.
    Validates semantic rules from Volume III and produces diagnostics.
    """

    def analyze(self, doc: DocumentNode) -> SemanticResult:
        diag = DiagnosticCollection()
        result = SemanticResult(
            doc_id=doc.doc_id or doc.title,
            title=doc.title,
            version=doc.version,
            status=doc.status,
            diagnostics=diag,
        )

        # Validate required metadata
        self._validate_metadata(doc, result, diag)

        # Extract semantics from sections
        section_index = 0
        for section in doc.sections():
            sec_data = self._analyze_section(section, result, diag)
            sec_data["index"] = section_index
            result.sections.append(sec_data)
            section_index += 1

        # Semantic rules
        self._check_dependency_references(result, diag)

        return result

    def _validate_metadata(self, doc: DocumentNode, result: SemanticResult, diag: DiagnosticCollection) -> None:
        if not doc.version:
            diag.warning(
                "SEM-001",
                f"Document '{doc.doc_id}' is missing a Version declaration",
                DiagnosticCategory.SEMANTIC,
                source_ref=doc.source_path,
            )
        elif not _VERSION_RE.match(doc.version):
            diag.warning(
                "SEM-002",
                f"Document '{doc.doc_id}' version '{doc.version}' does not match expected semver format",
                DiagnosticCategory.SEMANTIC,
                source_ref=doc.source_path,
            )

        if not doc.status:
            diag.warning(
                "SEM-003",
                f"Document '{doc.doc_id}' is missing a Status declaration",
                DiagnosticCategory.SEMANTIC,
                source_ref=doc.source_path,
            )

        if not doc.title:
            diag.error(
                "SEM-004",
                f"Document at '{doc.source_path}' has no title (H1 heading)",
                DiagnosticCategory.SEMANTIC,
                source_ref=doc.source_path,
            )

    def _analyze_section(self, section: SectionNode, result: SemanticResult, diag: DiagnosticCollection) -> Dict:
        heading_lower = section.heading.lower().strip()
        content = section.text_content()

        sec_data: Dict = {
            "id": f"{result.doc_id}:section:{self._slugify(section.heading)}",
            "heading": section.heading,
            "content": content,
            "bullets": [],
            "metadata": {},
        }

        # Extract bullets
        for bl in section.find_all(AstNodeType.BULLET_LIST):
            if isinstance(bl, BulletListNode):
                for item in bl.items():
                    sec_data["bullets"].append(item.text)

        # Extract section-level metadata
        for meta in section.find_all(AstNodeType.METADATA):
            if isinstance(meta, MetadataNode):
                sec_data["metadata"][meta.key.lower()] = meta.value

        # Semantic extraction by known section names
        if heading_lower in ("purpose",):
            result.purpose = content

        elif heading_lower in ("objectives", "goals"):
            if sec_data["bullets"]:
                result.objectives = sec_data["bullets"]
            elif content:
                result.objectives = [line.strip() for line in content.splitlines() if line.strip()]

        elif heading_lower in ("dependencies",):
            refs = _CANON_REF_RE.findall(content)
            for ref in refs:
                if ref not in result.dependencies:
                    result.dependencies.append(ref)

        elif heading_lower in ("invariants",):
            if sec_data["bullets"]:
                result.invariants = sec_data["bullets"]
            elif content:
                result.invariants = [line.strip() for line in content.splitlines() if line.strip()]

        elif heading_lower in ("scope",):
            included, excluded = self._extract_scope(content, sec_data["bullets"])
            result.scope_included = included
            result.scope_excluded = excluded

        return sec_data

    def _extract_scope(self, content: str, bullets: List[str]) -> Tuple[List[str], List[str]]:
        included: List[str] = []
        excluded: List[str] = []
        state = None
        for line in content.splitlines():
            stripped = line.strip().lower()
            if stripped.startswith("included"):
                state = "included"
                continue
            if stripped.startswith("excluded"):
                state = "excluded"
                continue
            if line.strip().startswith("- "):
                item = line.strip()[2:].strip()
                if state == "excluded":
                    excluded.append(item)
                else:
                    included.append(item)
        if not included and not excluded:
            included = bullets
        return included, excluded

    def _check_dependency_references(self, result: SemanticResult, diag: DiagnosticCollection) -> None:
        for dep in result.dependencies:
            if not _CANON_REF_RE.match(dep):
                diag.warning(
                    "SEM-010",
                    f"Dependency reference '{dep}' does not match CANON-NNN identifier format",
                    DiagnosticCategory.RELATIONSHIP,
                    source_ref=result.doc_id,
                )

    def _slugify(self, value: str) -> str:
        value = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
        return value.strip("_")
