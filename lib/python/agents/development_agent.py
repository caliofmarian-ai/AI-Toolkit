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


class DevelopmentAgent(BaseAgent):

    NAME = "develop"

    def run(self, context):

        repository = context.repository

        report = {}

        report["repository"] = RepositoryEngine(
            repository
        ).statistics()

        report["dependencies"] = DependencyEngine(
            repository
        ).statistics()

        report["validation"] = ValidationEngine(
            repository
        ).statistics()

        report["planning"] = PlanningEngine(
            repository
        ).build_plan()

        report["inspection"] = RepositoryInspectorV2(
            repository
        ).inspect()

        report["canonical"] = CanonicalAuditEngine(
            repository
        ).audit()

        report["semantic"] = SemanticEngine(
            repository
        ).analyze()

        report["knowledge_graph"] = KnowledgeGraphEngine(
            repository
        ).build()

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

        DevelopmentReport.generate(report)

        return AgentResult(
            agent=self.NAME,
            success=True,
            data=report,
            messages=[
                "Development analysis completed."
            ],
        )
