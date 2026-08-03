"""
Executive Briefing Engine — Markdown Generator
CORE-010G

Renders the executive briefing as AI_CTO_EXECUTIVE_BRIEFING.md.
"""

from pathlib import Path
from typing import Any, Dict, Mapping

from .models import ExecutiveBriefing, ExecutiveRisk, ExecutiveRecommendation


_HEALTH_EMOJI = {
    "healthy": "🟢",
    "active": "🔵",
    "warning": "🟡",
    "degraded": "🔴",
    "critical": "🔴",
    "unavailable": "⚫",
    "unknown": "⚪",
}


def _health_badge(label: str) -> str:
    icon = _HEALTH_EMOJI.get(label, "⚪")
    return f"{icon} {label.capitalize()}"


class ExecutiveBriefingGenerator:
    """
    Renders the executive briefing as a markdown document.

    Consumes an ExecutiveBriefing dataclass and produces deterministic,
    human-readable markdown suitable for the AI CTO owner interface.
    """

    def generate(self, briefing: ExecutiveBriefing, output_path: Path) -> str:
        """Render briefing to markdown and write to output_path."""
        content = self._render(briefing)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        return content

    def render(self, briefing: ExecutiveBriefing) -> str:
        """Render briefing to markdown string without writing to disk."""
        return self._render(briefing)

    # ------------------------------------------------------------------
    # Private rendering
    # ------------------------------------------------------------------

    def _render(self, b: ExecutiveBriefing) -> str:
        sections = [
            self._header(b),
            self._owner_dashboard(b),
            self._executive_summary(b),
            self._workspace_status(b),
            self._health_overview(b),
            self._recommendations(b),
            self._risks(b),
            self._priorities(b),
            self._pending_decisions(b),
            self._suggested_next(b),
            self._footer(b),
        ]
        return "\n\n".join(s for s in sections if s.strip())

    def _header(self, b: ExecutiveBriefing) -> str:
        return (
            f"# AI CTO Executive Briefing\n\n"
            f"> **Briefing ID:** {b.briefing_id}  \n"
            f"> **Generated:** {b.generated_at}  \n"
            f"> **Repository:** `{b.repository}`  \n"
            f"> **Schema:** {b.schema_version}"
        )

    def _owner_dashboard(self, b: ExecutiveBriefing) -> str:
        d = b.owner_dashboard
        lines = [
            "## Owner Dashboard",
            "",
            f"| Dimension | Status |",
            f"|-----------|--------|",
            f"| **AI CTO Health** | {_health_badge(d.overall_health)} |",
            f"| **Repository Readiness** | {d.repository_readiness} |",
            f"| **Current Progress** | {d.current_progress} |",
            f"| **Open Risks** | {d.open_risks} |",
        ]
        if d.recommended_actions:
            lines.append("")
            lines.append("**Recommended Actions:**")
            for action in d.recommended_actions:
                lines.append(f"- {action}")
        if d.blocked_items:
            lines.append("")
            lines.append("**Blocked Items:**")
            for item in d.blocked_items:
                lines.append(f"- ⛔ {item}")
        return "\n".join(lines)

    def _executive_summary(self, b: ExecutiveBriefing) -> str:
        return f"## Executive Summary\n\n{b.executive_summary}"

    def _workspace_status(self, b: ExecutiveBriefing) -> str:
        rows = [
            ("Current Branch", b.current_branch),
            ("Current Issue", b.current_issue),
            ("Current Pull Request", b.current_pull_request),
            ("Current Batch", b.current_batch),
            ("Current Milestone", b.current_milestone),
            ("Current Epic", b.current_epic),
            ("Current Recommendation", b.current_recommendation),
        ]
        lines = [
            "## Current Workspace Status",
            "",
            "| Field | Value |",
            "|-------|-------|",
        ]
        for label, value in rows:
            display = f"`{value}`" if value else "—"
            lines.append(f"| **{label}** | {display} |")
        return "\n".join(lines)

    def _health_overview(self, b: ExecutiveBriefing) -> str:
        rows = [
            ("Architecture Health", b.architecture_health),
            ("Canonical Health", b.canonical_health),
            ("Development Health", b.development_health),
            ("Repository Health", b.repository_health),
            ("Runtime Health", b.runtime_health),
        ]
        lines = [
            "## Health Overview",
            "",
            "| Dimension | Status |",
            "|-----------|--------|",
        ]
        for label, health in rows:
            lines.append(f"| **{label}** | {_health_badge(health)} |")
        return "\n".join(lines)

    def _recommendations(self, b: ExecutiveBriefing) -> str:
        if not b.recommendations:
            return "## Recommendations\n\n_No recommendations generated._"
        lines = [
            "## Recommendations",
            "",
            f"_{len(b.recommendations)} recommendation(s) derived from repository intelligence._",
        ]
        for rec in b.recommendations:
            confidence_pct = f"{rec.confidence * 100:.0f}%"
            lines.append("")
            lines.append(f"### {rec.id}: {rec.title}")
            lines.append("")
            lines.append(f"| Field | Value |")
            lines.append(f"|-------|-------|")
            lines.append(f"| **Priority** | `{rec.priority}` |")
            lines.append(f"| **Impact** | {rec.impact} |")
            lines.append(f"| **Confidence** | {confidence_pct} |")
            lines.append(f"| **Required Effort** | `{rec.required_effort}` |")
            if rec.affected_components:
                components = ", ".join(f"`{c}`" for c in rec.affected_components[:3])
                lines.append(f"| **Affected Components** | {components} |")
            lines.append("")
            lines.append(f"**Description:** {rec.description}")
            lines.append("")
            lines.append(f"**Reasoning:** {rec.reasoning}")
            if rec.evidence:
                lines.append("")
                lines.append("**Evidence:**")
                for ev in rec.evidence[:3]:
                    lines.append(f"- `{ev}`")
        return "\n".join(lines)

    def _risks(self, b: ExecutiveBriefing) -> str:
        if not b.all_risks:
            return "## Risks\n\n_No risks detected._"
        lines = [
            "## Risks",
            "",
            f"_{len(b.all_risks)} risk(s) detected.  "
            f"{len(b.critical_risks)} critical._",
        ]
        for risk in b.all_risks:
            icon = _HEALTH_EMOJI.get(risk.severity, "⚪")
            lines.append("")
            lines.append(f"### {risk.id}: {risk.title}")
            lines.append("")
            lines.append(f"| Field | Value |")
            lines.append(f"|-------|-------|")
            lines.append(f"| **Severity** | {icon} `{risk.severity}` |")
            lines.append(f"| **Category** | `{risk.category}` |")
            if risk.affected_components:
                lines.append(
                    f"| **Affected** | "
                    + ", ".join(f"`{c}`" for c in risk.affected_components[:3])
                    + " |"
                )
            lines.append("")
            lines.append(f"**Description:** {risk.description}")
            lines.append("")
            lines.append(f"**Remediation:** {risk.remediation}")
            if risk.evidence:
                lines.append("")
                lines.append("**Evidence:**")
                for ev in risk.evidence[:3]:
                    lines.append(f"- `{ev}`")
        return "\n".join(lines)

    def _priorities(self, b: ExecutiveBriefing) -> str:
        if not b.priorities:
            return "## Priorities\n\n_No priority items classified._"
        lines = [
            "## Priorities",
            "",
            "| ID | Title | Classification | Category |",
            "|----|-------|----------------|----------|",
        ]
        for p in b.priorities:
            lines.append(f"| {p.id} | {p.title} | `{p.classification}` | {p.category} |")
        return "\n".join(lines)

    def _pending_decisions(self, b: ExecutiveBriefing) -> str:
        if not b.pending_decisions:
            return "## Pending Decisions\n\n_No pending decisions._"
        lines = [
            "## Pending Decisions",
            "",
            f"_{len(b.pending_decisions)} decision(s) require owner resolution._",
        ]
        for dec in b.pending_decisions:
            lines.append("")
            lines.append(f"### {dec.id}: {dec.title}")
            lines.append("")
            lines.append(f"**Urgency:** `{dec.urgency}`")
            lines.append("")
            lines.append(f"**Description:** {dec.description}")
            lines.append("")
            lines.append("**Options:**")
            for i, opt in enumerate(dec.options, 1):
                marker = "✅" if opt == dec.recommended_option else f"{i}."
                lines.append(f"- {marker} {opt}")
            lines.append("")
            lines.append(f"**Recommended:** {dec.recommended_option}")
            lines.append("")
            lines.append(f"**Impact:** {dec.impact}")
        return "\n".join(lines)

    def _suggested_next(self, b: ExecutiveBriefing) -> str:
        lines = [
            "## Suggested Next Steps",
            "",
            "| Item | Value |",
            "|------|-------|",
        ]
        next_core = b.suggested_next_core or "—"
        next_batch = b.suggested_next_batch or "—"
        next_pr = b.suggested_next_pr or "—"
        completion = b.estimated_completion or "—"

        lines.append(f"| **Next CORE** | `{next_core}` |")
        lines.append(f"| **Next Batch** | `{next_batch}` |")
        lines.append(f"| **Next PR** | `{next_pr}` |")
        lines.append(f"| **Estimated Completion** | {completion} |")
        return "\n".join(lines)

    def _footer(self, b: ExecutiveBriefing) -> str:
        return (
            f"---\n\n"
            f"_Generated by AI CTO Executive Briefing Engine — CORE-010_  \n"
            f"_Briefing ID: {b.briefing_id} | Version: {b.schema_version}_"
        )
