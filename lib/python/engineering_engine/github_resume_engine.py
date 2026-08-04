from __future__ import annotations

from dataclasses import dataclass, field

from lib.python.engineering_engine.github_publish_engine import (
    PublishPlan,
    PublishOperation,
)
from lib.python.engineering_engine.github_transaction_log import (
    TransactionLog,
)


@dataclass(slots=True)
class ResumePlan:
    operations: list[PublishOperation] = field(default_factory=list)


class GitHubResumeEngine:

    def build(
        self,
        plan: PublishPlan,
        log: TransactionLog,
    ) -> ResumePlan:

        completed = {
            record.title
            for record in log.records
            if record.status == "SUCCESS"
        }

        resume = ResumePlan()

        for operation in plan.operations:

            if operation.title in completed:
                continue

            resume.operations.append(operation)

        return resume
