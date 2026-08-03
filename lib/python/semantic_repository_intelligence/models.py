"""
Semantic Repository Intelligence — Data Models
CORE-008B
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# AST-level symbols
# ---------------------------------------------------------------------------

@dataclass
class ImportSymbol:
    """An import statement extracted from source code."""

    module: str
    names: List[str]
    alias: Optional[str]
    is_relative: bool
    level: int  # 0 = absolute, 1 = '.', 2 = '..', etc.
    line: int

    def to_dict(self):
        return {
            "module": self.module,
            "names": self.names,
            "alias": self.alias,
            "is_relative": self.is_relative,
            "level": self.level,
            "line": self.line,
        }


@dataclass
class ClassSymbol:
    """A class definition extracted from source code."""

    name: str
    bases: List[str]
    methods: List[str]
    is_abstract: bool
    decorators: List[str]
    line: int

    def to_dict(self):
        return {
            "name": self.name,
            "bases": self.bases,
            "methods": self.methods,
            "is_abstract": self.is_abstract,
            "decorators": self.decorators,
            "line": self.line,
        }


@dataclass
class FunctionSymbol:
    """A function or method definition extracted from source code."""

    name: str
    args: List[str]
    is_async: bool
    is_method: bool
    decorators: List[str]
    calls: List[str]  # bare function/method names invoked within the body
    line: int

    def to_dict(self):
        return {
            "name": self.name,
            "args": self.args,
            "is_async": self.is_async,
            "is_method": self.is_method,
            "decorators": self.decorators,
            "calls": self.calls,
            "line": self.line,
        }


@dataclass
class ConstantSymbol:
    """A module-level constant assignment."""

    name: str
    value_type: str  # str, int, float, bool, dict, list, none, other
    line: int

    def to_dict(self):
        return {"name": self.name, "value_type": self.value_type, "line": self.line}


@dataclass
class FileAnalysis:
    """Complete semantic analysis of one source file."""

    path: str
    language: str  # python, typescript, javascript, json, yaml, markdown
    classes: List[ClassSymbol] = field(default_factory=list)
    functions: List[FunctionSymbol] = field(default_factory=list)
    imports: List[ImportSymbol] = field(default_factory=list)
    constants: List[ConstantSymbol] = field(default_factory=list)
    entry_points: List[str] = field(default_factory=list)
    error: Optional[str] = None

    def to_dict(self):
        return {
            "path": self.path,
            "language": self.language,
            "classes": [c.to_dict() for c in self.classes],
            "functions": [f.to_dict() for f in self.functions],
            "imports": [i.to_dict() for i in self.imports],
            "constants": [c.to_dict() for c in self.constants],
            "entry_points": self.entry_points,
            "error": self.error,
        }


# ---------------------------------------------------------------------------
# Import Graph
# ---------------------------------------------------------------------------

@dataclass
class ImportEdge:
    """A directed import relationship between two modules."""

    source: str  # importing file/module path
    target: str  # symbolic import target
    resolved: Optional[str]  # resolved file path within the repo, if found
    confidence: float  # 0.0–1.0

    def to_dict(self):
        return {
            "source": self.source,
            "target": self.target,
            "resolved": self.resolved,
            "confidence": round(self.confidence, 3),
        }


@dataclass
class ImportGraphResult:
    """Result of import graph analysis."""

    nodes: List[str]  # all file paths included in the graph
    edges: List[ImportEdge]
    circular_dependencies: List[List[str]]  # each item is one cycle
    critical_modules: List[str]  # modules imported by many others (by in-degree)
    orphan_modules: List[str]  # modules never imported by anyone
    in_degree: Dict[str, int]  # resolved_path → import count

    def to_dict(self):
        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "circular_dependency_count": len(self.circular_dependencies),
            "circular_dependencies": self.circular_dependencies,
            "critical_modules": self.critical_modules,
            "orphan_modules": self.orphan_modules,
            "top_imported": sorted(
                self.in_degree.items(), key=lambda kv: kv[1], reverse=True
            )[:10],
        }


# ---------------------------------------------------------------------------
# Call Graph
# ---------------------------------------------------------------------------

@dataclass
class CallEdge:
    """A directed call relationship between two functions."""

    caller_file: str
    caller_func: str
    callee: str  # bare name of called function/method
    line: int

    def to_dict(self):
        return {
            "caller_file": self.caller_file,
            "caller_func": self.caller_func,
            "callee": self.callee,
            "line": self.line,
        }


@dataclass
class CallGraphResult:
    """Result of call graph analysis."""

    edges: List[CallEdge]
    entry_points: List[str]  # "<file>::<func>" references for entry-point functions
    execution_chains: List[List[str]]  # selected deep call chains

    def to_dict(self):
        return {
            "edge_count": len(self.edges),
            "entry_points": self.entry_points,
            "execution_chain_count": len(self.execution_chains),
            "execution_chains": self.execution_chains[:10],
        }


# ---------------------------------------------------------------------------
# Dependency Graph
# ---------------------------------------------------------------------------

@dataclass
class ExternalDependency:
    """An external package dependency declared in a manifest file."""

    name: str
    version_spec: str  # e.g. ">=1.0.0", "==2.0.0", ""
    source_file: str  # manifest file (requirements.txt, package.json, …)
    ecosystem: str  # pip, npm, cargo, etc.

    def to_dict(self):
        return {
            "name": self.name,
            "version_spec": self.version_spec,
            "source_file": self.source_file,
            "ecosystem": self.ecosystem,
        }


@dataclass
class DependencyGraphResult:
    """Result of dependency graph analysis."""

    external_dependencies: List[ExternalDependency]
    internal_modules: List[str]
    dependency_count: int

    def to_dict(self):
        return {
            "external_dependency_count": self.dependency_count,
            "internal_module_count": len(self.internal_modules),
            "external_dependencies": [d.to_dict() for d in self.external_dependencies],
        }


# ---------------------------------------------------------------------------
# Architecture Graph
# ---------------------------------------------------------------------------

@dataclass
class ArchitectureNode:
    """A layer/component node in the architecture graph."""

    id: str
    name: str
    layer: str  # Runtime, State, Telegram, Canonical, etc.
    modules: List[str]  # constituent file paths
    in_degree: int  # other layers that depend on this
    out_degree: int  # layers this depends on

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "layer": self.layer,
            "module_count": len(self.modules),
            "modules": self.modules[:10],
            "in_degree": self.in_degree,
            "out_degree": self.out_degree,
        }


@dataclass
class ArchitectureEdge:
    """A dependency relationship between two architecture layers."""

    source: str  # source layer id
    target: str  # target layer id
    relationship: str  # imports, extends, configures, depends_on
    strength: float  # 0.0–1.0

    def to_dict(self):
        return {
            "source": self.source,
            "target": self.target,
            "relationship": self.relationship,
            "strength": round(self.strength, 3),
        }


@dataclass
class ArchitectureRisk:
    """An identified architecture risk."""

    id: str
    title: str
    description: str
    severity: str  # critical, high, medium, low
    affected_modules: List[str]
    evidence: List[str]
    confidence: float

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "affected_modules": self.affected_modules,
            "evidence": self.evidence,
            "confidence": round(self.confidence, 3),
        }


@dataclass
class ArchitectureGraphResult:
    """Result of architecture graph analysis."""

    nodes: List[ArchitectureNode]
    edges: List[ArchitectureEdge]
    hotspots: List[str]  # module paths with high coupling
    risks: List[ArchitectureRisk]
    high_coupling_modules: List[str]
    low_cohesion_layers: List[str]
    extension_points: List[str]  # identified potential extension points

    def to_dict(self):
        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
            "hotspots": self.hotspots,
            "risks": [r.to_dict() for r in self.risks],
            "high_coupling_modules": self.high_coupling_modules,
            "low_cohesion_layers": self.low_cohesion_layers,
            "extension_points": self.extension_points,
        }


# ---------------------------------------------------------------------------
# Injection Points
# ---------------------------------------------------------------------------

@dataclass
class InjectionPoint:
    """A detected injection / extension point in the repository."""

    name: str
    type: str  # decorator, plugin_interface, event_bus, middleware, hook, di_container, service_boundary
    file: str
    line: int
    pattern: str  # the pattern that triggered detection
    confidence: float
    evidence: List[str]

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "file": self.file,
            "line": self.line,
            "pattern": self.pattern,
            "confidence": round(self.confidence, 3),
            "evidence": self.evidence,
        }


# ---------------------------------------------------------------------------
# Semantic Findings and Recommendations
# ---------------------------------------------------------------------------

@dataclass
class SemanticFinding:
    """A semantic observation about the repository architecture."""

    id: str
    category: str  # structure, dependency, coupling, pattern, risk
    title: str
    description: str
    severity: str  # info, warning, error
    evidence: List[str]
    affected_modules: List[str]
    confidence: float

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "evidence": self.evidence,
            "affected_modules": self.affected_modules,
            "confidence": round(self.confidence, 3),
        }


@dataclass
class SemanticRecommendation:
    """An evidence-based semantic recommendation."""

    id: str
    title: str
    description: str
    category: str  # architecture, dependency, injection, quality, extension
    priority: str  # critical, high, medium, low
    confidence: float
    evidence: List[str]
    affected_modules: List[str]
    estimated_effort: str  # trivial, small, medium, large, xlarge
    estimated_impact: str  # low, medium, high, critical
    estimated_risk: str  # low, medium, high
    implementation_order: int

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "confidence": round(self.confidence, 3),
            "evidence": self.evidence,
            "affected_modules": self.affected_modules,
            "estimated_effort": self.estimated_effort,
            "estimated_impact": self.estimated_impact,
            "estimated_risk": self.estimated_risk,
            "implementation_order": self.implementation_order,
        }


# ---------------------------------------------------------------------------
# Repository Complexity
# ---------------------------------------------------------------------------

@dataclass
class RepositoryComplexity:
    """Aggregate complexity metrics for the repository."""

    total_files: int
    total_symbols: int
    total_imports: int
    total_functions: int
    total_classes: int
    avg_imports_per_module: float
    avg_functions_per_file: float
    max_imports_in_module: int
    max_functions_in_file: int
    cyclomatic_complexity_estimate: float
    language_distribution: Dict[str, int]

    def to_dict(self):
        return {
            "total_files": self.total_files,
            "total_symbols": self.total_symbols,
            "total_imports": self.total_imports,
            "total_functions": self.total_functions,
            "total_classes": self.total_classes,
            "avg_imports_per_module": round(self.avg_imports_per_module, 2),
            "avg_functions_per_file": round(self.avg_functions_per_file, 2),
            "max_imports_in_module": self.max_imports_in_module,
            "max_functions_in_file": self.max_functions_in_file,
            "cyclomatic_complexity_estimate": round(self.cyclomatic_complexity_estimate, 2),
            "language_distribution": self.language_distribution,
        }
