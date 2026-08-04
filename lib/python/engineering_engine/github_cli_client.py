from __future__ import annotations

import subprocess

from lib.python.engineering_engine.github_client import GitHubClient
from lib.python.engineering_engine.github_publish_engine import PublishOperation


class GitHubCLIClient(GitHubClient):

    def __init__(self):

        repo = subprocess.check_output(
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

        self.owner, self.repo = repo.split("/", 1)

    def execute(
        self,
        operation: PublishOperation,
    ) -> str:

        if operation.kind == "milestone":
            return (
                f"gh api repos/{self.owner}/{self.repo}/milestones "
                f"--method POST --field title='{operation.title}'"
            )

        if operation.kind == "issue":
            return (
                "gh issue create "
                f"--title '{operation.title}'"
            )

        raise ValueError(
            f"Unsupported operation: {operation.kind}"
        )
