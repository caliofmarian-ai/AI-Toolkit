from __future__ import annotations

import subprocess

from lib.python.engineering_engine.github_client import GitHubClient
from lib.python.engineering_engine.github_publish_engine import PublishOperation
from lib.python.engineering_engine.github_repository_resolver import (
    GitHubRepositoryResolver,
)


class GitHubRealClient(GitHubClient):

    def __init__(self):
        repo = GitHubRepositoryResolver().resolve()
        self.owner = repo.owner
        self.repo = repo.repo

    def execute(
        self,
        operation: PublishOperation,
        *,
        plan_only: bool = True,
    ) -> str:

        if operation.kind == "milestone":
            command = [
                "gh",
                "api",
                f"repos/{self.owner}/{self.repo}/milestones",
                "--method",
                "POST",
                "--field",
                f"title={operation.title}",
            ]
        elif operation.kind == "issue":
            command = [
                "gh",
                "issue",
                "create",
                "--title",
                operation.title,
            ]
        else:
            raise ValueError(
                f"Unsupported operation: {operation.kind}"
            )

        if plan_only:
            return "PLAN: " + " ".join(command)

        subprocess.run(command, check=True)
        return "EXECUTED: " + operation.title
