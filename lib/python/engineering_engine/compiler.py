from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from python.canonical_parser import CslParser, SemanticAnalyzer
from python.canonical_entities import UniversalEngineeringModel, UemBuilder
from python.validation_engine import CslNormativeValidator, NormativeValidationResult
from .generator_framework import ArtifactGenerator, GeneratorArtifact, GeneratorRegistry, GeneratorRunner, default_registry

logger = logging.getLogger(__name__)


@dataclass
class CompilationResult:
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
    def __init__(self, generator_registry: Optional[GeneratorRegistry] = None) -> None:
        self._parser = CslParser()
        self._analyzer = SemanticAnalyzer()
        self._uem_builder = UemBuilder()
        self._validator = CslNormativeValidator()
        self._registry = generator_registry or default_registry()
        self._runner = GeneratorRunner(self._registry)
    def compile(self, docs_path, run_generators: bool = True) -> CompilationResult:
        docs_path = Path(docs_path)
        result = CompilationResult(source_path=str(docs_path))
        csl_files = sorted(docs_path.glob('*.csl'))
        if not csl_files:
            result.errors.append(f'No *.csl files found in {docs_path}')
            return result
        semantic_results = []
        validation_results = []
        for csl_file in csl_files:
            try:
                text = csl_file.read_text(encoding='utf-8')
                doc = self._parser.parse_text(text, source_name=str(csl_file))
                semantic = self._analyzer.analyze(doc)
                semantic_results.append(semantic)
                validation = self._validator.validate_text(text, source_ref=str(csl_file))
                validation_results.append(validation)
                for finding in validation.errors():
                    result.errors.append(f"{csl_file.name}: [{finding.code}] {finding.message}")
                for finding in validation.warnings():
                    result.warnings.append(f"{csl_file.name}: [{finding.code}] {finding.message}")
            except Exception as exc:
                result.errors.append(f'{csl_file.name}: compilation error: {exc}')
        result.validation_results = validation_results
        result.uem = self._uem_builder.build(semantic_results)
        result.validation_results.append(self._validator.validate_uem(result.uem))
        if run_generators and result.uem is not None:
            try:
                result.artifacts = self._runner.run_all(result.uem)
            except Exception as exc:
                result.warnings.append(f'Artifact generation error: {exc}')
        result.stats = {'source_files': len(csl_files), 'semantic_results': len(semantic_results), 'uem_objects': len(result.uem or []), 'validation_results': len(result.validation_results), 'artifacts': len(result.artifacts), 'errors': len(result.errors), 'warnings': len(result.warnings)}
        return result
    def register_generator(self, generator: ArtifactGenerator) -> None:
        self._registry.register(generator)
    def registered_generators(self) -> List[str]:
        return self._registry.ids()
