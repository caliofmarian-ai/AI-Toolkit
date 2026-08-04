from pathlib import Path
import sys

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))

from lib.python.engineering_engine.backlog_generator import (
    BacklogGenerator,
)
from lib.python.engineering_engine.github_milestone_generator import (
    GitHubMilestoneGenerator,
)
from lib.python.engineering_engine.github_project_planner import (
    GitHubProjectPlanner,
)


def test_backlog_pipeline():

    backlog = BacklogGenerator(ROOT).generate()

    assert len(backlog.issues) > 0
    assert len(backlog.roadmap.phases) > 0

    milestones = GitHubMilestoneGenerator().generate(
        backlog.roadmap
    )

    assert len(milestones) == len(backlog.roadmap.phases)

    planner = GitHubProjectPlanner()

    plan = planner.build(
        backlog,
        backlog.roadmap.phases,
        milestones,
    )

    assert len(plan.milestones) == len(milestones)
    assert len(plan.issues) == len(backlog.issues)

    milestone_titles = {
        m.title for m in milestones
    }

    for issue in plan.issues:
        assert issue.milestone in milestone_titles
