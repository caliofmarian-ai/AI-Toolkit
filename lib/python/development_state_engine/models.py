"""
Development State Engine — Canonical Models
CORE-009A
"""

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Tuple


MODEL_VERSION = "1.0.0"


def _require_non_empty_string(name: str, value: str):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")


def _coerce_tuple_of_strings(values: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(values)


def _validate_tuple_of_strings(name: str, values: Tuple[str, ...]):
    if not isinstance(values, tuple):
        raise ValueError(f"{name} must be a tuple")
    for item in values:
        if not isinstance(item, str):
            raise ValueError(f"{name} must contain only strings")


def _require_percentage(name: str, value: float):
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    if value < 0 or value > 100:
        raise ValueError(f"{name} must be in [0, 100]")


@dataclass(frozen=True)
class WorkspaceState:
    identifier: str
    active_project: str
    active_workspace: str
    current_milestone: str
    current_batch: str
    current_task: str
    completed_tasks: Tuple[str, ...] = ()
    blocked_tasks: Tuple[str, ...] = ()
    current_objective: str = ""
    estimated_progress: float = 0.0
    schema_version: str = MODEL_VERSION

    def __post_init__(self):
        object.__setattr__(self, "completed_tasks", _coerce_tuple_of_strings(self.completed_tasks))
        object.__setattr__(self, "blocked_tasks", _coerce_tuple_of_strings(self.blocked_tasks))
        self.validate()

    def validate(self):
        _require_non_empty_string("identifier", self.identifier)
        _require_non_empty_string("active_project", self.active_project)
        _require_non_empty_string("active_workspace", self.active_workspace)
        _require_non_empty_string("current_milestone", self.current_milestone)
        _require_non_empty_string("current_batch", self.current_batch)
        _require_non_empty_string("current_task", self.current_task)
        _require_non_empty_string("schema_version", self.schema_version)
        _validate_tuple_of_strings("completed_tasks", self.completed_tasks)
        _validate_tuple_of_strings("blocked_tasks", self.blocked_tasks)
        _require_percentage("estimated_progress", self.estimated_progress)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "schema_version": self.schema_version,
            "active_project": self.active_project,
            "active_workspace": self.active_workspace,
            "current_milestone": self.current_milestone,
            "current_batch": self.current_batch,
            "current_task": self.current_task,
            "completed_tasks": list(self.completed_tasks),
            "blocked_tasks": list(self.blocked_tasks),
            "current_objective": self.current_objective,
            "estimated_progress": float(self.estimated_progress),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "WorkspaceState":
        return cls(
            identifier=data["identifier"],
            schema_version=data.get("schema_version", MODEL_VERSION),
            active_project=data["active_project"],
            active_workspace=data["active_workspace"],
            current_milestone=data["current_milestone"],
            current_batch=data["current_batch"],
            current_task=data["current_task"],
            completed_tasks=tuple(data.get("completed_tasks", ())),
            blocked_tasks=tuple(data.get("blocked_tasks", ())),
            current_objective=data.get("current_objective", ""),
            estimated_progress=float(data.get("estimated_progress", 0.0)),
        )


@dataclass(frozen=True)
class RepositoryState:
    identifier: str
    repository: str
    branch: str
    head_commit: str
    open_pull_requests: Tuple[str, ...] = ()
    latest_merge: str = ""
    tags: Tuple[str, ...] = ()
    release: str = ""
    repository_health: str = "UNKNOWN"
    schema_version: str = MODEL_VERSION

    def __post_init__(self):
        object.__setattr__(self, "open_pull_requests", _coerce_tuple_of_strings(self.open_pull_requests))
        object.__setattr__(self, "tags", _coerce_tuple_of_strings(self.tags))
        self.validate()

    def validate(self):
        _require_non_empty_string("identifier", self.identifier)
        _require_non_empty_string("repository", self.repository)
        _require_non_empty_string("branch", self.branch)
        _require_non_empty_string("head_commit", self.head_commit)
        _require_non_empty_string("schema_version", self.schema_version)
        _validate_tuple_of_strings("open_pull_requests", self.open_pull_requests)
        _validate_tuple_of_strings("tags", self.tags)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "schema_version": self.schema_version,
            "repository": self.repository,
            "branch": self.branch,
            "head_commit": self.head_commit,
            "open_pull_requests": list(self.open_pull_requests),
            "latest_merge": self.latest_merge,
            "tags": list(self.tags),
            "release": self.release,
            "repository_health": self.repository_health,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "RepositoryState":
        return cls(
            identifier=data["identifier"],
            schema_version=data.get("schema_version", MODEL_VERSION),
            repository=data["repository"],
            branch=data["branch"],
            head_commit=data["head_commit"],
            open_pull_requests=tuple(data.get("open_pull_requests", ())),
            latest_merge=data.get("latest_merge", ""),
            tags=tuple(data.get("tags", ())),
            release=data.get("release", ""),
            repository_health=data.get("repository_health", "UNKNOWN"),
        )


@dataclass(frozen=True)
class ExecutionState:
    identifier: str
    current_executor: str
    running_jobs: Tuple[str, ...] = ()
    completed_jobs: Tuple[str, ...] = ()
    failed_jobs: Tuple[str, ...] = ()
    execution_queue: Tuple[str, ...] = ()
    retry_queue: Tuple[str, ...] = ()
    execution_history: Tuple[str, ...] = ()
    schema_version: str = MODEL_VERSION

    def __post_init__(self):
        object.__setattr__(self, "running_jobs", _coerce_tuple_of_strings(self.running_jobs))
        object.__setattr__(self, "completed_jobs", _coerce_tuple_of_strings(self.completed_jobs))
        object.__setattr__(self, "failed_jobs", _coerce_tuple_of_strings(self.failed_jobs))
        object.__setattr__(self, "execution_queue", _coerce_tuple_of_strings(self.execution_queue))
        object.__setattr__(self, "retry_queue", _coerce_tuple_of_strings(self.retry_queue))
        object.__setattr__(self, "execution_history", _coerce_tuple_of_strings(self.execution_history))
        self.validate()

    def validate(self):
        _require_non_empty_string("identifier", self.identifier)
        _require_non_empty_string("current_executor", self.current_executor)
        _require_non_empty_string("schema_version", self.schema_version)
        _validate_tuple_of_strings("running_jobs", self.running_jobs)
        _validate_tuple_of_strings("completed_jobs", self.completed_jobs)
        _validate_tuple_of_strings("failed_jobs", self.failed_jobs)
        _validate_tuple_of_strings("execution_queue", self.execution_queue)
        _validate_tuple_of_strings("retry_queue", self.retry_queue)
        _validate_tuple_of_strings("execution_history", self.execution_history)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "schema_version": self.schema_version,
            "current_executor": self.current_executor,
            "running_jobs": list(self.running_jobs),
            "completed_jobs": list(self.completed_jobs),
            "failed_jobs": list(self.failed_jobs),
            "execution_queue": list(self.execution_queue),
            "retry_queue": list(self.retry_queue),
            "execution_history": list(self.execution_history),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ExecutionState":
        return cls(
            identifier=data["identifier"],
            schema_version=data.get("schema_version", MODEL_VERSION),
            current_executor=data["current_executor"],
            running_jobs=tuple(data.get("running_jobs", ())),
            completed_jobs=tuple(data.get("completed_jobs", ())),
            failed_jobs=tuple(data.get("failed_jobs", ())),
            execution_queue=tuple(data.get("execution_queue", ())),
            retry_queue=tuple(data.get("retry_queue", ())),
            execution_history=tuple(data.get("execution_history", ())),
        )


@dataclass(frozen=True)
class PlanningState:
    identifier: str
    current_roadmap: str
    current_sprint: str
    recommended_batch: str
    priority_queue: Tuple[str, ...] = ()
    estimated_roi: float = 0.0
    estimated_time: float = 0.0
    dependencies: Tuple[str, ...] = ()
    schema_version: str = MODEL_VERSION

    def __post_init__(self):
        object.__setattr__(self, "priority_queue", _coerce_tuple_of_strings(self.priority_queue))
        object.__setattr__(self, "dependencies", _coerce_tuple_of_strings(self.dependencies))
        self.validate()

    def validate(self):
        _require_non_empty_string("identifier", self.identifier)
        _require_non_empty_string("current_roadmap", self.current_roadmap)
        _require_non_empty_string("current_sprint", self.current_sprint)
        _require_non_empty_string("recommended_batch", self.recommended_batch)
        _require_non_empty_string("schema_version", self.schema_version)
        _validate_tuple_of_strings("priority_queue", self.priority_queue)
        _validate_tuple_of_strings("dependencies", self.dependencies)
        if not isinstance(self.estimated_roi, (int, float)):
            raise ValueError("estimated_roi must be numeric")
        if not isinstance(self.estimated_time, (int, float)):
            raise ValueError("estimated_time must be numeric")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "schema_version": self.schema_version,
            "current_roadmap": self.current_roadmap,
            "current_sprint": self.current_sprint,
            "recommended_batch": self.recommended_batch,
            "priority_queue": list(self.priority_queue),
            "estimated_roi": float(self.estimated_roi),
            "estimated_time": float(self.estimated_time),
            "dependencies": list(self.dependencies),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "PlanningState":
        return cls(
            identifier=data["identifier"],
            schema_version=data.get("schema_version", MODEL_VERSION),
            current_roadmap=data["current_roadmap"],
            current_sprint=data["current_sprint"],
            recommended_batch=data["recommended_batch"],
            priority_queue=tuple(data.get("priority_queue", ())),
            estimated_roi=float(data.get("estimated_roi", 0.0)),
            estimated_time=float(data.get("estimated_time", 0.0)),
            dependencies=tuple(data.get("dependencies", ())),
        )


@dataclass(frozen=True)
class ReviewState:
    identifier: str
    pending_reviews: Tuple[str, ...] = ()
    open_prs: Tuple[str, ...] = ()
    architecture_findings: Tuple[str, ...] = ()
    canonical_findings: Tuple[str, ...] = ()
    testing_status: str = "UNKNOWN"
    approval_status: str = "PENDING"
    schema_version: str = MODEL_VERSION

    def __post_init__(self):
        object.__setattr__(self, "pending_reviews", _coerce_tuple_of_strings(self.pending_reviews))
        object.__setattr__(self, "open_prs", _coerce_tuple_of_strings(self.open_prs))
        object.__setattr__(self, "architecture_findings", _coerce_tuple_of_strings(self.architecture_findings))
        object.__setattr__(self, "canonical_findings", _coerce_tuple_of_strings(self.canonical_findings))
        self.validate()

    def validate(self):
        _require_non_empty_string("identifier", self.identifier)
        _require_non_empty_string("schema_version", self.schema_version)
        _validate_tuple_of_strings("pending_reviews", self.pending_reviews)
        _validate_tuple_of_strings("open_prs", self.open_prs)
        _validate_tuple_of_strings("architecture_findings", self.architecture_findings)
        _validate_tuple_of_strings("canonical_findings", self.canonical_findings)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "schema_version": self.schema_version,
            "pending_reviews": list(self.pending_reviews),
            "open_prs": list(self.open_prs),
            "architecture_findings": list(self.architecture_findings),
            "canonical_findings": list(self.canonical_findings),
            "testing_status": self.testing_status,
            "approval_status": self.approval_status,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ReviewState":
        return cls(
            identifier=data["identifier"],
            schema_version=data.get("schema_version", MODEL_VERSION),
            pending_reviews=tuple(data.get("pending_reviews", ())),
            open_prs=tuple(data.get("open_prs", ())),
            architecture_findings=tuple(data.get("architecture_findings", ())),
            canonical_findings=tuple(data.get("canonical_findings", ())),
            testing_status=data.get("testing_status", "UNKNOWN"),
            approval_status=data.get("approval_status", "PENDING"),
        )


@dataclass(frozen=True)
class OwnerState:
    identifier: str
    owner_priorities: Tuple[str, ...] = ()
    manual_decisions: Tuple[str, ...] = ()
    overrides: Tuple[str, ...] = ()
    pinned_tasks: Tuple[str, ...] = ()
    deferred_tasks: Tuple[str, ...] = ()
    schema_version: str = MODEL_VERSION

    def __post_init__(self):
        object.__setattr__(self, "owner_priorities", _coerce_tuple_of_strings(self.owner_priorities))
        object.__setattr__(self, "manual_decisions", _coerce_tuple_of_strings(self.manual_decisions))
        object.__setattr__(self, "overrides", _coerce_tuple_of_strings(self.overrides))
        object.__setattr__(self, "pinned_tasks", _coerce_tuple_of_strings(self.pinned_tasks))
        object.__setattr__(self, "deferred_tasks", _coerce_tuple_of_strings(self.deferred_tasks))
        self.validate()

    def validate(self):
        _require_non_empty_string("identifier", self.identifier)
        _require_non_empty_string("schema_version", self.schema_version)
        _validate_tuple_of_strings("owner_priorities", self.owner_priorities)
        _validate_tuple_of_strings("manual_decisions", self.manual_decisions)
        _validate_tuple_of_strings("overrides", self.overrides)
        _validate_tuple_of_strings("pinned_tasks", self.pinned_tasks)
        _validate_tuple_of_strings("deferred_tasks", self.deferred_tasks)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "schema_version": self.schema_version,
            "owner_priorities": list(self.owner_priorities),
            "manual_decisions": list(self.manual_decisions),
            "overrides": list(self.overrides),
            "pinned_tasks": list(self.pinned_tasks),
            "deferred_tasks": list(self.deferred_tasks),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "OwnerState":
        return cls(
            identifier=data["identifier"],
            schema_version=data.get("schema_version", MODEL_VERSION),
            owner_priorities=tuple(data.get("owner_priorities", ())),
            manual_decisions=tuple(data.get("manual_decisions", ())),
            overrides=tuple(data.get("overrides", ())),
            pinned_tasks=tuple(data.get("pinned_tasks", ())),
            deferred_tasks=tuple(data.get("deferred_tasks", ())),
        )


@dataclass(frozen=True)
class TelegramState:
    identifier: str
    session_id: str
    chat_id: str
    active_thread: str = ""
    last_message_at: str = ""
    subscribed_channels: Tuple[str, ...] = ()
    pending_notifications: Tuple[str, ...] = ()
    schema_version: str = MODEL_VERSION

    def __post_init__(self):
        object.__setattr__(self, "subscribed_channels", _coerce_tuple_of_strings(self.subscribed_channels))
        object.__setattr__(self, "pending_notifications", _coerce_tuple_of_strings(self.pending_notifications))
        self.validate()

    def validate(self):
        _require_non_empty_string("identifier", self.identifier)
        _require_non_empty_string("session_id", self.session_id)
        _require_non_empty_string("chat_id", self.chat_id)
        _require_non_empty_string("schema_version", self.schema_version)
        _validate_tuple_of_strings("subscribed_channels", self.subscribed_channels)
        _validate_tuple_of_strings("pending_notifications", self.pending_notifications)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "schema_version": self.schema_version,
            "session_id": self.session_id,
            "chat_id": self.chat_id,
            "active_thread": self.active_thread,
            "last_message_at": self.last_message_at,
            "subscribed_channels": list(self.subscribed_channels),
            "pending_notifications": list(self.pending_notifications),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TelegramState":
        return cls(
            identifier=data["identifier"],
            schema_version=data.get("schema_version", MODEL_VERSION),
            session_id=data["session_id"],
            chat_id=data["chat_id"],
            active_thread=data.get("active_thread", ""),
            last_message_at=data.get("last_message_at", ""),
            subscribed_channels=tuple(data.get("subscribed_channels", ())),
            pending_notifications=tuple(data.get("pending_notifications", ())),
        )


@dataclass(frozen=True)
class SnapshotMetadata:
    identifier: str
    trigger: str
    created_at: str
    source_event: str
    sequence_number: int
    tags: Tuple[str, ...] = ()
    schema_version: str = MODEL_VERSION

    def __post_init__(self):
        object.__setattr__(self, "tags", _coerce_tuple_of_strings(self.tags))
        self.validate()

    def validate(self):
        _require_non_empty_string("identifier", self.identifier)
        _require_non_empty_string("trigger", self.trigger)
        _require_non_empty_string("created_at", self.created_at)
        _require_non_empty_string("source_event", self.source_event)
        _require_non_empty_string("schema_version", self.schema_version)
        _validate_tuple_of_strings("tags", self.tags)
        if not isinstance(self.sequence_number, int) or self.sequence_number < 0:
            raise ValueError("sequence_number must be a non-negative int")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "schema_version": self.schema_version,
            "trigger": self.trigger,
            "created_at": self.created_at,
            "source_event": self.source_event,
            "sequence_number": self.sequence_number,
            "tags": list(self.tags),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SnapshotMetadata":
        return cls(
            identifier=data["identifier"],
            schema_version=data.get("schema_version", MODEL_VERSION),
            trigger=data["trigger"],
            created_at=data["created_at"],
            source_event=data["source_event"],
            sequence_number=int(data["sequence_number"]),
            tags=tuple(data.get("tags", ())),
        )


@dataclass(frozen=True)
class IntegrityReport:
    identifier: str
    repository_integrity: float
    canonical_integrity: float
    memory_integrity: float
    execution_integrity: float
    planning_integrity: float
    resume_integrity: float
    overall_context_integrity_score: float
    schema_version: str = MODEL_VERSION

    def __post_init__(self):
        self.validate()

    def validate(self):
        _require_non_empty_string("identifier", self.identifier)
        _require_non_empty_string("schema_version", self.schema_version)
        _require_percentage("repository_integrity", self.repository_integrity)
        _require_percentage("canonical_integrity", self.canonical_integrity)
        _require_percentage("memory_integrity", self.memory_integrity)
        _require_percentage("execution_integrity", self.execution_integrity)
        _require_percentage("planning_integrity", self.planning_integrity)
        _require_percentage("resume_integrity", self.resume_integrity)
        _require_percentage("overall_context_integrity_score", self.overall_context_integrity_score)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "schema_version": self.schema_version,
            "repository_integrity": float(self.repository_integrity),
            "canonical_integrity": float(self.canonical_integrity),
            "memory_integrity": float(self.memory_integrity),
            "execution_integrity": float(self.execution_integrity),
            "planning_integrity": float(self.planning_integrity),
            "resume_integrity": float(self.resume_integrity),
            "overall_context_integrity_score": float(self.overall_context_integrity_score),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "IntegrityReport":
        return cls(
            identifier=data["identifier"],
            schema_version=data.get("schema_version", MODEL_VERSION),
            repository_integrity=float(data["repository_integrity"]),
            canonical_integrity=float(data["canonical_integrity"]),
            memory_integrity=float(data["memory_integrity"]),
            execution_integrity=float(data["execution_integrity"]),
            planning_integrity=float(data["planning_integrity"]),
            resume_integrity=float(data["resume_integrity"]),
            overall_context_integrity_score=float(data["overall_context_integrity_score"]),
        )


@dataclass(frozen=True)
class DevelopmentState:
    identifier: str
    workspace_state: WorkspaceState
    repository_state: RepositoryState
    execution_state: ExecutionState
    planning_state: PlanningState
    review_state: ReviewState
    owner_state: OwnerState
    telegram_state: TelegramState
    snapshot_metadata: SnapshotMetadata
    integrity_report: IntegrityReport
    schema_version: str = MODEL_VERSION

    def __post_init__(self):
        self.validate()

    def validate(self):
        _require_non_empty_string("identifier", self.identifier)
        _require_non_empty_string("schema_version", self.schema_version)

        if not isinstance(self.workspace_state, WorkspaceState):
            raise ValueError("workspace_state must be WorkspaceState")
        if not isinstance(self.repository_state, RepositoryState):
            raise ValueError("repository_state must be RepositoryState")
        if not isinstance(self.execution_state, ExecutionState):
            raise ValueError("execution_state must be ExecutionState")
        if not isinstance(self.planning_state, PlanningState):
            raise ValueError("planning_state must be PlanningState")
        if not isinstance(self.review_state, ReviewState):
            raise ValueError("review_state must be ReviewState")
        if not isinstance(self.owner_state, OwnerState):
            raise ValueError("owner_state must be OwnerState")
        if not isinstance(self.telegram_state, TelegramState):
            raise ValueError("telegram_state must be TelegramState")
        if not isinstance(self.snapshot_metadata, SnapshotMetadata):
            raise ValueError("snapshot_metadata must be SnapshotMetadata")
        if not isinstance(self.integrity_report, IntegrityReport):
            raise ValueError("integrity_report must be IntegrityReport")

        self.workspace_state.validate()
        self.repository_state.validate()
        self.execution_state.validate()
        self.planning_state.validate()
        self.review_state.validate()
        self.owner_state.validate()
        self.telegram_state.validate()
        self.snapshot_metadata.validate()
        self.integrity_report.validate()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "schema_version": self.schema_version,
            "workspace_state": self.workspace_state.to_dict(),
            "repository_state": self.repository_state.to_dict(),
            "execution_state": self.execution_state.to_dict(),
            "planning_state": self.planning_state.to_dict(),
            "review_state": self.review_state.to_dict(),
            "owner_state": self.owner_state.to_dict(),
            "telegram_state": self.telegram_state.to_dict(),
            "snapshot_metadata": self.snapshot_metadata.to_dict(),
            "integrity_report": self.integrity_report.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "DevelopmentState":
        return cls(
            identifier=data["identifier"],
            schema_version=data.get("schema_version", MODEL_VERSION),
            workspace_state=WorkspaceState.from_dict(data["workspace_state"]),
            repository_state=RepositoryState.from_dict(data["repository_state"]),
            execution_state=ExecutionState.from_dict(data["execution_state"]),
            planning_state=PlanningState.from_dict(data["planning_state"]),
            review_state=ReviewState.from_dict(data["review_state"]),
            owner_state=OwnerState.from_dict(data["owner_state"]),
            telegram_state=TelegramState.from_dict(data["telegram_state"]),
            snapshot_metadata=SnapshotMetadata.from_dict(data["snapshot_metadata"]),
            integrity_report=IntegrityReport.from_dict(data["integrity_report"]),
        )
