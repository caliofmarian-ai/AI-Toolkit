"""
Executive Briefing Engine — Risk Analyzer
CORE-010B

Detects executive-level risks from existing engine intelligence.
No analysis is duplicated — all data is consumed from inputs.
"""

from typing import Any, Dict, List, Mapping

from .models import (
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    RISK_ARCHITECTURE,
    RISK_BROKEN_DEPENDENCIES,
    RISK_CANONICAL_DRIFT,
    RISK_MISSING_COMPONENTS,
    RISK_REGRESSION,
    RISK_REPOSITORY_INTEGRITY,
    RISK_TECHNICAL_DEBT,
    SEVERITY_CRITICAL,
    SEVERITY_HIGH,
    SEVERITY_LOW,
    SEVERITY_MEDIUM,
    ExecutiveRisk,
)


class ExecutiveRiskAnalyzer:
    """
    Detects executive-level risks from existing intelligence data.

    Consumes snapshot produced by DevelopmentStateManager and derives risks
    from: architecture graphs, canonical drift findings, dependency graphs,
    integrity reports, and executable intelligence.  Never re-runs analysis.
    """

    def analyze(self, snapshot: Mapping[str, Any]) -> List[ExecutiveRisk]:
        """Return deduplicated, severity-sorted risk list from snapshot data."""
        risks: List[ExecutiveRisk] = []
        counter = [0]

        def next_id() -> str:
            counter[0] += 1
            return f"RISK-{counter[0]:03d}"

        integrations = snapshot.get("integrations", {})
        state = snapshot.get("state", {})
        integrity = snapshot.get("integrity", {})

        risks.extend(self._architecture_risks(next_id, integrations))
        risks.extend(self._canonical_drift_risks(next_id, integrations))
        risks.extend(self._missing_component_risks(next_id, integrations))
        risks.extend(self._broken_dependency_risks(next_id, integrations))
        risks.extend(self._repository_integrity_risks(next_id, integrity, state))
        risks.extend(self._regression_risks(next_id, integrations))
        risks.extend(self._technical_debt_risks(next_id, integrations))

        return self._sort_risks(risks)

    # ------------------------------------------------------------------
    # Architecture Risks
    # ------------------------------------------------------------------

    def _architecture_risks(
        self, next_id, integrations: Mapping[str, Any]
    ) -> List[ExecutiveRisk]:
        risks: List[ExecutiveRisk] = []
        arch = (
            integrations
            .get("semantic_repository_intelligence", {})
            .get("analysis", {})
            .get("architecture_graph", {})
        )
        arch_risks = arch.get("risks", [])
        hotspots = arch.get("hotspots", [])

        for item in arch_risks[:5]:
            description = item if isinstance(item, str) else str(item)
            risks.append(ExecutiveRisk(
                id=next_id(),
                category=RISK_ARCHITECTURE,
                severity=SEVERITY_HIGH,
                title="Architecture risk detected",
                description=description,
                evidence=(description,),
                affected_components=tuple(hotspots[:3]),
                remediation="Review architecture graph and resolve identified structural issues.",
            ))

        if len(hotspots) > 3:
            risks.append(ExecutiveRisk(
                id=next_id(),
                category=RISK_ARCHITECTURE,
                severity=SEVERITY_MEDIUM,
                title=f"High-coupling hotspots detected ({len(hotspots)})",
                description=(
                    f"{len(hotspots)} architecture hotspots indicate high coupling "
                    "that may impede future changes."
                ),
                evidence=tuple(hotspots[:5]),
                affected_components=tuple(hotspots[:5]),
                remediation="Decompose hotspot modules to reduce coupling and improve maintainability.",
            ))

        return risks

    # ------------------------------------------------------------------
    # Canonical Drift Risks
    # ------------------------------------------------------------------

    def _canonical_drift_risks(
        self, next_id, integrations: Mapping[str, Any]
    ) -> List[ExecutiveRisk]:
        risks: List[ExecutiveRisk] = []
        canon = integrations.get("canonical_intelligence", {})
        drift_count = canon.get("drift_findings", 0)
        coverage = float(canon.get("overall_coverage", 100.0))

        if drift_count > 0:
            severity = SEVERITY_CRITICAL if drift_count > 5 else SEVERITY_HIGH
            risks.append(ExecutiveRisk(
                id=next_id(),
                category=RISK_CANONICAL_DRIFT,
                severity=severity,
                title=f"Canonical drift detected ({drift_count} findings)",
                description=(
                    f"{drift_count} canonical drift findings indicate the implementation "
                    "has diverged from specification."
                ),
                evidence=(f"drift_findings={drift_count}",),
                affected_components=(),
                remediation="Run canonical intelligence pipeline and resolve all drift findings.",
            ))

        if coverage < 80.0:
            severity = SEVERITY_CRITICAL if coverage < 50.0 else SEVERITY_HIGH
            risks.append(ExecutiveRisk(
                id=next_id(),
                category=RISK_CANONICAL_DRIFT,
                severity=severity,
                title=f"Low canonical coverage ({coverage:.1f}%)",
                description=(
                    f"Overall canonical coverage is {coverage:.1f}%, "
                    "below the 80% target."
                ),
                evidence=(f"overall_coverage={coverage:.1f}%",),
                affected_components=(),
                remediation="Implement missing canonical specifications to raise coverage above 80%.",
            ))

        return risks

    # ------------------------------------------------------------------
    # Missing Component Risks
    # ------------------------------------------------------------------

    def _missing_component_risks(
        self, next_id, integrations: Mapping[str, Any]
    ) -> List[ExecutiveRisk]:
        risks: List[ExecutiveRisk] = []
        scanner = integrations.get("ai_cto_scanner", {})
        detection = scanner.get("detection", {})
        missing: List[str] = []

        for category, result in detection.items():
            if isinstance(result, dict):
                items = result.get("missing", []) or result.get("not_found", [])
                if isinstance(items, list):
                    for item in items:
                        missing.append(f"{category}: {item}")

        if missing:
            severity = SEVERITY_HIGH if len(missing) > 3 else SEVERITY_MEDIUM
            risks.append(ExecutiveRisk(
                id=next_id(),
                category=RISK_MISSING_COMPONENTS,
                severity=severity,
                title=f"Missing components detected ({len(missing)})",
                description=(
                    f"{len(missing)} required components are not present in the repository."
                ),
                evidence=tuple(missing[:5]),
                affected_components=tuple(missing[:5]),
                remediation="Implement missing components as indicated by the AI CTO scanner.",
            ))

        return risks

    # ------------------------------------------------------------------
    # Broken Dependency Risks
    # ------------------------------------------------------------------

    def _broken_dependency_risks(
        self, next_id, integrations: Mapping[str, Any]
    ) -> List[ExecutiveRisk]:
        risks: List[ExecutiveRisk] = []
        semantic = (
            integrations
            .get("semantic_repository_intelligence", {})
            .get("analysis", {})
        )
        dep_graph = semantic.get("dependency_graph", {})
        broken = dep_graph.get("broken", []) or dep_graph.get("unresolved", [])

        if isinstance(broken, list) and broken:
            risks.append(ExecutiveRisk(
                id=next_id(),
                category=RISK_BROKEN_DEPENDENCIES,
                severity=SEVERITY_HIGH,
                title=f"Broken dependencies detected ({len(broken)})",
                description=(
                    f"{len(broken)} broken or unresolved dependencies detected "
                    "in the dependency graph."
                ),
                evidence=tuple(str(b) for b in broken[:5]),
                affected_components=tuple(str(b) for b in broken[:3]),
                remediation="Resolve broken dependencies to prevent runtime failures.",
            ))

        return risks

    # ------------------------------------------------------------------
    # Repository Integrity Risks
    # ------------------------------------------------------------------

    def _repository_integrity_risks(
        self, next_id, integrity: Mapping[str, Any], state: Mapping[str, Any]
    ) -> List[ExecutiveRisk]:
        risks: List[ExecutiveRisk] = []
        state_sha = integrity.get("state_sha256", "")

        integrity_report = state.get("integrity_report", {})
        failed_checks = integrity_report.get("failed_checks", [])
        if isinstance(failed_checks, list) and failed_checks:
            risks.append(ExecutiveRisk(
                id=next_id(),
                category=RISK_REPOSITORY_INTEGRITY,
                severity=SEVERITY_CRITICAL,
                title=f"Repository integrity failures ({len(failed_checks)})",
                description=(
                    f"{len(failed_checks)} integrity checks failed for this repository."
                ),
                evidence=tuple(str(c) for c in failed_checks[:5]),
                affected_components=(),
                remediation="Investigate and resolve all integrity failures before proceeding.",
            ))

        if not state_sha:
            risks.append(ExecutiveRisk(
                id=next_id(),
                category=RISK_REPOSITORY_INTEGRITY,
                severity=SEVERITY_LOW,
                title="No integrity hash recorded",
                description="The development state has not been integrity-hashed yet.",
                evidence=("state_sha256 is absent",),
                affected_components=(),
                remediation="Save development state to generate integrity hash.",
            ))

        return risks

    # ------------------------------------------------------------------
    # Regression Risks
    # ------------------------------------------------------------------

    def _regression_risks(
        self, next_id, integrations: Mapping[str, Any]
    ) -> List[ExecutiveRisk]:
        risks: List[ExecutiveRisk] = []
        exec_intel = integrations.get("executable_repository_intelligence", {})
        failed_jobs = exec_intel.get("failed_jobs", 0)

        if isinstance(failed_jobs, int) and failed_jobs > 0:
            risks.append(ExecutiveRisk(
                id=next_id(),
                category=RISK_REGRESSION,
                severity=SEVERITY_HIGH,
                title=f"Execution failures detected ({failed_jobs} jobs)",
                description=(
                    f"{failed_jobs} execution jobs have failed, indicating potential regressions."
                ),
                evidence=(f"failed_jobs={failed_jobs}",),
                affected_components=(),
                remediation="Investigate failed execution jobs and resolve root causes.",
            ))

        complexity = (
            integrations
            .get("semantic_repository_intelligence", {})
            .get("analysis", {})
            .get("complexity", {})
        )
        total_files = int(complexity.get("total_files", 0))
        if total_files > 200:
            risks.append(ExecutiveRisk(
                id=next_id(),
                category=RISK_REGRESSION,
                severity=SEVERITY_MEDIUM,
                title=f"High codebase size increases regression risk ({total_files} files)",
                description=(
                    f"With {total_files} files, changes carry elevated regression risk "
                    "without comprehensive test coverage."
                ),
                evidence=(f"total_files={total_files}",),
                affected_components=(),
                remediation="Increase test coverage and enforce CI/CD gates for large changesets.",
            ))

        return risks

    # ------------------------------------------------------------------
    # Technical Debt Risks
    # ------------------------------------------------------------------

    def _technical_debt_risks(
        self, next_id, integrations: Mapping[str, Any]
    ) -> List[ExecutiveRisk]:
        risks: List[ExecutiveRisk] = []
        canon = integrations.get("canonical_intelligence", {})
        batches = int(canon.get("batches", 0))

        if batches > 5:
            risks.append(ExecutiveRisk(
                id=next_id(),
                category=RISK_TECHNICAL_DEBT,
                severity=SEVERITY_MEDIUM,
                title=f"Accumulated canonical batches indicate technical debt ({batches})",
                description=(
                    f"{batches} unresolved canonical batches represent accumulated "
                    "implementation debt."
                ),
                evidence=(f"pending_batches={batches}",),
                affected_components=(),
                remediation="Prioritize batch resolution to reduce canonical debt.",
            ))

        return risks

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    _SEVERITY_ORDER = {
        SEVERITY_CRITICAL: 0,
        SEVERITY_HIGH: 1,
        SEVERITY_MEDIUM: 2,
        SEVERITY_LOW: 3,
    }

    def _sort_risks(self, risks: List[ExecutiveRisk]) -> List[ExecutiveRisk]:
        return sorted(
            risks,
            key=lambda r: self._SEVERITY_ORDER.get(r.severity, 9),
        )
