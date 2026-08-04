from __future__ import annotations

from dataclasses import dataclass, field

from lib.python.engineering_engine.github_project_planner import GitHubProjectPlan
from lib.python.engineering_engine.github_issue_state_provider import GitHubIssueStateProvider
from lib.python.engineering_engine.github_cli_state_provider import GitHubCLIStateProvider
from lib.python.engineering_engine.github_sync_engine import SyncAction


@dataclass(slots=True)
class PlannedSyncOperation:
    kind: str
    title: str
    action: SyncAction


@dataclass(slots=True)
class PlannedSync:
    operations: list[PlannedSyncOperation] = field(default_factory=list)


class GitHubSyncPlanner:

    def build(
        self,
        project: GitHubProjectPlan,
    ) -> PlannedSync:

        milestone_state = GitHubCLIStateProvider().load()
        issue_state = GitHubIssueStateProvider().load()

        plan = PlannedSync()

        for milestone in project.milestones:
            plan.operations.append(
                PlannedSyncOperation(
                    kind="milestone",
                    title=milestone.title,
                    action=(
                        SyncAction.SKIP
                        if milestone.title in milestone_state.milestones
                        else SyncAction.CREATE
                    ),
                )
            )

        for item in project.issues:
            plan.operations.append(
                PlannedSyncOperation(
                    kind="issue",
                    title=item.issue.title,
                    action=(
                        SyncAction.SKIP
                        if item.issue.title in issue_state.issues
                        else SyncAction.CREATE
                    ),
                )
            )

        return plan
