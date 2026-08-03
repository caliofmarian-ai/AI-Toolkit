"""
Workspace Orchestrator — CORE-012

Multi-Repository Workspace Orchestrator.

The permanent top-level coordinator of the entire AI CTO architecture.
Manages an unlimited portfolio of software repositories simultaneously.

Coordinates every existing CORE engine:
  CORE-007  Canonical Intelligence
  CORE-008A AI CTO Integration Scanner
  CORE-008B Semantic Repository Intelligence
  CORE-008C Executable Repository Intelligence
  CORE-009  Development State Engine
  CORE-010  Executive Briefing Engine

Public API::

    from python.workspace_orchestrator import WorkspaceOrchestrator

    # Scan all repos in a workspace directory
    orchestrator = WorkspaceOrchestrator(workspace_root="/path/to/workspace")
    result = orchestrator.scan()

    # Produce the workspace dashboard
    dashboard = orchestrator.dashboard()

    # Register a specific repository
    repo = orchestrator.register_repository("/path/to/repo")
"""

from .engine import WorkspaceOrchestrator
from .models import (
    WORKSPACE_SCHEMA_VERSION,
    HEALTH_HEALTHY,
    HEALTH_DEGRADED,
    HEALTH_CRITICAL,
    HEALTH_UNKNOWN,
    RISK_CRITICAL,
    RISK_HIGH,
    RISK_MEDIUM,
    RISK_LOW,
    STATUS_ACTIVE,
    STATUS_BLOCKED,
    STATUS_IDLE,
    STATUS_ARCHIVED,
    STATUS_UNKNOWN,
    STATUS_COMPLIANT,
    STATUS_PARTIAL,
    STATUS_MISSING,
    STATUS_ANALYZED,
    REPO_TYPE_SERVICE,
    REPO_TYPE_LIBRARY,
    REPO_TYPE_TOOL,
    REPO_TYPE_PLATFORM,
    REPO_TYPE_UNKNOWN,
    REPO_CATEGORY_AI,
    REPO_CATEGORY_BACKEND,
    REPO_CATEGORY_FRONTEND,
    REPO_CATEGORY_INFRASTRUCTURE,
    REPO_CATEGORY_DOCUMENTATION,
    REPO_CATEGORY_UNKNOWN,
    WorkspaceRepository,
    WorkspaceDependencyEdge,
    WorkspaceRelationship,
    WorkspaceHealth,
    WorkspaceRecommendation,
    WorkspaceRisk,
    WorkspacePriority,
    WorkspaceScanResult,
    WorkspaceStatistics,
)
from .registry import WorkspaceRegistry, RepositoryRegistry
from .persistence import WorkspacePersistence
from .scanner import WorkspaceDiscoveryEngine, WorkspaceScanner
from .dependency_graph import WorkspaceDependencyGraph, WorkspaceRelationshipAnalyzer
from .intelligence import (
    WorkspaceHealthEngine,
    WorkspacePriorityEngine,
    WorkspaceRiskAnalyzer,
    WorkspaceRecommendationEngine,
)
from .dashboard import WorkspaceExecutiveDashboard, WorkspaceReportGenerator
from .state_manager import WorkspaceStateManager

__all__ = [
    # Main orchestrator
    "WorkspaceOrchestrator",
    # Models
    "WORKSPACE_SCHEMA_VERSION",
    "HEALTH_HEALTHY",
    "HEALTH_DEGRADED",
    "HEALTH_CRITICAL",
    "HEALTH_UNKNOWN",
    "RISK_CRITICAL",
    "RISK_HIGH",
    "RISK_MEDIUM",
    "RISK_LOW",
    "STATUS_ACTIVE",
    "STATUS_BLOCKED",
    "STATUS_IDLE",
    "STATUS_ARCHIVED",
    "STATUS_UNKNOWN",
    "STATUS_COMPLIANT",
    "STATUS_PARTIAL",
    "STATUS_MISSING",
    "STATUS_ANALYZED",
    "REPO_TYPE_SERVICE",
    "REPO_TYPE_LIBRARY",
    "REPO_TYPE_TOOL",
    "REPO_TYPE_PLATFORM",
    "REPO_TYPE_UNKNOWN",
    "REPO_CATEGORY_AI",
    "REPO_CATEGORY_BACKEND",
    "REPO_CATEGORY_FRONTEND",
    "REPO_CATEGORY_INFRASTRUCTURE",
    "REPO_CATEGORY_DOCUMENTATION",
    "REPO_CATEGORY_UNKNOWN",
    "WorkspaceRepository",
    "WorkspaceDependencyEdge",
    "WorkspaceRelationship",
    "WorkspaceHealth",
    "WorkspaceRecommendation",
    "WorkspaceRisk",
    "WorkspacePriority",
    "WorkspaceScanResult",
    "WorkspaceStatistics",
    # Registry
    "WorkspaceRegistry",
    "RepositoryRegistry",
    # Persistence
    "WorkspacePersistence",
    # Scanner
    "WorkspaceDiscoveryEngine",
    "WorkspaceScanner",
    # Dependency graph
    "WorkspaceDependencyGraph",
    "WorkspaceRelationshipAnalyzer",
    # Intelligence
    "WorkspaceHealthEngine",
    "WorkspacePriorityEngine",
    "WorkspaceRiskAnalyzer",
    "WorkspaceRecommendationEngine",
    # Dashboard
    "WorkspaceExecutiveDashboard",
    "WorkspaceReportGenerator",
    # State
    "WorkspaceStateManager",
]
