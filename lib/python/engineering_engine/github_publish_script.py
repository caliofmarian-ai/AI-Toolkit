from __future__ import annotations

from lib.python.engineering_engine.github_publish_engine import (
    PublishPlan,
)


class GitHubPublishScript:

    def render(
        self,
        plan: PublishPlan,
    ) -> str:

        lines = [
            "# GitHub Publish Plan",
            "",
        ]

        for index, op in enumerate(plan.operations, start=1):
            lines.append(
                f"{index:03}. [{op.kind.upper()}] {op.title}"
            )

        return "\n".join(lines)
