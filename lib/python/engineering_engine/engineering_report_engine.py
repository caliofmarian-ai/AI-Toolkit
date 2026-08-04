from __future__ import annotations

from lib.python.engineering_engine.engineering_workflow_engine import (
    EngineeringWorkflowResult,
)


class EngineeringReportEngine:

    def render(
        self,
        result: EngineeringWorkflowResult,
    ) -> str:

        lines = []

        lines.append("# Engineering Report")
        lines.append("")
        lines.append(f"Risk: {result.impact.risk}")
        lines.append("")

        lines.append("## Recommendations")
        for item in result.recommendation.recommendations:
            lines.append(f"- {item}")

        lines.append("")
        lines.append("## Execution Plan")
        for index, phase in enumerate(result.execution.phases, start=1):
            lines.append(f"{index}. {phase}")

        lines.append("")
        lines.append("## Validation Plan")
        for index, check in enumerate(result.validation.checks, start=1):
            lines.append(f"{index}. {check}")

        return "\n".join(lines)
