from __future__ import annotations

from pathlib import Path

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

    def execute(
        self,
        plan: PublishPlan,
        *,
        log_path: Path,
        plan_only: bool = True,
    ) -> list[str]:

        logger = GitHubTransactionLogger()
        log = logger.load(log_path)

        client = GitHubRealClient()

        results: list[str] = []

        for operation in plan.operations:

            result = client.execute(
                operation,
                plan_only=plan_only,
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
