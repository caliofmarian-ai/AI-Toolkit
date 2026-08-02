from pathlib import Path

from python.agent_runtime.base import BaseAgent
from python.agent_runtime.models import AgentResult

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

        report["repository"] = profiler.run("RepositoryEngine", lambda: RepositoryEngine(repository).statistics())

        report["dependencies"] = profiler.run("DependencyEngine", lambda: DependencyEngine(repository).statistics())

        report["validation"] = profiler.run("ValidationEngine", lambda: ValidationEngine(repository).statistics())

        report["planning"] = profiler.run("PlanningEngine", lambda: PlanningEngine(repository).build_plan())

        report["inspection"] = profiler.run("RepositoryInspector", lambda: RepositoryInspectorV2(repository).inspect())

        report["canonical"] = profiler.run("CanonicalAudit", lambda: CanonicalAuditEngine(repository).audit())

        report["semantic"] = profiler.run("SemanticEngine", lambda: SemanticEngine(repository).analyze())

        report["knowledge_graph"] = profiler.run("KnowledgeGraph", lambda: KnowledgeGraphEngine(repository).build())

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
            ExecutionEngine().execute()
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
