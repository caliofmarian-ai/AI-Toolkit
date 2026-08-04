from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field

from lib.python.engineering_engine.github_repository_resolver import (
    GitHubRepositoryResolver,
)
from lib.python.engineering_engine.github_issue_generator import (
    GitHubIssue,
)


@dataclass(slots=True)
class GitHubIssueState:

    issues: dict[str, GitHubIssue] = field(default_factory=dict)


class GitHubIssueStateProvider:

    def load(self) -> GitHubIssueState:

        repository = GitHubRepositoryResolver().resolve()

        data = subprocess.check_output(
            [
                "gh",
                "issue",
                "list",
                "--repo",
                f"{repository.owner}/{repository.repo}",
                "--limit",
                "1000",
                "--json",
                "title,body,labels",
            ],
            text=True,
        )

        state = GitHubIssueState()

        for item in json.loads(data):

            state.issues[item["title"]] = GitHubIssue(
                title=item["title"],
                body=item.get("body", ""),
                labels=[
                    label["name"]
                    for label in item.get("labels", [])
                ],
            )

        return state
