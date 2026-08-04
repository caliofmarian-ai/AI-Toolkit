from __future__ import annotations

from pathlib import Path

from lib.python.engineering_engine.engineering_task_engine import (
    EngineeringTaskEngine,
    EngineeringBacklog,
)
from lib.python.engineering_engine.batch_planner_engine import BatchPlannerEngine
from lib.python.engineering_engine.roadmap_engine import RoadmapEngine
from lib.python.engineering_engine.github_issue_generator import GitHubIssueGenerator, GitHubIssue


class BacklogGenerator:

    def __init__(self, root: Path):
        self.root = root

    def generate(self) -> EngineeringBacklog:

        backlog = EngineeringTaskEngine(self.root).generate()

        batches = BatchPlannerEngine().build(backlog)

        roadmap = RoadmapEngine().build(batches)

        generator = GitHubIssueGenerator()

        issues = [
            generator.generate(task)
            for task in backlog.tasks
        ]

        return EngineeringBacklog(
            tasks=backlog.tasks,
            roadmap=roadmap,
            issues=issues,
        )
