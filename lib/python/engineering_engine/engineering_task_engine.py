from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from lib.python.engineering_engine.semantic_repository_builder import (
    SemanticRepositoryBuilder,
)
from lib.python.engineering_engine.semantic_entities import (
    EntityType,
)


class TaskPriority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass(slots=True)
class EngineeringTask:
    id: str
    title: str
    priority: TaskPriority
    rationale: str
    affected_modules: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EngineeringBacklog:
    tasks: list[EngineeringTask] = field(default_factory=list)
    roadmap: object | None = None
    issues: list = field(default_factory=list)


class EngineeringTaskEngine:

    def __init__(self, root):
        self.root = root

    def generate(self) -> EngineeringBacklog:

        repository = SemanticRepositoryBuilder(self.root).build()

        backlog = EngineeringBacklog()

        task_number = 1

        for entity in sorted(repository.entities, key=lambda e: e.name):

            if entity.type not in (
                EntityType.ENGINE,
                EntityType.MODULE,
            ):
                continue

            priority = TaskPriority.MEDIUM

            if entity.type == EntityType.ENGINE:
                priority = TaskPriority.HIGH
            elif "interface" in entity.name.lower():
                priority = TaskPriority.HIGH
            elif entity.name.endswith("__init__.py"):
                priority = TaskPriority.LOW

            backlog.tasks.append(
                EngineeringTask(
                    id=f"TASK-{task_number:03}",
                    title=f"Review {entity.name}",
                    priority=priority,
                    rationale=f"Semantic review of {entity.type.value}.",
                    affected_modules=[entity.name],
                )
            )

            task_number += 1

        return backlog
