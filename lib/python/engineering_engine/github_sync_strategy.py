from __future__ import annotations

from dataclasses import dataclass, field

from lib.python.engineering_engine.github_comparison_engine import (
    GitHubComparisonEngine,
)
from lib.python.engineering_engine.github_issue_state_provider import (
    GitHubIssueStateProvider,
)
from lib.python.engineering_engine.github_project_planner import (
    GitHubProjectPlan,
)
from lib.python.engineering_engine.github_state_provider import (
    GitHubStateProvider,
)
from lib.python.engineering_engine.github_sync_engine import (
    SyncAction,
)


@dataclass(slots=True)
class SyncDecision:
    kind: str
    title: str
    action: SyncAction


@dataclass(slots=True)
class SmartSyncPlan:
    operations: list[SyncDecision] = field(default_factory=list)


class GitHubSyncStrategy:

    def __init__(self, issue_state_provider: GitHubIssueStateProvider | None = None):
        self._issue_state_provider = issue_state_provider or GitHubIssueStateProvider()

    def build(
        self,
        project: GitHubProjectPlan,
        provider: GitHubStateProvider,
    ) -> SmartSyncPlan:

        state = provider.load()
        issue_state = self._issue_state_provider.load()
        compare = GitHubComparisonEngine()

        plan = SmartSyncPlan()

        for milestone in project.milestones:

            action = (
                SyncAction.SKIP
                if milestone.title in state.milestones
                else SyncAction.CREATE
            )

            plan.operations.append(
                SyncDecision(
                    kind="milestone",
                    title=milestone.title,
                    action=action,
                )
            )

        for planned in project.issues:

            current = issue_state.issues.get(
                planned.issue.title
            )

            if current is None:
                action = SyncAction.CREATE
            else:
                result = compare.compare_issue(
                    planned.issue,
                    current,
                )

                action = (
                    SyncAction.SKIP
                    if result.identical
                    else SyncAction.UPDATE
                )

            plan.operations.append(
                SyncDecision(
                    kind="issue",
                    title=planned.issue.title,
                    action=action,
                )
            )

        return plan
