from __future__ import annotations

from datetime import UTC, datetime

from lib.python.engineering_engine.models import (
    EngineeringBatch,
    ImplementationPackageModel,
)


class MarkdownRenderer:

    def render_implementation_package(
        self,
        model: ImplementationPackageModel,
    ) -> str:

        lines = []

        lines.append("# Implementation Package")
        lines.append("")
        lines.append(f"CORE: {model.core}")
        lines.append(f"TITLE: {model.title}")
        lines.append(f"Generated: {datetime.now(UTC).isoformat()}")
        lines.append("")

        def section(title: str, items: list[str]):
            lines.append(f"## {title}")
            lines.append("")
            if items:
                for item in items:
                    lines.append(f"- {item}")
            else:
                lines.append("- None")
            lines.append("")

        section("Canonical References", model.canonical_references)
        section("Objectives", model.objectives)
        section("Scope", model.scope)
        section("Deliverables", model.deliverables)
        section("Acceptance Criteria", model.acceptance_criteria)

        lines.append("## Engineering Batches")
        lines.append("")

        if model.batches:
            for batch in model.batches:
                lines.append(f"### {batch.id}")
                lines.append("")
                lines.append(f"Objective: {batch.objective}")
                lines.append(f"Priority: {batch.priority}")
                lines.append(f"Status: {batch.status}")
                lines.append(f"Risk: {batch.risk}")
                lines.append("")
        else:
            lines.append("No engineering batches defined.")
            lines.append("")

        return "\n".join(lines)
