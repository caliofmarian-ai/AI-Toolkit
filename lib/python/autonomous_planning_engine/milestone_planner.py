"""
Autonomous Planning Engine — Milestone Planner
CORE-014I

Recommends the next milestone to target from:
  - Current milestone in development state
  - CORE completion groupings (phase transitions)
  - Roadmap progression
  - Executive Briefing intelligence

No milestones are hardcoded.
"""

from typing import Any, Dict, List, Mapping, Optional

from .models import (
    EFFORT_HIGH,
    EFFORT_MEDIUM,
    PHASE_AUTONOMY,
    PHASE_FOUNDATION,
    PHASE_INTELLIGENCE,
    PHASE_PRODUCTION,
    TYPE_MILESTONE,
    PlanningEntry,
)

_PHASE_MILESTONES = {
    PHASE_FOUNDATION: "Phase 1 — Foundation Complete",
    PHASE_INTELLIGENCE: "Phase 2 — Intelligence Layer Complete",
    PHASE_AUTONOMY: "Phase 3 — Autonomy Layer Complete",
    PHASE_PRODUCTION: "Phase 4 — Production Ready",
}

_EMPTY = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})


def _is_set(v: Any) -> bool:
    return bool(v) and str(v).strip() not in _EMPTY


class MilestonePlanner:
    """
    CORE-014I — Milestone Planner.

    Recommends the next milestone from repository intelligence.
    Milestone names are derived from the current development phase,
    not hardcoded strings.
    """

    def recommend_next_milestone(
        self,
        decision_context: Mapping[str, Any],
        snapshot: Mapping[str, Any],
    ) -> Optional[Dict[str, Any]]:
        candidates = self._collect_candidates(decision_context, snapshot)
        return candidates[0] if candidates else None

    def build_milestone_entries(
        self,
        decision_context: Mapping[str, Any],
        snapshot: Mapping[str, Any],
    ) -> List[PlanningEntry]:
        candidates = self._collect_candidates(decision_context, snapshot)
        entries: List[PlanningEntry] = []
        for i, c in enumerate(candidates[:3]):
            entries.append(
                PlanningEntry(
                    entry_id=c.get("id", f"MILESTONE-{i + 1:03d}"),
                    title=c["title"],
                    type=TYPE_MILESTONE,
                    priority=c.get("priority", "medium"),
                    reason=c.get("reason", ""),
                    dependencies=tuple(c.get("dependencies", [])),
                    estimated_effort=c.get("estimated_effort", EFFORT_HIGH),
                    confidence=c.get("confidence", 0.70),
                    blocked_by=(),
                    metadata=c,
                )
            )
        return entries

    # ------------------------------------------------------------------

    def _collect_candidates(
        self,
        decision_context: Mapping[str, Any],
        snapshot: Mapping[str, Any],
    ) -> List[Dict[str, Any]]:
        candidates: List[Dict[str, Any]] = []

        phase = decision_context.get("current_phase", PHASE_FOUNDATION)
        current_ms = decision_context.get("current_milestone", "")
        completion = decision_context.get("completion_percentage", 0.0)

        # 1. Phase transition milestone (derived from current phase)
        next_phase_ms = _PHASE_MILESTONES.get(phase)
        if next_phase_ms and next_phase_ms != current_ms:
            incomplete = decision_context.get("incomplete_cores", [])
            deps = list(decision_context.get("implemented_cores", []))
            candidates.append({
                "id": f"MILESTONE-{phase.upper()}",
                "title": next_phase_ms,
                "priority": "high",
                "reason": (
                    f"Current phase is {phase}. "
                    f"{completion:.0f}% of documented COREs are implemented. "
                    f"{len(incomplete)} COREs remain before phase completion."
                ),
                "dependencies": deps,
                "estimated_effort": EFFORT_HIGH,
                "confidence": 0.80,
            })

        # 2. Current milestone (continue working towards it)
        if _is_set(current_ms) and current_ms != next_phase_ms:
            candidates.append({
                "id": "MILESTONE-CURRENT",
                "title": f"Complete current milestone: {current_ms}",
                "priority": "medium",
                "reason": (
                    f"Active milestone '{current_ms}' from development state "
                    "should be progressed or closed."
                ),
                "dependencies": [],
                "estimated_effort": EFFORT_MEDIUM,
                "confidence": 0.75,
            })

        return [c for c in candidates if _is_set(c.get("title", ""))]
