from pathlib import Path
import sys
import json

sys.path.insert(0, str(Path.cwd()))

from lib.python.engineering_engine.engineering_task_engine import (
    EngineeringTaskEngine,
)
from lib.python.engineering_engine.batch_planner_engine import (
    BatchPlannerEngine,
)
from lib.python.engineering_engine.roadmap_engine import (
    RoadmapEngine,
)
from lib.python.engineering_engine.github_milestone_generator import (
    GitHubMilestoneGenerator,
)
from lib.python.engineering_engine.github_project_planner import (
    GitHubProjectPlanner,
)
from lib.python.engineering_engine.project_exporter import (
    ProjectExporter,
)
from lib.python.engineering_engine.project_importer import (
    ProjectImporter,
)


def test_export_import_roundtrip(tmp_path: Path):

    root = Path.cwd()

    backlog = EngineeringTaskEngine(root).generate()

    batches = BatchPlannerEngine().build(backlog)

    roadmap = RoadmapEngine().build(batches)

    milestones = GitHubMilestoneGenerator().generate(
        roadmap
    )

    plan = GitHubProjectPlanner().build(
        backlog,
        batches,
        milestones,
    )

    outfile = tmp_path / "engineering-project.json"

    ProjectExporter().export_json(
        plan,
        outfile,
    )

    assert outfile.exists()

    imported = ProjectImporter().import_json(
        outfile,
    )

    assert len(imported.milestones) == len(plan.milestones)
    assert len(imported.issues) == len(plan.issues)

    data = json.loads(outfile.read_text())

    assert "milestones" in data
    assert "issues" in data
