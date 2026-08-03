"""
Self Evaluation Engine — Main Orchestrator
CORE-016

Implements the AI CTO quality assurance layer.

Responsibility: determining whether every implementation satisfies
canonical architecture, repository standards, and engineering quality.

Consumes (never re-implements):
  CORE-007  Canonical Intelligence
  CORE-008A AI CTO Scanner
  CORE-008B Semantic Repository Intelligence
  CORE-008C Executable Repository Intelligence
  CORE-009  Development State Engine
  CORE-010  Executive Briefing Engine
  CORE-012  Workspace Orchestrator
  CORE-013  Context Synchronization Engine
  CORE-014  Autonomous Planning Engine
  CORE-015  Autonomous Execution Engine

Produces:
  .ai/self_evaluation/evaluation.json
  .ai/self_evaluation/quality.json
  .ai/self_evaluation/confidence.json
  .ai/self_evaluation/compliance.json
  .ai/self_evaluation/architecture.json
  .ai/self_evaluation/coverage.json
  .ai/self_evaluation/regressions.json
  .ai/self_evaluation/evidence.json
  .ai/self_evaluation/history.json
  .ai/self_evaluation/snapshot.json
  .ai/self_evaluation/AI_CTO_SELF_EVALUATION.md
"""

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .analyzers import (
    ArchitectureComplianceAnalyzer,
    CanonicalComplianceAnalyzer,
    CoverageAnalyzer,
    EvidenceAnalyzer,
    ImprovementAnalyzer,
    RegressionAnalyzer,
    RepositoryComplianceAnalyzer,
)
from .models import (
    EVALUATION_VERSION,
    GATE_FAILED,
    GATE_PASS,
    GATE_WARNING,
    ArchitectureFinding,
    EvaluationContext,
    EvaluationResult,
    QualityScore,
    RegressionFinding,
)
from .persistence import EvaluationPersistence
from .report import EvaluationReportGenerator
from .scoring import ConfidenceScorer, QualityScorer


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _evaluation_id(repository: str, generated_at: str) -> str:
    digest = hashlib.sha1(
        f"{repository}{generated_at}".encode("utf-8")
    ).hexdigest()[:8].upper()
    return f"EVAL-{digest}"


class EvaluationCoordinator:
    """
    CORE-016 — Evaluation Coordinator.

    Orchestrates all analyzers and scorers into a single evaluation result.
    """

    def __init__(self, repository: str = ".") -> None:
        self.repository = repository

    def coordinate(
        self,
        planning_data: Dict[str, Any],
        execution_data: Dict[str, Any],
        context_data: Dict[str, Any],
        briefing_data: Dict[str, Any],
        workspace_data: Dict[str, Any],
    ) -> tuple:
        """Run all analyzers. Return (quality_scores, regression_findings, architecture_findings)."""
        quality_scores: List[QualityScore] = []
        regression_findings: List[RegressionFinding] = []
        architecture_findings: List[ArchitectureFinding] = []

        # Canonical compliance (CORE-007)
        quality_scores.append(
            CanonicalComplianceAnalyzer(self.repository).analyze()
        )

        # Architecture compliance (CORE-008B)
        arch_score, arch_findings = ArchitectureComplianceAnalyzer(self.repository).analyze()
        quality_scores.append(arch_score)
        architecture_findings.extend(arch_findings)

        # Repository health (CORE-008A)
        quality_scores.append(
            RepositoryComplianceAnalyzer(self.repository).analyze()
        )

        # Regression analysis
        reg_score, reg_findings = RegressionAnalyzer(self.repository).analyze(
            planning_data, context_data, execution_data
        )
        quality_scores.append(reg_score)
        regression_findings.extend(reg_findings)

        # Coverage analysis
        quality_scores.append(CoverageAnalyzer(self.repository).analyze())

        # Evidence quality
        quality_scores.append(EvidenceAnalyzer().analyze(execution_data))

        # Confidence scorer
        confidence_score = ConfidenceScorer().score(
            has_planning=bool(planning_data),
            has_execution=bool(execution_data),
            has_context=bool(context_data),
            has_briefing=bool(briefing_data),
            has_workspace=bool(workspace_data),
        )
        quality_scores.append(confidence_score)

        return quality_scores, regression_findings, architecture_findings


class SelfEvaluationEngine:
    """
    Self Evaluation Engine — CORE-016.

    Primary interface for the AI CTO quality assurance layer.

    Usage::

        engine = SelfEvaluationEngine(repository="/path/to/repo")
        result = engine.evaluate()

    The returned dict contains:
      - evaluation_result   EvaluationResult dataclass
      - evaluation_dict     Fully serialisable dict
      - markdown            Rendered markdown string
      - paths               Dict mapping artifact name → file path
    """

    def __init__(
        self,
        repository: str = ".",
        workspace_root: Optional[str] = None,
        output_dir: Optional[str] = None,
        persist: bool = True,
        refresh_integrations: bool = False,
    ) -> None:
        self.root = Path(repository).resolve()
        self.workspace_root = (
            Path(workspace_root).resolve() if workspace_root else self.root.parent
        )
        self.output_dir = Path(output_dir).resolve() if output_dir else self.root
        self.persist = persist
        self.refresh_integrations = refresh_integrations

        self._coordinator = EvaluationCoordinator(repository=str(self.root))
        self._scorer = QualityScorer()
        self._report_generator = EvaluationReportGenerator()
        self._improvement_analyzer = ImprovementAnalyzer()

    def evaluate(self) -> Dict[str, Any]:
        """
        Run the full self-evaluation pipeline.

        Returns a fully serialisable dict with the evaluation result,
        rendered markdown, and file paths of persisted artifacts.
        """
        generated_at = _utcnow()
        evaluation_id = _evaluation_id(str(self.root), generated_at)

        # Load intelligence from existing COREs
        planning_data = self._load_planning()
        execution_data = self._load_execution()
        context_data = self._load_context()
        briefing_data = self._load_briefing()
        workspace_data = self._load_workspace()

        # Build evaluation context
        eval_context = EvaluationContext(
            evaluation_id=evaluation_id,
            repository=str(self.root),
            workspace=str(self.workspace_root),
            generated_at=generated_at,
            schema_version=EVALUATION_VERSION,
            planning_id=planning_data.get("planning_id", ""),
            execution_id=execution_data.get("execution_id", ""),
            briefing_id=briefing_data.get("briefing_id", ""),
            synchronization_id=context_data.get("synchronization_id", ""),
        )

        # Run all analyzers
        quality_scores, regression_findings, architecture_findings = (
            self._coordinator.coordinate(
                planning_data=planning_data,
                execution_data=execution_data,
                context_data=context_data,
                briefing_data=briefing_data,
                workspace_data=workspace_data,
            )
        )

        # Compute overall score
        overall_score = self._scorer.score_overall(quality_scores)
        quality_scores.append(overall_score)

        # Compute overall confidence
        confidence_scores = [s for s in quality_scores if s.dimension == "confidence"]
        overall_confidence = confidence_scores[0].score if confidence_scores else 0.0

        # Generate improvement recommendations
        recommendations = self._improvement_analyzer.analyze(
            quality_scores, regression_findings, architecture_findings
        )

        # Build result
        evaluation_result = EvaluationResult(
            evaluation_id=evaluation_id,
            generated_at=generated_at,
            repository=str(self.root),
            schema_version=EVALUATION_VERSION,
            context=eval_context,
            quality_scores=quality_scores,
            regression_findings=regression_findings,
            architecture_findings=architecture_findings,
            overall_gate=overall_score.gate,
            overall_score=overall_score.score,
            overall_confidence=round(overall_confidence, 3),
            recommendations=recommendations,
            summary=self._build_summary(evaluation_id, overall_score),
        )

        markdown = self._report_generator.render(evaluation_result)
        paths: Dict[str, str] = {}

        if self.persist:
            persistence = EvaluationPersistence(str(self.root))
            paths = persistence.save(evaluation_result, markdown=markdown)
            report_path = self.output_dir / "AI_CTO_SELF_EVALUATION.md"
            self._report_generator.generate(evaluation_result, report_path)
            paths["markdown_root"] = str(report_path)

        return {
            "evaluation_result": evaluation_result,
            "evaluation_dict": evaluation_result.to_dict(),
            "markdown": markdown,
            "paths": paths,
        }

    # ------------------------------------------------------------------
    # Intelligence loading (delegates to existing COREs)
    # ------------------------------------------------------------------

    def _load_planning(self) -> Dict[str, Any]:
        try:
            from python.autonomous_planning_engine.persistence import (  # type: ignore[import]
                PlanningPersistence,
            )
            return PlanningPersistence(str(self.root)).load_planning()
        except Exception:
            return {}

    def _load_execution(self) -> Dict[str, Any]:
        try:
            from python.autonomous_execution_engine.persistence import (  # type: ignore[import]
                ExecutionPersistence,
            )
            return ExecutionPersistence(str(self.root)).load_execution()
        except Exception:
            return {}

    def _load_context(self) -> Dict[str, Any]:
        try:
            from python.context_synchronization_engine.persistence import (  # type: ignore[import]
                ContextPersistence,
            )
            return ContextPersistence(str(self.root)).load_live_context()
        except Exception:
            return {}

    def _load_briefing(self) -> Dict[str, Any]:
        try:
            from python.executive_briefing_engine.persistence import (  # type: ignore[import]
                ExecutiveBriefingPersistence,
            )
            return ExecutiveBriefingPersistence(str(self.root)).load_briefing()
        except Exception:
            return {}

    def _load_workspace(self) -> Dict[str, Any]:
        try:
            from python.workspace_orchestrator.persistence import (  # type: ignore[import]
                WorkspacePersistence,
            )
            wp = WorkspacePersistence(str(self.workspace_root))
            data = wp.load_workspace()
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    # ------------------------------------------------------------------

    def _build_summary(self, evaluation_id: str, overall_score: QualityScore) -> str:
        return (
            f"Evaluation {evaluation_id} completed. "
            f"Overall engineering quality: {overall_score.score:.0%} ({overall_score.gate}). "
            f"Repository: {self.root.name}."
        )
