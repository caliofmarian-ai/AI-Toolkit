"""
Executable Repository Intelligence — Data Models
CORE-008C
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# File Classification
# ---------------------------------------------------------------------------

# Canonical file categories
FILE_CATEGORIES = [
    "Executable Code",
    "Runtime Entry Point",
    "Bootstrap",
    "Public API",
    "Internal API",
    "Plugin API",
    "Extension Point",
    "Configuration",
    "Environment",
    "Canonical Specification",
    "Documentation",
    "Generated Artifact",
    "Reports",
    "Tests",
    "Scripts",
    "Infrastructure",
    "Assets",
    "Temporary",
    "Deprecated",
    "Unknown",
]

# Repository zone categories
ZONE_CATEGORIES = [
    "Runtime",
    "Documentation",
    "Generated",
    "Configuration",
    "Testing",
    "Infrastructure",
    "Deployment",
    "Canonical",
    "Experimental",
]

# Injection safety classifications
SAFETY_CLASSIFICATIONS = [
    "SAFE",
    "SAFE_WITH_CONDITIONS",
    "UNSAFE",
    "READ_ONLY",
    "GENERATED",
    "DEPRECATED",
]


@dataclass
class FileClassification:
    """Classification of a single repository file."""

    path: str
    category: str          # one of FILE_CATEGORIES
    subcategory: str       # finer-grained label
    is_executable: bool    # participates in runtime execution
    confidence: float      # 0.0–1.0
    evidence: List[str]    # human-readable evidence strings

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "category": self.category,
            "subcategory": self.subcategory,
            "is_executable": self.is_executable,
            "confidence": round(self.confidence, 3),
            "evidence": self.evidence,
        }


# ---------------------------------------------------------------------------
# Runtime Map
# ---------------------------------------------------------------------------

@dataclass
class RuntimeComponent:
    """A runtime component identified in the repository."""

    name: str
    file: str
    role: str          # e.g. "entry_point", "worker", "scheduler"
    layer: str         # e.g. "Telegram", "Persistence", "Core"
    dependencies: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "file": self.file,
            "role": self.role,
            "layer": self.layer,
            "dependencies": self.dependencies,
        }


@dataclass
class RepositoryRuntimeMap:
    """
    Full runtime map of a repository.

    Describes which files actually participate in runtime execution,
    in what order they are initialised, and how they relate to each other.
    """

    main_entry_point: Optional[str]
    execution_chain: List[str]
    bootstrap_sequence: List[str]
    runtime_components: List[RuntimeComponent]
    initialization_order: List[str]
    scheduler_entry: Optional[str]
    background_workers: List[str]
    telegram_runtime: List[str]
    owner_runtime: List[str]
    admin_runtime: List[str]
    persistence_runtime: List[str]
    shutdown_hooks: List[str]
    restart_hooks: List[str]
    resume_hooks: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "main_entry_point": self.main_entry_point,
            "execution_chain": self.execution_chain,
            "bootstrap_sequence": self.bootstrap_sequence,
            "runtime_components": [c.to_dict() for c in self.runtime_components],
            "initialization_order": self.initialization_order,
            "scheduler_entry": self.scheduler_entry,
            "background_workers": self.background_workers,
            "telegram_runtime": self.telegram_runtime,
            "owner_runtime": self.owner_runtime,
            "admin_runtime": self.admin_runtime,
            "persistence_runtime": self.persistence_runtime,
            "shutdown_hooks": self.shutdown_hooks,
            "restart_hooks": self.restart_hooks,
            "resume_hooks": self.resume_hooks,
        }


# ---------------------------------------------------------------------------
# Executable Dependency Graph
# ---------------------------------------------------------------------------

@dataclass
class ExecutableDependencyEdge:
    """A dependency edge between two executable files."""

    source: str   # file path of the importing module
    target: str   # file path of the imported module (resolved)
    kind: str     # "import", "call", "configuration"

    def to_dict(self) -> Dict[str, Any]:
        return {"source": self.source, "target": self.target, "kind": self.kind}


@dataclass
class ExecutableDependencyGraph:
    """
    Dependency graph restricted to executable files only.

    Excludes documentation, generated artifacts, reports, and temporary files.
    """

    nodes: List[str]                         # executable file paths
    edges: List[ExecutableDependencyEdge]
    excluded: List[str]                      # paths excluded with reason
    exclusion_reasons: Dict[str, str]        # path → reason string

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "nodes": sorted(self.nodes),
            "edges": [e.to_dict() for e in self.edges],
            "excluded_count": len(self.excluded),
            "exclusion_reasons": {
                k: v for k, v in sorted(self.exclusion_reasons.items())
            },
        }


# ---------------------------------------------------------------------------
# Injection Safety
# ---------------------------------------------------------------------------

@dataclass
class InjectionSafetyRecord:
    """
    Safety classification for a detected injection point.

    Builds on CORE-008B InjectionPoint data to produce a runtime safety verdict.
    """

    file: str
    name: str
    injection_type: str    # from InjectionPoint.type
    safety: str            # one of SAFETY_CLASSIFICATIONS
    rationale: str
    conditions: List[str]  # only populated for SAFE_WITH_CONDITIONS
    confidence: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": self.file,
            "name": self.name,
            "injection_type": self.injection_type,
            "safety": self.safety,
            "rationale": self.rationale,
            "conditions": self.conditions,
            "confidence": round(self.confidence, 3),
        }


# ---------------------------------------------------------------------------
# Repository Zones
# ---------------------------------------------------------------------------

@dataclass
class RepositoryZone:
    """A classified directory zone."""

    path: str          # directory path (relative to repo root)
    zone: str          # one of ZONE_CATEGORIES
    file_count: int
    evidence: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "zone": self.zone,
            "file_count": self.file_count,
            "evidence": self.evidence,
        }


# ---------------------------------------------------------------------------
# Executable Recommendations
# ---------------------------------------------------------------------------

@dataclass
class ExecutableRecommendation:
    """An evidence-based recommendation from the executable intelligence layer."""

    id: str
    title: str
    description: str
    category: str      # "isolation", "coupling", "documentation", "generation", "entry_point"
    priority: str      # "critical", "high", "medium", "low"
    confidence: float
    evidence: List[str]
    affected_files: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "confidence": round(self.confidence, 3),
            "evidence": self.evidence,
            "affected_files": self.affected_files,
        }


# ---------------------------------------------------------------------------
# Top-level result
# ---------------------------------------------------------------------------

@dataclass
class ExecutableRepositoryResult:
    """Full result produced by the ExecutableRepositoryEngine."""

    repository: str
    file_classifications: List[FileClassification]
    runtime_map: RepositoryRuntimeMap
    executable_dependency_graph: ExecutableDependencyGraph
    injection_safety: List[InjectionSafetyRecord]
    zones: List[RepositoryZone]
    recommendations: List[ExecutableRecommendation]
    # Summary statistics
    executable_file_count: int
    non_executable_file_count: int
    category_distribution: Dict[str, int]
    zone_distribution: Dict[str, int]
    safety_distribution: Dict[str, int]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "repository": self.repository,
            "executable_file_count": self.executable_file_count,
            "non_executable_file_count": self.non_executable_file_count,
            "category_distribution": dict(sorted(self.category_distribution.items())),
            "zone_distribution": dict(sorted(self.zone_distribution.items())),
            "safety_distribution": dict(sorted(self.safety_distribution.items())),
            "file_classifications": [fc.to_dict() for fc in self.file_classifications],
            "runtime_map": self.runtime_map.to_dict(),
            "executable_dependency_graph": self.executable_dependency_graph.to_dict(),
            "injection_safety": [r.to_dict() for r in self.injection_safety],
            "zones": [z.to_dict() for z in self.zones],
            "recommendations": [r.to_dict() for r in self.recommendations],
        }
