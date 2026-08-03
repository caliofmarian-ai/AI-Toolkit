"""
Self Improvement Engine — Main Orchestrator
CORE-017

Implements the AI CTO continuous improvement layer.

Responsibility: analyzing every repository, execution, and evaluation
to determine how AI Toolkit can become a better AI CTO.

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
  CORE-016  Self Evaluation Engine

Produces:
  .ai/self_improvement/improvements.json
  .ai/self_improvement/technical_debt.json
  .ai/self_improvement/performance.json
  .ai/self_improvement/optimization_plan.json
  .ai/self_improvement/proposed_issues.json
  .ai/self_improvement/proposed_batches.json
  .ai/self_improvement/proposed_cores.json
  .ai/self_improvement/roadmap_updates.json
  .ai/self_improvement/capability_analysis.json
  .ai/self_improvement/history.json
  .ai/self_improvement/snapshot.json
  .ai/self_improvement/AI_CTO_SELF_IMPROVEMENT.md
"""

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .analyzers import CapabilityAnalyzer, PerformanceAnalyzer, TechnicalDebtAnalyzer
from .generators import (
    BatchGenerator,
    CoreProposalEngine,
    IssueGenerator,
    RoadmapEvolutionEngine,
)
from .models import IMPROVEMENT_VERSION, OptimizationPlan
from .persistence import ImprovementPersistence
from .report import ImprovementReportGenerator


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _plan_id(repository: str, generated_at: str) -> str:
    digest = hashlib.sha1(
        f"{repository}{generated_at}".encode("utf-8")
    ).hexdigest()[:8].upper()
    return f"IMP-{digest}"


class OptimizationPlanner:
    """
    CORE-017 — Optimization Planner.

    Coordinates all analyzers and generators into an OptimizationPlan.
    """

    def __init__(self, repository: str = ".") -> None:
        self.repository = repository
        self._debt_analyzer = TechnicalDebtAnalyzer(repository)
        self._perf_analyzer = PerformanceAnalyzer(repository)
        self._cap_analyzer = CapabilityAnalyzer(repository)
        self._issue_gen = IssueGenerator()
        self._batch_gen = BatchGenerator()
        self._core_engine = CoreProposalEngine()
        self._roadmap_engine = RoadmapEvolutionEngine()

    def plan(self, evaluation_score: float = 0.7) -> tuple:
        """Run all analyzers and generators. Return (plan components)."""
        debt = self._debt_analyzer.analyze()
        metrics = self._perf_analyzer.analyze()
        gaps = self._cap_analyzer.analyze()

        debt_issues = self._issue_gen.generate_from_debt(debt)
        gap_issues = self._issue_gen.generate_from_gaps(gaps)
        all_issues = debt_issues + gap_issues

        batches = self._batch_gen.generate(all_issues)
        core_proposals = self._core_engine.generate(gaps, evaluation_score)
        roadmap_updates = self._roadmap_engine.generate_updates(gaps, debt, evaluation_score)

        return debt, metrics, gaps, all_issues, batches, core_proposals, roadmap_updates


class EvolutionPlanner:
    """
    CORE-017 — Evolution Planner.

    Coordinates the full improvement lifecycle by consuming all CORE
    intelligence to determine the next evolution steps.
    """

    def __init__(self, repository: str = ".") -> None:
        self.repository = repository

    def plan_evolution(
        self,
        evaluation_data: Dict[str, Any],
    ) -> List[str]:
        """
        Derive high-level evolution recommendations from evaluation data.

        Returns a list of actionable string recommendations.
        """
        recs: List[str] = []
        score = evaluation_data.get("overall_score", 0.0)
        gate = evaluation_data.get("overall_gate", "")

        if gate == "FAILED":
            recs.append(
                f"CRITICAL: Engineering quality ({score:.0%}) is below threshold. "
                "Prioritise quality improvements before new feature development."
            )
        elif gate == "WARNING":
            recs.append(
                f"WARNING: Engineering quality ({score:.0%}) needs improvement. "
                "Schedule quality improvement sprint."
            )

        regressions = evaluation_data.get("regression_findings", [])
        if regressions:
            recs.append(
                f"Fix {len(regressions)} regression(s) detected in self-evaluation."
            )

        architecture_issues = evaluation_data.get("architecture_findings", [])
        high_arch = [a for a in architecture_issues if a.get("severity") == "high"]
        if high_arch:
            recs.append(
                f"Resolve {len(high_arch)} high-severity architecture issue(s)."
            )

        return recs


class ImprovementCoordinator:
    """
    CORE-017 — Improvement Coordinator.

    Orchestrates the full self-improvement pipeline.
    """

    def __init__(self, repository: str = ".") -> None:
        self.repository = repository
        self._optimizer = OptimizationPlanner(repository)
        self._evolver = EvolutionPlanner(repository)

    def coordinate(self, evaluation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the full improvement pipeline. Return all components."""
        evaluation_score = evaluation_data.get("overall_score", 0.7)
        (
            debt, metrics, gaps, issues, batches, core_proposals, roadmap_updates
        ) = self._optimizer.plan(evaluation_score)
        evolution_recs = self._evolver.plan_evolution(evaluation_data)

        return {
            "technical_debt": debt,
            "performance_metrics": metrics,
            "capability_gaps": gaps,
            "proposed_issues": issues,
            "proposed_batches": batches,
            "core_proposals": core_proposals,
            "roadmap_updates": roadmap_updates,
            "evolution_recommendations": evolution_recs,
        }


class SelfImprovementEngine:
    """
    Self Improvement Engine — CORE-017.

    Primary interface for the AI CTO continuous improvement layer.

    Usage::

        engine = SelfImprovementEngine(repository="/path/to/repo")
        result = engine.improve()

    The returned dict contains:
      - optimization_plan  OptimizationPlan dataclass
      - plan_dict          Fully serialisable dict
      - markdown           Rendered markdown string
      - paths              Dict mapping artifact name → file path
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

        self._coordinator = ImprovementCoordinator(repository=str(self.root))
        self._report_generator = ImprovementReportGenerator()

    def improve(self) -> Dict[str, Any]:
        """
        Run the full self-improvement pipeline.

        Returns a fully serialisable dict with the optimization plan,
        rendered markdown, and file paths of persisted artifacts.
        """
        generated_at = _utcnow()
        plan_id = _plan_id(str(self.root), generated_at)

        # Load evaluation intelligence from CORE-016
        evaluation_data = self._load_evaluation()

        # Coordinate all improvement analysis
        components = self._coordinator.coordinate(evaluation_data)

        # Build optimization plan
        optimization_plan = OptimizationPlan(
            plan_id=plan_id,
            generated_at=generated_at,
            repository=str(self.root),
            schema_version=IMPROVEMENT_VERSION,
            technical_debt_items=components["technical_debt"],
            performance_metrics=components["performance_metrics"],
            capability_gaps=components["capability_gaps"],
            proposed_issues=components["proposed_issues"],
            proposed_batches=components["proposed_batches"],
            core_proposals=components["core_proposals"],
            roadmap_updates=components["roadmap_updates"],
            summary=self._build_summary(plan_id, components),
        )

        markdown = self._report_generator.render(optimization_plan)
        paths: Dict[str, str] = {}

        if self.persist:
            persistence = ImprovementPersistence(str(self.root))
            paths = persistence.save(optimization_plan, markdown=markdown)
            report_path = self.output_dir / "AI_CTO_SELF_IMPROVEMENT.md"
            self._report_generator.generate(optimization_plan, report_path)
            paths["markdown_root"] = str(report_path)

        return {
            "optimization_plan": optimization_plan,
            "plan_dict": optimization_plan.to_dict(),
            "markdown": markdown,
            "paths": paths,
        }

    # ------------------------------------------------------------------
    # Intelligence loading (delegates to existing COREs)
    # ------------------------------------------------------------------

    def _load_evaluation(self) -> Dict[str, Any]:
        try:
            from python.self_evaluation_engine.persistence import (  # type: ignore[import]
                EvaluationPersistence,
            )
            return EvaluationPersistence(str(self.root)).load_evaluation()
        except Exception:
            return {}

    # ------------------------------------------------------------------

    def _build_summary(self, plan_id: str, components: Dict[str, Any]) -> str:
        debt_count = len(components.get("technical_debt", []))
        gap_count = len(components.get("capability_gaps", []))
        issue_count = len(components.get("proposed_issues", []))
        return (
            f"Improvement plan {plan_id}: "
            f"{debt_count} technical debt item(s), "
            f"{gap_count} capability gap(s), "
            f"{issue_count} proposed issue(s). "
            f"All proposals require Owner approval before execution."
        )
