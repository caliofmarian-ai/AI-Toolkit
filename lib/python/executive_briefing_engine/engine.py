"""
Executive Briefing Engine — Main Orchestrator
CORE-010

Implements the executive intelligence layer of AI CTO.

Builds on top of:
  CORE-007 Canonical Intelligence
  CORE-008A AI CTO Integration Scanner
  CORE-008B Semantic Repository Intelligence
  CORE-008C Executable Repository Intelligence
  CORE-009  Development State Engine

Produces:
  AI_CTO_EXECUTIVE_BRIEFING.md
  .ai/executive/briefing.json
  .ai/executive/recommendations.json
  .ai/executive/priorities.json
  .ai/executive/risks.json
  .ai/executive/owner_actions.json
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Type

from python.development_state_engine import DevelopmentStateEngine

from .decision_tracker import ExecutiveDecisionTracker
from .generator import ExecutiveBriefingGenerator
from .insight_generator import ExecutiveInsightGenerator
from .models import (
    BRIEFING_VERSION,
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    SEVERITY_CRITICAL,
    ExecutiveBriefing,
    ExecutiveRecommendation,
    ExecutiveRisk,
    OwnerDashboard,
)
from .persistence import ExecutiveBriefingPersistence
from .priority_engine import ExecutivePriorityEngine
from .recommendation_engine import ExecutiveRecommendationEngine
from .risk_analyzer import ExecutiveRiskAnalyzer


class ExecutiveBriefingEngine:
    """
    Executive Briefing Engine — CORE-010.

    Primary interface between AI CTO and the Owner.

    Transforms repository state into executive decisions, priorities,
    and recommendations.  All intelligence is consumed from existing
    lower-layer engines.  No analysis is duplicated.

    Usage::

        engine = ExecutiveBriefingEngine(repository="/path/to/repo")
        result = engine.generate()

    The *result* dict contains:
      - briefing        ExecutiveBriefing dataclass
      - markdown        The rendered markdown string
      - paths           Dict mapping artifact name → file path
    """

    def __init__(
        self,
        repository: str = ".",
        output_dir: Optional[str] = None,
        persist: bool = True,
        refresh_integrations: bool = False,
        state_engine_class: Type = DevelopmentStateEngine,
    ):
        self.root = Path(repository).resolve()
        self.output_dir = Path(output_dir).resolve() if output_dir else self.root
        self.persist = persist
        self.refresh_integrations = refresh_integrations
        self._state_engine_class = state_engine_class

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self) -> Dict[str, Any]:
        """
        Run the full executive briefing pipeline.

        Returns a fully serialisable dict with the briefing, markdown,
        and file paths of persisted artifacts.
        """
        snapshot = self._load_snapshot()
        briefing = self._build_briefing(snapshot)
        result: Dict[str, Any] = {
            "briefing": briefing,
            "briefing_dict": briefing.to_dict(),
            "markdown": "",
            "paths": {},
        }

        generator = ExecutiveBriefingGenerator()
        result["markdown"] = generator.render(briefing)

        if self.persist:
            md_path = self.output_dir / "AI_CTO_EXECUTIVE_BRIEFING.md"
            generator.generate(briefing, md_path)
            persistence = ExecutiveBriefingPersistence(str(self.root))
            paths = persistence.save(briefing)
            paths["markdown"] = str(md_path)
            result["paths"] = paths

        return result

    # ------------------------------------------------------------------
    # Snapshot acquisition
    # ------------------------------------------------------------------

    def _load_snapshot(self) -> Dict[str, Any]:
        """Load or generate the development state snapshot."""
        engine = self._state_engine_class(repository_root=str(self.root))
        state = engine.LoadCurrentState(create_if_missing=True)
        manager = engine.manager
        snapshot = manager.GenerateExecutiveSnapshot(
            state,
            refresh_integrations=self.refresh_integrations,
        )
        return snapshot.to_dict()

    # ------------------------------------------------------------------
    # Briefing assembly
    # ------------------------------------------------------------------

    def _build_briefing(self, snapshot: Dict[str, Any]) -> ExecutiveBriefing:
        """Assemble the full ExecutiveBriefing from snapshot data."""
        # Sub-engine instances
        risk_analyzer = ExecutiveRiskAnalyzer()
        rec_engine = ExecutiveRecommendationEngine()
        priority_engine = ExecutivePriorityEngine()
        decision_tracker = ExecutiveDecisionTracker()
        insight_gen = ExecutiveInsightGenerator()

        # Phase 1 — Risks (needed by recommendation engine)
        all_risks = risk_analyzer.analyze(snapshot)
        critical_risks = [r for r in all_risks if r.severity == SEVERITY_CRITICAL]

        # Phase 2 — Recommendations (depends on risks)
        recommendations = rec_engine.generate(snapshot, all_risks)

        # Phase 3 — Priorities
        priorities = priority_engine.classify(snapshot)

        # Phase 4 — Pending decisions
        pending_decisions = decision_tracker.extract(snapshot)

        # Phase 5 — Health dimensions
        arch_health = insight_gen.architecture_health(snapshot)
        canonical_health = insight_gen.canonical_health(snapshot)
        dev_health = insight_gen.development_health(snapshot)
        repo_health = insight_gen.repository_health(snapshot)
        runtime_health = insight_gen.runtime_health(snapshot)

        # Phase 6 — Executive summary
        executive_summary = insight_gen.executive_summary(
            snapshot, arch_health, canonical_health, dev_health, repo_health,
            runtime_health, len(all_risks), len(recommendations),
        )

        # Phase 7 — Context fields (strip sentinel values from uninitialized state)
        context = snapshot.get("current_context", {})
        current_branch = self._clean_context(context.get("current_branch", ""))
        current_issue = self._clean_context(context.get("current_issue", ""))
        current_batch = self._clean_context(context.get("current_batch", ""))
        current_milestone = self._clean_context(context.get("current_milestone", ""))
        current_epic = self._clean_context(context.get("current_epic", ""))
        current_recommendation = self._clean_context(context.get("current_recommendation", ""))
        current_pull_request = self._clean_context(context.get("current_pull_request", ""))

        # Phase 8 — Suggested next / estimated completion
        suggested_next_core = insight_gen.suggested_next_core(snapshot)
        suggested_next_batch = insight_gen.suggested_next_batch(snapshot)
        suggested_next_pr = insight_gen.suggested_next_pr(snapshot)
        estimated_completion = insight_gen.estimated_completion(snapshot)

        # Phase 9 — Owner dashboard
        owner_dashboard = self._build_owner_dashboard(
            all_risks, recommendations, priorities,
            arch_health, canonical_health, dev_health, repo_health, runtime_health,
        )

        # Phase 10 — Repository path
        repository = str(
            snapshot.get("integrations", {})
            .get("repository_intelligence", {})
            .get("repository_root", str(self.root))
        )

        return ExecutiveBriefing(
            briefing_id=self._generate_briefing_id(snapshot),
            generated_at=snapshot.get("generated_at", self._utcnow()),
            schema_version=BRIEFING_VERSION,
            repository=repository,
            executive_summary=executive_summary,
            current_branch=current_branch,
            current_issue=current_issue,
            current_pull_request=current_pull_request,
            current_batch=current_batch,
            current_milestone=current_milestone,
            current_epic=current_epic,
            current_recommendation=current_recommendation,
            architecture_health=arch_health,
            canonical_health=canonical_health,
            development_health=dev_health,
            repository_health=repo_health,
            runtime_health=runtime_health,
            recommendations=tuple(recommendations),
            critical_risks=tuple(critical_risks),
            all_risks=tuple(all_risks),
            pending_decisions=tuple(pending_decisions),
            priorities=tuple(priorities),
            suggested_next_core=suggested_next_core,
            suggested_next_batch=suggested_next_batch,
            suggested_next_pr=suggested_next_pr,
            estimated_completion=estimated_completion,
            owner_dashboard=owner_dashboard,
        )

    # ------------------------------------------------------------------
    # Owner dashboard
    # ------------------------------------------------------------------

    def _build_owner_dashboard(
        self,
        all_risks,
        recommendations,
        priorities,
        arch_health, canonical_health, dev_health, repo_health, runtime_health,
    ) -> OwnerDashboard:
        """Derive the concise owner dashboard from intelligence data."""
        health_labels = [arch_health, canonical_health, dev_health, repo_health, runtime_health]
        critical_count = sum(1 for h in health_labels if h in ("critical", "degraded"))
        warning_count = sum(1 for h in health_labels if h == "warning")

        if critical_count >= 2:
            overall_health = "critical"
        elif critical_count == 1:
            overall_health = "degraded"
        elif warning_count >= 2:
            overall_health = "warning"
        elif warning_count == 1:
            overall_health = "warning"
        else:
            overall_health = "healthy"

        # Repository readiness from canonical health
        readiness_map = {
            "healthy": "production-ready",
            "warning": "development-ready",
            "degraded": "requires-attention",
            "critical": "not-ready",
            "unavailable": "unknown",
            "unknown": "unknown",
        }
        repository_readiness = readiness_map.get(canonical_health, "unknown")

        # Current progress from priorities
        from .models import PRIORITY_COMPLETED, PRIORITY_BLOCKED
        completed_count = sum(1 for p in priorities if p.classification == PRIORITY_COMPLETED)
        blocked_count = sum(1 for p in priorities if p.classification == PRIORITY_BLOCKED)
        total_count = len(priorities)

        if total_count > 0:
            pct = int(completed_count / total_count * 100)
            current_progress = f"{completed_count}/{total_count} items completed ({pct}%)"
        else:
            current_progress = "no tracked items"

        # Recommended actions from top recommendations
        recommended_actions = tuple(
            rec.title for rec in recommendations[:5]
            if rec.priority in (PRIORITY_CRITICAL, PRIORITY_HIGH)
        )
        if not recommended_actions:
            recommended_actions = tuple(rec.title for rec in recommendations[:3])

        # Blocked items
        from .models import PRIORITY_BLOCKED
        blocked_items = tuple(
            p.title for p in priorities if p.classification == PRIORITY_BLOCKED
        )

        return OwnerDashboard(
            overall_health=overall_health,
            repository_readiness=repository_readiness,
            current_progress=current_progress,
            open_risks=len(all_risks),
            recommended_actions=recommended_actions,
            blocked_items=blocked_items,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    _EMPTY_SENTINELS = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})

    def _clean_context(self, value) -> str:
        """Strip sentinel/uninitialized values from context fields."""
        s = str(value).strip() if value is not None else ""
        return "" if s in self._EMPTY_SENTINELS else s

    def _generate_briefing_id(self, snapshot: Dict[str, Any]) -> str:
        """Generate a stable briefing ID from snapshot content."""
        state_id = snapshot.get("state", {}).get("identifier", "")
        generated_at = snapshot.get("generated_at", self._utcnow())
        raw = f"{state_id}|{generated_at}|{str(self.root)}"
        digest = hashlib.sha256(raw.encode()).hexdigest()[:12].upper()
        return f"BRIEF-{digest}"

    def _utcnow(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
