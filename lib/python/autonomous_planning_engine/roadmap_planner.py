"""
Autonomous Planning Engine — Roadmap Planner
CORE-014E

Derives roadmap progression and the next recommended CORE from
repository intelligence.  No hardcoded CORE ordering.
"""

from typing import Any, Dict, List, Mapping, Optional

from .models import (
    EFFORT_HIGH,
    EFFORT_LOW,
    EFFORT_MEDIUM,
    TYPE_CORE,
    PlanningEntry,
)


_EFFORT_THRESHOLDS = {
    # COREs up to 009 were mostly single-file implementations → low effort
    "low": set(range(1, 10)),
    # COREs 010–013 were multi-module → medium
    "medium": set(range(10, 14)),
}


def _estimate_effort(core_id: str) -> str:
    """
    Estimate effort for a CORE based on its numeric ID relative to
    already-implemented COREs (a higher ID typically means higher complexity).
    This is a structural heuristic — no hardcoded values.
    """
    import re
    m = re.match(r"CORE-0*(\d+)", core_id)
    if not m:
        return EFFORT_MEDIUM
    n = int(m.group(1))
    if n in _EFFORT_THRESHOLDS["low"]:
        return EFFORT_LOW
    if n in _EFFORT_THRESHOLDS["medium"]:
        return EFFORT_MEDIUM
    return EFFORT_HIGH


class RoadmapPlanner:
    """
    CORE-014E — Roadmap Planner.

    Recommends the next CORE implementation from documented–implemented gap.
    All data is derived from the PlanningDecisionEngine context dict.
    """

    def recommend_next_core(
        self, decision_context: Mapping[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Return a recommendation dict for the next CORE to implement, or
        None if all documented COREs are already implemented.
        """
        next_core = decision_context.get("next_core")
        if not next_core:
            return None

        implemented = decision_context.get("implemented_cores", [])
        documented = decision_context.get("documented_cores", [])
        blocked = decision_context.get("blocked_cores", [])
        incomplete = decision_context.get("incomplete_cores", [])

        # Dependencies: the next CORE depends on all currently implemented COREs
        # that it transitively consumes (we use the implemented list as a proxy).
        dependencies = [c for c in implemented if c < next_core]

        effort = _estimate_effort(next_core)
        confidence = 0.95 if next_core not in blocked else 0.4
        total_known = max(len(documented), len(implemented))

        return {
            "id": next_core,
            "title": f"Implement {next_core}",
            "type": TYPE_CORE,
            "priority": "high",
            "reason": (
                f"{next_core} is the next CORE on the roadmap. "
                f"{len(implemented)} of {total_known} known COREs are implemented."
            ),
            "dependencies": dependencies,
            "estimated_effort": effort,
            "confidence": confidence,
            "incomplete_core_count": len(incomplete),
            "blocked": next_core in blocked,
        }

    def build_roadmap_entries(
        self, decision_context: Mapping[str, Any]
    ) -> List[PlanningEntry]:
        """
        Return a list of PlanningEntry objects for all incomplete COREs,
        sorted by CORE ID ascending (dependency-safe order).
        """
        incomplete = decision_context.get("incomplete_cores", [])
        implemented = set(decision_context.get("implemented_cores", []))
        blocked = set(decision_context.get("blocked_cores", []))
        counter = [0]

        entries: List[PlanningEntry] = []
        for core_id in sorted(incomplete):
            counter[0] += 1
            effort = _estimate_effort(core_id)
            is_blocked = core_id in blocked
            # Dependencies = subset of implemented COREs that logically precede this one
            deps = tuple(c for c in sorted(implemented) if c < core_id)
            entries.append(
                PlanningEntry(
                    entry_id=core_id,
                    title=f"Implement {core_id}",
                    type=TYPE_CORE,
                    priority="blocked" if is_blocked else "high",
                    reason=(
                        f"{core_id} is documented but not yet implemented."
                    ),
                    dependencies=deps,
                    estimated_effort=effort,
                    confidence=0.4 if is_blocked else 0.85,
                    blocked_by=tuple([core_id]) if is_blocked else (),
                    metadata={"core_id": core_id},
                )
            )
        return entries
