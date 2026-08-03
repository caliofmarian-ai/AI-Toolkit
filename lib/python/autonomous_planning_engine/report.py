"""
Autonomous Planning Engine — Planning Report Generator
CORE-014L

Renders AI_CTO_PLANNING_REPORT.md from PlanningResult intelligence.
The report is fully derived from the planning artifacts — no hardcoded text.
"""

from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from .models import PlanningResult


def _fmt_list(items: List[str], indent: str = "  ") -> str:
    if not items:
        return f"{indent}_(none)_\n"
    return "".join(f"{indent}- {item}\n" for item in items)


def _fmt_entry(entry: Mapping[str, Any], rank: int) -> str:
    blocked = entry.get("blocked_by", [])
    blocked_str = f" ⚠ BLOCKED by: {', '.join(str(b) for b in blocked)}" if blocked else ""
    deps = entry.get("dependencies", [])
    dep_str = f"\n     Dependencies: {', '.join(str(d) for d in deps)}" if deps else ""
    return (
        f"{rank}. **[{entry.get('priority', '').upper()}]** "
        f"{entry.get('title', '')} "
        f"(`{entry.get('type', '')}`){blocked_str}\n"
        f"   - Reason: {entry.get('reason', '')}\n"
        f"   - Effort: {entry.get('estimated_effort', '')} | "
        f"Confidence: {entry.get('confidence', 0.0):.0%}{dep_str}\n"
    )


class PlanningReportGenerator:
    """
    CORE-014L — Planning Report Generator.

    Renders a human-readable Markdown planning report from PlanningResult.
    """

    def render(self, result: PlanningResult) -> str:
        """Return the Markdown string for AI_CTO_PLANNING_REPORT.md."""
        d = result.to_dict()
        return self._build_markdown(d)

    def generate(self, result: PlanningResult, output_path: Path) -> None:
        """Write the report to ``output_path``."""
        content = self.render(result)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            content if content.endswith("\n") else content + "\n",
            encoding="utf-8",
        )

    # ------------------------------------------------------------------

    def _build_markdown(self, d: Mapping[str, Any]) -> str:
        rp = d.get("roadmap_progress", {})
        na = d.get("next_actions", {})
        queue = d.get("execution_queue", {})
        entries = queue.get("entries", [])

        lines = []

        # Header
        lines.append("# AI CTO Planning Report\n")
        lines.append(f"**Planning ID:** {d.get('planning_id', '')}\n")
        lines.append(f"**Generated:** {d.get('generated_at', '')}\n")
        lines.append(f"**Repository:** {d.get('repository', '')}\n")
        lines.append("")

        # Roadmap Progress
        lines.append("---\n")
        lines.append("## Roadmap Progress\n")
        lines.append(
            f"| Phase | Maturity | Completion | Remaining Effort |\n"
            f"|-------|----------|------------|------------------|\n"
            f"| {rp.get('current_phase', '')} "
            f"| {rp.get('repository_maturity', '')} "
            f"| {rp.get('completion_percentage', 0.0):.1f}% "
            f"| {rp.get('estimated_remaining_effort', '')} |\n"
        )
        lines.append("")

        completed = rp.get("completed_cores", [])
        incomplete = rp.get("incomplete_cores", [])
        blocked = rp.get("blocked_cores", [])

        lines.append(f"**Completed COREs ({len(completed)}):**\n")
        lines.append(_fmt_list(completed))
        lines.append(f"**Incomplete COREs ({len(incomplete)}):**\n")
        lines.append(_fmt_list(incomplete))
        if blocked:
            lines.append(f"**Blocked COREs ({len(blocked)}):**\n")
            lines.append(_fmt_list(blocked))

        # Next Actions
        lines.append("---\n")
        lines.append("## Next Actions\n")

        def _action_row(label: str, action: Optional[Dict[str, Any]]) -> str:
            if not action:
                return f"| {label} | _(not determined)_ | — | — |\n"
            return (
                f"| {label} | {action.get('title', '')} "
                f"| {action.get('priority', '')} "
                f"| {action.get('confidence', 0.0):.0%} |\n"
            )

        lines.append("| Action | Title | Priority | Confidence |\n")
        lines.append("|--------|-------|----------|------------|\n")
        lines.append(_action_row("Next CORE", na.get("next_core")))
        lines.append(_action_row("Next Issue", na.get("next_issue")))
        lines.append(_action_row("Next Batch", na.get("next_batch")))
        lines.append(_action_row("Next PR", na.get("next_pr")))
        lines.append(_action_row("Next Milestone", na.get("next_milestone")))
        lines.append("")

        # Execution Queue
        lines.append("---\n")
        lines.append(f"## Execution Queue ({len(entries)} items)\n")
        lines.append(
            "_Items are ordered by priority score and dependency constraints._\n"
        )
        lines.append("")
        for i, entry in enumerate(entries[:20], 1):
            lines.append(_fmt_entry(entry, i))

        if len(entries) > 20:
            lines.append(f"_...and {len(entries) - 20} more items._\n")

        # Individual Recommendations
        lines.append("---\n")
        lines.append("## Individual Recommendations\n")

        for section_key, section_label in (
            ("recommended_core", "Recommended CORE"),
            ("recommended_issue", "Recommended Issue"),
            ("recommended_batch", "Recommended Batch"),
            ("recommended_pr", "Recommended Pull Request"),
            ("recommended_milestone", "Recommended Milestone"),
        ):
            rec = d.get(section_key)
            lines.append(f"### {section_label}\n")
            if rec:
                lines.append(f"**{rec.get('title', rec.get('id', ''))}**\n")
                lines.append(f"{rec.get('reason', '')}\n")
                effort = rec.get("estimated_effort", "")
                conf = rec.get("confidence", 0.0)
                if effort or conf:
                    lines.append(
                        f"- Effort: {effort} | Confidence: {conf:.0%}\n"
                    )
            else:
                lines.append("_(not determined)_\n")
            lines.append("")

        # Footer
        lines.append("---\n")
        lines.append(
            "_Generated by AI CTO Autonomous Planning Engine — CORE-014._\n"
        )

        return "\n".join(lines)
