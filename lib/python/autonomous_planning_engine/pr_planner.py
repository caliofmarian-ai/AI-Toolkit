"""
Autonomous Planning Engine — Pull Request Planner
CORE-014H

Recommends the next pull request to create or review from:
  - Development state (current branch, open PRs, review state)
  - Executive Briefing suggested_next_pr
  - In-progress work (current_batch, current_task from development state)
  - Completed COREs not yet merged

No PR decisions are hardcoded.
"""

from typing import Any, Dict, List, Mapping, Optional

from .models import EFFORT_LOW, EFFORT_MEDIUM, TYPE_PR, PlanningEntry

_EMPTY = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})


def _is_set(v: Any) -> bool:
    return bool(v) and str(v).strip() not in _EMPTY


class PullRequestPlanner:
    """
    CORE-014H — Pull Request Planner.

    Recommends the next PR to create from repository intelligence.
    """

    def recommend_next_pr(
        self,
        decision_context: Mapping[str, Any],
        snapshot: Mapping[str, Any],
        briefing: Mapping[str, Any],
    ) -> Optional[Dict[str, Any]]:
        candidates = self._collect_candidates(decision_context, snapshot, briefing)
        return candidates[0] if candidates else None

    def build_pr_entries(
        self,
        decision_context: Mapping[str, Any],
        snapshot: Mapping[str, Any],
        briefing: Mapping[str, Any],
    ) -> List[PlanningEntry]:
        candidates = self._collect_candidates(decision_context, snapshot, briefing)
        entries: List[PlanningEntry] = []
        for i, c in enumerate(candidates[:3]):
            entries.append(
                PlanningEntry(
                    entry_id=c.get("id", f"PR-{i + 1:03d}"),
                    title=c["title"],
                    type=TYPE_PR,
                    priority=c.get("priority", "medium"),
                    reason=c.get("reason", ""),
                    dependencies=tuple(c.get("dependencies", [])),
                    estimated_effort=c.get("estimated_effort", EFFORT_LOW),
                    confidence=c.get("confidence", 0.7),
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
        briefing: Mapping[str, Any],
    ) -> List[Dict[str, Any]]:
        candidates: List[Dict[str, Any]] = []

        # 1. Executive Briefing suggested_next_pr
        suggested = decision_context.get("suggested_next_pr", "")
        if _is_set(suggested):
            candidates.append({
                "id": "PR-SUGGESTED",
                "title": f"Create PR: {suggested}",
                "priority": "high",
                "reason": f"Executive Briefing recommends creating PR for: {suggested}.",
                "dependencies": [],
                "estimated_effort": EFFORT_LOW,
                "confidence": 0.85,
            })

        # 2. Current branch work → should become a PR
        branch = decision_context.get("current_branch", "")
        if _is_set(branch) and "/" in branch:
            # Looks like a feature branch (e.g. copilot/core-014-...)
            task = decision_context.get("current_batch", "") or branch
            candidates.append({
                "id": "PR-CURRENT-BRANCH",
                "title": f"Open PR for current branch: {branch}",
                "priority": "high",
                "reason": (
                    f"Active feature branch '{branch}' has work in progress "
                    f"({task}). A PR should be opened."
                ),
                "dependencies": [],
                "estimated_effort": EFFORT_LOW,
                "confidence": 0.80,
            })

        # 3. Review state: pending reviews
        state = snapshot.get("state", {})
        pending = state.get("review_state", {}).get("pending_reviews", []) or []
        for review in pending[:2]:
            r_str = str(review)
            if _is_set(r_str):
                candidates.append({
                    "id": f"PR-REVIEW-{r_str[:20]}",
                    "title": f"Complete review: {r_str[:60]}",
                    "priority": "medium",
                    "reason": f"Pending review: {r_str}",
                    "dependencies": [],
                    "estimated_effort": EFFORT_LOW,
                    "confidence": 0.75,
                })

        return [c for c in candidates if _is_set(c.get("title", ""))]
