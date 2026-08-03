"""
Workspace Orchestrator — Dashboard Generator
CORE-012

WorkspaceExecutiveDashboard: produces a structured dashboard dict.
WorkspaceReportGenerator:    renders the markdown AI_CTO_WORKSPACE_DASHBOARD.md.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import (
    HEALTH_HEALTHY,
    WorkspaceDependencyEdge,
    WorkspaceHealth,
    WorkspacePriority,
    WorkspaceRecommendation,
    WorkspaceRelationship,
    WorkspaceRepository,
    WorkspaceRisk,
    WorkspaceScanResult,
    WorkspaceStatistics,
)


class WorkspaceExecutiveDashboard:
    """
    Produces a structured dashboard dict from a workspace scan result.

    The dashboard dict is serialisable and contains everything needed
    to render the markdown report without additional I/O.
    """

    def build(
        self,
        result: WorkspaceScanResult,
        statistics: WorkspaceStatistics,
    ) -> Dict[str, Any]:
        health = result.health
        priorities = result.priorities
        recommendations = result.recommendations
        risks = result.risks
        repositories = result.repositories

        top_priority = priorities[0] if priorities else None
        critical_risks = [r for r in risks if r.severity == "critical"]
        high_risks = [r for r in risks if r.severity == "high"]
        blocked_repos = [r for r in repositories if r.development_state == "blocked"]

        return {
            "generated_at": result.generated_at,
            "workspace_id": result.workspace_id,
            "workspace_root": result.workspace_root,
            "executive_summary": self._executive_summary(result, statistics),
            "workspace_summary": {
                "total_repositories": result.total_repositories,
                "scanned_repositories": result.scanned_repositories,
                "failed_repositories": result.failed_repositories,
                "overall_health": health.overall_health,
                "overall_readiness": round(health.overall_readiness, 2),
                "healthy_count": health.healthy_count,
                "degraded_count": health.degraded_count,
                "critical_count": health.critical_count,
            },
            "health": health.to_dict(),
            "statistics": statistics.to_dict(),
            "repository_ranking": [
                {
                    "rank": p.rank,
                    "repository": p.repository,
                    "reason": p.reason,
                    "confidence": p.confidence,
                }
                for p in priorities[:10]
            ],
            "current_priorities": [p.to_dict() for p in priorities[:5]],
            "current_risks": [r.to_dict() for r in risks[:10]],
            "current_recommendations": [r.to_dict() for r in recommendations[:5]],
            "blocked_work": [r.to_dict() for r in blocked_repos],
            "pending_decisions": self._pending_decisions(repositories, risks),
            "suggested_next_repository": top_priority.repository if top_priority else "",
            "suggested_next_milestone": top_priority.suggested_next_milestone if top_priority else "",
            "suggested_next_epic": top_priority.suggested_next_epic if top_priority else "",
            "suggested_next_issue": top_priority.suggested_next_issue if top_priority else "",
            "suggested_next_batch": top_priority.suggested_next_batch if top_priority else "",
            "suggested_next_pr": top_priority.suggested_next_pr if top_priority else "",
            "suggested_next_core": self._suggest_next_core(repositories),
            "estimated_overall_progress": round(health.overall_readiness, 2),
            "repository_readiness": {
                r.name: round(r.readiness, 2) for r in repositories
            },
            "repository_health": {
                r.name: r.repository_health for r in repositories
            },
        }

    # ------------------------------------------------------------------

    def _executive_summary(
        self, result: WorkspaceScanResult, statistics: WorkspaceStatistics
    ) -> str:
        health = result.health
        n = result.total_repositories
        scanned = result.scanned_repositories
        readiness = health.overall_readiness
        status = health.overall_health.upper()
        return (
            f"Workspace contains {n} repository/repositories "
            f"({scanned} scanned, {result.failed_repositories} failed). "
            f"Overall workspace health: {status}. "
            f"Aggregate AI CTO readiness: {readiness:.0f}%. "
            f"Critical risks: {statistics.critical_risks}. "
            f"Total recommendations: {statistics.total_recommendations}."
        )

    def _pending_decisions(
        self,
        repositories: List[WorkspaceRepository],
        risks: List[WorkspaceRisk],
    ) -> List[Dict[str, str]]:
        decisions = []
        critical_risks = [r for r in risks if r.severity == "critical"]
        for risk in critical_risks[:3]:
            decisions.append({
                "id": f"DEC-{risk.id}",
                "title": f"Decide remediation for: {risk.title}",
                "urgency": "critical",
                "context": risk.remediation,
            })
        return decisions

    def _suggest_next_core(self, repositories: List[WorkspaceRepository]) -> str:
        """Suggest the next CORE specification to implement."""
        # Look for any current recommendation that mentions CORE-NNN
        import re
        for repo in sorted(repositories, key=lambda r: r.priority):
            text = repo.current_recommendation + " " + repo.current_batch
            m = re.search(r"CORE-\d+[A-Z]?", text)
            if m:
                return m.group(0)
        return ""


class WorkspaceReportGenerator:
    """
    Renders the AI_CTO_WORKSPACE_DASHBOARD.md markdown report from a
    dashboard dict.
    """

    def generate(self, dashboard: Dict[str, Any]) -> str:
        lines = []
        _add = lines.append

        _add("# AI CTO Workspace Dashboard")
        _add("")
        _add(f"> Generated: {dashboard.get('generated_at', '')}")
        _add(f"> Workspace: `{dashboard.get('workspace_root', '')}`")
        _add("")

        # Executive Summary
        _add("## Executive Summary")
        _add("")
        _add(dashboard.get("executive_summary", ""))
        _add("")

        # Workspace Summary
        summary = dashboard.get("workspace_summary", {})
        _add("## Workspace Summary")
        _add("")
        _add(f"| Metric | Value |")
        _add(f"|--------|-------|")
        _add(f"| Total Repositories | {summary.get('total_repositories', 0)} |")
        _add(f"| Scanned | {summary.get('scanned_repositories', 0)} |")
        _add(f"| Failed | {summary.get('failed_repositories', 0)} |")
        _add(f"| Overall Health | **{summary.get('overall_health', 'unknown').upper()}** |")
        _add(f"| Overall Readiness | {summary.get('overall_readiness', 0):.1f}% |")
        _add(f"| Healthy | {summary.get('healthy_count', 0)} |")
        _add(f"| Degraded | {summary.get('degraded_count', 0)} |")
        _add(f"| Critical | {summary.get('critical_count', 0)} |")
        _add("")

        # Health Dimensions
        health = dashboard.get("health", {})
        _add("## Workspace Health")
        _add("")
        _add("| Dimension | Status |")
        _add("|-----------|--------|")
        for dim in [
            "overall_health", "repository_health", "architecture_health",
            "canonical_health", "development_health", "runtime_health",
            "executive_health", "owner_health",
        ]:
            label = dim.replace("_", " ").title()
            value = health.get(dim, "unknown").upper()
            _add(f"| {label} | **{value}** |")
        _add("")

        # Repository Ranking
        ranking = dashboard.get("repository_ranking", [])
        if ranking:
            _add("## Repository Ranking")
            _add("")
            _add("| Rank | Repository | Reason | Confidence |")
            _add("|------|------------|--------|------------|")
            for item in ranking:
                reason = item.get("reason", "")[:80].rstrip(".")
                conf = f"{item.get('confidence', 0) * 100:.0f}%"
                _add(f"| {item['rank']} | **{item['repository']}** | {reason} | {conf} |")
            _add("")

        # Repository Readiness
        readiness = dashboard.get("repository_readiness", {})
        repo_health = dashboard.get("repository_health", {})
        if readiness:
            _add("## Repository Readiness")
            _add("")
            _add("| Repository | Health | Readiness |")
            _add("|------------|--------|-----------|")
            for name in sorted(readiness.keys()):
                h = repo_health.get(name, "unknown").upper()
                r = f"{readiness[name]:.1f}%"
                _add(f"| {name} | **{h}** | {r} |")
            _add("")

        # Current Priorities
        priorities = dashboard.get("current_priorities", [])
        if priorities:
            _add("## Current Priorities")
            _add("")
            for p in priorities:
                _add(f"### #{p['rank']} — {p['repository']}")
                _add("")
                _add(f"**Reason:** {p.get('reason', '')}")
                _add("")
                _add(f"**Expected Impact:** {p.get('expected_impact', '')}")
                _add("")
                effort = p.get("required_effort", "")
                conf = f"{p.get('confidence', 0) * 100:.0f}%"
                _add(f"- Confidence: {conf}")
                _add(f"- Required Effort: {effort.title()}")
                if p.get("blocking_dependencies"):
                    _add(f"- Blocking Dependencies: {', '.join(p['blocking_dependencies'])}")
                if p.get("suggested_next_milestone"):
                    _add(f"- Next Milestone: {p['suggested_next_milestone']}")
                if p.get("suggested_next_issue"):
                    _add(f"- Next Issue: {p['suggested_next_issue']}")
                if p.get("suggested_next_batch"):
                    _add(f"- Next Batch: {p['suggested_next_batch']}")
                _add("")

        # Current Risks
        risks = dashboard.get("current_risks", [])
        if risks:
            _add("## Current Risks")
            _add("")
            for risk in risks:
                sev = risk.get("severity", "").upper()
                _add(f"### [{sev}] {risk.get('title', '')}")
                _add("")
                _add(risk.get("description", ""))
                _add("")
                if risk.get("affected_repositories"):
                    _add(f"**Affected:** {', '.join(risk['affected_repositories'])}")
                    _add("")
                _add(f"**Remediation:** {risk.get('remediation', '')}")
                _add("")

        # Current Recommendations
        recs = dashboard.get("current_recommendations", [])
        if recs:
            _add("## Current Recommendations")
            _add("")
            for rec in recs:
                pri = rec.get("priority", "").upper()
                _add(f"### [{pri}] {rec.get('title', '')}")
                _add("")
                _add(rec.get("description", ""))
                _add("")
                conf = f"{rec.get('confidence', 0) * 100:.0f}%"
                _add(f"- Confidence: {conf}")
                _add(f"- Required Effort: {rec.get('required_effort', '').title()}")
                if rec.get("target_repository"):
                    _add(f"- Target Repository: {rec['target_repository']}")
                _add("")

        # Blocked Work
        blocked = dashboard.get("blocked_work", [])
        if blocked:
            _add("## Blocked Work")
            _add("")
            for repo in blocked:
                _add(f"- **{repo.get('name', '')}** — {repo.get('development_state', '')}")
            _add("")

        # Pending Decisions
        decisions = dashboard.get("pending_decisions", [])
        if decisions:
            _add("## Pending Decisions")
            _add("")
            for dec in decisions:
                urgency = dec.get("urgency", "").upper()
                _add(f"### [{urgency}] {dec.get('title', '')}")
                _add("")
                _add(dec.get("context", ""))
                _add("")

        # Suggested Next Actions
        _add("## Suggested Next Actions")
        _add("")
        next_repo = dashboard.get("suggested_next_repository", "")
        next_core = dashboard.get("suggested_next_core", "")
        next_ms = dashboard.get("suggested_next_milestone", "")
        next_epic = dashboard.get("suggested_next_epic", "")
        next_issue = dashboard.get("suggested_next_issue", "")
        next_batch = dashboard.get("suggested_next_batch", "")
        next_pr = dashboard.get("suggested_next_pr", "")
        progress = dashboard.get("estimated_overall_progress", 0)

        _add(f"| Action | Value |")
        _add(f"|--------|-------|")
        _add(f"| Suggested Next Repository | **{next_repo or '—'}** |")
        if next_core:
            _add(f"| Suggested Next CORE | **{next_core}** |")
        if next_ms:
            _add(f"| Suggested Next Milestone | {next_ms} |")
        if next_epic:
            _add(f"| Suggested Next Epic | {next_epic} |")
        if next_issue:
            _add(f"| Suggested Next Issue | {next_issue} |")
        if next_batch:
            _add(f"| Suggested Next Batch | {next_batch} |")
        if next_pr:
            _add(f"| Suggested Next PR | {next_pr} |")
        _add(f"| Estimated Overall Progress | **{progress:.1f}%** |")
        _add("")

        _add("---")
        _add("")
        _add("*Generated by AI CTO Workspace Orchestrator (CORE-012)*")
        _add("")

        return "\n".join(lines)

    def write(self, markdown: str, output_dir: str) -> str:
        """Write the dashboard markdown to output_dir/AI_CTO_WORKSPACE_DASHBOARD.md."""
        path = Path(output_dir) / "AI_CTO_WORKSPACE_DASHBOARD.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown, encoding="utf-8")
        return str(path)
