from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from lib.python.engineering_engine.github_project_planner import (
    GitHubProjectPlan,
)


class ProjectExporter:

    def export_json(
        self,
        project: GitHubProjectPlan,
        output: Path,
    ) -> Path:

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            json.dumps(
                asdict(project),
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return output
