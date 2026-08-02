from python.agent_runtime.runtime import AgentRuntime

from python.agents.repository_inspector_agent import RepositoryInspectorAgent
from python.agents.development_agent import DevelopmentAgent


def build_runtime():

    runtime = AgentRuntime()

    runtime.register(
        RepositoryInspectorAgent.NAME,
        RepositoryInspectorAgent()
    )


    runtime.register(
        DevelopmentAgent.NAME,
        DevelopmentAgent()
    )

    return runtime
