from __future__ import annotations

from dataclasses import dataclass, field

from lib.python.engineering_engine.batch_planner_engine import (
    EngineeringBatch,
)


@dataclass(slots=True)
class Roadmap:

    phases: list[EngineeringBatch] = field(default_factory=list)


class RoadmapEngine:

    def build(
        self,
        batches: list[EngineeringBatch],
    ) -> Roadmap:

        priority_order = {
            "HIGH": 0,
            "MEDIUM": 1,
            "LOW": 2,
        }

        ordered = sorted(
            batches,
            key=lambda b: (
                priority_order.get(b.priority, 99),
                b.id,
            ),
        )

        return Roadmap(
            phases=ordered,
        )
