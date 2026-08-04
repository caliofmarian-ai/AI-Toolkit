from __future__ import annotations

from dataclasses import dataclass, field

from lib.python.engineering_engine.batch_planner_engine import (
    EngineeringBatch,
)
from lib.python.engineering_engine.engineering_task_engine import (
    EngineeringBacklog,
)
from lib.python.engineering_engine.github_issue_generator import (
    GitHubIssue,
    GitHubIssueGenerator,
)
from lib.python.engineering_engine.github_milestone_generator import (
    GitHubMilestone,
)


@dataclass(slots=True)
class PlannedIssue:

    task_id: str

    issue: GitHubIssue

    milestone: str


@dataclass(slots=True)
class GitHubProjectPlan:

    milestones: list[GitHubMilestone] = field(default_factory=list)

    issues: list[PlannedIssue] = field(default_factory=list)


class GitHubProjectPlanner:

    def build(
        self,
        backlog: EngineeringBacklog,
        batches: list[EngineeringBatch],
        milestones: list[GitHubMilestone],
    ) -> GitHubProjectPlan:

        generator = GitHubIssueGenerator()

        task_lookup = {
            task.id: task
            for task in backlog.tasks
        }

        milestone_lookup = {
            milestone.batch_id: milestone.title
            for milestone in milestones
        }

        plan = GitHubProjectPlan(
            milestones=milestones,
        )

        for batch in batches:

            milestone = milestone_lookup[batch.id]

            for task_id in batch.tasks:

                task = task_lookup[task_id]

                plan.issues.append(
                    PlannedIssue(
                        task_id=task.id,
                        issue=generator.generate(task),
                        milestone=milestone,
                    )
                )

        return plan
