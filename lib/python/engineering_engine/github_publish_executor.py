from __future__ import annotations

from lib.python.engineering_engine.github_publish_engine import (
    PublishPlan,
)


from lib.python.engineering_engine.github_client import GitHubDryRunClient


from lib.python.engineering_engine.github_client import GitHubDryRunClient


class GitHubPublishExecutor:

    def execute(
        self,
        plan: PublishPlan,
        dry_run: bool = True,
    ) -> list[str]:

        client = GitHubDryRunClient()

        results = []

        for operation in plan.operations:

            if not dry_run:
                raise NotImplementedError(
                    "GitHub API execution not implemented yet."
                )

            results.append(
                client.execute(operation)
            )

        return results
