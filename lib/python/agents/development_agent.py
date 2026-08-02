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

        DevelopmentReport.generate(report)

        return AgentResult(
            agent=self.NAME,
            success=True,
            data=report,
            messages=[
                "Development analysis completed."
            ],
        )
