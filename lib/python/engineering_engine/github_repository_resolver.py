from __future__ import annotations

import subprocess
from dataclasses import dataclass


@dataclass(slots=True)
class GitHubRepository:
    owner: str
    repo: str


class GitHubRepositoryResolver:

    def resolve(self) -> GitHubRepository:

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
