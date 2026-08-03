from python.agent_runtime.runtime import AgentRuntime

from python.agents.ai_cto_scanner_agent import AICTOScannerAgent
from python.agents.development_agent import DevelopmentAgent


def build_runtime():

    runtime = AgentRuntime()

    runtime.register(
        AICTOScannerAgent.NAME,
        AICTOScannerAgent()
    )

    runtime.register(
        DevelopmentAgent.NAME,
        DevelopmentAgent()
    )

    return runtime
