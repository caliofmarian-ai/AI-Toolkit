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
    acceptance: list[str] = field(default_factory=list)

    @property
    def batch(self) -> str:
        return self.id
