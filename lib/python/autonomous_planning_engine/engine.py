"""
Autonomous Planning Engine — Main Orchestrator
CORE-014

Implements the AI CTO planning brain.

Responsibility: deciding what should be developed next.

Consumes (never re-implements):
  CORE-007  Canonical Intelligence
  CORE-008A AI CTO Scanner
  CORE-008B Semantic Repository Intelligence
  CORE-008C Executable Repository Intelligence
  CORE-009  Development State Engine
  CORE-010  Executive Briefing Engine
  CORE-012  Workspace Orchestrator
  CORE-013  Context Synchronization Engine

Produces:
  .ai/planning/planning.json
  .ai/planning/execution_queue.json
  .ai/planning/next_actions.json
  .ai/planning/roadmap_progress.json
  .ai/planning/recommended_pr.json
  .ai/planning/recommended_issue.json
  .ai/planning/recommended_batch.json
  .ai/planning/recommended_milestone.json
  .ai/planning/recommended_core.json
  AI_CTO_PLANNING_REPORT.md
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Type

from python.development_state_engine import DevelopmentStateEngine
from python.executive_briefing_engine import ExecutiveBriefingEngine

from .batch_planner import BatchPlanner
from .decision_engine import PlanningDecisionEngine
from .dependency_resolver import DependencyResolver
from .execution_queue import ExecutionQueueBuilder
from .issue_planner import IssuePlanner
from .milestone_planner import MilestonePlanner
from .models import (
    PLANNING_VERSION,
    NextActions,
    PlanningEntry,
    PlanningResult,
    RoadmapProgress,
)
from .persistence import PlanningPersistence
from .pr_planner import PullRequestPlanner
from .priority_optimizer import PriorityOptimizer
from .report import PlanningReportGenerator
from .roadmap_planner import RoadmapPlanner


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _planning_id(repository: str, generated_at: str) -> str:
    digest = hashlib.sha1(
        f"{repository}{generated_at}".encode("utf-8")
    ).hexdigest()[:8].upper()
    return f"PLAN-{digest}"


class AutonomousPlanningEngine:
    """
    Autonomous Planning Engine — CORE-014.

    Primary interface for the AI CTO planning brain.

    Usage::

        engine = AutonomousPlanningEngine(repository="/path/to/repo")
        result = engine.plan()

    The returned dict contains:
      - planning_result   PlanningResult dataclass
      - planning_dict     Fully serialisable dict
      - markdown          Rendered markdown string
      - paths             Dict mapping artifact name → file path
    """

    def __init__(
        self,
        repository: str = ".",
        workspace_root: Optional[str] = None,
        output_dir: Optional[str] = None,
        persist: bool = True,
        refresh_integrations: bool = False,
        state_engine_class: Type = DevelopmentStateEngine,
        briefing_engine_class: Type = ExecutiveBriefingEngine,
    ) -> None:
        self.root = Path(repository).resolve()
        self.workspace_root = (
            Path(workspace_root).resolve()
            if workspace_root
            else self.root.parent
        )
        self.output_dir = Path(output_dir).resolve() if output_dir else self.root
        self.persist = persist
        self.refresh_integrations = refresh_integrations
        self._state_engine_class = state_engine_class
        self._briefing_engine_class = briefing_engine_class

    def plan(self) -> Dict[str, Any]:
        """
        Run the full autonomous planning pipeline.

        Returns a fully serialisable dict with the planning result,
        rendered markdown, and file paths of persisted artifacts.
        """
        generated_at = _utcnow()
        snapshot = self._load_snapshot()
        briefing_dict = self._load_briefing()

        # Core pipeline
        decision_ctx = self._run_decision_engine(snapshot, briefing_dict)
        entries = self._collect_entries(decision_ctx, snapshot, briefing_dict)
        entries = ExecutionQueueBuilder.deduplicate(entries)

        queue_id = _planning_id(str(self.root), generated_at)
        queue_builder = ExecutionQueueBuilder(str(self.root))
        execution_queue = queue_builder.build(
            entries=entries,
            snapshot=snapshot,
            queue_id=queue_id,
            generated_at=generated_at,
            repository=str(self.root),
        )

        roadmap_progress = self._build_roadmap_progress(
            decision_ctx, generated_at
        )
        next_actions = self._build_next_actions(
            decision_ctx, snapshot, briefing_dict, generated_at
        )

        planning_result = PlanningResult(
            planning_id=queue_id,
            generated_at=generated_at,
            repository=str(self.root),
            schema_version=PLANNING_VERSION,
            execution_queue=execution_queue,
            next_actions=next_actions,
            roadmap_progress=roadmap_progress,
            recommended_core=decision_ctx.get("next_core_recommendation"),
            recommended_issue=next_actions.next_issue,
            recommended_batch=next_actions.next_batch,
            recommended_pr=next_actions.next_pr,
            recommended_milestone=next_actions.next_milestone,
        )

        result: Dict[str, Any] = {
            "planning_result": planning_result,
            "planning_dict": planning_result.to_dict(),
            "markdown": "",
            "paths": {},
        }

        generator = PlanningReportGenerator()
        result["markdown"] = generator.render(planning_result)

        if self.persist:
            persistence = PlanningPersistence(str(self.root))
            paths = persistence.save(planning_result)

            report_path = self.output_dir / "AI_CTO_PLANNING_REPORT.md"
            generator.generate(planning_result, report_path)
            paths["markdown"] = str(report_path)
            result["paths"] = paths

        return result

    # ------------------------------------------------------------------
    # Intelligence loading
    # ------------------------------------------------------------------

    def _load_snapshot(self) -> Dict[str, Any]:
        """Load or generate the development state snapshot."""
        try:
            engine = self._state_engine_class(repository_root=str(self.root))
            state = engine.LoadCurrentState(create_if_missing=True)
            manager = engine.manager
            snapshot = manager.GenerateExecutiveSnapshot(
                state,
                refresh_integrations=self.refresh_integrations,
            )
            return snapshot.to_dict() if hasattr(snapshot, "to_dict") else dict(snapshot)
        except Exception:
            return {}

    def _load_briefing(self) -> Dict[str, Any]:
        """Load the executive briefing dict from .ai/executive/briefing.json."""
        try:
            from python.executive_briefing_engine.persistence import (
                ExecutiveBriefingPersistence,
            )
            persistence = ExecutiveBriefingPersistence(str(self.root))
            return persistence.load_briefing()
        except Exception:
            return {}

    # ------------------------------------------------------------------
    # Planning pipeline
    # ------------------------------------------------------------------

    def _run_decision_engine(
        self,
        snapshot: Mapping[str, Any],
        briefing: Mapping[str, Any],
    ) -> Dict[str, Any]:
        """Run the PlanningDecisionEngine and enrich with next_core_recommendation."""
        decision_engine = PlanningDecisionEngine(str(self.root))
        ctx = decision_engine.decide(snapshot, briefing)

        roadmap_planner = RoadmapPlanner()
        ctx["next_core_recommendation"] = roadmap_planner.recommend_next_core(ctx)
        return ctx

    def _collect_entries(
        self,
        decision_ctx: Mapping[str, Any],
        snapshot: Mapping[str, Any],
        briefing: Mapping[str, Any],
    ) -> List[PlanningEntry]:
        """Collect PlanningEntry items from all individual planners."""
        entries: List[PlanningEntry] = []

        # CORE roadmap entries
        roadmap_planner = RoadmapPlanner()
        entries.extend(roadmap_planner.build_roadmap_entries(decision_ctx))

        # Issue entries
        issue_planner = IssuePlanner()
        entries.extend(
            issue_planner.build_issue_entries(decision_ctx, snapshot, briefing)
        )

        # Batch entries
        batch_planner = BatchPlanner(str(self.root))
        entries.extend(
            batch_planner.build_batch_entries(decision_ctx, snapshot, briefing)
        )

        # PR entries
        pr_planner = PullRequestPlanner()
        entries.extend(
            pr_planner.build_pr_entries(decision_ctx, snapshot, briefing)
        )

        # Milestone entries
        milestone_planner = MilestonePlanner()
        entries.extend(
            milestone_planner.build_milestone_entries(decision_ctx, snapshot)
        )

        return entries

    def _build_roadmap_progress(
        self,
        decision_ctx: Mapping[str, Any],
        generated_at: str,
    ) -> RoadmapProgress:
        implemented = decision_ctx.get("implemented_cores", [])
        documented = decision_ctx.get("documented_cores", [])
        incomplete = decision_ctx.get("incomplete_cores", [])
        blocked = decision_ctx.get("blocked_cores", [])
        completion = decision_ctx.get("completion_percentage", 0.0)
        phase = decision_ctx.get("current_phase", "foundation")
        maturity = decision_ctx.get("repository_maturity", "early")
        next_core = decision_ctx.get("next_core")

        remaining = len(incomplete)
        if remaining == 0:
            effort_str = "none"
        elif remaining <= 3:
            effort_str = "low"
        elif remaining <= 8:
            effort_str = "medium"
        else:
            effort_str = "high"

        return RoadmapProgress(
            generated_at=generated_at,
            repository=str(self.root),
            total_cores=len(documented),
            completed_cores=list(implemented),
            incomplete_cores=list(incomplete),
            blocked_cores=list(blocked),
            current_phase=phase,
            repository_maturity=maturity,
            completion_percentage=completion,
            estimated_remaining_effort=effort_str,
            next_core=next_core,
        )

    def _build_next_actions(
        self,
        decision_ctx: Mapping[str, Any],
        snapshot: Mapping[str, Any],
        briefing: Mapping[str, Any],
        generated_at: str,
    ) -> NextActions:
        roadmap_planner = RoadmapPlanner()
        issue_planner = IssuePlanner()
        batch_planner = BatchPlanner(str(self.root))
        pr_planner = PullRequestPlanner()
        milestone_planner = MilestonePlanner()

        next_core_rec = roadmap_planner.recommend_next_core(decision_ctx)
        next_issue_rec = issue_planner.recommend_next_issue(
            decision_ctx, snapshot, briefing
        )
        next_batch_rec = batch_planner.recommend_next_batch(
            decision_ctx, snapshot, briefing
        )
        next_pr_rec = pr_planner.recommend_next_pr(
            decision_ctx, snapshot, briefing
        )
        next_milestone_rec = milestone_planner.recommend_next_milestone(
            decision_ctx, snapshot
        )

        # Determine next repository to prioritise (from workspace state if available)
        next_repo: Optional[str] = None
        try:
            from python.workspace_orchestrator.persistence import WorkspacePersistence
            wp = WorkspacePersistence(str(self.workspace_root))
            priorities = wp.load_priorities()
            if priorities:
                top = priorities[0]
                # WorkspacePriority is a dataclass with a .repository attribute
                next_repo = str(
                    top.repository if hasattr(top, "repository")
                    else top.get("repository", "")
                )
        except Exception:
            pass

        return NextActions(
            generated_at=generated_at,
            repository=str(self.root),
            next_core=next_core_rec,
            next_issue=next_issue_rec,
            next_batch=next_batch_rec,
            next_pr=next_pr_rec,
            next_milestone=next_milestone_rec,
            next_repository=next_repo,
        )
