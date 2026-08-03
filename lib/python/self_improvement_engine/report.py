"""
Self Improvement Engine — Improvement Report Generator
CORE-017E

Renders AI_CTO_SELF_IMPROVEMENT.md from OptimizationPlan intelligence.
"""

from pathlib import Path
from typing import Any, List, Mapping


def _fmt_list(items: List[str], indent: str = "  ") -> str:
    if not items:
        return f"{indent}_(none)_\n"
    return "".join(f"{indent}- {item}\n" for item in items)


class ImprovementReportGenerator:
    """
    CORE-017E — Improvement Report Generator.

    Renders the AI_CTO_SELF_IMPROVEMENT.md report.
    """

    def render(self, plan: Any) -> str:
        d = plan.to_dict() if hasattr(plan, "to_dict") else plan
        return self._build_markdown(d)

    def generate(self, plan: Any, output_path: Path) -> None:
        content = self.render(plan)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            content if content.endswith("\n") else content + "\n",
            encoding="utf-8",
        )

    # ------------------------------------------------------------------

    def _build_markdown(self, d: Mapping[str, Any]) -> str:
        debt = d.get("technical_debt", [])
        metrics = d.get("performance_metrics", [])
        gaps = d.get("capability_gaps", [])
        issues = d.get("proposed_issues", [])
        batches = d.get("proposed_batches", [])
        cores = d.get("core_proposals", [])
        roadmap = d.get("roadmap_updates", [])

        lines = []

        # Header
        lines.append("# AI CTO Self Improvement Report\n")
        lines.append(f"**Plan ID:** {d.get('plan_id', '')}\n")
        lines.append(f"**Generated:** {d.get('generated_at', '')}\n")
        lines.append(f"**Repository:** {d.get('repository', '')}\n")
        lines.append("")

        # Summary counts
        lines.append("---\n")
        lines.append("## Summary\n")
        lines.append(f"| Item | Count |\n|------|-------|\n")
        lines.append(f"| Technical Debt Items | {len(debt)} |\n")
        lines.append(f"| Performance Metrics | {len(metrics)} |\n")
        lines.append(f"| Capability Gaps | {len(gaps)} |\n")
        lines.append(f"| Proposed Issues | {len(issues)} |\n")
        lines.append(f"| Proposed Batches | {len(batches)} |\n")
        lines.append(f"| CORE Proposals | {len(cores)} |\n")
        lines.append(f"| Roadmap Updates | {len(roadmap)} |\n")
        lines.append("")

        # Technical Debt
        lines.append("---\n")
        lines.append(f"## Technical Debt ({len(debt)} items)\n")
        if debt:
            for item in debt[:20]:
                lines.append(
                    f"- **[{item.get('severity', '').upper()}]** "
                    f"`{item.get('component', '')}`: {item.get('description', '')}\n"
                    f"  - Recommendation: {item.get('recommendation', '')}\n"
                )
        else:
            lines.append("_(no technical debt detected)_\n")
        lines.append("")

        # Performance
        lines.append("---\n")
        lines.append(f"## Performance Metrics ({len(metrics)} items)\n")
        if metrics:
            lines.append("| Metric | Value | Unit | Trend |\n")
            lines.append("|--------|-------|------|-------|\n")
            for m in metrics:
                lines.append(
                    f"| {m.get('name', '')} "
                    f"| {m.get('value', 0)} "
                    f"| {m.get('unit', '')} "
                    f"| {m.get('trend', '')} |\n"
                )
        else:
            lines.append("_(no performance metrics available)_\n")
        lines.append("")

        # Capability Gaps
        lines.append("---\n")
        lines.append(f"## Capability Gaps ({len(gaps)} found)\n")
        if gaps:
            for gap in gaps:
                lines.append(
                    f"- **[{gap.get('priority', '').upper()}]** "
                    f"{gap.get('description', '')}\n"
                )
        else:
            lines.append("_(no capability gaps detected)_\n")
        lines.append("")

        # Proposed Issues
        lines.append("---\n")
        lines.append(f"## Proposed Issues ({len(issues)} items)\n")
        if issues:
            for issue in issues[:10]:
                lines.append(
                    f"- **{issue.get('issue_id', '')}** [{issue.get('priority', '').upper()}]: "
                    f"{issue.get('title', '')}\n"
                    f"  - {issue.get('objective', '')}\n"
                )
        else:
            lines.append("_(no issues proposed)_\n")
        lines.append("")

        # Proposed Batches
        lines.append("---\n")
        lines.append(f"## Proposed Batches ({len(batches)} items)\n")
        if batches:
            for batch in batches:
                lines.append(
                    f"- **{batch.get('batch_id', '')}**: {batch.get('title', '')} "
                    f"({len(batch.get('issue_ids', []))} issues)\n"
                    f"  - Owner approval required: {batch.get('owner_approval_required', True)}\n"
                )
        else:
            lines.append("_(no batches proposed)_\n")
        lines.append("")

        # CORE Proposals
        lines.append("---\n")
        lines.append(f"## CORE Proposals ({len(cores)} items)\n")
        if cores:
            for core in cores:
                lines.append(
                    f"- **{core.get('core_id', '')}**: {core.get('problem_statement', '')}\n"
                    f"  - Complexity: {core.get('estimated_complexity', '')}\n"
                    f"  - Roadmap Position: {core.get('roadmap_position', '')}\n"
                )
        else:
            lines.append("_(no new CORE proposals at this time)_\n")
        lines.append("")

        # Roadmap Updates
        lines.append("---\n")
        lines.append(f"## Roadmap Updates ({len(roadmap)} recommended)\n")
        if roadmap:
            for update in roadmap:
                lines.append(
                    f"- **[{update.get('priority', '').upper()}]** "
                    f"{update.get('category', '')}: {update.get('description', '')}\n"
                    f"  - Owner approval required: {update.get('owner_approval_required', True)}\n"
                )
        else:
            lines.append("_(no roadmap updates recommended)_\n")
        lines.append("")

        # Summary
        lines.append("---\n")
        lines.append("## Optimization Summary\n")
        lines.append(f"{d.get('summary', 'No summary available.')}\n")

        return "".join(lines)
