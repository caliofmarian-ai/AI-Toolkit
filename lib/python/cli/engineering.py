from pathlib import Path

from lib.python.engineering_engine.engineering_workflow_engine import EngineeringWorkflowEngine
from lib.python.engineering_engine.engineering_report_engine import EngineeringReportEngine
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from lib.python.engineering_engine.pipeline import EngineeringPipeline
from lib.python.engineering_engine.repository_audit import RepositoryAudit
from lib.python.engineering_engine.gap_analysis import GapAnalysis
from lib.python.engineering_engine.planning_engine import PlanningEngine
from lib.python.engineering_engine.execution_engine import ExecutionEngine
from lib.python.engineering_engine.validation_engine import ValidationEngine


def engineering_audit(core):
    RepositoryAudit(ROOT).write_markdown(
        ROOT / "implementation-packages" / core / "repository-audit.md"
    )


def engineering_gap(core):
    GapAnalysis(ROOT).write_markdown(
        ROOT / "implementation-packages" / core / "gap-analysis.md"
    )


def engineering_plan(core):
    PlanningEngine(ROOT).write_markdown(core)


def engineering_execute(core):
    return ExecutionEngine(ROOT).generate(core)


def engineering_validate(core):
    ValidationEngine(ROOT).validate(core)


def engineering_build(core):
    EngineeringPipeline(ROOT).run(core)


def analyse(root: Path, module: str) -> None:
    workflow = EngineeringWorkflowEngine(root)
    result = workflow.analyse(module)

    report = EngineeringReportEngine().render(result)

    print(report)
