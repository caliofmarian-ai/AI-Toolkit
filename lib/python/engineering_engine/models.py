from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class EngineeringBatch:
    id: str
    title: str
    objective: str
    priority: str
    status: str
    risk: str
    rationale: str
    affected_modules: list[str] = field(default_factory=list)
    suggested_tests: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ImplementationPackageModel:
    core: str
    title: str
    canonical_references: list[str] = field(default_factory=list)
    objectives: list[str] = field(default_factory=list)
    scope: list[str] = field(default_factory=list)
    deliverables: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    batches: list[EngineeringBatch] = field(default_factory=list)
