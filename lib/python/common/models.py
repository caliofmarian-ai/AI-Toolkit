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


    def to_dict(self):
        return {
            "identifier": self.identifier,
            "title": self.title,
            "priority": self.priority,
            "reason": self.reason,
            "estimated_hours": self.estimated_hours,
            "status": self.status,
            "acceptance_criteria": list(self.acceptance_criteria),
            "steps": [
                {
                    "identifier": s.identifier,
                    "name": s.name,
                    "step_type": s.step_type,
                    "status": s.status,
                }
                for s in self.steps
            ],
        }

    @classmethod
    def from_dict(cls, data):

        steps = [
            BatchStep(
                identifier=s["identifier"],
                name=s["name"],
                step_type=s["step_type"],
                status=s.get("status", "READY"),
            )
            for s in data.get("steps", [])
        ]

        return cls(
            identifier=data["identifier"],
            title=data["title"],
            priority=data["priority"],
            reason=data["reason"],
            estimated_hours=data["estimated_hours"],
            status=data.get("status", "READY"),
            acceptance_criteria=data.get("acceptance_criteria", []),
            steps=steps,
        )
