from __future__ import annotations

from dataclasses import dataclass, field

from lib.python.engineering_engine.engineering_task_engine import (
    EngineeringBacklog,
    TaskPriority,
)


@dataclass(slots=True)
class EngineeringBatch:

    id: str

    priority: str

    tasks: list[str] = field(default_factory=list)


class BatchPlannerEngine:

    def build(
        self,
        backlog: EngineeringBacklog,
    ) -> list[EngineeringBatch]:

        groups = {
            TaskPriority.HIGH: [],
            TaskPriority.MEDIUM: [],
            TaskPriority.LOW: [],
        }

        for task in backlog.tasks:
            groups[task.priority].append(task.id)

        batches = []

        batch_index = 1

        MAX_BATCH_SIZE = 10

        for priority in (
            TaskPriority.HIGH,
            TaskPriority.MEDIUM,
            TaskPriority.LOW,
        ):

            tasks = groups[priority]

            if not tasks:
                continue

            for start in range(0, len(tasks), MAX_BATCH_SIZE):

                chunk = tasks[start:start + MAX_BATCH_SIZE]

                batches.append(
                    EngineeringBatch(
                        id=f"BATCH-{batch_index:03}",
                        priority=priority.value,
                        tasks=chunk,
                    )
                )

                batch_index += 1

        return batches
