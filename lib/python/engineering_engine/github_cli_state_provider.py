from __future__ import annotations

import json
import subprocess

from lib.python.engineering_engine.github_repository_resolver import (
    GitHubRepository,
    GitHubRepositoryResolver,
)
from lib.python.engineering_engine.github_state_provider import (
    GitHubState,
    GitHubStateProvider,
)


class GitHubCLIStateProvider(GitHubStateProvider):

    def __init__(
        self,
        repository: GitHubRepository | None = None,
        repository_resolver: GitHubRepositoryResolver | None = None,
    ):
        self._repository_resolver = repository_resolver or GitHubRepositoryResolver(repository)

    def load(self) -> GitHubState:

        repository = self._repository_resolver.resolve()

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
                "--repo",
                f"{repository.owner}/{repository.repo}",
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
