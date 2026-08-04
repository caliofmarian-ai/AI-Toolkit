from __future__ import annotations

from abc import ABC, abstractmethod

from lib.python.engineering_engine.github_publish_engine import (
    PublishOperation,
)


class GitHubClient(ABC):

    @abstractmethod
    def execute(
        self,
        operation: PublishOperation,
    ) -> str:
        raise NotImplementedError


class GitHubDryRunClient(GitHubClient):

    def execute(
        self,
        operation: PublishOperation,
    ) -> str:

        return (
            f"DRY-RUN: "
            f"{operation.kind.upper()} -> "
            f"{operation.title}"
        )
