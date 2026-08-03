"""
Self Evaluation Engine — Analyzers
CORE-016B

Delegates to existing CORE intelligence to produce objective,
evidence-based evaluation findings.

Does NOT duplicate:
  Repository discovery    (CORE-008A)
  Semantic intelligence   (CORE-008B)
  Canonical intelligence  (CORE-007)
  Planning               (CORE-014)
  Execution              (CORE-015)
  Workspace orchestration (CORE-012)
"""

from typing import Any, Dict, List, Mapping

from .models import (
    GATE_FAILED,
    GATE_MANUAL_REVIEW,
    GATE_PASS,
    GATE_WARNING,
    ArchitectureFinding,
    QualityScore,
    RegressionFinding,
)


# ---------------------------------------------------------------------------
# Canonical Compliance Analyzer
# ---------------------------------------------------------------------------

class CanonicalComplianceAnalyzer:
    """Evaluate canonical specification compliance via CORE-007."""

    def __init__(self, repository: str = ".") -> None:
        self.repository = repository

    def analyze(self) -> QualityScore:
        deviations: List[str] = []
        evidence: List[str] = []

        try:
            from python.canonical_intelligence.engine import (  # type: ignore[import]
                CanonicalIntelligenceEngine,
            )
            engine = CanonicalIntelligenceEngine(repository=self.repository)
            result = engine.analyze()
            deviations = [str(d) for d in result.get("deviations", [])]
            evidence.append(f"CORE-007: {len(deviations)} deviation(s) detected")
        except Exception as exc:  # noqa: BLE001
            evidence.append(f"CORE-007 unavailable: {exc}")

        score = max(0.0, 1.0 - len(deviations) * 0.1)
        gate = GATE_PASS if not deviations else (GATE_WARNING if score > 0.5 else GATE_FAILED)

        return QualityScore(
            dimension="canonical_compliance",
            score=round(score, 3),
            gate=gate,
            evidence=evidence,
            findings=deviations[:10],
            recommendation=(
                "Review canonical specification deviations." if deviations else "No action required."
            ),
        )


# ---------------------------------------------------------------------------
# Architecture Compliance Analyzer
# ---------------------------------------------------------------------------

class ArchitectureComplianceAnalyzer:
    """Detect architecture drift and layer violations via CORE-008B."""

    _KNOWN_PACKAGES = {
        "canonical_intelligence",
        "ai_cto_scanner",
        "semantic_repository_intelligence",
        "executable_repository_intelligence",
        "development_state_engine",
        "executive_briefing_engine",
        "workspace_orchestrator",
        "context_synchronization_engine",
        "autonomous_planning_engine",
        "autonomous_execution_engine",
        "self_evaluation_engine",
        "self_improvement_engine",
    }

    def __init__(self, repository: str = ".") -> None:
        self.repository = repository

    def analyze(self) -> tuple:
        """Return (QualityScore, List[ArchitectureFinding])."""
        findings: List[ArchitectureFinding] = []
        evidence: List[str] = []

        try:
            from python.semantic_repository_intelligence import (  # type: ignore[import]
                SemanticRepositoryEngine,
            )
            engine = SemanticRepositoryEngine(repository=self.repository, persist=False)
            result = engine.analyze()
            risks = result.get("architecture_graph", {}).get("risks", [])
            for risk in risks[:10]:
                findings.append(
                    ArchitectureFinding(
                        category="architecture_risk",
                        component=str(risk),
                        description=str(risk),
                        severity="medium",
                        evidence={"source": "CORE-008B"},
                    )
                )
            evidence.append(f"CORE-008B: {len(risks)} risk(s) detected")
        except Exception as exc:  # noqa: BLE001
            evidence.append(f"CORE-008B unavailable: {exc}")

        score = max(0.0, 1.0 - len(findings) * 0.05)
        gate = GATE_PASS if not findings else (GATE_WARNING if score > 0.5 else GATE_FAILED)

        quality_score = QualityScore(
            dimension="architecture_quality",
            score=round(score, 3),
            gate=gate,
            evidence=evidence,
            findings=[f.description for f in findings],
            recommendation=(
                "Investigate architecture risks." if findings else "Architecture looks clean."
            ),
        )
        return quality_score, findings


# ---------------------------------------------------------------------------
# Repository Compliance Analyzer
# ---------------------------------------------------------------------------

class RepositoryComplianceAnalyzer:
    """Evaluate repository health via CORE-008A."""

    def __init__(self, repository: str = ".") -> None:
        self.repository = repository

    def analyze(self) -> QualityScore:
        evidence: List[str] = []
        findings: List[str] = []
        score = 0.7

        try:
            from python.ai_cto_scanner import AICTOScannerEngine  # type: ignore[import]

            scanner = AICTOScannerEngine(self.repository)
            result = scanner.scan()
            readiness_score = result.get("readiness_score")
            if readiness_score is None:
                overall = (result.get("scores") or {}).get("Overall AI CTO Readiness")
                if isinstance(overall, (int, float)):
                    readiness_score = float(overall) / 100.0
            score = float(readiness_score if readiness_score is not None else 0.7)
            findings = [str(f) for f in result.get("findings", [])][:10]
            evidence.append(f"CORE-008A: readiness={score:.0%}")
        except Exception as exc:  # noqa: BLE001
            evidence.append(f"CORE-008A unavailable: {exc}")

        gate = GATE_PASS if score >= 0.8 else (GATE_WARNING if score >= 0.5 else GATE_FAILED)

        return QualityScore(
            dimension="repository_health",
            score=round(score, 3),
            gate=gate,
            evidence=evidence,
            findings=findings,
            recommendation=(
                "Improve repository readiness." if score < 0.8 else "Repository health is good."
            ),
        )


# ---------------------------------------------------------------------------
# Regression Analyzer
# ---------------------------------------------------------------------------

class RegressionAnalyzer:
    """Detect regressions by comparing current state with persisted artifacts."""

    _REQUIRED_PLANNING_KEYS = {"planning_id", "schema_version", "execution_queue"}
    _REQUIRED_CONTEXT_KEYS = {"repository", "current_branch"}

    def __init__(self, repository: str = ".") -> None:
        self.repository = repository

    def analyze(
        self,
        planning_data: Mapping[str, Any],
        context_data: Mapping[str, Any],
        execution_data: Mapping[str, Any],
    ) -> tuple:
        """Return (QualityScore, List[RegressionFinding])."""
        findings: List[RegressionFinding] = []
        evidence: List[str] = []

        # Planning regressions
        missing_plan = self._REQUIRED_PLANNING_KEYS - set(planning_data.keys())
        if missing_plan:
            findings.append(
                RegressionFinding(
                    severity="high",
                    component="planning",
                    finding=f"Missing planning keys: {sorted(missing_plan)}",
                    impact="Planning output is incomplete",
                    affected_modules=["autonomous_planning_engine"],
                    confidence=0.9,
                    recommendation="Re-run `ai plan` to regenerate planning artifacts.",
                    evidence={"missing_keys": sorted(missing_plan)},
                )
            )
        evidence.append(f"Planning keys checked: {sorted(self._REQUIRED_PLANNING_KEYS)}")

        # Context regressions
        missing_ctx = self._REQUIRED_CONTEXT_KEYS - set(context_data.keys())
        if missing_ctx:
            findings.append(
                RegressionFinding(
                    severity="medium",
                    component="context",
                    finding=f"Missing context keys: {sorted(missing_ctx)}",
                    impact="Context synchronization is incomplete",
                    affected_modules=["context_synchronization_engine"],
                    confidence=0.85,
                    recommendation="Re-run `ai context --refresh` to resynchronize.",
                    evidence={"missing_keys": sorted(missing_ctx)},
                )
            )
        evidence.append(f"Context keys checked: {sorted(self._REQUIRED_CONTEXT_KEYS)}")

        score = max(0.0, 1.0 - len(findings) * 0.2)
        gate = GATE_PASS if not findings else (GATE_WARNING if score > 0.5 else GATE_FAILED)

        quality_score = QualityScore(
            dimension="execution_quality",
            score=round(score, 3),
            gate=gate,
            evidence=evidence,
            findings=[f.finding for f in findings],
            recommendation=(
                "Fix regressions before proceeding." if findings else "No regressions detected."
            ),
        )
        return quality_score, findings


# ---------------------------------------------------------------------------
# Coverage Analyzer
# ---------------------------------------------------------------------------

class CoverageAnalyzer:
    """Evaluate test coverage completeness by inspecting the tests directory."""

    _CORE_PACKAGES = {
        "canonical_intelligence": "test_canonical_intelligence",
        "ai_cto_scanner": "test_ai_cto_scanner",
        "semantic_repository_intelligence": "test_semantic_repository_intelligence",
        "executable_repository_intelligence": "test_executable_repository_intelligence",
        "autonomous_planning_engine": "test_autonomous_planning_engine",
        "autonomous_execution_engine": "test_autonomous_execution_engine",
        "self_evaluation_engine": "test_self_evaluation_engine",
        "self_improvement_engine": "test_self_improvement_engine",
    }

    def __init__(self, repository: str = ".") -> None:
        self.repository = repository

    def analyze(self) -> QualityScore:
        from pathlib import Path
        tests_dir = Path(self.repository) / "tests"
        existing = {p.stem for p in tests_dir.glob("*.sh")} if tests_dir.exists() else set()
        existing |= {p.stem for p in tests_dir.glob("*.py")} if tests_dir.exists() else set()

        covered = {
            pkg for pkg, test in self._CORE_PACKAGES.items()
            if test in existing
        }
        uncovered = set(self._CORE_PACKAGES.keys()) - covered
        total = len(self._CORE_PACKAGES)
        score = len(covered) / total if total > 0 else 1.0

        gate = GATE_PASS if score >= 0.8 else (GATE_WARNING if score >= 0.5 else GATE_FAILED)

        return QualityScore(
            dimension="testing_quality",
            score=round(score, 3),
            gate=gate,
            evidence=[f"Test coverage: {len(covered)}/{total} CORE packages"],
            findings=[f"Missing test: {pkg}" for pkg in sorted(uncovered)],
            recommendation=(
                f"Add tests for: {sorted(uncovered)}" if uncovered else "Test coverage is complete."
            ),
        )


# ---------------------------------------------------------------------------
# Evidence Analyzer
# ---------------------------------------------------------------------------

class EvidenceAnalyzer:
    """Evaluate the quality of evidence produced by previous executions."""

    def analyze(self, execution_data: Mapping[str, Any]) -> QualityScore:
        evidence_data = execution_data.get("evidence", {})
        count = evidence_data.get("evidence_count", 0)
        score = min(1.0, count / 10.0) if count > 0 else 0.3
        gate = GATE_PASS if score >= 0.7 else GATE_WARNING

        return QualityScore(
            dimension="confidence",
            score=round(score, 3),
            gate=gate,
            evidence=[f"Evidence items collected: {count}"],
            findings=[] if count > 0 else ["No evidence items recorded in last execution"],
            recommendation=(
                "Increase evidence collection coverage."
                if score < 0.7
                else "Evidence quality is adequate."
            ),
        )


# ---------------------------------------------------------------------------
# Improvement Analyzer
# ---------------------------------------------------------------------------

class ImprovementAnalyzer:
    """Suggest improvements based on evaluation findings."""

    def analyze(
        self,
        quality_scores: List[QualityScore],
        regression_findings: List[RegressionFinding],
        architecture_findings: List[ArchitectureFinding],
    ) -> List[str]:
        """Return a list of improvement recommendations."""
        improvements: List[str] = []

        failed = [s for s in quality_scores if s.gate == GATE_FAILED]
        for s in failed:
            improvements.append(
                f"Critical: {s.dimension} scored {s.score:.0%} — {s.recommendation}"
            )

        if regression_findings:
            improvements.append(
                f"Fix {len(regression_findings)} regression(s) before next execution."
            )

        if architecture_findings:
            high = [f for f in architecture_findings if f.severity == "high"]
            if high:
                improvements.append(
                    f"Resolve {len(high)} high-severity architecture finding(s)."
                )

        return improvements
