from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(slots=True)
class GitHubState:

    milestones: set[str] = field(default_factory=set)

    issues: set[str] = field(default_factory=set)


class GitHubStateProvider(ABC):

    @abstractmethod
    def load(self) -> GitHubState:
        raise NotImplementedError


class EmptyGitHubStateProvider(GitHubStateProvider):

    def load(self) -> GitHubState:
        return GitHubState()


class InMemoryGitHubStateProvider(GitHubStateProvider):

    def __init__(
        self,
        milestones: set[str] | None = None,
        issues: set[str] | None = None,
    ):
        self._state = GitHubState(
            milestones=milestones or set(),
            issues=issues or set(),
        )

    def load(self) -> GitHubState:
        return self._state
