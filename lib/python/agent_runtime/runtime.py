class AgentRuntime:

    def __init__(self):

        self._agents = {}

    def register(self, name, agent):

        self._agents[name] = agent

    def list_agents(self):

        return sorted(self._agents.keys())

    def execute(self, name, context):

        if name not in self._agents:
            raise RuntimeError(f"Unknown agent: {name}")

        return self._agents[name].run(context)
