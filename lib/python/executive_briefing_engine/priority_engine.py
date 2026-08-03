"""
Executive Briefing Engine — Priority Engine
CORE-010D

Classifies work items derived from snapshot intelligence into executive
priority levels: Critical, High, Medium, Low, Blocked, Waiting, Completed.
"""

from typing import Any, List, Mapping

from .models import (
    PRIORITY_BLOCKED,
    PRIORITY_COMPLETED,
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_LOW,
    PRIORITY_MEDIUM,
    PRIORITY_WAITING,
    ExecutivePriorityItem,
)

_EMPTY_SENTINELS = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})


def _is_set(value) -> bool:
    return bool(value) and str(value).strip() not in _EMPTY_SENTINELS


class ExecutivePriorityEngine:
    """
    Classifies work items from snapshot data into priority levels.

    Sources:
    - Development state: current tasks, blocked tasks, completed tasks
    - Canonical intelligence: pending batches
    - Execution state: running, failed jobs
    - Planning state: roadmap, milestones
    """

    def classify(self, snapshot: Mapping[str, Any]) -> List[ExecutivePriorityItem]:
        """Return priority-sorted work items derived from snapshot."""
        items: List[ExecutivePriorityItem] = []
        counter = [0]

        def next_id() -> str:
            counter[0] += 1
            return f"PRI-{counter[0]:03d}"

        state = snapshot.get("state", {})
        integrations = snapshot.get("integrations", {})
        context = snapshot.get("current_context", {})

        items.extend(self._classify_blocked_items(next_id, state))
        items.extend(self._classify_critical_items(next_id, integrations))
        items.extend(self._classify_high_items(next_id, state, context))
        items.extend(self._classify_medium_items(next_id, integrations, context))
        items.extend(self._classify_completed_items(next_id, state))
        items.extend(self._classify_waiting_items(next_id, state))

        return self._sort_items(items)

    # ------------------------------------------------------------------
    # Blocked items
    # ------------------------------------------------------------------

    def _classify_blocked_items(
        self, next_id, state: Mapping[str, Any]
    ) -> List[ExecutivePriorityItem]:
        items: List[ExecutivePriorityItem] = []
        workspace = state.get("workspace_state", {})
        blocked_tasks = workspace.get("blocked_tasks", [])

        if isinstance(blocked_tasks, list):
            for task in blocked_tasks:
                items.append(ExecutivePriorityItem(
                    id=next_id(),
                    title=str(task),
                    classification=PRIORITY_BLOCKED,
                    category="task",
                    rationale="Task is in the blocked_tasks list and requires unblocking.",
                ))

        execution = state.get("execution_state", {})
        failed_jobs = execution.get("failed_jobs", [])
        if isinstance(failed_jobs, list):
            for job in failed_jobs:
                items.append(ExecutivePriorityItem(
                    id=next_id(),
                    title=str(job),
                    classification=PRIORITY_BLOCKED,
                    category="execution_job",
                    rationale="Execution job has failed and blocks downstream work.",
                ))

        return items

    # ------------------------------------------------------------------
    # Critical items
    # ------------------------------------------------------------------

    def _classify_critical_items(
        self, next_id, integrations: Mapping[str, Any]
    ) -> List[ExecutivePriorityItem]:
        items: List[ExecutivePriorityItem] = []
        canon = integrations.get("canonical_intelligence", {})
        drift = int(canon.get("drift_findings", 0))
        coverage = float(canon.get("overall_coverage", 100.0))

        if drift > 5:
            items.append(ExecutivePriorityItem(
                id=next_id(),
                title=f"Resolve {drift} canonical drift findings",
                classification=PRIORITY_CRITICAL,
                category="canonical_health",
                rationale=(
                    f"{drift} drift findings exceed the critical threshold of 5. "
                    "Immediate resolution required."
                ),
            ))

        if coverage < 50.0:
            items.append(ExecutivePriorityItem(
                id=next_id(),
                title=f"Raise canonical coverage from {coverage:.1f}% to ≥80%",
                classification=PRIORITY_CRITICAL,
                category="canonical_health",
                rationale=(
                    f"Coverage of {coverage:.1f}% is critically below the 50% floor."
                ),
            ))

        return items

    # ------------------------------------------------------------------
    # High priority items
    # ------------------------------------------------------------------

    def _classify_high_items(
        self, next_id, state: Mapping[str, Any], context: Mapping[str, Any]
    ) -> List[ExecutivePriorityItem]:
        items: List[ExecutivePriorityItem] = []
        review = state.get("review_state", {})
        open_prs = review.get("open_prs", [])

        if isinstance(open_prs, list) and open_prs:
            items.append(ExecutivePriorityItem(
                id=next_id(),
                title=f"Review {len(open_prs)} open pull requests",
                classification=PRIORITY_HIGH,
                category="code_review",
                rationale="Open pull requests represent pending integration work.",
            ))

        current_batch = context.get("current_batch", "")
        if _is_set(current_batch):
            items.append(ExecutivePriorityItem(
                id=next_id(),
                title=f"Complete current batch: {current_batch}",
                classification=PRIORITY_HIGH,
                category="batch_execution",
                rationale="The current batch is the active unit of work.",
            ))

        current_issue = context.get("current_issue", "")
        if _is_set(current_issue):
            items.append(ExecutivePriorityItem(
                id=next_id(),
                title=f"Resolve current issue: {current_issue}",
                classification=PRIORITY_HIGH,
                category="issue_tracking",
                rationale="The current issue is the active development focus.",
            ))

        return items

    # ------------------------------------------------------------------
    # Medium priority items
    # ------------------------------------------------------------------

    def _classify_medium_items(
        self, next_id, integrations: Mapping[str, Any], context: Mapping[str, Any]
    ) -> List[ExecutivePriorityItem]:
        items: List[ExecutivePriorityItem] = []
        canon = integrations.get("canonical_intelligence", {})
        batches = int(canon.get("batches", 0))

        if batches > 0:
            items.append(ExecutivePriorityItem(
                id=next_id(),
                title=f"Execute {batches} pending canonical batch(es)",
                classification=PRIORITY_MEDIUM,
                category="canonical_execution",
                rationale=f"{batches} canonical batches are ready for execution.",
            ))

        current_milestone = context.get("current_milestone", "")
        if _is_set(current_milestone):
            items.append(ExecutivePriorityItem(
                id=next_id(),
                title=f"Advance milestone: {current_milestone}",
                classification=PRIORITY_MEDIUM,
                category="milestone",
                rationale="Active milestone requires steady progress.",
            ))

        return items

    # ------------------------------------------------------------------
    # Completed items
    # ------------------------------------------------------------------

    def _classify_completed_items(
        self, next_id, state: Mapping[str, Any]
    ) -> List[ExecutivePriorityItem]:
        items: List[ExecutivePriorityItem] = []
        workspace = state.get("workspace_state", {})
        completed_tasks = workspace.get("completed_tasks", [])

        if isinstance(completed_tasks, list):
            for task in completed_tasks[:5]:
                items.append(ExecutivePriorityItem(
                    id=next_id(),
                    title=str(task),
                    classification=PRIORITY_COMPLETED,
                    category="task",
                    rationale="Task has been completed.",
                ))

        execution = state.get("execution_state", {})
        completed_jobs = execution.get("completed_jobs", [])
        if isinstance(completed_jobs, list):
            for job in completed_jobs[:3]:
                items.append(ExecutivePriorityItem(
                    id=next_id(),
                    title=str(job),
                    classification=PRIORITY_COMPLETED,
                    category="execution_job",
                    rationale="Execution job completed successfully.",
                ))

        return items

    # ------------------------------------------------------------------
    # Waiting items
    # ------------------------------------------------------------------

    def _classify_waiting_items(
        self, next_id, state: Mapping[str, Any]
    ) -> List[ExecutivePriorityItem]:
        items: List[ExecutivePriorityItem] = []
        execution = state.get("execution_state", {})
        running_jobs = execution.get("running_jobs", [])

        if isinstance(running_jobs, list) and running_jobs:
            items.append(ExecutivePriorityItem(
                id=next_id(),
                title=f"{len(running_jobs)} execution job(s) in progress",
                classification=PRIORITY_WAITING,
                category="execution_job",
                rationale="Execution jobs are running and awaiting completion.",
            ))

        review = state.get("review_state", {})
        pending_reviews = review.get("pending_reviews", [])
        if isinstance(pending_reviews, list) and pending_reviews:
            items.append(ExecutivePriorityItem(
                id=next_id(),
                title=f"{len(pending_reviews)} review(s) awaiting feedback",
                classification=PRIORITY_WAITING,
                category="code_review",
                rationale="Reviews have been submitted and are awaiting feedback.",
            ))

        return items

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    _CLASSIFICATION_ORDER = {
        PRIORITY_CRITICAL: 0,
        PRIORITY_BLOCKED: 1,
        PRIORITY_HIGH: 2,
        PRIORITY_MEDIUM: 3,
        PRIORITY_LOW: 4,
        PRIORITY_WAITING: 5,
        PRIORITY_COMPLETED: 6,
    }

    def _sort_items(self, items: List[ExecutivePriorityItem]) -> List[ExecutivePriorityItem]:
        return sorted(
            items,
            key=lambda p: self._CLASSIFICATION_ORDER.get(p.classification, 9),
        )
