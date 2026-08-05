"""
CSL Generator Framework — Canonical Specification Language v1.0.0

Provides the UEM-driven generator contract for all Engineering Artifact
generation. All generators receive the UEM as their sole input.

CSL Reference: RFC-0004 (Artifact Generator Framework), Volume V Chapter 12 (Artifact Generation)
CORE: CORE-023-007
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Type

from python.canonical_entities import UniversalEngineeringModel


# ---------------------------------------------------------------------------
# Artifact types
# ---------------------------------------------------------------------------

class ArtifactType(str, Enum):
    DOCUMENT = "DOCUMENT"
    REPORT = "REPORT"
    ROADMAP = "ROADMAP"
    AUDIT = "AUDIT"
    PLAN = "PLAN"
    PACKAGE = "PACKAGE"
    SCHEMA = "SCHEMA"
    CONFIGURATION = "CONFIGURATION"
    TEST_SUITE = "TEST_SUITE"
    API = "API"


# ---------------------------------------------------------------------------
# Generator contract
# ---------------------------------------------------------------------------

@dataclass
class GeneratorContext:
    """Context passed to every generator invocation."""

    uem: UniversalEngineeringModel
    parameters: Dict[str, Any] = field(default_factory=dict)
    output_path: str = ""
    source_ref: str = ""


@dataclass
class GeneratorArtifact:
    """
    An Engineering Artifact produced by a generator.

    Every artifact carries its complete traceability chain:
    source_document → uem_object_ids → generator → artifact
    """

    artifact_type: ArtifactType
    name: str
    content: Any
    generator_id: str = ""
    source_ref: str = ""
    uem_object_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    # Full traceability chain
    traceability: Dict[str, Any] = field(default_factory=dict)


class ArtifactGenerator(abc.ABC):
    """
    Abstract base class for all CSL artifact generators.

    Every generator:
    - receives the UEM as its sole authoritative input
    - produces GeneratorArtifact instances with full traceability
    - is deterministic (same UEM → same artifacts)
    - never modifies Canonical Knowledge
    """

    generator_id: str = ""
    artifact_type: ArtifactType = ArtifactType.DOCUMENT
    description: str = ""

    @abc.abstractmethod
    def generate(self, context: GeneratorContext) -> List[GeneratorArtifact]:
        """Generate artifacts from the UEM. Must be deterministic."""
        ...

    def can_generate(self, context: GeneratorContext) -> bool:
        """Return True if this generator can produce output for the given context."""
        return True


# ---------------------------------------------------------------------------
# Generator Registry
# ---------------------------------------------------------------------------

class GeneratorRegistry:
    """
    Registry of all available artifact generators.

    Generators are registered by their generator_id.
    The compiler uses the registry to discover available generators.
    """

    def __init__(self) -> None:
        self._generators: Dict[str, ArtifactGenerator] = {}

    def register(self, generator: ArtifactGenerator) -> None:
        """Register a generator."""
        if not generator.generator_id:
            raise ValueError(f"Generator {type(generator).__name__} has no generator_id")
        self._generators[generator.generator_id] = generator

    def get(self, generator_id: str) -> Optional[ArtifactGenerator]:
        return self._generators.get(generator_id)

    def all(self) -> List[ArtifactGenerator]:
        return [self._generators[k] for k in sorted(self._generators)]

    def for_type(self, artifact_type: ArtifactType) -> List[ArtifactGenerator]:
        return [g for g in self._generators.values() if g.artifact_type == artifact_type]

    def ids(self) -> List[str]:
        return sorted(self._generators)

    def __len__(self) -> int:
        return len(self._generators)


# ---------------------------------------------------------------------------
# Generator Runner
# ---------------------------------------------------------------------------

class GeneratorRunner:
    """
    Executes generators from the registry against a UEM.

    All artifacts are produced from the UEM.
    Traceability is preserved for every artifact.
    """

    def __init__(self, registry: GeneratorRegistry) -> None:
        self._registry = registry

    def run_all(self, uem: UniversalEngineeringModel, parameters: Optional[Dict[str, Any]] = None,
                output_path: str = "") -> List[GeneratorArtifact]:
        """Run all registered generators and return all artifacts."""
        context = GeneratorContext(
            uem=uem,
            parameters=parameters or {},
            output_path=output_path,
        )
        artifacts: List[GeneratorArtifact] = []
        for generator in self._registry.all():
            if generator.can_generate(context):
                produced = generator.generate(context)
                artifacts.extend(produced)
        return artifacts

    def run(self, generator_id: str, uem: UniversalEngineeringModel,
            parameters: Optional[Dict[str, Any]] = None, output_path: str = "") -> List[GeneratorArtifact]:
        """Run a specific generator."""
        generator = self._registry.get(generator_id)
        if generator is None:
            raise KeyError(f"Generator '{generator_id}' not found in registry")
        context = GeneratorContext(uem=uem, parameters=parameters or {}, output_path=output_path)
        return generator.generate(context)


# ---------------------------------------------------------------------------
# Built-in: Statistics Generator
# ---------------------------------------------------------------------------

class UemStatisticsGenerator(ArtifactGenerator):
    """Built-in generator: produces UEM statistics report."""

    generator_id = "uem-statistics"
    artifact_type = ArtifactType.REPORT
    description = "Generates a statistics report from the Universal Engineering Model"

    def generate(self, context: GeneratorContext) -> List[GeneratorArtifact]:
        uem = context.uem
        stats = uem.statistics()
        obj_ids = [o.obj_id for o in uem.all_objects()]
        return [
            GeneratorArtifact(
                artifact_type=self.artifact_type,
                name="uem-statistics",
                content=stats,
                generator_id=self.generator_id,
                source_ref="UEM",
                uem_object_ids=obj_ids,
                traceability={
                    "uem_object_count": stats["total_objects"],
                    "uem_relationship_count": stats["total_relationships"],
                    "generator": self.generator_id,
                },
            )
        ]


def default_registry() -> GeneratorRegistry:
    """Return the default generator registry with built-in generators."""
    registry = GeneratorRegistry()
    registry.register(UemStatisticsGenerator())
    return registry
