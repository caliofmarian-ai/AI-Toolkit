from __future__ import annotations

from dataclasses import dataclass

from lib.python.engineering_engine.engineering_task_engine import (
    EngineeringTask,
)


@dataclass(slots=True)
class GitHubIssue:

    title: str

    body: str

    labels: list[str]


class GitHubIssueGenerator:

    def generate(
        self,
        task: EngineeringTask,
    ) -> GitHubIssue:

        labels = [
            "engineering",
            task.priority.value.lower(),
        ]

        body = "\n".join([
            f"# {task.title}",
            "",
            "## Priority",
            task.priority.value,
            "",
            "## Objective",
            task.rationale,
            "",
            "## Affected Modules",
            *[
                f"- {module}"
                for module in task.affected_modules
            ],
            "",
            "## Implementation Checklist",
            "- [ ] Analyse current implementation",
            "- [ ] Implement required changes",
            "- [ ] Execute validation",
            "- [ ] Perform engineering review",
            "",
            "## Acceptance Criteria",
            "- [ ] Implementation completed",
            "- [ ] Validation passes",
            "- [ ] No regression introduced",
            "- [ ] Documentation updated",
        ])

        return GitHubIssue(
            title=task.title,
            body=body,
            labels=labels,
        )
