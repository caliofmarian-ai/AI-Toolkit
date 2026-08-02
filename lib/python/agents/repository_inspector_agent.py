from python.agent_runtime.base import BaseAgent
from python.agent_runtime.models import AgentResult

from python.repository_inspector_v2.engine import RepositoryInspectorV2


class RepositoryInspectorAgent(BaseAgent):

    NAME = "inspect"

    def run(self, context):

        engine = RepositoryInspectorV2(context.repository)

        report = engine.inspect()

        return AgentResult(
            agent=self.NAME,
            success=True,
            data=report,
            messages=[
                "Repository inspection completed."
            ],
        )
