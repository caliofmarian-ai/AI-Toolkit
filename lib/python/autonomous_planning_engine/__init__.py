"""
Autonomous Planning Engine — CORE-014

The AI CTO planning brain.

Determines what should be developed next by deriving all planning decisions
from existing CORE engine intelligence.  Nothing is hardcoded.

Public API::

    from python.autonomous_planning_engine import AutonomousPlanningEngine

    engine = AutonomousPlanningEngine(repository="/path/to/repo")
    result = engine.plan()
"""

from .engine import AutonomousPlanningEngine
from .decision_engine import PlanningDecisionEngine
from .dependency_resolver import DependencyGraph, DependencyResolver
from .priority_optimizer import PriorityOptimizer
from .roadmap_planner import RoadmapPlanner
from .issue_planner import IssuePlanner
from .batch_planner import BatchPlanner
from .pr_planner import PullRequestPlanner
from .milestone_planner import MilestonePlanner
from .execution_queue import ExecutionQueueBuilder
from .persistence import PlanningPersistence
from .report import PlanningReportGenerator
from .models import (
    PLANNING_VERSION,
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    PRIORITY_LOW,
    PRIORITY_BLOCKED,
    EFFORT_LOW,
    EFFORT_MEDIUM,
    EFFORT_HIGH,
    TYPE_CORE,
    TYPE_ISSUE,
    TYPE_BATCH,
    TYPE_PR,
    TYPE_MILESTONE,
    TYPE_REPOSITORY,
    PHASE_FOUNDATION,
    PHASE_INTELLIGENCE,
    PHASE_AUTONOMY,
    PHASE_PRODUCTION,
    MATURITY_EARLY,
    MATURITY_DEVELOPING,
    MATURITY_MATURE,
    MATURITY_ADVANCED,
    PlanningEntry,
    ExecutionQueue,
    RoadmapProgress,
    NextActions,
    PlanningResult,
)

__all__ = [
    # Main engine
    "AutonomousPlanningEngine",
    # Sub-engines
    "PlanningDecisionEngine",
    "DependencyGraph",
    "DependencyResolver",
    "PriorityOptimizer",
    "RoadmapPlanner",
    "IssuePlanner",
    "BatchPlanner",
    "PullRequestPlanner",
    "MilestonePlanner",
    "ExecutionQueueBuilder",
    "PlanningPersistence",
    "PlanningReportGenerator",
    # Constants
    "PLANNING_VERSION",
    "PRIORITY_CRITICAL",
    "PRIORITY_HIGH",
    "PRIORITY_MEDIUM",
    "PRIORITY_LOW",
    "PRIORITY_BLOCKED",
    "EFFORT_LOW",
    "EFFORT_MEDIUM",
    "EFFORT_HIGH",
    "TYPE_CORE",
    "TYPE_ISSUE",
    "TYPE_BATCH",
    "TYPE_PR",
    "TYPE_MILESTONE",
    "TYPE_REPOSITORY",
    "PHASE_FOUNDATION",
    "PHASE_INTELLIGENCE",
    "PHASE_AUTONOMY",
    "PHASE_PRODUCTION",
    "MATURITY_EARLY",
    "MATURITY_DEVELOPING",
    "MATURITY_MATURE",
    "MATURITY_ADVANCED",
    # Models
    "PlanningEntry",
    "ExecutionQueue",
    "RoadmapProgress",
    "NextActions",
    "PlanningResult",
]
