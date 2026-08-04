from __future__ import annotations

from dataclasses import dataclass

from lib.python.engineering_engine.github_issue_generator import GitHubIssue


@dataclass(slots=True)
class ComparisonResult:
    identical: bool
    requires_update: bool


class GitHubComparisonEngine:

    def compare_issue(
        self,
        expected: GitHubIssue,
        current: GitHubIssue,
    ) -> ComparisonResult:

        identical = (
            expected.title == current.title
            and expected.body == current.body
            and sorted(expected.labels) == sorted(current.labels)
        )

        return ComparisonResult(
            identical=identical,
            requires_update=not identical,
        )
