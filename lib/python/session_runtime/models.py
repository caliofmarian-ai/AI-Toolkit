from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Session:

    identifier: str

    repository: str

    status: str = "ACTIVE"

    completed_steps: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)
