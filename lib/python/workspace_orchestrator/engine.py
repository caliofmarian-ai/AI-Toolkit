"""
Workspace Orchestrator — Main Engine
CORE-012

WorkspaceOrchestrator: the permanent top-level coordinator of the entire
AI CTO architecture.  Manages an unlimited number of repositories
simultaneously.

Coordinates (but does NOT duplicate) every existing engine:
  CORE-007  Canonical Intelligence
  CORE-008A AI CTO Integration Scanner
  CORE-008B Semantic Repository Intelligence
  CORE-008C Executable Repository Intelligence
  CORE-009  Development State Engine
  CORE-010  Executive Briefing Engine

Produces:
  .ai/workspace/workspace.json
  .ai/workspace/repositories.json
  .ai/workspace/relationships.json
  .ai/workspace/dependencies.json
  .ai/workspace/health.json
  .ai/workspace/priorities.json
  .ai/workspace/recommendations.json
  .ai/workspace/risks.json
  .ai/workspace/dashboard.json
  .ai/workspace/history.json
  .ai/workspace/statistics.json
  AI_CTO_WORKSPACE_DASHBOARD.md
"""

import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from python.agent_runtime.models import AgentContext
from python.agent_runtime.registry import build_runtime
from python.progress_monitor.engine import ProgressMonitor
from python.workspace_manager.engine import WorkspaceManager

from .dashboard import WorkspaceExecutiveDashboard, WorkspaceReportGenerator
from .dependency_graph import WorkspaceDependencyGraph, WorkspaceRelationshipAnalyzer
from .intelligence import (
    WorkspaceHealthEngine,
    WorkspacePriorityEngine,
    WorkspaceRecommendationEngine,
    WorkspaceRiskAnalyzer,
)
from .models import (
    HEALTH_UNKNOWN,
    WorkspaceRepository,
    WorkspaceScanResult,
    WorkspaceStatistics,
    WORKSPACE_SCHEMA_VERSION,
)
from .persistence import WorkspacePersistence
from .registry import RepositoryRegistry
from .scanner import WorkspaceDiscoveryEngine, WorkspaceScanner
from .state_manager import WorkspaceStateManager


class WorkspaceOrchestrator:
    """
    Multi-Repository Workspace Orchestrator — CORE-012.

    The top-level AI CTO controller for an unlimited portfolio of repositories.

    Primary public interface::

        # Scan all repos in a workspace directory
        orchestrator = WorkspaceOrchestrator(workspace_root="/path/to/workspace")
        result = orchestrator.scan()

        # Register a single specific repository
        orchestrator.register_repository("/path/to/repo")

        # Load existing state and generate dashboard
        orchestrator.dashboard()

    The scan() method:
    1. Discovers all git repositories under workspace_root
    2. Scans each using AICTOScannerEngine (CORE-008A)
    3. Builds the cross-repository dependency graph
    4. Analyzes cross-repository relationships
    5. Computes workspace health, priority ranking, risks, and recommendations
    6. Persists all artifacts under .ai/workspace/
    7. Generates AI_CTO_WORKSPACE_DASHBOARD.md

    The execute() method (backward-compatible) runs the full development agent
    pipeline across all discovered repositories, preserving prior behavior.
    """

    def __init__(
        self,
        workspace_root: str = ".",
        output_dir: Optional[str] = None,
        persist: bool = True,
    ) -> None:
        self.workspace_root = str(Path(workspace_root).resolve())
        self.output_dir = str(Path(output_dir).resolve()) if output_dir else self.workspace_root
        self.persist = persist
        self._state_manager = WorkspaceStateManager(self.workspace_root)

    # ------------------------------------------------------------------
    # Public API — scan
    # ------------------------------------------------------------------

    def scan(self, refresh: bool = False) -> WorkspaceScanResult:
        """
        Run a complete workspace scan.

        Args:
            refresh: If True, re-scan all repositories even if they were
                     recently scanned.  If False, uses cached data where
                     possible (future optimisation; currently always full scan).

        Returns:
            WorkspaceScanResult with all intelligence outputs.
        """
        start_time = time.monotonic()
        now = datetime.now(timezone.utc).isoformat()

        # 1. Discover repositories
        discovery = WorkspaceDiscoveryEngine(self.workspace_root)
        discovered = discovery.discover()

        # Also merge any previously registered repositories not in the workspace dir
        self._state_manager.load()
        existing_registry = self._state_manager.registry

        workspace_id = self._state_manager.ensure_workspace_id()

        # 2. Scan each repository
        scanner = WorkspaceScanner()
        scanned_repos: List[WorkspaceRepository] = []
        failed_repos: List[str] = []

        # Scan newly discovered repos
        discovered_names = {item["name"] for item in discovered}
        for item in discovered:
            try:
                repo = scanner.scan_repository(item["name"], item["path"])
                scanned_repos.append(repo)
                self._state_manager.update_repository(repo)
            except Exception as exc:  # noqa: BLE001
                failed_repos.append(item["name"])

        # Merge manually registered repos that weren't auto-discovered
        for repo in existing_registry.all():
            if repo.name not in discovered_names:
                scanned_repos.append(repo)

        # 3. Build dependency graph
        dep_graph = WorkspaceDependencyGraph(scanned_repos)
        dependencies = dep_graph.build()
        cycles = dep_graph.detect_cycles(dependencies)

        # 4. Analyze relationships
        rel_analyzer = WorkspaceRelationshipAnalyzer(scanned_repos)
        relationships = rel_analyzer.analyze()

        # 5. Compute health
        health_engine = WorkspaceHealthEngine()
        health = health_engine.compute(scanned_repos)

        # 6. Compute priorities
        priority_engine = WorkspacePriorityEngine()
        priorities = priority_engine.rank(scanned_repos, dependencies)

        # 7. Analyze risks
        risk_analyzer = WorkspaceRiskAnalyzer()
        risks = risk_analyzer.analyze(scanned_repos, dependencies, cycles)

        # 8. Generate recommendations
        rec_engine = WorkspaceRecommendationEngine()
        recommendations = rec_engine.generate(scanned_repos, health, risks, priorities)

        elapsed = time.monotonic() - start_time

        result = WorkspaceScanResult(
            workspace_id=workspace_id,
            workspace_root=self.workspace_root,
            generated_at=now,
            schema_version=WORKSPACE_SCHEMA_VERSION,
            repositories=scanned_repos,
            dependencies=dependencies,
            relationships=relationships,
            health=health,
            priorities=priorities,
            recommendations=recommendations,
            risks=risks,
            total_repositories=len(scanned_repos),
            scanned_repositories=len(scanned_repos) - len(failed_repos),
            failed_repositories=len(failed_repos),
        )

        stats = WorkspaceStatistics(
            total_repositories=len(scanned_repos),
            healthy_repositories=health.healthy_count,
            degraded_repositories=health.degraded_count,
            critical_repositories=health.critical_count,
            unknown_repositories=health.unknown_count,
            blocked_repositories=sum(1 for r in scanned_repos if r.development_state == "blocked"),
            active_repositories=sum(1 for r in scanned_repos if r.development_state == "active"),
            total_dependencies=len(dependencies),
            total_relationships=len(relationships),
            total_risks=len(risks),
            critical_risks=sum(1 for r in risks if r.severity == "critical"),
            total_recommendations=len(recommendations),
            overall_readiness=health.overall_readiness,
            scan_duration=elapsed,
        )

        # 9. Persist and generate dashboard
        if self.persist:
            persistence = WorkspacePersistence(self.workspace_root)
            persistence.save(result, stats)

            dashboard_engine = WorkspaceExecutiveDashboard()
            dashboard_dict = dashboard_engine.build(result, stats)
            persistence.save_dashboard(workspace_id, now, dashboard_dict)

            report_gen = WorkspaceReportGenerator()
            markdown = report_gen.generate(dashboard_dict)
            report_gen.write(markdown, self.output_dir)

        return result

    # ------------------------------------------------------------------
    # Public API — dashboard
    # ------------------------------------------------------------------

    def dashboard(self) -> Dict[str, Any]:
        """
        Generate (or reload) the workspace dashboard.

        If a previous scan result exists, loads it and regenerates the
        dashboard.  Otherwise triggers a fresh scan.

        Returns:
            Dict with 'markdown', 'dashboard_dict', 'paths'.
        """
        persistence = WorkspacePersistence(self.workspace_root)

        if not persistence.exists():
            # No prior scan — run one now
            result = self.scan()
            repositories = result.repositories
            health = result.health
            priorities = result.priorities
            recommendations = result.recommendations
            risks = result.risks
        else:
            # Load from persistence
            repositories = persistence.load_repositories()
            health = persistence.load_health()
            priorities = persistence.load_priorities()
            recommendations = persistence.load_recommendations()
            risks = persistence.load_risks()
            workspace_meta = persistence.load_workspace()
            workspace_id = workspace_meta.get("workspace_id", "") if workspace_meta else ""
            now = datetime.now(timezone.utc).isoformat()
            stats_obj = persistence.load_statistics()

            if health is None:
                health_engine = WorkspaceHealthEngine()
                health = health_engine.compute(repositories)

            if stats_obj is None:
                stats_obj = WorkspaceStatistics(
                    total_repositories=len(repositories),
                    healthy_repositories=health.healthy_count,
                    degraded_repositories=health.degraded_count,
                    critical_repositories=health.critical_count,
                    unknown_repositories=health.unknown_count,
                    blocked_repositories=0,
                    active_repositories=0,
                    total_dependencies=len(persistence.load_dependencies()),
                    total_relationships=len(persistence.load_relationships()),
                    total_risks=len(risks),
                    critical_risks=sum(1 for r in risks if r.severity == "critical"),
                    total_recommendations=len(recommendations),
                    overall_readiness=health.overall_readiness,
                    scan_duration=0.0,
                )

            dependencies = persistence.load_dependencies()
            relationships = persistence.load_relationships()

            result = WorkspaceScanResult(
                workspace_id=workspace_id,
                workspace_root=self.workspace_root,
                generated_at=now,
                schema_version=WORKSPACE_SCHEMA_VERSION,
                repositories=repositories,
                dependencies=dependencies,
                relationships=relationships,
                health=health,
                priorities=priorities,
                recommendations=recommendations,
                risks=risks,
                total_repositories=len(repositories),
                scanned_repositories=len(repositories),
                failed_repositories=0,
            )

        health_engine = WorkspaceHealthEngine()
        if not repositories:
            health = health_engine.compute([])
        stats_obj = WorkspaceStatistics(
            total_repositories=len(repositories),
            healthy_repositories=health.healthy_count,
            degraded_repositories=health.degraded_count,
            critical_repositories=health.critical_count,
            unknown_repositories=health.unknown_count,
            blocked_repositories=sum(
                1 for r in repositories if r.development_state == "blocked"
            ),
            active_repositories=sum(
                1 for r in repositories if r.development_state == "active"
            ),
            total_dependencies=len(result.dependencies),
            total_relationships=len(result.relationships),
            total_risks=len(risks),
            critical_risks=sum(1 for r in risks if r.severity == "critical"),
            total_recommendations=len(recommendations),
            overall_readiness=health.overall_readiness,
            scan_duration=0.0,
        )

        dashboard_engine = WorkspaceExecutiveDashboard()
        dashboard_dict = dashboard_engine.build(result, stats_obj)

        report_gen = WorkspaceReportGenerator()
        markdown = report_gen.generate(dashboard_dict)

        paths: Dict[str, str] = {}
        if self.persist:
            now = datetime.now(timezone.utc).isoformat()
            workspace_id = self._state_manager.ensure_workspace_id()
            persistence.save_dashboard(workspace_id, now, dashboard_dict)
            paths["dashboard_md"] = report_gen.write(markdown, self.output_dir)
            paths["dashboard_json"] = str(
                Path(self.workspace_root) / ".ai" / "workspace" / "dashboard.json"
            )

        return {
            "markdown": markdown,
            "dashboard_dict": dashboard_dict,
            "paths": paths,
        }

    # ------------------------------------------------------------------
    # Public API — register single repository
    # ------------------------------------------------------------------

    def register_repository(self, repository_path: str) -> WorkspaceRepository:
        """
        Register or update a single repository.

        Scans the repository immediately using AICTOScannerEngine and
        persists the result.
        """
        root = Path(repository_path).resolve()
        scanner = WorkspaceScanner()
        repo = scanner.scan_repository(root.name, str(root))

        self._state_manager.load()
        self._state_manager.register_repository(repo)

        if self.persist:
            persistence = WorkspacePersistence(self.workspace_root)
            repos = self._state_manager.current_repositories()
            workspace_id = self._state_manager.ensure_workspace_id()
            now = datetime.now(timezone.utc).isoformat()
            health_engine = WorkspaceHealthEngine()
            health = health_engine.compute(repos)
            dep_graph = WorkspaceDependencyGraph(repos)
            deps = dep_graph.build()
            cycles = dep_graph.detect_cycles(deps)
            rel_analyzer = WorkspaceRelationshipAnalyzer(repos)
            relationships = rel_analyzer.analyze()
            priority_engine = WorkspacePriorityEngine()
            priorities = priority_engine.rank(repos, deps)
            risk_analyzer = WorkspaceRiskAnalyzer()
            risks = risk_analyzer.analyze(repos, deps, cycles)
            rec_engine = WorkspaceRecommendationEngine()
            recommendations = rec_engine.generate(repos, health, risks, priorities)

            result = WorkspaceScanResult(
                workspace_id=workspace_id,
                workspace_root=self.workspace_root,
                generated_at=now,
                schema_version=WORKSPACE_SCHEMA_VERSION,
                repositories=repos,
                dependencies=deps,
                relationships=relationships,
                health=health,
                priorities=priorities,
                recommendations=recommendations,
                risks=risks,
                total_repositories=len(repos),
                scanned_repositories=len(repos),
                failed_repositories=0,
            )
            stats = WorkspaceStatistics(
                total_repositories=len(repos),
                healthy_repositories=health.healthy_count,
                degraded_repositories=health.degraded_count,
                critical_repositories=health.critical_count,
                unknown_repositories=health.unknown_count,
                blocked_repositories=0,
                active_repositories=0,
                total_dependencies=len(deps),
                total_relationships=len(relationships),
                total_risks=len(risks),
                critical_risks=sum(1 for r in risks if r.severity == "critical"),
                total_recommendations=len(recommendations),
                overall_readiness=health.overall_readiness,
                scan_duration=0.0,
            )
            persistence.save(result, stats)

        return repo

    # ------------------------------------------------------------------
    # Backward-compatible execute() — runs the full development agent pipeline
    # ------------------------------------------------------------------

    def execute(self, workspace: str) -> List[Dict[str, Any]]:
        """
        Backward-compatible method: runs DevelopmentAgent across every
        repository in *workspace*.

        This method is preserved for compatibility with the original
        WorkspaceOrchestrator interface.  New code should use scan().
        """
        runtime = build_runtime()
        monitor = ProgressMonitor()
        repositories = WorkspaceManager().discover(workspace)

        monitor.section("Workspace Execution")
        monitor.message(f"Repositories discovered: {len(repositories)}")

        results = []
        for repo in repositories:
            try:
                started = monitor.start(repo["name"])
                result = runtime.execute(
                    "develop",
                    AgentContext(repository=repo["path"]),
                )
                elapsed = monitor.finish(repo["name"], started)
                results.append({
                    "repository": repo["name"],
                    "status": "SUCCESS",
                    "report_score": result.data["inspection"]["repository_score"],
                    "health": result.data["inspection"]["repository_health"],
                    "recommendations": len(result.data["recommendations_generated"]),
                    "batches": len(result.data["generated_batches"]),
                    "elapsed": elapsed,
                })
            except Exception as exc:  # noqa: BLE001
                elapsed = monitor.finish(repo["name"], started)
                results.append({
                    "repository": repo["name"],
                    "status": "FAILED",
                    "error": str(exc),
                })

        monitor.total()
        return results
