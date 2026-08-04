from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from lib.python.engineering_engine.github_state_provider import (
    GitHubStateProvider,
)

from lib.python.engineering_engine.github_project_planner import (
    GitHubProjectPlan,
)


class SyncAction(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    SKIP = "SKIP"


@dataclass(slots=True)
class SyncOperation:
    kind: str
    title: str
    action: SyncAction


@dataclass(slots=True)
class SyncPlan:
    operations: list[SyncOperation] = field(default_factory=list)


class GitHubSynchronizationEngine:


    def build(
        self,
        project: GitHubProjectPlan,
        state_provider: GitHubStateProvider,
    ) -> SyncPlan:

        state = state_provider.load()

        plan = SyncPlan()

        for milestone in project.milestones:
            plan.operations.append(
                SyncOperation(
                    kind="milestone",
                    title=milestone.title,
                    action=(
                        SyncAction.SKIP
                        if milestone.title in state.milestones
                        else SyncAction.CREATE
                    ),
                )
            )

        for issue in project.issues:
            plan.operations.append(
                SyncOperation(
                    kind="issue",
                    title=issue.issue.title,
                    action=(
                        SyncAction.SKIP
                        if issue.issue.title in state.issues
                        else SyncAction.CREATE
                    ),
                )
            )

        return plan

