from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass


@dataclass(slots=True)
class GitHubRepository:
    owner: str
    repo: str


class GitHubRepositoryResolver:

    def __init__(self, repository: GitHubRepository | None = None):
        self._repository = repository

    def resolve(self) -> GitHubRepository:
        if self._repository is not None:
            return self._repository

        env_repository = os.environ.get("GITHUB_REPOSITORY", "").strip()
        if env_repository and "/" in env_repository:
            owner, repo = env_repository.split("/", 1)
            return GitHubRepository(owner=owner, repo=repo)

        name = subprocess.check_output(
            [
                "gh",
                "repo",
                "view",
                "--json",
                "nameWithOwner",
                "--jq",
                ".nameWithOwner",
            ],
            text=True,
        ).strip()

        owner, repo = name.split("/", 1)

        return GitHubRepository(
            owner=owner,
            repo=repo,
        )
