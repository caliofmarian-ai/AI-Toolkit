from dataclasses import dataclass, field
from typing import List


@dataclass
class BatchStep:

    identifier: str
    name: str
    step_type: str
    status: str = "READY"


@dataclass
class Batch:

    identifier: str
    title: str
    priority: str
    reason: str
    estimated_hours: int

    status: str = "READY"

    acceptance_criteria: List[str] = field(default_factory=list)

    steps: List[BatchStep] = field(default_factory=list)
