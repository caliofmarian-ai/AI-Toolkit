from __future__ import annotations

from lib.python.engineering_engine.github_client import GitHubClient
from lib.python.engineering_engine.github_publish_engine import PublishOperation
from lib.python.engineering_engine.github_repository_resolver import (
    GitHubRepositoryResolver,
)


class GitHubCLIClient(GitHubClient):

    def __init__(self):
        repository = GitHubRepositoryResolver().resolve()
        self.owner = repository.owner
        self.repo = repository.repo

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
