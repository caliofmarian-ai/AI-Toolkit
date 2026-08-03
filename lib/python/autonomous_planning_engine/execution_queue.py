"""
Autonomous Planning Engine — Execution Queue Builder
CORE-014J

Assembles an ordered, dependency-safe execution queue from all individual
planner outputs.  Each entry carries:
  - entry_id
  - title
  - type   (core | issue | batch | pr | milestone | repository)
  - priority
  - reason
  - dependencies
  - estimated_effort
  - confidence
  - blocked_by

Ordering:
  1. Unblocked entries sorted by priority score (Critical → High → Medium → Low)
  2. Blocked entries appended at the end

Dependencies are respected via DependencyResolver.resolve_entries().
"""

from typing import Any, Dict, List, Mapping

from .dependency_resolver import DependencyResolver
from .models import (
    PLANNING_VERSION,
    PRIORITY_BLOCKED,
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_LOW,
    PRIORITY_MEDIUM,
    ExecutionQueue,
    PlanningEntry,
)
from .priority_optimizer import PriorityOptimizer

_PRIORITY_RANK = {
    PRIORITY_CRITICAL: 0,
    PRIORITY_HIGH: 1,
    PRIORITY_MEDIUM: 2,
    PRIORITY_LOW: 3,
    PRIORITY_BLOCKED: 4,
}


class ExecutionQueueBuilder:
    """
    CORE-014J — Execution Queue Builder.

    Combines entries from all planners, applies priority optimisation,
    and resolves dependencies to produce a final execution queue.
    """

    def __init__(self, repository_root: str = ".") -> None:
        self._resolver = DependencyResolver(repository_root)
        self._optimizer = PriorityOptimizer()

    def build(
        self,
        entries: List[PlanningEntry],
        snapshot: Mapping[str, Any],
        queue_id: str,
        generated_at: str,
        repository: str,
    ) -> ExecutionQueue:
        """
        Build the final execution queue.

        Parameters
        ----------
        entries:
            All PlanningEntry items from individual planners (may be
            unsorted, may contain blocked items).
        snapshot:
            DevelopmentStateManager.GenerateExecutiveSnapshot output.
        queue_id, generated_at, repository:
            Metadata for the resulting ExecutionQueue.
        """
        if not entries:
            return ExecutionQueue(
                queue_id=queue_id,
                generated_at=generated_at,
                schema_version=PLANNING_VERSION,
                repository=repository,
                entries=[],
            )

        # Derive CORE dependency map for priority scoring
        dep_graph = self._resolver.core_dependency_map()

        # Apply priority optimisation
        optimised = self._optimizer.optimize(entries, snapshot, dep_graph)

        # Resolve dependency order
        entry_dicts = [e.to_dict() for e in optimised]
        resolved_dicts = self._resolver.resolve_entries(entry_dicts)

        # Reconstruct PlanningEntry objects in resolved order
        entry_index: Dict[str, PlanningEntry] = {e.entry_id: e for e in optimised}
        resolved: List[PlanningEntry] = []
        seen = set()
        for d in resolved_dicts:
            eid = d["entry_id"]
            if eid in entry_index and eid not in seen:
                resolved.append(entry_index[eid])
                seen.add(eid)

        # Stable sort: blocked last, then by priority rank, then by entry_id
        resolved.sort(
            key=lambda e: (
                1 if e.blocked_by else 0,
                _PRIORITY_RANK.get(e.priority, 3),
                e.entry_id,
            )
        )

        return ExecutionQueue(
            queue_id=queue_id,
            generated_at=generated_at,
            schema_version=PLANNING_VERSION,
            repository=repository,
            entries=resolved,
        )

    @staticmethod
    def deduplicate(entries: List[PlanningEntry]) -> List[PlanningEntry]:
        """Remove duplicate entries by entry_id, keeping first occurrence."""
        seen: set = set()
        result: List[PlanningEntry] = []
        for e in entries:
            if e.entry_id not in seen:
                seen.add(e.entry_id)
                result.append(e)
        return result
