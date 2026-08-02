from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class AgentContext:

    repository: str = "."

    memory: Dict = field(default_factory=dict)

    metadata: Dict = field(default_factory=dict)


@dataclass
class AgentResult:

    agent: str

    success: bool

    data: Dict = field(default_factory=dict)

    messages: List[str] = field(default_factory=list)
