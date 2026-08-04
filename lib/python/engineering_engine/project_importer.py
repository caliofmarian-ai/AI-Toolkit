from __future__ import annotations

import json
from pathlib import Path

from lib.python.engineering_engine.github_project_planner import (
    GitHubProjectPlan,
    PlannedIssue,
)
from lib.python.engineering_engine.github_issue_generator import (
    GitHubIssue,
)
from lib.python.engineering_engine.github_milestone_generator import (
    GitHubMilestone,
)


class ProjectImporter:

    def import_json(
        self,
        source: Path,
    ) -> GitHubProjectPlan:

        data = json.loads(
            source.read_text(encoding="utf-8")
        )

        milestones = [
            GitHubMilestone(**item)
            for item in data.get("milestones", [])
        ]

        issues = []

        for item in data.get("issues", []):

            issue = GitHubIssue(
                **item["issue"]
            )

            issues.append(
                PlannedIssue(
                    task_id=item["task_id"],
                    issue=issue,
                    milestone=item["milestone"],
                )
            )

        return GitHubProjectPlan(
            milestones=milestones,
            issues=issues,
        )
