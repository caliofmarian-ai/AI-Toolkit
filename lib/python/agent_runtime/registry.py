from python.agent_runtime.runtime import AgentRuntime

from python.agents.repository_inspector_agent import RepositoryInspectorAgent


def build_runtime():

    runtime = AgentRuntime()

    runtime.register(
        RepositoryInspectorAgent.NAME,
        RepositoryInspectorAgent()
    )

    return runtime
