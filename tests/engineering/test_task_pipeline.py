from pathlib import Path
import sys

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))

from lib.python.engineering_engine.engineering_task_engine import (
    EngineeringTaskEngine,
)
from lib.python.engineering_engine.batch_planner_engine import (
    BatchPlannerEngine,
)
from lib.python.engineering_engine.roadmap_engine import (
    RoadmapEngine,
)


def test_task_pipeline():

    backlog = EngineeringTaskEngine(ROOT).generate()

    assert len(backlog.tasks) > 0

    batches = BatchPlannerEngine().build(backlog)

    assert len(batches) > 0

    roadmap = RoadmapEngine().build(batches)

    assert len(roadmap.phases) == len(batches)

    task_count = sum(len(batch.tasks) for batch in batches)

    assert task_count == len(backlog.tasks)

    assert roadmap.phases[0].priority == "HIGH"

    assert roadmap.phases[-1].priority == "LOW"
