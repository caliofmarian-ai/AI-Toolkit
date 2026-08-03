"""
Autonomous Planning Engine — Issue Planner
CORE-014F

Derives the next GitHub issue to open from:
  - Incomplete COREs (each needs a tracking issue)
  - Missing features detected by AI CTO Scanner
  - Canonical gaps from CanonicalIntelligenceEngine
  - Executive Briefing recommendations

No issues are hardcoded.
"""

from typing import Any, Dict, List, Mapping, Optional

from .models import (
    EFFORT_LOW,
    EFFORT_MEDIUM,
    TYPE_ISSUE,
    PlanningEntry,
)

_EMPTY = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})


def _is_set(v: Any) -> bool:
    return bool(v) and str(v).strip() not in _EMPTY


class IssuePlanner:
    """
    CORE-014F — Issue Planner.

    Recommends the next issue to open from repository intelligence.
    All recommendations are evidence-backed — no hardcoded issue text.
    """

    def recommend_next_issue(
        self,
        decision_context: Mapping[str, Any],
        snapshot: Mapping[str, Any],
        briefing: Mapping[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """
        Return the single highest-priority issue recommendation, or None.
        """
        candidates = self._collect_candidates(decision_context, snapshot, briefing)
        if not candidates:
            return None
        return candidates[0]

    def build_issue_entries(
        self,
        decision_context: Mapping[str, Any],
        snapshot: Mapping[str, Any],
        briefing: Mapping[str, Any],
    ) -> List[PlanningEntry]:
        """Return PlanningEntry objects for the top issue recommendations."""
        candidates = self._collect_candidates(decision_context, snapshot, briefing)
        entries: List[PlanningEntry] = []
        for i, c in enumerate(candidates[:5]):
            entries.append(
                PlanningEntry(
                    entry_id=f"ISSUE-{i + 1:03d}",
                    title=c["title"],
                    type=TYPE_ISSUE,
                    priority=c.get("priority", "medium"),
                    reason=c.get("reason", ""),
                    dependencies=tuple(c.get("dependencies", [])),
                    estimated_effort=c.get("estimated_effort", EFFORT_MEDIUM),
                    confidence=c.get("confidence", 0.7),
                    blocked_by=(),
                    metadata=c,
                )
            )
        return entries

    # ------------------------------------------------------------------
    # Candidate generation
    # ------------------------------------------------------------------

    def _collect_candidates(
        self,
        decision_context: Mapping[str, Any],
        snapshot: Mapping[str, Any],
        briefing: Mapping[str, Any],
    ) -> List[Dict[str, Any]]:
        candidates: List[Dict[str, Any]] = []

        # 1. Next unimplemented CORE → needs a tracking issue
        next_core = decision_context.get("next_core")
        if next_core:
            candidates.append({
                "title": f"[{next_core}] Implement {next_core} — Autonomous Planning Engine",
                "type": "core_tracking",
                "priority": "high",
                "reason": (
                    f"{next_core} is the next CORE on the roadmap and has no "
                    "implementation yet."
                ),
                "dependencies": [],
                "estimated_effort": EFFORT_MEDIUM,
                "confidence": 0.90,
            })

        # 2. Executive briefing high-priority recommendations
        for rec in briefing.get("recommendations", []):
            p = rec.get("priority", "low")
            if p in ("critical", "high"):
                candidates.append({
                    "title": rec.get("title", ""),
                    "type": "briefing_recommendation",
                    "priority": p,
                    "reason": rec.get("description", ""),
                    "dependencies": list(rec.get("dependencies", [])),
                    "estimated_effort": rec.get("required_effort", EFFORT_MEDIUM),
                    "confidence": float(rec.get("confidence", 0.7)),
                })

        # 3. Canonical coverage gaps
        integrations = snapshot.get("integrations", {})
        canonical = integrations.get("canonical_intelligence", {})
        coverage = float(canonical.get("average_coverage", 100.0))
        if coverage < 70:
            candidates.append({
                "title": "Improve canonical coverage (currently below 70%)",
                "type": "canonical_gap",
                "priority": "medium",
                "reason": (
                    f"Canonical coverage is at {coverage:.1f}%. "
                    "Canonical compliance underpins all CORE quality."
                ),
                "dependencies": [],
                "estimated_effort": EFFORT_MEDIUM,
                "confidence": 0.80,
            })

        # 4. AI CTO Scanner findings
        scanner = integrations.get("ai_cto_scanner", {})
        for finding in scanner.get("critical_findings", [])[:3]:
            desc = str(finding.get("description", finding.get("title", "")))
            if desc:
                candidates.append({
                    "title": f"Fix: {desc[:80]}",
                    "type": "scanner_finding",
                    "priority": "high",
                    "reason": desc,
                    "dependencies": [],
                    "estimated_effort": EFFORT_LOW,
                    "confidence": 0.75,
                })

        # Remove empty titles
        return [c for c in candidates if _is_set(c.get("title", ""))]
