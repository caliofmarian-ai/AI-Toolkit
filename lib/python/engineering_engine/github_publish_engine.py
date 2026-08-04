from __future__ import annotations

from dataclasses import dataclass, field

from lib.python.engineering_engine.github_project_planner import (
    GitHubProjectPlan,
)


@dataclass(slots=True)
class PublishOperation:

    kind: str

    title: str

    payload: dict = field(default_factory=dict)


@dataclass(slots=True)
class PublishPlan:

    operations: list[PublishOperation] = field(default_factory=list)


class GitHubPublishEngine:

    def build(
        self,
        project: GitHubProjectPlan,
    ) -> PublishPlan:

        plan = PublishPlan()

        for milestone in project.milestones:
            plan.operations.append(
                PublishOperation(
                    kind="milestone",
                    title=milestone.title,
                    payload={
                        "description": milestone.description,
                        "priority": milestone.priority,
                    },
                )
            )

        for issue in project.issues:
            plan.operations.append(
                PublishOperation(
                    kind="issue",
                    title=issue.issue.title,
                    payload={
                        "milestone": issue.milestone,
                        "labels": issue.issue.labels,
                    },
                )
            )

        return plan
