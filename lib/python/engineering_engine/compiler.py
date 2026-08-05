"""
CSL Engineering Compiler — Canonical Specification Language v1.0.0

Orchestrates the full compilation pipeline:
Knowledge Acquisition → Lexical Analysis → Parsing → AST →
Semantic Analysis → UEM Construction → Validation → Artifact Generation

CSL Reference: Volume V (Compiler Specification)
CORE: CORE-023-007
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from python.canonical_parser import CslParser, SemanticAnalyzer
from python.canonical_repository import CanonicalRepository
from python.canonical_entities import UniversalEngineeringModel, UemBuilder
from python.validation_engine import CslNormativeValidator, NormativeValidationResult

from .generator_framework import (
    ArtifactGenerator,
    GeneratorArtifact,
    GeneratorRegistry,
    GeneratorRunner,
    default_registry,
)

logger = logging.getLogger(__name__)


@dataclass
class CompilationResult:
    """Result of a full CSL compilation pass."""

    source_path: str
    uem: Optional[UniversalEngineeringModel] = None
    validation_results: List[NormativeValidationResult] = field(default_factory=list)
    artifacts: List[GeneratorArtifact] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)

    def succeeded(self) -> bool:
        return not self.errors and self.uem is not None

    def validation_passed(self) -> bool:
        return all(r.passed() for r in self.validation_results)


class EngineeringCompiler:
    """
    CSL Engineering Compiler.

    The compiler is the single authoritative orchestrator for transforming
    Canonical Knowledge into the UEM and subsequently into Engineering Artifacts.

    Pipeline stages (Volume V Chapter 3):
    1. Knowledge Acquisition
    2. Lexical Analysis
    3. Parsing (AST construction)
    4. Semantic Analysis
    5. UEM Construction
    6. Validation
    7. Artifact Generation

    Every stage is deterministic.
    """

    def __init__(self, generator_registry: Optional[GeneratorRegistry] = None) -> None:
        self._parser = CslParser()
        self._analyzer = SemanticAnalyzer()
        self._uem_builder = UemBuilder()
        self._validator = CslNormativeValidator()
        self._registry = generator_registry or default_registry()
        self._runner = GeneratorRunner(self._registry)

    def compile(self, docs_path, run_generators: bool = True) -> CompilationResult:
        """
        Compile all canonical documents from docs_path.

        Returns a CompilationResult with the UEM, validation results, and artifacts.
        """
        docs_path = Path(docs_path)
        result = CompilationResult(source_path=str(docs_path))

        # Stage 1: Knowledge Acquisition
        logger.debug("Compiler: stage 1 — knowledge acquisition from %s", docs_path)
        canon_files = sorted(docs_path.glob("CANON-*.md"))
        if not canon_files:
            result.errors.append(f"No CANON-*.md files found in {docs_path}")
            return result

        # Stages 2–4: Lex → Parse → Semantic Analysis (per document)
        semantic_results = []
        validation_results = []

        for canon_file in canon_files:
            logger.debug("Compiler: processing %s", canon_file.name)
            try:
                text = canon_file.read_text(encoding="utf-8")

                # Stage 2+3: Lex + Parse
                doc = self._parser.parse_text(text, source_name=str(canon_file))

                # Stage 4: Semantic Analysis
                sem = self._analyzer.analyze(doc)
                semantic_results.append(sem)

                # Stage 6 (per-file): Normative Validation
                val = self._validator.validate_text(text, source_ref=str(canon_file))
                validation_results.append(val)

                for finding in val.errors():
                    result.errors.append(f"{canon_file.name}: [{finding.code}] {finding.message}")
                for finding in val.warnings():
                    result.warnings.append(f"{canon_file.name}: [{finding.code}] {finding.message}")

            except Exception as exc:
                result.errors.append(f"{canon_file.name}: compilation error: {exc}")

        result.validation_results = validation_results

        # Stage 5: UEM Construction
        logger.debug("Compiler: stage 5 — UEM construction from %d semantic results", len(semantic_results))
        uem = self._uem_builder.build(semantic_results)
        result.uem = uem

        # Stage 6 (UEM-level): UEM validation
        uem_val = self._validator.validate_uem(uem)
        result.validation_results.append(uem_val)

        # Stage 7: Artifact Generation
        if run_generators and uem is not None:
            logger.debug("Compiler: stage 7 — artifact generation")
            try:
                artifacts = self._runner.run_all(uem)
                result.artifacts = artifacts
            except Exception as exc:
                result.warnings.append(f"Artifact generation error: {exc}")

        result.stats = {
            "source_files": len(canon_files),
            "semantic_results": len(semantic_results),
            "uem_objects": len(uem),
            "validation_results": len(result.validation_results),
            "artifacts": len(result.artifacts),
            "errors": len(result.errors),
            "warnings": len(result.warnings),
        }

        logger.debug("Compiler: compilation complete — %s", result.stats)
        return result

    def register_generator(self, generator: ArtifactGenerator) -> None:
        """Register an additional artifact generator."""
        self._registry.register(generator)

    def registered_generators(self) -> List[str]:
        return self._registry.ids()
