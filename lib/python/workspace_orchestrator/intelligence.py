"""
Workspace Orchestrator — Intelligence Layer
CORE-012

WorkspaceHealthEngine:          computes aggregated workspace health
WorkspacePriorityEngine:        determines next recommended repository / work item
WorkspaceRiskAnalyzer:          detects workspace-level risks
WorkspaceRecommendationEngine:  produces evidence-based workspace recommendations
"""

from typing import Any, Dict, List, Tuple

from .models import (
    HEALTH_CRITICAL,
    HEALTH_DEGRADED,
    HEALTH_HEALTHY,
    HEALTH_UNKNOWN,
    RISK_CRITICAL,
    RISK_HIGH,
    RISK_LOW,
    RISK_MEDIUM,
    STATUS_BLOCKED,
    STATUS_COMPLIANT,
    STATUS_MISSING,
    STATUS_PARTIAL,
    WorkspaceDependencyEdge,
    WorkspaceHealth,
    WorkspacePriority,
    WorkspaceRecommendation,
    WorkspaceRepository,
    WorkspaceRisk,
)


class WorkspaceHealthEngine:
    """
    Computes aggregated health across all workspace repositories.

    Derives each dimension (architecture, canonical, development, runtime,
    executive, owner) from the individual repository models.
    """

    def compute(self, repositories: List[WorkspaceRepository]) -> WorkspaceHealth:
        if not repositories:
            return WorkspaceHealth(
                overall_health=HEALTH_UNKNOWN,
                repository_health=HEALTH_UNKNOWN,
                architecture_health=HEALTH_UNKNOWN,
                canonical_health=HEALTH_UNKNOWN,
                development_health=HEALTH_UNKNOWN,
                runtime_health=HEALTH_UNKNOWN,
                executive_health=HEALTH_UNKNOWN,
                owner_health=HEALTH_UNKNOWN,
                total_repositories=0,
            )

        total = len(repositories)
        healthy_count = sum(1 for r in repositories if r.repository_health == HEALTH_HEALTHY)
        degraded_count = sum(1 for r in repositories if r.repository_health == HEALTH_DEGRADED)
        critical_count = sum(1 for r in repositories if r.repository_health == HEALTH_CRITICAL)
        unknown_count = total - healthy_count - degraded_count - critical_count

        overall_readiness = (
            sum(r.readiness for r in repositories) / total if total else 0.0
        )
        average_priority = (
            sum(r.priority for r in repositories) / total if total else 5.0
        )

        repo_health = self._aggregate_health(healthy_count, degraded_count, critical_count, total)
        canonical_health = self._canonical_health(repositories)
        dev_health = self._development_health(repositories)
        runtime_health = self._runtime_health(repositories)
        exec_health = self._executive_health(overall_readiness)
        owner_health = self._owner_health(repositories)
        arch_health = self._architecture_health(repositories)
        overall = self._overall_health(
            healthy_count, degraded_count, critical_count, total, overall_readiness
        )

        return WorkspaceHealth(
            overall_health=overall,
            repository_health=repo_health,
            architecture_health=arch_health,
            canonical_health=canonical_health,
            development_health=dev_health,
            runtime_health=runtime_health,
            executive_health=exec_health,
            owner_health=owner_health,
            healthy_count=healthy_count,
            degraded_count=degraded_count,
            critical_count=critical_count,
            unknown_count=unknown_count,
            total_repositories=total,
            overall_readiness=overall_readiness,
            average_priority=average_priority,
        )

    # ------------------------------------------------------------------
    # Dimension helpers
    # ------------------------------------------------------------------

    def _aggregate_health(
        self, healthy: int, degraded: int, critical: int, total: int
    ) -> str:
        if total == 0:
            return HEALTH_UNKNOWN
        if critical > 0:
            return HEALTH_DEGRADED if critical / total < 0.5 else HEALTH_CRITICAL
        if degraded > total / 2:
            return HEALTH_DEGRADED
        return HEALTH_HEALTHY

    def _overall_health(
        self,
        healthy: int,
        degraded: int,
        critical: int,
        total: int,
        readiness: float,
    ) -> str:
        if total == 0:
            return HEALTH_UNKNOWN
        if critical / max(1, total) > 0.3 or readiness < 40:
            return HEALTH_CRITICAL
        if degraded / max(1, total) > 0.3 or readiness < 70:
            return HEALTH_DEGRADED
        return HEALTH_HEALTHY

    def _canonical_health(self, repositories: List[WorkspaceRepository]) -> str:
        statuses = [r.canonical_status for r in repositories]
        missing = statuses.count(STATUS_MISSING)
        partial = statuses.count(STATUS_PARTIAL)
        total = len(statuses)
        if missing / max(1, total) > 0.5:
            return HEALTH_CRITICAL
        if (missing + partial) / max(1, total) > 0.5:
            return HEALTH_DEGRADED
        return HEALTH_HEALTHY

    def _development_health(self, repositories: List[WorkspaceRepository]) -> str:
        blocked = sum(1 for r in repositories if r.development_state == STATUS_BLOCKED)
        total = len(repositories)
        if blocked / max(1, total) > 0.3:
            return HEALTH_DEGRADED
        return HEALTH_HEALTHY

    def _runtime_health(self, repositories: List[WorkspaceRepository]) -> str:
        critical = sum(1 for r in repositories if r.runtime_status == HEALTH_CRITICAL)
        degraded = sum(1 for r in repositories if r.runtime_status == HEALTH_DEGRADED)
        total = len(repositories)
        if critical / max(1, total) > 0.3:
            return HEALTH_CRITICAL
        if (critical + degraded) / max(1, total) > 0.5:
            return HEALTH_DEGRADED
        return HEALTH_HEALTHY

    def _executive_health(self, overall_readiness: float) -> str:
        if overall_readiness >= 80:
            return HEALTH_HEALTHY
        if overall_readiness >= 50:
            return HEALTH_DEGRADED
        return HEALTH_CRITICAL

    def _owner_health(self, repositories: List[WorkspaceRepository]) -> str:
        blocked = sum(1 for r in repositories if r.owner_status == STATUS_BLOCKED)
        total = len(repositories)
        if blocked / max(1, total) > 0.3:
            return HEALTH_DEGRADED
        return HEALTH_HEALTHY

    def _architecture_health(self, repositories: List[WorkspaceRepository]) -> str:
        # Architecture health correlates with canonical compliance and overall readiness
        avg_readiness = (
            sum(r.readiness for r in repositories) / len(repositories)
            if repositories
            else 0.0
        )
        canonical_ok = sum(
            1 for r in repositories if r.canonical_status == STATUS_COMPLIANT
        )
        total = len(repositories)
        if avg_readiness >= 80 and canonical_ok / max(1, total) >= 0.8:
            return HEALTH_HEALTHY
        if avg_readiness < 50 or canonical_ok / max(1, total) < 0.4:
            return HEALTH_CRITICAL
        return HEALTH_DEGRADED


class WorkspacePriorityEngine:
    """
    Determines the recommended order in which repositories should be worked on.

    The Owner-first workflow:  one repository at a time, fully evidence-based.
    """

    def rank(
        self,
        repositories: List[WorkspaceRepository],
        dependencies: List[WorkspaceDependencyEdge],
    ) -> List[WorkspacePriority]:
        """Return repositories ranked by urgency with full next-action suggestions."""
        if not repositories:
            return []

        # Build dependency lookup: which repos block others
        blocking: Dict[str, List[str]] = {}
        for edge in dependencies:
            blocking.setdefault(edge.target, []).append(edge.source)

        # Sort by: risk_status > health > readiness > priority field
        _risk_order = {
            RISK_CRITICAL: 0,
            RISK_HIGH: 1,
            RISK_MEDIUM: 2,
            RISK_LOW: 3,
        }
        _health_order = {
            HEALTH_CRITICAL: 0,
            HEALTH_DEGRADED: 1,
            HEALTH_UNKNOWN: 2,
            HEALTH_HEALTHY: 3,
        }

        def sort_key(repo: WorkspaceRepository) -> Tuple:
            return (
                _risk_order.get(repo.risk_status, 9),
                _health_order.get(repo.repository_health, 9),
                -repo.readiness,
                repo.priority,
                repo.name,
            )

        sorted_repos = sorted(repositories, key=sort_key)

        priorities = []
        for rank, repo in enumerate(sorted_repos, start=1):
            blocking_deps = blocking.get(repo.name, [])
            reason = self._build_reason(repo)
            impact = self._build_impact(repo)
            confidence = self._compute_confidence(repo)
            effort = self._estimate_effort(repo)

            priorities.append(WorkspacePriority(
                rank=rank,
                repository=repo.name,
                reason=reason,
                expected_impact=impact,
                confidence=confidence,
                required_effort=effort,
                blocking_dependencies=tuple(blocking_deps),
                suggested_next_milestone=repo.current_milestone or "",
                suggested_next_epic=repo.current_epic or "",
                suggested_next_issue=repo.current_issue or "",
                suggested_next_batch=repo.current_batch or "",
                suggested_next_pr=repo.current_pull_request or "",
            ))

        return priorities

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _build_reason(self, repo: WorkspaceRepository) -> str:
        parts = []
        if repo.repository_health == HEALTH_CRITICAL:
            parts.append("repository is in critical health")
        elif repo.repository_health == HEALTH_DEGRADED:
            parts.append("repository health is degraded")
        if repo.risk_status in (RISK_CRITICAL, RISK_HIGH):
            parts.append(f"risk level is {repo.risk_status}")
        if repo.canonical_status == STATUS_MISSING:
            parts.append("canonical specifications are missing")
        elif repo.canonical_status == STATUS_PARTIAL:
            parts.append("canonical compliance is partial")
        if repo.development_state == STATUS_BLOCKED:
            parts.append("development is blocked")
        if not parts:
            parts.append("scheduled for regular maintenance cycle")
        return "; ".join(parts).capitalize() + "."

    def _build_impact(self, repo: WorkspaceRepository) -> str:
        if repo.repository_health == HEALTH_CRITICAL:
            return "Restoring this repository will unblock dependent work and reduce overall risk."
        if repo.canonical_status in (STATUS_MISSING, STATUS_PARTIAL):
            return "Completing canonical compliance will improve architecture consistency across the workspace."
        return "Continuing development will increase workspace readiness and reduce technical debt."

    def _compute_confidence(self, repo: WorkspaceRepository) -> float:
        if repo.scan_scores:
            return 0.90
        return 0.60

    def _estimate_effort(self, repo: WorkspaceRepository) -> str:
        if repo.repository_health == HEALTH_CRITICAL or repo.canonical_status == STATUS_MISSING:
            return "high"
        if repo.repository_health == HEALTH_DEGRADED or repo.canonical_status == STATUS_PARTIAL:
            return "medium"
        return "low"


class WorkspaceRiskAnalyzer:
    """
    Detects workspace-level risks from repository models and dependency edges.
    """

    def analyze(
        self,
        repositories: List[WorkspaceRepository],
        dependencies: List[WorkspaceDependencyEdge],
        cycles: List[List[str]],
    ) -> List[WorkspaceRisk]:
        risks: List[WorkspaceRisk] = []
        counter = [0]

        def next_id() -> str:
            counter[0] += 1
            return f"WRISK-{counter[0]:03d}"

        risks.extend(self._critical_health_risks(next_id, repositories))
        risks.extend(self._canonical_drift_risks(next_id, repositories))
        risks.extend(self._blocked_repository_risks(next_id, repositories))
        risks.extend(self._dependency_cycle_risks(next_id, cycles))
        risks.extend(self._low_readiness_risks(next_id, repositories))
        risks.extend(self._isolated_repository_risks(next_id, repositories, dependencies))

        # Sort: critical first, then high, medium, low
        order = {RISK_CRITICAL: 0, RISK_HIGH: 1, RISK_MEDIUM: 2, RISK_LOW: 3}
        return sorted(risks, key=lambda r: (order.get(r.severity, 9), r.id))

    def _critical_health_risks(
        self, next_id, repositories: List[WorkspaceRepository]
    ) -> List[WorkspaceRisk]:
        critical = [r for r in repositories if r.repository_health == HEALTH_CRITICAL]
        if not critical:
            return []
        return [WorkspaceRisk(
            id=next_id(),
            category="health",
            severity=RISK_CRITICAL,
            title="Critical repository health detected",
            description=(
                f"{len(critical)} repository/repositories are in critical health: "
                + ", ".join(r.name for r in critical)
            ),
            affected_repositories=tuple(r.name for r in critical),
            remediation="Run 'ai workspace --refresh' to re-scan and identify root causes. "
                        "Review canonical compliance and runtime status for each affected repository.",
            evidence=tuple(
                f"{r.name}: readiness={r.readiness:.0f}%" for r in critical
            ),
        )]

    def _canonical_drift_risks(
        self, next_id, repositories: List[WorkspaceRepository]
    ) -> List[WorkspaceRisk]:
        missing = [r for r in repositories if r.canonical_status == STATUS_MISSING]
        partial = [r for r in repositories if r.canonical_status == STATUS_PARTIAL]
        risks = []
        if missing:
            risks.append(WorkspaceRisk(
                id=next_id(),
                category="canonical_drift",
                severity=RISK_HIGH,
                title="Missing canonical specifications",
                description=(
                    f"{len(missing)} repositories have no canonical specifications detected."
                ),
                affected_repositories=tuple(r.name for r in missing),
                remediation="Implement canonical CORE specifications for each affected repository.",
                evidence=tuple(f"{r.name}: canonical_status=missing" for r in missing),
            ))
        if partial:
            risks.append(WorkspaceRisk(
                id=next_id(),
                category="canonical_drift",
                severity=RISK_MEDIUM,
                title="Partial canonical compliance",
                description=(
                    f"{len(partial)} repositories have partial canonical compliance."
                ),
                affected_repositories=tuple(r.name for r in partial),
                remediation="Complete outstanding canonical CORE specifications.",
                evidence=tuple(f"{r.name}: canonical_status=partial" for r in partial),
            ))
        return risks

    def _blocked_repository_risks(
        self, next_id, repositories: List[WorkspaceRepository]
    ) -> List[WorkspaceRisk]:
        blocked = [r for r in repositories if r.development_state == STATUS_BLOCKED]
        if not blocked:
            return []
        return [WorkspaceRisk(
            id=next_id(),
            category="progress",
            severity=RISK_HIGH,
            title="Blocked repository development",
            description=f"{len(blocked)} repositories have blocked development state.",
            affected_repositories=tuple(r.name for r in blocked),
            remediation="Identify and resolve blocking dependencies. Review current issues and PRs.",
            evidence=tuple(f"{r.name}: development_state=blocked" for r in blocked),
        )]

    def _dependency_cycle_risks(
        self, next_id, cycles: List[List[str]]
    ) -> List[WorkspaceRisk]:
        if not cycles:
            return []
        return [WorkspaceRisk(
            id=next_id(),
            category="dependency",
            severity=RISK_HIGH,
            title="Dependency cycle detected across workspace repositories",
            description=(
                f"{len(cycles)} circular dependency cycle(s) detected across repositories."
            ),
            affected_repositories=tuple(sorted({repo for cycle in cycles for repo in cycle})),
            remediation="Refactor dependencies to eliminate cycles. Consider introducing a shared library.",
            evidence=tuple(
                " -> ".join(cycle + [cycle[0]]) for cycle in cycles[:5]
            ),
        )]

    def _low_readiness_risks(
        self, next_id, repositories: List[WorkspaceRepository]
    ) -> List[WorkspaceRisk]:
        low = [r for r in repositories if 0 < r.readiness < 50]
        if not low:
            return []
        return [WorkspaceRisk(
            id=next_id(),
            category="health",
            severity=RISK_MEDIUM,
            title="Low AI CTO readiness in multiple repositories",
            description=f"{len(low)} repositories have readiness below 50%.",
            affected_repositories=tuple(r.name for r in low),
            remediation="Run 'ai inspect --execution-model' on each repository and implement missing components.",
            evidence=tuple(f"{r.name}: readiness={r.readiness:.0f}%" for r in low),
        )]

    def _isolated_repository_risks(
        self,
        next_id,
        repositories: List[WorkspaceRepository],
        dependencies: List[WorkspaceDependencyEdge],
    ) -> List[WorkspaceRisk]:
        if len(repositories) <= 1:
            return []
        connected = {e.source for e in dependencies} | {e.target for e in dependencies}
        isolated = [r for r in repositories if r.name not in connected]
        if not isolated:
            return []
        return [WorkspaceRisk(
            id=next_id(),
            category="architecture",
            severity=RISK_LOW,
            title="Isolated repositories with no detected cross-repo connections",
            description=(
                f"{len(isolated)} repositories have no detected connections to other workspace repositories."
            ),
            affected_repositories=tuple(r.name for r in isolated),
            remediation="Review repository purpose and declare dependencies if connections exist.",
            evidence=tuple(f"{r.name}: no dependency edges" for r in isolated),
        )]


class WorkspaceRecommendationEngine:
    """
    Produces evidence-based workspace recommendations for the owner.

    All recommendations are derived from existing repository models.
    No analysis is duplicated.
    """

    def generate(
        self,
        repositories: List[WorkspaceRepository],
        health: WorkspaceHealth,
        risks: List[WorkspaceRisk],
        priorities: List[WorkspacePriority],
    ) -> List[WorkspaceRecommendation]:
        recs: List[WorkspaceRecommendation] = []
        counter = [0]

        def next_id() -> str:
            counter[0] += 1
            return f"WREC-{counter[0]:03d}"

        recs.extend(self._next_repository_recommendation(next_id, priorities))
        recs.extend(self._critical_risk_recommendations(next_id, risks))
        recs.extend(self._canonical_compliance_recommendations(next_id, repositories))
        recs.extend(self._workspace_health_recommendation(next_id, health))

        if not recs:
            recs.append(WorkspaceRecommendation(
                id=next_id(),
                title="Workspace is healthy — continue planned development",
                description="All repositories are in good health. Continue executing the development roadmap.",
                priority=RISK_LOW,
                impact="Sustained development velocity and architecture quality.",
                confidence=0.95,
                required_effort="low",
                target_repository="",
                reasoning="No critical issues detected.",
                evidence=("Overall workspace health is healthy",),
            ))

        # Sort: critical > high > medium > low
        order = {RISK_CRITICAL: 0, RISK_HIGH: 1, RISK_MEDIUM: 2, RISK_LOW: 3}
        return sorted(recs, key=lambda r: (order.get(r.priority, 9), r.id))

    # ------------------------------------------------------------------

    def _next_repository_recommendation(
        self, next_id, priorities: List[WorkspacePriority]
    ) -> List[WorkspaceRecommendation]:
        if not priorities:
            return []
        top = priorities[0]
        return [WorkspaceRecommendation(
            id=next_id(),
            title=f"Work on repository: {top.repository}",
            description=(
                f"Start with {top.repository} — {top.reason} "
                f"Suggested: milestone='{top.suggested_next_milestone}', "
                f"epic='{top.suggested_next_epic}', issue='{top.suggested_next_issue}'."
            ),
            priority=RISK_HIGH,
            impact=top.expected_impact,
            confidence=top.confidence,
            required_effort=top.required_effort,
            target_repository=top.repository,
            dependencies=top.blocking_dependencies,
            reasoning=top.reason,
            evidence=(f"Ranked #{top.rank} in workspace priority list",),
        )]

    def _critical_risk_recommendations(
        self, next_id, risks: List[WorkspaceRisk]
    ) -> List[WorkspaceRecommendation]:
        critical = [r for r in risks if r.severity == RISK_CRITICAL]
        recs = []
        for risk in critical:
            recs.append(WorkspaceRecommendation(
                id=next_id(),
                title=f"Resolve critical risk: {risk.title}",
                description=risk.description + " " + risk.remediation,
                priority=RISK_CRITICAL,
                impact="Eliminating this risk will restore workspace stability.",
                confidence=0.95,
                required_effort="high",
                target_repository=(
                    risk.affected_repositories[0] if risk.affected_repositories else ""
                ),
                reasoning=risk.description,
                evidence=risk.evidence,
            ))
        return recs

    def _canonical_compliance_recommendations(
        self, next_id, repositories: List[WorkspaceRepository]
    ) -> List[WorkspaceRecommendation]:
        missing = [r for r in repositories if r.canonical_status == STATUS_MISSING]
        if not missing:
            return []
        return [WorkspaceRecommendation(
            id=next_id(),
            title="Implement missing canonical CORE specifications",
            description=(
                f"{len(missing)} repositories lack canonical specifications. "
                "Run 'ai inspect' on each and implement the recommended CORE specs."
            ),
            priority=RISK_HIGH,
            impact="Canonical compliance unlocks the full AI CTO intelligence layer.",
            confidence=0.90,
            required_effort="medium",
            target_repository=missing[0].name,
            reasoning="Missing canonical specifications prevent AI CTO from reasoning about these repositories.",
            evidence=tuple(f"{r.name}: canonical_status=missing" for r in missing[:5]),
        )]

    def _workspace_health_recommendation(
        self, next_id, health: WorkspaceHealth
    ) -> List[WorkspaceRecommendation]:
        if health.overall_health == HEALTH_HEALTHY:
            return []
        severity = RISK_CRITICAL if health.overall_health == HEALTH_CRITICAL else RISK_HIGH
        return [WorkspaceRecommendation(
            id=next_id(),
            title=f"Improve overall workspace health (current: {health.overall_health})",
            description=(
                f"Workspace readiness is {health.overall_readiness:.0f}%. "
                f"Critical: {health.critical_count}, Degraded: {health.degraded_count}, "
                f"Healthy: {health.healthy_count} out of {health.total_repositories}."
            ),
            priority=severity,
            impact="Increasing workspace health enables faster development and reduces future rework.",
            confidence=0.85,
            required_effort="medium",
            target_repository="",
            reasoning=f"Overall workspace health is {health.overall_health}.",
            evidence=(
                f"overall_readiness={health.overall_readiness:.0f}%",
                f"critical_count={health.critical_count}",
                f"degraded_count={health.degraded_count}",
            ),
        )]
