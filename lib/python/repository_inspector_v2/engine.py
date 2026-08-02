import json
from pathlib import Path
from .report import MarkdownReport

from python.repository_engine.engine import RepositoryEngine
from python.dependency_engine.engine import DependencyEngine
from python.validation_engine.engine import ValidationEngine
from python.planning_engine.engine import PlanningEngine


class RepositoryInspectorV2:

    def __init__(self, root="."):

        self.repository = RepositoryEngine(root)
        self.dependencies = DependencyEngine(root)
        self.validation = ValidationEngine(root)
        self.planner = PlanningEngine(root)

    def inspect(self):

        report = {
            "repository": self.repository.statistics(),
            "dependencies": self.dependencies.statistics(),
            "validation": self.validation.statistics(),
        }

        plan = self.planner.build_plan()

        report["plan"] = {
            "identifier": plan.identifier,
            "tasks": [
                {
                    "identifier": t.identifier,
                    "title": t.title,
                    "priority": t.priority,
                    "status": t.status,
                }
                for t in plan.tasks
            ]
        }

        report["repository_health"] = (
            "HEALTHY"
            if report["validation"]["failed"] == 0
            else "ATTENTION"
        )

        return report

    def export(self, filename):

        report = self.inspect()

        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(report, indent=2),
            encoding="utf-8",
        )

        MarkdownReport.generate(
            report,
            ".ai/audit/repository_report.md"
        )

        return report
