"""
Autonomous Planning Engine — Priority Optimizer
CORE-014C

Optimises planning entries according to multiple weighted dimensions:

  - Architecture impact        (derived from AI CTO Scanner + Semantic Intelligence)
  - Dependency graph position  (derived from DependencyResolver)
  - Repository health          (derived from Workspace Orchestrator)
  - Risk                       (derived from Executive Briefing risk analyzer)
  - Estimated effort           (derived from development state)
  - Owner priorities           (derived from development state owner_state)
  - Development state          (derived from DevelopmentStateEngine)
  - Canonical compliance       (derived from CanonicalIntelligenceEngine)

No priorities are hardcoded.  Every score is computed from live
intelligence data passed in via snapshot dicts.
"""

from typing import Any, Dict, List, Mapping, Sequence

from .models import (
    EFFORT_HIGH,
    EFFORT_LOW,
    EFFORT_MEDIUM,
    PRIORITY_BLOCKED,
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_LOW,
    PRIORITY_MEDIUM,
    PlanningEntry,
)

_PRIORITY_ORDER = {
    PRIORITY_CRITICAL: 0,
    PRIORITY_HIGH: 1,
    PRIORITY_MEDIUM: 2,
    PRIORITY_LOW: 3,
    PRIORITY_BLOCKED: 4,
}

_EFFORT_WEIGHT = {
    EFFORT_LOW: 1.0,
    EFFORT_MEDIUM: 0.8,
    EFFORT_HIGH: 0.6,
}

_EMPTY = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})


def _is_set(value: Any) -> bool:
    return bool(value) and str(value).strip() not in _EMPTY


class PriorityOptimizer:
    """
    CORE-014C — Priority Optimizer.

    Accepts a list of PlanningEntry objects and intelligence snapshot
    data, and returns a new list with:
    - Assigned priority based on multi-factor scoring
    - Stable sort order (blocked items always last)

    All scoring is derived from the snapshot — no hardcoded priorities.
    """

    # Dimension weights (sum does not need to equal 1)
    _W_ARCHITECTURE = 0.30
    _W_DEPENDENCY = 0.20
    _W_HEALTH = 0.15
    _W_RISK = 0.15
    _W_EFFORT = 0.10
    _W_OWNER = 0.05
    _W_CANONICAL = 0.05

    def optimize(
        self,
        entries: List[PlanningEntry],
        snapshot: Mapping[str, Any],
        dep_graph: Mapping[str, List[str]],
    ) -> List[PlanningEntry]:
        """
        Return entries sorted by multi-factor priority score.

        Parameters
        ----------
        entries:
            Raw planning entries from the individual planners.
        snapshot:
            The development state executive snapshot dict
            (from DevelopmentStateManager.GenerateExecutiveSnapshot).
        dep_graph:
            CORE dependency map from DependencyResolver.core_dependency_map().
        """
        if not entries:
            return entries

        scored = [
            (self._score(entry, snapshot, dep_graph), entry)
            for entry in entries
        ]
        # Higher score = higher priority; stable sort
        scored.sort(key=lambda t: (-t[0], t[1].entry_id))

        optimised: List[PlanningEntry] = []
        for score, entry in scored:
            new_priority = self._score_to_priority(score, entry)
            if new_priority != entry.priority:
                # Replace only the priority field — all other fields unchanged
                import dataclasses
                entry = dataclasses.replace(entry, priority=new_priority)
            optimised.append(entry)

        return optimised

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------

    def _score(
        self,
        entry: PlanningEntry,
        snapshot: Mapping[str, Any],
        dep_graph: Mapping[str, List[str]],
    ) -> float:
        """
        Compute a composite priority score in [0, 1].
        Higher is more urgent.
        """
        # Blocked entries always get the minimum score
        if entry.blocked_by:
            return 0.0

        arch = self._architecture_score(entry, snapshot)
        dep = self._dependency_score(entry, dep_graph)
        health = self._health_score(entry, snapshot)
        risk = self._risk_score(entry, snapshot)
        effort = self._effort_score(entry)
        owner = self._owner_score(entry, snapshot)
        canonical = self._canonical_score(entry, snapshot)

        return (
            arch * self._W_ARCHITECTURE
            + dep * self._W_DEPENDENCY
            + health * self._W_HEALTH
            + risk * self._W_RISK
            + effort * self._W_EFFORT
            + owner * self._W_OWNER
            + canonical * self._W_CANONICAL
        )

    def _architecture_score(
        self, entry: PlanningEntry, snapshot: Mapping[str, Any]
    ) -> float:
        """Higher score for entries that unblock more dependent work."""
        integrations = snapshot.get("integrations", {})
        semantic = integrations.get("semantic_repository_intelligence", {})
        arch_graph = semantic.get("architecture_graph", {})
        hotspots = [str(h).lower() for h in arch_graph.get("hotspots", [])]

        title_lower = entry.title.lower()
        if any(h in title_lower for h in hotspots):
            return 1.0
        if entry.type == "core":
            return 0.8
        if entry.type == "milestone":
            return 0.6
        if entry.type == "batch":
            return 0.5
        return 0.3

    def _dependency_score(
        self,
        entry: PlanningEntry,
        dep_graph: Mapping[str, List[str]],
    ) -> float:
        """
        Entries that many others depend on score higher.
        Compute the reverse fan-in from the dependency graph.
        """
        entry_id = entry.entry_id
        fan_in = sum(
            1 for deps in dep_graph.values() if entry_id in deps
        )
        # Normalise: 0 fan-in → 0.3 base; scale by presence of dependents
        return min(0.3 + fan_in * 0.15, 1.0)

    def _health_score(
        self, entry: PlanningEntry, snapshot: Mapping[str, Any]
    ) -> float:
        """Entries addressing unhealthy repositories score higher."""
        integrations = snapshot.get("integrations", {})
        scanner = integrations.get("ai_cto_scanner", {})
        health = scanner.get("overall_health", "healthy")
        if health == "critical":
            return 1.0
        if health == "degraded":
            return 0.7
        return 0.3

    def _risk_score(
        self, entry: PlanningEntry, snapshot: Mapping[str, Any]
    ) -> float:
        """Entries that mitigate critical risks score higher."""
        state = snapshot.get("state", {})
        blocked = state.get("workspace_state", {}).get("blocked_tasks", [])
        if not blocked:
            blocked = []
        if entry.entry_id in blocked or entry.title in blocked:
            return 1.0

        # Scan executive recommendations for risk mentions
        integrations = snapshot.get("integrations", {})
        executive = integrations.get("executive_briefing", {})
        critical_risks = executive.get("critical_risks", [])
        entry_title_lower = entry.title.lower()
        for risk in critical_risks:
            desc = str(risk.get("description", "")).lower()
            if any(w in desc for w in entry_title_lower.split()):
                return 0.9
        return 0.2

    def _effort_score(self, entry: PlanningEntry) -> float:
        """Low-effort items score slightly higher (quick wins)."""
        return _EFFORT_WEIGHT.get(entry.estimated_effort, 0.5)

    def _owner_score(
        self, entry: PlanningEntry, snapshot: Mapping[str, Any]
    ) -> float:
        """Items matching owner priorities score higher."""
        state = snapshot.get("state", {})
        owner_priorities = state.get("owner_state", {}).get("owner_priorities", [])
        if not owner_priorities:
            return 0.5

        title_lower = entry.title.lower()
        for prio in owner_priorities:
            if str(prio).lower() in title_lower or title_lower in str(prio).lower():
                return 1.0
        return 0.3

    def _canonical_score(
        self, entry: PlanningEntry, snapshot: Mapping[str, Any]
    ) -> float:
        """Entries improving canonical compliance score higher."""
        integrations = snapshot.get("integrations", {})
        canonical = integrations.get("canonical_intelligence", {})
        coverage = canonical.get("average_coverage", 100.0)
        if coverage < 40:
            return 1.0
        if coverage < 70:
            return 0.7
        return 0.3

    @staticmethod
    def _score_to_priority(score: float, entry: PlanningEntry) -> str:
        """Map composite score to a priority level string."""
        if entry.blocked_by:
            return PRIORITY_BLOCKED
        if score >= 0.75:
            return PRIORITY_CRITICAL
        if score >= 0.55:
            return PRIORITY_HIGH
        if score >= 0.35:
            return PRIORITY_MEDIUM
        return PRIORITY_LOW
