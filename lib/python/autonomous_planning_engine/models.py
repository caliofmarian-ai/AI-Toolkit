"""
Autonomous Planning Engine — Canonical Models
CORE-014A

All planning artifacts are deterministic, serialisable, and frozen.
No planning decisions are hardcoded — every field is derived from
existing CORE engine intelligence.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

PLANNING_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Priority constants
# ---------------------------------------------------------------------------

PRIORITY_CRITICAL = "critical"
PRIORITY_HIGH = "high"
PRIORITY_MEDIUM = "medium"
PRIORITY_LOW = "low"
PRIORITY_BLOCKED = "blocked"

# ---------------------------------------------------------------------------
# Effort constants
# ---------------------------------------------------------------------------

EFFORT_LOW = "low"
EFFORT_MEDIUM = "medium"
EFFORT_HIGH = "high"

# ---------------------------------------------------------------------------
# Entry type constants
# ---------------------------------------------------------------------------

TYPE_CORE = "core"
TYPE_ISSUE = "issue"
TYPE_BATCH = "batch"
TYPE_PR = "pr"
TYPE_MILESTONE = "milestone"
TYPE_REPOSITORY = "repository"

# ---------------------------------------------------------------------------
# Phase / maturity constants
# ---------------------------------------------------------------------------

PHASE_FOUNDATION = "foundation"
PHASE_INTELLIGENCE = "intelligence"
PHASE_AUTONOMY = "autonomy"
PHASE_PRODUCTION = "production"

MATURITY_EARLY = "early"
MATURITY_DEVELOPING = "developing"
MATURITY_MATURE = "mature"
MATURITY_ADVANCED = "advanced"


# ---------------------------------------------------------------------------
# PlanningEntry
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PlanningEntry:
    """A single item in the autonomous execution queue."""

    entry_id: str
    title: str
    type: str
    priority: str
    reason: str
    dependencies: Tuple[str, ...]
    estimated_effort: str
    confidence: float
    blocked_by: Tuple[str, ...]
    metadata: Dict[str, Any]

    def __post_init__(self):
        object.__setattr__(self, "dependencies", tuple(self.dependencies))
        object.__setattr__(self, "blocked_by", tuple(self.blocked_by))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "title": self.title,
            "type": self.type,
            "priority": self.priority,
            "reason": self.reason,
            "dependencies": list(self.dependencies),
            "estimated_effort": self.estimated_effort,
            "confidence": self.confidence,
            "blocked_by": list(self.blocked_by),
            "metadata": self.metadata,
        }


# ---------------------------------------------------------------------------
# ExecutionQueue
# ---------------------------------------------------------------------------

@dataclass
class ExecutionQueue:
    """Ordered queue of planning entries ready for autonomous execution."""

    queue_id: str
    generated_at: str
    schema_version: str
    repository: str
    entries: List[PlanningEntry] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "queue_id": self.queue_id,
            "generated_at": self.generated_at,
            "schema_version": self.schema_version,
            "repository": self.repository,
            "entry_count": len(self.entries),
            "entries": [e.to_dict() for e in self.entries],
        }


# ---------------------------------------------------------------------------
# RoadmapProgress
# ---------------------------------------------------------------------------

@dataclass
class RoadmapProgress:
    """Current CORE roadmap completion status derived from the repository."""

    generated_at: str
    repository: str
    total_cores: int
    completed_cores: List[str]
    incomplete_cores: List[str]
    blocked_cores: List[str]
    current_phase: str
    repository_maturity: str
    completion_percentage: float
    estimated_remaining_effort: str
    next_core: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "repository": self.repository,
            "total_cores": self.total_cores,
            "completed_cores": self.completed_cores,
            "incomplete_cores": self.incomplete_cores,
            "blocked_cores": self.blocked_cores,
            "current_phase": self.current_phase,
            "repository_maturity": self.repository_maturity,
            "completion_percentage": self.completion_percentage,
            "estimated_remaining_effort": self.estimated_remaining_effort,
            "next_core": self.next_core,
        }


# ---------------------------------------------------------------------------
# NextActions
# ---------------------------------------------------------------------------

@dataclass
class NextActions:
    """Top-level next action recommendations derived from all intelligence."""

    generated_at: str
    repository: str
    next_core: Optional[Dict[str, Any]] = None
    next_issue: Optional[Dict[str, Any]] = None
    next_batch: Optional[Dict[str, Any]] = None
    next_pr: Optional[Dict[str, Any]] = None
    next_milestone: Optional[Dict[str, Any]] = None
    next_repository: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "repository": self.repository,
            "next_core": self.next_core,
            "next_issue": self.next_issue,
            "next_batch": self.next_batch,
            "next_pr": self.next_pr,
            "next_milestone": self.next_milestone,
            "next_repository": self.next_repository,
        }


# ---------------------------------------------------------------------------
# PlanningResult
# ---------------------------------------------------------------------------

@dataclass
class PlanningResult:
    """Aggregate result from a single AutonomousPlanningEngine run."""

    planning_id: str
    generated_at: str
    repository: str
    schema_version: str
    execution_queue: ExecutionQueue
    next_actions: NextActions
    roadmap_progress: RoadmapProgress
    recommended_core: Optional[Dict[str, Any]]
    recommended_issue: Optional[Dict[str, Any]]
    recommended_batch: Optional[Dict[str, Any]]
    recommended_pr: Optional[Dict[str, Any]]
    recommended_milestone: Optional[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "planning_id": self.planning_id,
            "generated_at": self.generated_at,
            "repository": self.repository,
            "schema_version": self.schema_version,
            "execution_queue": self.execution_queue.to_dict(),
            "next_actions": self.next_actions.to_dict(),
            "roadmap_progress": self.roadmap_progress.to_dict(),
            "recommended_core": self.recommended_core,
            "recommended_issue": self.recommended_issue,
            "recommended_batch": self.recommended_batch,
            "recommended_pr": self.recommended_pr,
            "recommended_milestone": self.recommended_milestone,
        }
