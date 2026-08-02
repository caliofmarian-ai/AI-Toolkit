from dataclasses import dataclass, field
from typing import List


@dataclass
class PlanningTask:

    identifier: str

    title: str

    priority: str

    status: str = "PENDING"


@dataclass
class ExecutionPlan:

    identifier: str

    tasks: List[PlanningTask] = field(default_factory=list)

    status: str = "READY"
