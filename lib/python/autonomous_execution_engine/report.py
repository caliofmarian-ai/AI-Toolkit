"""
Autonomous Execution Engine — Execution Report Generator
CORE-015H

Renders AI_CTO_EXECUTION_REPORT.md from ExecutionResult intelligence.
The report is fully derived from execution artifacts — no hardcoded text.
"""

from pathlib import Path
from typing import Any, Dict, List, Mapping


def _fmt_list(items: List[str], indent: str = "  ") -> str:
    if not items:
        return f"{indent}_(none)_\n"
    return "".join(f"{indent}- {item}\n" for item in items)


def _score_bar(score: float, width: int = 20) -> str:
    filled = max(0, min(width, int(score * width)))
    return "[" + "█" * filled + "░" * (width - filled) + f"] {score:.0%}"


class ExecutionReportGenerator:
    """
    CORE-015H — Execution Report Generator.

    Renders a human-readable Markdown execution report from the execution result.
    """

    def render(self, result: Any) -> str:
        """Return the Markdown string for AI_CTO_EXECUTION_REPORT.md."""
        d = result.to_dict() if hasattr(result, "to_dict") else result
        return self._build_markdown(d)

    def generate(self, result: Any, output_path: Path) -> None:
        """Write the report to ``output_path``."""
        content = self.render(result)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            content if content.endswith("\n") else content + "\n",
            encoding="utf-8",
        )

    # ------------------------------------------------------------------

    def _build_markdown(self, d: Mapping[str, Any]) -> str:
        ctx = d.get("context", {})
        metrics = d.get("metrics", {})
        stage_results = d.get("stage_results", [])
        validation_results = d.get("validation_results", [])
        errors = d.get("errors", [])
        warnings = d.get("warnings", [])
        next_actions = d.get("next_actions", [])
        confidence = ctx.get("confidence", 0.0)

        lines = []

        # Header
        lines.append("# AI CTO Execution Report\n")
        lines.append(f"**Execution ID:** {d.get('execution_id', '')}\n")
        lines.append(f"**Generated:** {d.get('generated_at', '')}\n")
        lines.append(f"**Repository:** {d.get('repository', '')}\n")
        lines.append(f"**Mode:** {d.get('mode', '')}\n")
        lines.append(f"**Approval:** {d.get('approval', '')}\n")
        lines.append(f"**Status:** {d.get('status', '')}\n")
        lines.append("")

        # Confidence
        lines.append("---\n")
        lines.append("## Confidence\n")
        lines.append(f"`{_score_bar(confidence)}`\n")
        lines.append("")

        # Execution Context
        lines.append("---\n")
        lines.append("## Execution Context\n")
        if ctx:
            lines.append(f"| Field | Value |\n|-------|-------|\n")
            for k, v in sorted(ctx.items()):
                if k not in ("schema_version", "confidence"):
                    lines.append(f"| {k} | {v} |\n")
        lines.append("")

        # Pipeline Stages
        lines.append("---\n")
        lines.append("## Pipeline Stages\n")
        if stage_results:
            lines.append("| Stage | Status | Duration (ms) | Errors |\n")
            lines.append("|-------|--------|---------------|--------|\n")
            for s in stage_results:
                lines.append(
                    f"| {s.get('stage', '')} "
                    f"| {s.get('status', '')} "
                    f"| {s.get('duration_ms', 0.0):.1f} "
                    f"| {len(s.get('errors', []))} |\n"
                )
        else:
            lines.append("_(no stages recorded)_\n")
        lines.append("")

        # Validation
        lines.append("---\n")
        lines.append("## Validation Results\n")
        if validation_results:
            lines.append("| Validator | Status | Score |\n")
            lines.append("|-----------|--------|-------|\n")
            for v in validation_results:
                lines.append(
                    f"| {v.get('validator', '')} "
                    f"| {v.get('status', '')} "
                    f"| {v.get('score', 0.0):.0%} |\n"
                )
        else:
            lines.append("_(no validators ran)_\n")
        lines.append("")

        # Performance
        lines.append("---\n")
        lines.append("## Performance Metrics\n")
        if metrics:
            lines.append(
                f"- Total Duration: {metrics.get('total_duration_ms', 0.0):.1f} ms\n"
            )
            lines.append(f"- Evidence Count: {metrics.get('evidence_count', 0)}\n")
            lines.append(f"- Artifact Count: {metrics.get('artifact_count', 0)}\n")
            lines.append(f"- Error Count: {metrics.get('error_count', 0)}\n")
            lines.append(f"- Warning Count: {metrics.get('warning_count', 0)}\n")
        lines.append("")

        # Errors
        if errors:
            lines.append("---\n")
            lines.append("## Errors\n")
            lines.append(_fmt_list(errors))
            lines.append("")

        # Warnings
        if warnings:
            lines.append("---\n")
            lines.append("## Warnings\n")
            lines.append(_fmt_list(warnings))
            lines.append("")

        # Next Actions
        lines.append("---\n")
        lines.append("## Next Actions\n")
        lines.append(_fmt_list(next_actions))
        lines.append("")

        # Summary
        lines.append("---\n")
        lines.append("## Summary\n")
        lines.append(f"{d.get('summary', 'No summary available.')}\n")

        return "".join(lines)
