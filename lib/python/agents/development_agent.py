"""
AI Toolkit Agents
"""
from pathlib import Path

from python.agent_runtime.base import BaseAgent
from python.agent_runtime.models import AgentResult

from python.workspace_index import (
    RepositoryPolicy,
    IncrementalWorkspaceIndex,
)

from python.repository_engine.engine import RepositoryEngine
from python.dependency_engine.engine import DependencyEngine
from python.validation_engine.engine import ValidationEngine
from python.planning_engine.engine import PlanningEngine
from python.repository_inspector_v2.engine import RepositoryInspectorV2
from python.canonical_audit.engine import CanonicalAuditEngine
from python.semantic_engine.engine import SemanticEngine
from python.knowledge_graph_v2.engine import KnowledgeGraphEngine
from python.agents.development_report import DevelopmentReport
from python.recommendation_engine.engine import RecommendationEngine
from python.batch_generator.engine import BatchGenerator
from python.github_materialization.engine import GitHubMaterializationEngine
from python.execution_engine.engine import ExecutionEngine
from python.review_agent.engine import ReviewAgent
from python.autonomous_planner.engine import AutonomousPlanner
from python.execution_coordinator.engine import ExecutionCoordinator
from python.workspace_manager.engine import WorkspaceManager
from python.profiler.engine import Profiler


class DevelopmentAgent(BaseAgent):

    NAME = "develop"

    def run(self, context):

        repository = context.repository

        report = {}

        profiler = Profiler()

        # ------------------------------------------------------------------
        # Phase 1 — Incremental repository traversal (CORE-006)
        # ------------------------------------------------------------------

        policy = RepositoryPolicy()

        incremental_result = profiler.run(
            "IncrementalWorkspaceIndex",
            lambda: IncrementalWorkspaceIndex(repository, policy=policy).build(),
        )

        workspace_index = incremental_result.index
        inc_stats = incremental_result.stats
        inc_delta = incremental_result.delta

        report["workspace_index"] = {
            "files": workspace_index.statistics.total_files,
            "directories": workspace_index.statistics.total_directories,
            "ignored_files": workspace_index.statistics.ignored_files,
            "ignored_directories": workspace_index.statistics.ignored_directories,
            "scan_duration": workspace_index.statistics.scan_duration,
            "files_per_second": workspace_index.statistics.files_per_second,
            "incremental": inc_stats.to_dict(),
        }

        profiler.record_incremental(inc_stats)

        # ------------------------------------------------------------------
        # Phase 2 — All engines consume the same immutable WorkspaceIndex
        # ------------------------------------------------------------------

        report["repository"] = profiler.run(
            "RepositoryEngine",
            lambda: RepositoryEngine(repository, workspace_index=workspace_index).statistics(),
        )

        report["dependencies"] = profiler.run(
            "DependencyEngine",
            lambda: DependencyEngine(repository, workspace_index=workspace_index).statistics(),
        )

        report["validation"] = profiler.run(
            "ValidationEngine",
            lambda: ValidationEngine(repository).statistics(),
        )

        report["planning"] = profiler.run(
            "PlanningEngine",
            lambda: PlanningEngine(repository, workspace_index=workspace_index).build_plan(),
        )

        report["inspection"] = profiler.run(
            "RepositoryInspector",
            lambda: RepositoryInspectorV2(repository, workspace_index=workspace_index).inspect(),
        )

        report["canonical"] = profiler.run(
            "CanonicalAudit",
            lambda: CanonicalAuditEngine(repository, workspace_index=workspace_index).audit(),
        )

        report["semantic"] = profiler.run(
            "SemanticEngine",
            lambda: SemanticEngine(repository, workspace_index=workspace_index).analyze(),
        )

        report["knowledge_graph"] = profiler.run(
            "KnowledgeGraph",
            lambda: KnowledgeGraphEngine(repository, workspace_index=workspace_index).build(),
        )

        # ------------------------------------------------------------------
        # Phase 3 — Downstream pipeline (unchanged)
        # ------------------------------------------------------------------

        report["recommendations_generated"] = (
            RecommendationEngine().build(report)
        )

        report["generated_batches"] = (
            BatchGenerator().generate(
                report["recommendations_generated"]
            )
        )

        report["materialized_batches"] = (
            GitHubMaterializationEngine().generate(
                report["generated_batches"]
            )
        )

        report["execution"] = (
            ExecutionEngine().execute(
                report["generated_batches"]
            )
        )

        report["review"] = (
            ReviewAgent().review(report)
        )

        report["roadmap"] = (
            AutonomousPlanner().build(report)
        )

        report["execution_state"] = (
            ExecutionCoordinator().coordinate(
                report["roadmap"]
            )
        )

        report["workspace"] = (
            WorkspaceManager().discover(
                Path(repository).parent
            )
        )

        profiler.summary()

        DevelopmentReport.generate(report)

        return AgentResult(
            agent=self.NAME,
            success=True,
            data=report,
            messages=[
                "Development analysis completed."
            ],
        )
