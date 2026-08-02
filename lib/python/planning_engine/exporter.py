import json
from pathlib import Path


class PlanningExporter:

    @staticmethod
    def export(plan, filename):

        Path(filename).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        Path(filename).write_text(
            json.dumps(
                {
                    "identifier": plan.identifier,
                    "status": plan.status,
                    "tasks": [
                        {
                            "identifier": t.identifier,
                            "title": t.title,
                            "priority": t.priority,
                            "status": t.status,
                        }
                        for t in plan.tasks
                    ]
                },
                indent=2,
            ),
            encoding="utf-8",
        )
