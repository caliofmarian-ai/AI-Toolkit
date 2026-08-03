from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class NodeType(str, Enum):
    """Canonical node categories."""

    DOCUMENT = "DOCUMENT"
    SECTION = "SECTION"
    MODULE = "MODULE"
    COMPONENT = "COMPONENT"
    ENGINE = "ENGINE"
    SERVICE = "SERVICE"
    INTERFACE = "INTERFACE"
    STRATEGY = "STRATEGY"
    PIPELINE = "PIPELINE"
    RUNTIME = "RUNTIME"
    CONFIGURATION = "CONFIGURATION"
    PARAMETER = "PARAMETER"
    EVENT = "EVENT"
    STATE = "STATE"
    TEST = "TEST"
    BATCH = "BATCH"
    RECOMMENDATION = "RECOMMENDATION"


class EdgeType(str, Enum):
    """Canonical edge categories."""

    DEFINES = "DEFINES"
    CONTAINS = "CONTAINS"
    IMPLEMENTS = "IMPLEMENTS"
    REFERENCES = "REFERENCES"
    DEPENDS_ON = "DEPENDS_ON"
    EXTENDS = "EXTENDS"
    VALIDATES = "VALIDATES"
    TESTS = "TESTS"
    CONFIGURES = "CONFIGURES"
    EVOLVES_INTO = "EVOLVES_INTO"
    DEPRECATES = "DEPRECATES"


class LifecycleStatus(str, Enum):
    """Canonical lifecycle states."""

    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    IMPLEMENTED = "IMPLEMENTED"
    MAINTAINED = "MAINTAINED"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


class CoverageState(str, Enum):
    """Coverage state classifications."""

    IMPLEMENTED = "IMPLEMENTED"
    PARTIALLY_IMPLEMENTED = "PARTIALLY_IMPLEMENTED"
    MISSING = "MISSING"
    DEPRECATED = "DEPRECATED"
    OBSOLETE = "OBSOLETE"
    UNKNOWN = "UNKNOWN"


class ComplianceState(str, Enum):
    """Compliance state classifications."""

    COMPLIANT = "COMPLIANT"
    CONDITIONALLY_COMPLIANT = "CONDITIONALLY_COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    UNKNOWN = "UNKNOWN"


class DriftSeverity(str, Enum):
    """Drift severity levels."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFORMATIONAL = "INFORMATIONAL"


class Priority(str, Enum):
    """Implementation planning priorities."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    DEFERRED = "DEFERRED"


@dataclass(frozen=True)
class CanonicalNode:
    """Semantic canonical graph node."""

    id: str
    node_type: NodeType
    name: str
    source_document: str
    version: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    provenance: str = ""


@dataclass(frozen=True)
class CanonicalEdge:
    """Semantic canonical graph edge."""

    source_id: str
    target_id: str
    edge_type: EdgeType
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CanonicalSection:
    """Top-level section extracted from a canonical document."""

    id: str
    document_id: str
    title: str
    content: str
    index: int


@dataclass(frozen=True)
class CanonicalDocument:
    """Parsed canonical document."""

    id: str
    filename: str
    title: str
    version: str
    status: LifecycleStatus
    purpose: str = ""
    objectives: List[str] = field(default_factory=list)
    scope_included: List[str] = field(default_factory=list)
    scope_excluded: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    invariants: List[str] = field(default_factory=list)
    sections: List[CanonicalSection] = field(default_factory=list)


@dataclass(frozen=True)
class SemanticMatch:
    """Evidence-backed mapping between canonical and implementation entities."""

    canonical_id: str
    implementation_ref: str
    match_level: int
    confidence: float
    evidence: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass(frozen=True)
class CoverageMetric:
    """Coverage score for one evaluation category."""

    category: str
    score: float
    total: int
    covered: int
    missing: int
    partial: int
    evidence: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ComplianceMetric:
    """Compliance score for one evaluation category."""

    category: str
    state: ComplianceState
    score: float
    evidence: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class DriftFinding:
    """Architecture drift finding."""

    id: str
    category: str
    severity: DriftSeverity
    canonical_ref: str
    implementation_ref: str
    description: str
    evidence: List[str] = field(default_factory=list)
    recommendation: str = ""
    confidence: float = 0.0
    detected_at: str = ""


@dataclass(frozen=True)
class PlanBatch:
    """Planned implementation batch derived from drift findings."""

    id: str
    title: str
    description: str
    canonical_refs: List[str] = field(default_factory=list)
    repository_refs: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    estimated_hours: int = 0
    confidence: float = 0.0
    priority: Priority = Priority.MEDIUM
    acceptance_criteria: List[str] = field(default_factory=list)
