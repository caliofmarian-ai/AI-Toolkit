"""
Self Evaluation Engine — Evaluation Report Generator
CORE-016E

Renders AI_CTO_SELF_EVALUATION.md from EvaluationResult intelligence.
"""

from pathlib import Path
from typing import Any, List, Mapping


def _score_bar(score: float, width: int = 20) -> str:
    filled = max(0, min(width, int(score * width)))
    return "[" + "█" * filled + "░" * (width - filled) + f"] {score:.0%}"


def _fmt_list(items: List[str], indent: str = "  ") -> str:
    if not items:
        return f"{indent}_(none)_\n"
    return "".join(f"{indent}- {item}\n" for item in items)


class EvaluationReportGenerator:
    """
    CORE-016E — Evaluation Report Generator.

    Renders the AI_CTO_SELF_EVALUATION.md report.
    """

    def render(self, result: Any) -> str:
        d = result.to_dict() if hasattr(result, "to_dict") else result
        return self._build_markdown(d)

    def generate(self, result: Any, output_path: Path) -> None:
        content = self.render(result)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            content if content.endswith("\n") else content + "\n",
            encoding="utf-8",
        )

    # ------------------------------------------------------------------

    def _build_markdown(self, d: Mapping[str, Any]) -> str:
        quality_scores = d.get("quality_scores", [])
        regressions = d.get("regression_findings", [])
        architecture = d.get("architecture_findings", [])
        recommendations = d.get("recommendations", [])
        errors = d.get("errors", [])
        warnings = d.get("warnings", [])
        overall = d.get("overall_score", 0.0)
        gate = d.get("overall_gate", "")

        lines = []

        # Header
        lines.append("# AI CTO Self Evaluation Report\n")
        lines.append(f"**Evaluation ID:** {d.get('evaluation_id', '')}\n")
        lines.append(f"**Generated:** {d.get('generated_at', '')}\n")
        lines.append(f"**Repository:** {d.get('repository', '')}\n")
        lines.append(f"**Overall Gate:** {gate}\n")
        lines.append(f"**Overall Score:** `{_score_bar(overall)}`\n")
        lines.append("")

        # Quality Scores
        lines.append("---\n")
        lines.append("## Quality Scores\n")
        if quality_scores:
            lines.append("| Dimension | Score | Gate |\n")
            lines.append("|-----------|-------|------|\n")
            for s in quality_scores:
                lines.append(
                    f"| {s.get('dimension', '')} "
                    f"| `{_score_bar(s.get('score', 0.0), 10)}` "
                    f"| {s.get('gate', '')} |\n"
                )
        else:
            lines.append("_(no scores available)_\n")
        lines.append("")

        # Regressions
        lines.append("---\n")
        lines.append(f"## Regressions ({len(regressions)} found)\n")
        if regressions:
            for r in regressions:
                lines.append(
                    f"- **[{r.get('severity', '').upper()}]** "
                    f"{r.get('component', '')}: {r.get('finding', '')}\n"
                    f"  - Impact: {r.get('impact', '')}\n"
                    f"  - Recommendation: {r.get('recommendation', '')}\n"
                )
        else:
            lines.append("_(no regressions detected)_\n")
        lines.append("")

        # Architecture
        lines.append("---\n")
        lines.append(f"## Architecture Findings ({len(architecture)} found)\n")
        if architecture:
            for a in architecture:
                lines.append(
                    f"- **[{a.get('severity', '').upper()}]** "
                    f"{a.get('category', '')}: {a.get('description', '')}\n"
                )
        else:
            lines.append("_(no architecture findings)_\n")
        lines.append("")

        # Errors and warnings
        if errors:
            lines.append("---\n")
            lines.append("## Errors\n")
            lines.append(_fmt_list(errors))
            lines.append("")

        if warnings:
            lines.append("---\n")
            lines.append("## Warnings\n")
            lines.append(_fmt_list(warnings))
            lines.append("")

        # Recommendations
        lines.append("---\n")
        lines.append("## Recommendations\n")
        lines.append(_fmt_list(recommendations))
        lines.append("")

        # Summary
        lines.append("---\n")
        lines.append("## Summary\n")
        lines.append(f"{d.get('summary', 'No summary available.')}\n")

        return "".join(lines)
