"""
Workspace Orchestrator — Canonical Models
CORE-012

Data models for the Multi-Repository Workspace Orchestrator.

All models are serialisable, deterministic, and support future resume.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Tuple

WORKSPACE_SCHEMA_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Repository type / category constants
# ---------------------------------------------------------------------------

REPO_TYPE_SERVICE = "service"
REPO_TYPE_LIBRARY = "library"
REPO_TYPE_TOOL = "tool"
REPO_TYPE_PLATFORM = "platform"
REPO_TYPE_DOCUMENTATION = "documentation"
REPO_TYPE_UNKNOWN = "unknown"

REPO_CATEGORY_BACKEND = "backend"
REPO_CATEGORY_FRONTEND = "frontend"
REPO_CATEGORY_INFRASTRUCTURE = "infrastructure"
REPO_CATEGORY_DOCUMENTATION = "documentation"
REPO_CATEGORY_AI = "ai"
REPO_CATEGORY_UNKNOWN = "unknown"

# ---------------------------------------------------------------------------
# Health / status constants
# ---------------------------------------------------------------------------

HEALTH_HEALTHY = "healthy"
HEALTH_DEGRADED = "degraded"
HEALTH_CRITICAL = "critical"
HEALTH_UNKNOWN = "unknown"

STATUS_ACTIVE = "active"
STATUS_STABLE = "stable"
STATUS_BLOCKED = "blocked"
STATUS_IDLE = "idle"
STATUS_ARCHIVED = "archived"
STATUS_UNKNOWN = "unknown"

STATUS_COMPLIANT = "compliant"
STATUS_PARTIAL = "partial"
STATUS_MISSING = "missing"

STATUS_ANALYZED = "analyzed"

RISK_CRITICAL = "critical"
RISK_HIGH = "high"
RISK_MEDIUM = "medium"
RISK_LOW = "low"

# ---------------------------------------------------------------------------
# WorkspaceRepository
# ---------------------------------------------------------------------------


@dataclass
class WorkspaceRepository:
    """
    Canonical model for a single repository managed by the Workspace Orchestrator.

    Combines identity, tracking state, intelligence outputs, and cross-repo
    relationship data.  All scalar fields are serialisable primitives.
    """

    # Identity
    name: str
    display_name: str
    description: str
    repository_root: str

    # Classification
    repository_type: str = REPO_TYPE_UNKNOWN
    repository_category: str = REPO_CATEGORY_UNKNOWN

    # Git state
    default_branch: str = "main"
    current_branch: str = ""

    # Work tracking
    current_issue: str = ""
    current_pull_request: str = ""
    current_batch: str = ""
    current_milestone: str = ""
    current_epic: str = ""
    current_recommendation: str = ""

    # Intelligence outputs
    development_state: str = STATUS_UNKNOWN
    executive_briefing_id: str = ""
    repository_health: str = HEALTH_UNKNOWN
    readiness: float = 0.0

    # Component statuses
    canonical_status: str = STATUS_UNKNOWN
    semantic_status: str = STATUS_UNKNOWN
    runtime_status: str = STATUS_UNKNOWN
    development_status: str = STATUS_UNKNOWN
    owner_status: str = STATUS_UNKNOWN
    risk_status: str = RISK_LOW

    # Priority (1 = highest urgency)
    priority: int = 5

    # Cross-repository relationships
    dependencies: Tuple[str, ...] = field(default_factory=tuple)
    dependents: Tuple[str, ...] = field(default_factory=tuple)
    tags: Tuple[str, ...] = field(default_factory=tuple)

    # Timestamps
    last_scan: str = ""
    last_refresh: str = ""
    last_briefing: str = ""
    last_validation: str = ""

    # Raw scan scores (populated from AICTOScannerEngine)
    scan_scores: Dict[str, Any] = field(default_factory=dict)

    # Schema
    schema_version: str = WORKSPACE_SCHEMA_VERSION

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "repository_root": self.repository_root,
            "repository_type": self.repository_type,
            "repository_category": self.repository_category,
            "default_branch": self.default_branch,
            "current_branch": self.current_branch,
            "current_issue": self.current_issue,
            "current_pull_request": self.current_pull_request,
            "current_batch": self.current_batch,
            "current_milestone": self.current_milestone,
            "current_epic": self.current_epic,
            "current_recommendation": self.current_recommendation,
            "development_state": self.development_state,
            "executive_briefing_id": self.executive_briefing_id,
            "repository_health": self.repository_health,
            "readiness": round(float(self.readiness), 4),
            "canonical_status": self.canonical_status,
            "semantic_status": self.semantic_status,
            "runtime_status": self.runtime_status,
            "development_status": self.development_status,
            "owner_status": self.owner_status,
            "risk_status": self.risk_status,
            "priority": int(self.priority),
            "dependencies": list(self.dependencies),
            "dependents": list(self.dependents),
            "tags": list(self.tags),
            "last_scan": self.last_scan,
            "last_refresh": self.last_refresh,
            "last_briefing": self.last_briefing,
            "last_validation": self.last_validation,
            "scan_scores": dict(self.scan_scores),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "WorkspaceRepository":
        return cls(
            name=data.get("name", ""),
            display_name=data.get("display_name", data.get("name", "")),
            description=data.get("description", ""),
            repository_root=data.get("repository_root", ""),
            repository_type=data.get("repository_type", REPO_TYPE_UNKNOWN),
            repository_category=data.get("repository_category", REPO_CATEGORY_UNKNOWN),
            default_branch=data.get("default_branch", "main"),
            current_branch=data.get("current_branch", ""),
            current_issue=data.get("current_issue", ""),
            current_pull_request=data.get("current_pull_request", ""),
            current_batch=data.get("current_batch", ""),
            current_milestone=data.get("current_milestone", ""),
            current_epic=data.get("current_epic", ""),
            current_recommendation=data.get("current_recommendation", ""),
            development_state=data.get("development_state", STATUS_UNKNOWN),
            executive_briefing_id=data.get("executive_briefing_id", ""),
            repository_health=data.get("repository_health", HEALTH_UNKNOWN),
            readiness=float(data.get("readiness", 0.0)),
            canonical_status=data.get("canonical_status", STATUS_UNKNOWN),
            semantic_status=data.get("semantic_status", STATUS_UNKNOWN),
            runtime_status=data.get("runtime_status", STATUS_UNKNOWN),
            development_status=data.get("development_status", STATUS_UNKNOWN),
            owner_status=data.get("owner_status", STATUS_UNKNOWN),
            risk_status=data.get("risk_status", RISK_LOW),
            priority=int(data.get("priority", 5)),
            dependencies=tuple(data.get("dependencies", [])),
            dependents=tuple(data.get("dependents", [])),
            tags=tuple(data.get("tags", [])),
            last_scan=data.get("last_scan", ""),
            last_refresh=data.get("last_refresh", ""),
            last_briefing=data.get("last_briefing", ""),
            last_validation=data.get("last_validation", ""),
            scan_scores=dict(data.get("scan_scores", {})),
            schema_version=data.get("schema_version", WORKSPACE_SCHEMA_VERSION),
        )


# ---------------------------------------------------------------------------
# WorkspaceDependencyEdge
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WorkspaceDependencyEdge:
    """A directed dependency between two repositories."""

    source: str          # repository name that depends on target
    target: str          # repository name that is depended upon
    dependency_type: str  # "shared_library" | "shared_canonical" | "shared_runtime" | "declared" | "inferred"
    confidence: float = 1.0
    evidence: Tuple[str, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "dependency_type": self.dependency_type,
            "confidence": round(float(self.confidence), 4),
            "evidence": list(self.evidence),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "WorkspaceDependencyEdge":
        return cls(
            source=data.get("source", ""),
            target=data.get("target", ""),
            dependency_type=data.get("dependency_type", "inferred"),
            confidence=float(data.get("confidence", 1.0)),
            evidence=tuple(data.get("evidence", [])),
        )


# ---------------------------------------------------------------------------
# WorkspaceRelationship
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WorkspaceRelationship:
    """A semantic relationship between two repositories."""

    repo_a: str
    repo_b: str
    relationship_type: str   # "sibling" | "parent_child" | "peer" | "shared_architecture"
    strength: float = 0.5    # 0.0 to 1.0
    shared_components: Tuple[str, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "repo_a": self.repo_a,
            "repo_b": self.repo_b,
            "relationship_type": self.relationship_type,
            "strength": round(float(self.strength), 4),
            "shared_components": list(self.shared_components),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "WorkspaceRelationship":
        return cls(
            repo_a=data.get("repo_a", ""),
            repo_b=data.get("repo_b", ""),
            relationship_type=data.get("relationship_type", "peer"),
            strength=float(data.get("strength", 0.5)),
            shared_components=tuple(data.get("shared_components", [])),
        )


# ---------------------------------------------------------------------------
# WorkspaceHealth
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WorkspaceHealth:
    """Aggregated health metrics for the entire workspace."""

    overall_health: str
    repository_health: str
    architecture_health: str
    canonical_health: str
    development_health: str
    runtime_health: str
    executive_health: str
    owner_health: str

    healthy_count: int = 0
    degraded_count: int = 0
    critical_count: int = 0
    unknown_count: int = 0
    total_repositories: int = 0

    overall_readiness: float = 0.0
    average_priority: float = 5.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_health": self.overall_health,
            "repository_health": self.repository_health,
            "architecture_health": self.architecture_health,
            "canonical_health": self.canonical_health,
            "development_health": self.development_health,
            "runtime_health": self.runtime_health,
            "executive_health": self.executive_health,
            "owner_health": self.owner_health,
            "healthy_count": self.healthy_count,
            "degraded_count": self.degraded_count,
            "critical_count": self.critical_count,
            "unknown_count": self.unknown_count,
            "total_repositories": self.total_repositories,
            "overall_readiness": round(float(self.overall_readiness), 4),
            "average_priority": round(float(self.average_priority), 4),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "WorkspaceHealth":
        return cls(
            overall_health=data.get("overall_health", HEALTH_UNKNOWN),
            repository_health=data.get("repository_health", HEALTH_UNKNOWN),
            architecture_health=data.get("architecture_health", HEALTH_UNKNOWN),
            canonical_health=data.get("canonical_health", HEALTH_UNKNOWN),
            development_health=data.get("development_health", HEALTH_UNKNOWN),
            runtime_health=data.get("runtime_health", HEALTH_UNKNOWN),
            executive_health=data.get("executive_health", HEALTH_UNKNOWN),
            owner_health=data.get("owner_health", HEALTH_UNKNOWN),
            healthy_count=int(data.get("healthy_count", 0)),
            degraded_count=int(data.get("degraded_count", 0)),
            critical_count=int(data.get("critical_count", 0)),
            unknown_count=int(data.get("unknown_count", 0)),
            total_repositories=int(data.get("total_repositories", 0)),
            overall_readiness=float(data.get("overall_readiness", 0.0)),
            average_priority=float(data.get("average_priority", 5.0)),
        )


# ---------------------------------------------------------------------------
# WorkspaceRecommendation
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WorkspaceRecommendation:
    """Evidence-based workspace-level recommendation for the owner."""

    id: str
    title: str
    description: str
    priority: str           # critical | high | medium | low
    impact: str
    confidence: float
    required_effort: str    # low | medium | high
    target_repository: str  # empty = workspace-wide
    dependencies: Tuple[str, ...] = ()
    reasoning: str = ""
    evidence: Tuple[str, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "impact": self.impact,
            "confidence": round(float(self.confidence), 4),
            "required_effort": self.required_effort,
            "target_repository": self.target_repository,
            "dependencies": list(self.dependencies),
            "reasoning": self.reasoning,
            "evidence": list(self.evidence),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "WorkspaceRecommendation":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            priority=data.get("priority", RISK_MEDIUM),
            impact=data.get("impact", ""),
            confidence=float(data.get("confidence", 0.5)),
            required_effort=data.get("required_effort", "medium"),
            target_repository=data.get("target_repository", ""),
            dependencies=tuple(data.get("dependencies", [])),
            reasoning=data.get("reasoning", ""),
            evidence=tuple(data.get("evidence", [])),
        )


# ---------------------------------------------------------------------------
# WorkspaceRisk
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WorkspaceRisk:
    """Detected risk at the workspace or repository level."""

    id: str
    category: str           # architecture | canonical_drift | dependency | health | progress
    severity: str           # critical | high | medium | low
    title: str
    description: str
    affected_repositories: Tuple[str, ...]
    remediation: str
    evidence: Tuple[str, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
            "affected_repositories": list(self.affected_repositories),
            "remediation": self.remediation,
            "evidence": list(self.evidence),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "WorkspaceRisk":
        return cls(
            id=data.get("id", ""),
            category=data.get("category", "health"),
            severity=data.get("severity", RISK_MEDIUM),
            title=data.get("title", ""),
            description=data.get("description", ""),
            affected_repositories=tuple(data.get("affected_repositories", [])),
            remediation=data.get("remediation", ""),
            evidence=tuple(data.get("evidence", [])),
        )


# ---------------------------------------------------------------------------
# WorkspacePriority
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WorkspacePriority:
    """Priority ranking for the next recommended repository / work item."""

    rank: int
    repository: str
    reason: str
    expected_impact: str
    confidence: float
    required_effort: str
    blocking_dependencies: Tuple[str, ...]
    suggested_next_milestone: str = ""
    suggested_next_epic: str = ""
    suggested_next_issue: str = ""
    suggested_next_batch: str = ""
    suggested_next_pr: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rank": self.rank,
            "repository": self.repository,
            "reason": self.reason,
            "expected_impact": self.expected_impact,
            "confidence": round(float(self.confidence), 4),
            "required_effort": self.required_effort,
            "blocking_dependencies": list(self.blocking_dependencies),
            "suggested_next_milestone": self.suggested_next_milestone,
            "suggested_next_epic": self.suggested_next_epic,
            "suggested_next_issue": self.suggested_next_issue,
            "suggested_next_batch": self.suggested_next_batch,
            "suggested_next_pr": self.suggested_next_pr,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "WorkspacePriority":
        return cls(
            rank=int(data.get("rank", 1)),
            repository=data.get("repository", ""),
            reason=data.get("reason", ""),
            expected_impact=data.get("expected_impact", ""),
            confidence=float(data.get("confidence", 0.5)),
            required_effort=data.get("required_effort", "medium"),
            blocking_dependencies=tuple(data.get("blocking_dependencies", [])),
            suggested_next_milestone=data.get("suggested_next_milestone", ""),
            suggested_next_epic=data.get("suggested_next_epic", ""),
            suggested_next_issue=data.get("suggested_next_issue", ""),
            suggested_next_batch=data.get("suggested_next_batch", ""),
            suggested_next_pr=data.get("suggested_next_pr", ""),
        )


# ---------------------------------------------------------------------------
# WorkspaceScanResult
# ---------------------------------------------------------------------------


@dataclass
class WorkspaceScanResult:
    """Complete result of a workspace scan operation."""

    workspace_id: str
    workspace_root: str
    generated_at: str
    schema_version: str

    repositories: List[WorkspaceRepository]
    dependencies: List[WorkspaceDependencyEdge]
    relationships: List[WorkspaceRelationship]
    health: WorkspaceHealth
    priorities: List[WorkspacePriority]
    recommendations: List[WorkspaceRecommendation]
    risks: List[WorkspaceRisk]

    total_repositories: int = 0
    scanned_repositories: int = 0
    failed_repositories: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workspace_id": self.workspace_id,
            "workspace_root": self.workspace_root,
            "generated_at": self.generated_at,
            "schema_version": self.schema_version,
            "total_repositories": self.total_repositories,
            "scanned_repositories": self.scanned_repositories,
            "failed_repositories": self.failed_repositories,
            "repositories": [r.to_dict() for r in self.repositories],
            "dependencies": [d.to_dict() for d in self.dependencies],
            "relationships": [r.to_dict() for r in self.relationships],
            "health": self.health.to_dict(),
            "priorities": [p.to_dict() for p in self.priorities],
            "recommendations": [r.to_dict() for r in self.recommendations],
            "risks": [r.to_dict() for r in self.risks],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "WorkspaceScanResult":
        health_data = data.get("health", {})
        return cls(
            workspace_id=data.get("workspace_id", ""),
            workspace_root=data.get("workspace_root", ""),
            generated_at=data.get("generated_at", ""),
            schema_version=data.get("schema_version", WORKSPACE_SCHEMA_VERSION),
            total_repositories=int(data.get("total_repositories", 0)),
            scanned_repositories=int(data.get("scanned_repositories", 0)),
            failed_repositories=int(data.get("failed_repositories", 0)),
            repositories=[
                WorkspaceRepository.from_dict(r) for r in data.get("repositories", [])
            ],
            dependencies=[
                WorkspaceDependencyEdge.from_dict(d) for d in data.get("dependencies", [])
            ],
            relationships=[
                WorkspaceRelationship.from_dict(r) for r in data.get("relationships", [])
            ],
            health=WorkspaceHealth.from_dict(health_data) if health_data else WorkspaceHealth(
                overall_health=HEALTH_UNKNOWN,
                repository_health=HEALTH_UNKNOWN,
                architecture_health=HEALTH_UNKNOWN,
                canonical_health=HEALTH_UNKNOWN,
                development_health=HEALTH_UNKNOWN,
                runtime_health=HEALTH_UNKNOWN,
                executive_health=HEALTH_UNKNOWN,
                owner_health=HEALTH_UNKNOWN,
            ),
            priorities=[
                WorkspacePriority.from_dict(p) for p in data.get("priorities", [])
            ],
            recommendations=[
                WorkspaceRecommendation.from_dict(r) for r in data.get("recommendations", [])
            ],
            risks=[
                WorkspaceRisk.from_dict(r) for r in data.get("risks", [])
            ],
        )


# ---------------------------------------------------------------------------
# WorkspaceStatistics
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WorkspaceStatistics:
    """Aggregate workspace statistics for reporting and history."""

    total_repositories: int
    healthy_repositories: int
    degraded_repositories: int
    critical_repositories: int
    unknown_repositories: int
    blocked_repositories: int
    active_repositories: int
    total_dependencies: int
    total_relationships: int
    total_risks: int
    critical_risks: int
    total_recommendations: int
    overall_readiness: float
    scan_duration: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_repositories": self.total_repositories,
            "healthy_repositories": self.healthy_repositories,
            "degraded_repositories": self.degraded_repositories,
            "critical_repositories": self.critical_repositories,
            "unknown_repositories": self.unknown_repositories,
            "blocked_repositories": self.blocked_repositories,
            "active_repositories": self.active_repositories,
            "total_dependencies": self.total_dependencies,
            "total_relationships": self.total_relationships,
            "total_risks": self.total_risks,
            "critical_risks": self.critical_risks,
            "total_recommendations": self.total_recommendations,
            "overall_readiness": round(float(self.overall_readiness), 4),
            "scan_duration": round(float(self.scan_duration), 4),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "WorkspaceStatistics":
        return cls(
            total_repositories=int(data.get("total_repositories", 0)),
            healthy_repositories=int(data.get("healthy_repositories", 0)),
            degraded_repositories=int(data.get("degraded_repositories", 0)),
            critical_repositories=int(data.get("critical_repositories", 0)),
            unknown_repositories=int(data.get("unknown_repositories", 0)),
            blocked_repositories=int(data.get("blocked_repositories", 0)),
            active_repositories=int(data.get("active_repositories", 0)),
            total_dependencies=int(data.get("total_dependencies", 0)),
            total_relationships=int(data.get("total_relationships", 0)),
            total_risks=int(data.get("total_risks", 0)),
            critical_risks=int(data.get("critical_risks", 0)),
            total_recommendations=int(data.get("total_recommendations", 0)),
            overall_readiness=float(data.get("overall_readiness", 0.0)),
            scan_duration=float(data.get("scan_duration", 0.0)),
        )
