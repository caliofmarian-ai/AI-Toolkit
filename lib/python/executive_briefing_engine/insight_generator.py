"""
Executive Briefing Engine — Insight Generator
CORE-010F

Generates cross-intelligence insights from aggregated snapshot data.
Insights are narrative summaries used in the executive briefing sections.
"""

from typing import Any, Dict, List, Mapping


class ExecutiveInsightGenerator:
    """
    Generates narrative insights for each briefing health dimension.

    Each insight method returns a human-readable string derived from
    intelligence data.  No analysis is re-run.
    """

    # ------------------------------------------------------------------
    # Health dimension insights
    # ------------------------------------------------------------------

    def architecture_health(self, snapshot: Mapping[str, Any]) -> str:
        """Derive architecture health label and description."""
        arch = (
            snapshot
            .get("integrations", {})
            .get("semantic_repository_intelligence", {})
            .get("analysis", {})
            .get("architecture_graph", {})
        )
        arch_risks = arch.get("risks", [])
        hotspots = arch.get("hotspots", [])
        node_count = int(arch.get("node_count", 0))

        if not node_count:
            return "unknown"

        if isinstance(arch_risks, list) and len(arch_risks) > 3:
            return "degraded"
        if isinstance(arch_risks, list) and arch_risks:
            return "warning"
        if isinstance(hotspots, list) and len(hotspots) > 5:
            return "warning"
        return "healthy"

    def canonical_health(self, snapshot: Mapping[str, Any]) -> str:
        """Derive canonical health label."""
        canon = snapshot.get("integrations", {}).get("canonical_intelligence", {})
        if not canon.get("available", True):
            return "unavailable"

        coverage = float(canon.get("overall_coverage", 100.0))
        drift = int(canon.get("drift_findings", 0))
        compliance = float(canon.get("overall_compliance", 100.0))

        if coverage < 50.0 or drift > 10:
            return "critical"
        if coverage < 80.0 or drift > 5 or compliance < 70.0:
            return "degraded"
        if coverage < 90.0 or drift > 0 or compliance < 90.0:
            return "warning"
        return "healthy"

    def development_health(self, snapshot: Mapping[str, Any]) -> str:
        """Derive development health label."""
        state = snapshot.get("state", {})
        workspace = state.get("workspace_state", {})
        execution = state.get("execution_state", {})

        blocked_tasks = workspace.get("blocked_tasks", [])
        failed_jobs = execution.get("failed_jobs", [])
        running_jobs = execution.get("running_jobs", [])

        n_blocked = len(blocked_tasks) if isinstance(blocked_tasks, list) else 0
        n_failed = len(failed_jobs) if isinstance(failed_jobs, list) else 0
        n_running = len(running_jobs) if isinstance(running_jobs, list) else 0

        if n_failed > 0:
            return "degraded"
        if n_blocked > 3:
            return "warning"
        if n_blocked > 0:
            return "warning"
        if n_running > 0:
            return "active"
        return "healthy"

    def repository_health(self, snapshot: Mapping[str, Any]) -> str:
        """Derive repository health label."""
        integrity = snapshot.get("integrity", {})
        state = snapshot.get("state", {})
        integrity_report = state.get("integrity_report", {})
        failed_checks = integrity_report.get("failed_checks", [])

        repo_stats = (
            snapshot
            .get("integrations", {})
            .get("repository_intelligence", {})
            .get("statistics", {})
        )
        total_files = int(repo_stats.get("files", repo_stats.get("total_files", 0)))

        if isinstance(failed_checks, list) and failed_checks:
            return "degraded"
        if not integrity.get("state_sha256"):
            return "warning"
        if total_files == 0:
            return "unknown"
        return "healthy"

    def runtime_health(self, snapshot: Mapping[str, Any]) -> str:
        """Derive runtime health label."""
        exec_intel = snapshot.get("integrations", {}).get("executable_repository_intelligence", {})
        failed_jobs = int(exec_intel.get("failed_jobs", 0))
        running_jobs = int(exec_intel.get("running_jobs", 0))
        completed_jobs = int(exec_intel.get("completed_jobs", 0))

        if failed_jobs > 0:
            return "degraded"
        if running_jobs > 0:
            return "active"
        if completed_jobs > 0:
            return "healthy"

        # Fall back to executable repository map
        exec_file_count = int(exec_intel.get("executable_file_count", 0))
        if exec_file_count > 0:
            return "healthy"

        return "unknown"

    # ------------------------------------------------------------------
    # Executive summary
    # ------------------------------------------------------------------

    def executive_summary(
        self,
        snapshot: Mapping[str, Any],
        arch_health: str,
        canonical_health: str,
        dev_health: str,
        repo_health: str,
        runtime_health: str,
        risk_count: int,
        rec_count: int,
    ) -> str:
        """Generate the executive summary paragraph."""
        repo_name = (
            snapshot
            .get("integrations", {})
            .get("repository_intelligence", {})
            .get("statistics", {})
            .get("repository_name", "")
        )
        if not repo_name:
            repo_name = str(
                snapshot.get("state", {})
                .get("repository_state", {})
                .get("repository", "repository")
            )

        health_labels = [arch_health, canonical_health, dev_health, repo_health, runtime_health]
        critical_count = health_labels.count("critical") + health_labels.count("degraded")
        warning_count = health_labels.count("warning")

        if critical_count >= 2:
            overall = "requires immediate attention"
        elif critical_count == 1 or warning_count >= 2:
            overall = "has areas requiring attention"
        elif warning_count == 1:
            overall = "is generally healthy with minor issues"
        else:
            overall = "is healthy"

        lines = [
            f"The {repo_name} repository {overall}.",
            f"Architecture health: {arch_health}. "
            f"Canonical health: {canonical_health}. "
            f"Development health: {dev_health}.",
            f"Repository health: {repo_health}. "
            f"Runtime health: {runtime_health}.",
        ]

        if risk_count > 0:
            lines.append(f"{risk_count} risk(s) identified.")
        if rec_count > 0:
            lines.append(f"{rec_count} recommendation(s) generated.")

        return "  ".join(lines)

    # ------------------------------------------------------------------
    # Suggested next items
    # ------------------------------------------------------------------

    def suggested_next_core(self, snapshot: Mapping[str, Any]) -> str:
        """Derive next CORE suggestion from semantic intelligence."""
        return (
            snapshot
            .get("integrations", {})
            .get("semantic_repository_intelligence", {})
            .get("analysis", {})
            .get("next_core", "")
        ) or ""

    def suggested_next_batch(self, snapshot: Mapping[str, Any]) -> str:
        """Derive next batch suggestion from planning state."""
        planning = snapshot.get("state", {}).get("planning_state", {})
        return str(planning.get("recommended_batch", "") or "")

    def suggested_next_pr(self, snapshot: Mapping[str, Any]) -> str:
        """Derive next PR suggestion from review state."""
        review = snapshot.get("state", {}).get("review_state", {})
        pending = review.get("pending_reviews", [])
        if isinstance(pending, list) and pending:
            return str(pending[0])
        open_prs = review.get("open_prs", [])
        if isinstance(open_prs, list) and open_prs:
            return str(open_prs[0])
        return ""

    def estimated_completion(self, snapshot: Mapping[str, Any]) -> str:
        """Derive estimated completion from planning state."""
        planning = snapshot.get("state", {}).get("planning_state", {})
        target = planning.get("target_completion", "") or planning.get("estimated_completion", "")
        if target:
            return str(target)

        canon = snapshot.get("integrations", {}).get("canonical_intelligence", {})
        batches = int(canon.get("batches", 0))
        coverage = float(canon.get("overall_coverage", 100.0))

        if batches == 0 and coverage >= 95.0:
            return "near completion"
        if batches <= 3:
            return "within current milestone"
        if batches <= 10:
            return "multiple sprints remaining"
        return "long-term roadmap"
