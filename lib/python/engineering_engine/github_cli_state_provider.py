from __future__ import annotations

import json
import subprocess

from lib.python.engineering_engine.github_repository_resolver import (
    GitHubRepositoryResolver,
)
from lib.python.engineering_engine.github_state_provider import (
    GitHubState,
    GitHubStateProvider,
)


class GitHubCLIStateProvider(GitHubStateProvider):

    def load(self) -> GitHubState:

        repository = GitHubRepositoryResolver().resolve()

        milestones = subprocess.check_output(
            [
                "gh",
                "api",
                f"repos/{repository.owner}/{repository.repo}/milestones",
            ],
            text=True,
        )

        issues = subprocess.check_output(
            [
                "gh",
                "issue",
                "list",
                "--limit",
                "1000",
                "--json",
                "title",
            ],
            text=True,
        )

        milestone_titles = {
            item["title"]
            for item in json.loads(milestones)
        }

        issue_titles = {
            item["title"]
            for item in json.loads(issues)
        }

        return GitHubState(
            milestones=milestone_titles,
            issues=issue_titles,
        )
