from __future__ import annotations

from pathlib import Path

from lib.python.engineering_engine.github_client import GitHubClient, GitHubDryRunClient
from lib.python.engineering_engine.github_publish_engine import (
    PublishPlan,
)
from lib.python.engineering_engine.github_real_client import (
    GitHubRealClient,
)
from lib.python.engineering_engine.github_transaction_log import (
    GitHubTransactionLogger,
)


class GitHubTransactionalExecutor:

    def __init__(self, client: GitHubClient | None = None):
        self._client = client

    def execute(
        self,
        plan: PublishPlan,
        *,
        log_path: Path,
        plan_only: bool = True,
    ) -> list[str]:

        logger = GitHubTransactionLogger()
        log = logger.load(log_path)

        client = self._client or (GitHubDryRunClient() if plan_only else GitHubRealClient())

        results: list[str] = []

        for operation in plan.operations:

            result = client.execute(
                operation,
            )

            status = "SUCCESS"

            logger.append(
                log,
                operation="CREATE",
                title=operation.title,
                status=status,
            )

            logger.save(
                log,
                log_path,
            )

            results.append(result)

        return results
