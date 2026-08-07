from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

from python.context_synchronization_engine.engine import GitContextProvider
from python.repository_engine.engine import RepositoryEngine
from python.repository_engine.serializer import RepositoryProfileSerializer
from python.workspace_orchestrator import WorkspaceOrchestrator
from python.workspace_orchestrator.persistence import WorkspacePersistence


@dataclass(frozen=True)
class CapabilityDefinition:
    slug: str
    title: str
    purpose: str
    description: str
    architecture: str
    inputs: List[str]
    outputs: List[str]
    dependencies: List[str]
    related_paths: List[str]
    related_tests: List[str]
    cli_commands: List[str]
    dashboard_pages: List[str]
    future_roadmap: str
    known_limitations: str
    next_milestone: str
    engineering_decisions: List[str]
    why_problem: str
    why_architecture: str
    why_dependencies: str
    repository_usage: List[str]
    justification_documents: List[str]
    target_epic: str = "EPIC-003"


CAPABILITY_DEFINITIONS: List[CapabilityDefinition] = [
    CapabilityDefinition(
        slug="dashboard",
        title="Dashboard",
        purpose="Provide the primary Engineering Operating System interface.",
        description="Aggregates repository, workspace, reports, and engineering-session context into a single local application.",
        architecture="A stdlib HTTP server renders HTML pages from existing repository artifacts and engines without adding a frontend framework.",
        inputs=["repository state", "workspace state", "reports", "capability metadata"],
        outputs=["home page", "project manager page", "engineering explorer pages", "JSON endpoints"],
        dependencies=["repository-engine", "engineering-session", "project-manager"],
        related_paths=["bin/ai", "lib/python/dashboard", "lib/python/cli/main.py"],
        related_tests=["tests/test_dashboard.sh", "tests/test_dashboard_navigation.sh"],
        cli_commands=["bin/ai dashboard serve"],
        dashboard_pages=["/", "/projects", "/session", "/explorer", "/reports"],
        future_roadmap="Expand from local HTML pages into richer live operational views fed by more engines.",
        known_limitations="The MVP is server-rendered and depends on locally available repository artifacts.",
        next_milestone="Interactive engineering actions from the dashboard.",
        engineering_decisions=[
            "Reuse stdlib HTTP patterns already present in runtime interfaces.",
            "Render pages on the server to avoid adding a web framework.",
        ],
        why_problem="Engineers need one place to see context, progress, health, and next actions before starting work.",
        why_architecture="Server-rendered HTML keeps the MVP lightweight and aligned with the repository's existing minimal-dependency approach.",
        why_dependencies="The dashboard exists to expose the outputs of existing engines rather than duplicate them.",
        repository_usage=["AI-Toolkit"],
        justification_documents=["AI_CTO_EXECUTIVE_BRIEFING.md", "AI_CTO_INTEGRATION_REPORT.md"],
    ),
    CapabilityDefinition(
        slug="project-manager",
        title="Project Manager",
        purpose="Coordinate multiple repositories from one workspace view.",
        description="Tracks repository health, implementation progress, active branch, and workspace-level priorities.",
        architecture="Builds on WorkspaceOrchestrator persistence and dashboard summaries, then renders repository cards and tables.",
        inputs=["workspace scan results", "repository registrations", "repository reports"],
        outputs=["multi-repository summaries", "repository health table", "implementation progress overview"],
        dependencies=["repository-engine"],
        related_paths=["lib/python/workspace_orchestrator", "lib/python/dashboard"],
        related_tests=["tests/test_project_manager.sh"],
        cli_commands=["python3 -m python.cli.main workspace --scan", "bin/ai dashboard serve"],
        dashboard_pages=["/projects"],
        future_roadmap="Add remote repository registration and cross-repository execution workflows.",
        known_limitations="Only repositories available in the local workspace or persisted registry can be shown.",
        next_milestone="Workspace registration and refresh controls from the UI.",
        engineering_decisions=[
            "Use WorkspaceOrchestrator as the single source of workspace truth.",
            "Map repository readiness to implementation progress instead of introducing a second progress model.",
        ],
        why_problem="Engineering work spans multiple repositories and needs cross-repository visibility.",
        why_architecture="WorkspaceOrchestrator already computes health, risks, and priorities, so the dashboard should only present those outputs.",
        why_dependencies="Repository-level health and statistics are prerequisites for any useful project-management surface.",
        repository_usage=["AI-Toolkit", "Trading Signals Platform", "DROPi"],
        justification_documents=["AI_CTO_WORKSPACE_DASHBOARD.md", "AI_CTO_EXECUTIVE_BRIEFING.md"],
    ),
    CapabilityDefinition(
        slug="engineering-session",
        title="Engineering Session",
        purpose="Persist the current engineering context and recent activity.",
        description="Shows current project, repository, branch, sprint, epic, task, runtime, AI provider, and session history.",
        architecture="Reads development state, recent events, sessions, and git context to reconstruct a live engineering session view.",
        inputs=["development state", "session artifacts", "git metadata"],
        outputs=["session summary", "session history", "recent activity"],
        dependencies=["runtime", "repository-engine"],
        related_paths=["lib/python/development_state_engine", ".ai/development_state", ".ai/sessions", "lib/python/dashboard"],
        related_tests=["tests/test_engineering_session.sh"],
        cli_commands=["bin/ai dashboard serve"],
        dashboard_pages=["/session", "/"],
        future_roadmap="Turn session history into a full operational timeline and resumable workflow console.",
        known_limitations="The MVP reflects local persisted state and does not yet coordinate active remote agents.",
        next_milestone="Session actions and resumable execution controls.",
        engineering_decisions=[
            "Prefer persisted development state over recomputing every field at request time.",
        ],
        why_problem="Every engineering action should belong to a visible and resumable session.",
        why_architecture="The development-state artifacts already encode session context and recent changes.",
        why_dependencies="The dashboard must be grounded in the same runtime context used by other engines.",
        repository_usage=["AI-Toolkit"],
        justification_documents=["AI_CTO_EXECUTION_MODEL.md", "AI_CTO_EXECUTION_REPORT.md"],
    ),
    CapabilityDefinition(
        slug="engineering-explorer",
        title="Engineering Explorer",
        purpose="Expose every capability as an explorable product surface.",
        description="Provides modular navigation and dedicated pages for implemented, planned, and future capabilities.",
        architecture="Renders capability metadata plus live implementation evidence gathered from related files, tests, and reports.",
        inputs=["capability registry", "repository file system", "tests", "reports"],
        outputs=["capability index", "capability detail pages", "status matrix"],
        dependencies=["dashboard", "repository-engine"],
        related_paths=["lib/python/dashboard", "lib/python/repository_engine", "lib/python/workspace_orchestrator"],
        related_tests=["tests/test_engineering_explorer.sh", "tests/test_dashboard_navigation.sh"],
        cli_commands=["bin/ai dashboard serve"],
        dashboard_pages=["/explorer", "/capabilities/dashboard"],
        future_roadmap="Add search, graph navigation, and richer cross-linking between reports, files, and decisions.",
        known_limitations="Capabilities are defined in code for the MVP and not yet extended by plugin registration.",
        next_milestone="Dynamic capability registration from engines.",
        engineering_decisions=[
            "Keep capability metadata in code so it ships with the product and stays close to implementation.",
        ],
        why_problem="Users should understand the entire product by exploring it.",
        why_architecture="A capability registry enables modular navigation and uniform self-documentation.",
        why_dependencies="Explorer pages depend on the dashboard shell and repository evidence to stay truthful.",
        repository_usage=["AI-Toolkit"],
        justification_documents=["AI_CTO_PLANNING_REPORT.md", "AI_CTO_EXECUTIVE_BRIEFING.md"],
    ),
    CapabilityDefinition(
        slug="repository-engine",
        title="Repository Engine",
        purpose="Inspect repositories and provide foundational engineering intelligence.",
        description="Surfaces repository profile, languages, stack, dependencies, health checks, and statistics.",
        architecture="Uses RepositoryEngine plus existing inspection artifacts instead of duplicating scan logic.",
        inputs=["repository filesystem", "semantic analysis", "dependency manifests"],
        outputs=["repository profile", "inspection reports", "statistics"],
        dependencies=[],
        related_paths=["lib/python/repository_engine", ".ai/reports"],
        related_tests=["tests/test_repository_engine_inspect.sh", "tests/test_repository_profile.sh"],
        cli_commands=["python3 -m python.cli.main inspect .", "bin/ai inspect ."],
        dashboard_pages=["/", "/reports", "/capabilities/repository-engine"],
        future_roadmap="Add deeper trend analysis and richer diff-aware repository insights.",
        known_limitations="Insights are local to the current repository snapshot.",
        next_milestone="Expose more repository-engine detail through dashboard JSON endpoints.",
        engineering_decisions=[
            "The dashboard reads repository-engine output directly to avoid introducing a second inspection model.",
        ],
        why_problem="All higher-order engineering tooling depends on understanding the repository accurately.",
        why_architecture="RepositoryEngine already computes the required profile and health information.",
        why_dependencies="It is the base layer other operating-system capabilities consume.",
        repository_usage=["AI-Toolkit", "Trading Signals Platform", "DROPi"],
        justification_documents=["AI_CTO_INTEGRATION_REPORT.md"],
    ),
    CapabilityDefinition(
        slug="runtime",
        title="Runtime",
        purpose="Provide persistent execution state and HTTP interfaces for local operations.",
        description="Exposes the running context, recent execution state, and runtime-oriented artifacts.",
        architecture="Builds on runtime and development-state persistence rather than creating separate dashboard-specific state.",
        inputs=["runtime state", "development state", "execution artifacts"],
        outputs=["runtime summary", "status view", "health endpoints"],
        dependencies=[],
        related_paths=["lib/python/runtime", "lib/python/development_state_engine", ".ai/runtime", ".ai/execution"],
        related_tests=["tests/test_runtime_acceptance.sh", "tests/test_runtime_health.sh"],
        cli_commands=["bash bin/runtime-server"],
        dashboard_pages=["/", "/session"],
        future_roadmap="Integrate runtime controls, jobs, and live execution telemetry.",
        known_limitations="The dashboard shows persisted runtime context and not a live scheduler console.",
        next_milestone="Live runtime metrics and queue visualization.",
        engineering_decisions=[
            "Leverage existing runtime artifacts and keep the dashboard read-oriented for the MVP.",
        ],
        why_problem="Engineers need immediate visibility into runtime state before making changes.",
        why_architecture="Runtime already has a stdlib-first footprint that aligns with the dashboard server.",
        why_dependencies="Session state and report generation depend on runtime information being visible.",
        repository_usage=["AI-Toolkit"],
        justification_documents=["AI_CTO_EXECUTION_MODEL.md", "railway.json"],
    ),
    CapabilityDefinition(
        slug="validation-engine",
        title="Validation Engine",
        purpose="Surface repository validation and future validation reporting.",
        description="Represents validation-related capabilities inside the explorer, even where deeper UI views are still future work.",
        architecture="References existing validation engine modules and tests, then exposes their current implementation evidence and roadmap.",
        inputs=["validation engine code", "validation tests"],
        outputs=["capability status", "related tests", "CLI references"],
        dependencies=["repository-engine"],
        related_paths=["lib/python/validation_engine"],
        related_tests=["tests/test_validation_engine.sh"],
        cli_commands=["python3 -m python.cli.main validate"],
        dashboard_pages=["/capabilities/validation-engine"],
        future_roadmap="Add dedicated validation reports once those reports are generated by the engine.",
        known_limitations="The MVP surfaces implementation evidence but not a dedicated validation report viewer.",
        next_milestone="First validation report page.",
        engineering_decisions=[
            "Make planned and partial capabilities visible now so the explorer documents the roadmap.",
        ],
        why_problem="Validation is a core engineering operating-system concern.",
        why_architecture="The explorer can reveal implemented evidence before a full dashboard surface exists.",
        why_dependencies="Validation is downstream of repository understanding and runtime state.",
        repository_usage=["AI-Toolkit"],
        justification_documents=["AI_CTO_EXECUTION_REPORT.md"],
    ),
]


class EngineeringDashboardService:
    def __init__(
        self,
        repository_root: str = ".",
        workspace_root: Optional[str] = None,
        cache_ttl_seconds: float = 5.0,
    ) -> None:
        self.repository_root = Path(repository_root).resolve()
        self.workspace_root = (
            Path(workspace_root).resolve()
            if workspace_root
            else self.repository_root.parent
        )
        self.cache_ttl_seconds = cache_ttl_seconds
        self._cache_expires_at = 0.0
        self._cached_payload: Optional[Dict[str, Any]] = None

    def build(self, refresh: bool = False) -> Dict[str, Any]:
        now = time.time()
        if (
            not refresh
            and self._cached_payload is not None
            and now < self._cache_expires_at
        ):
            return self._cached_payload

        session = self._load_session()
        repository = self._load_repository_profile()
        workspace = self._load_workspace_summary()
        reports = self._load_reports()
        capabilities = self._load_capabilities(workspace, session)

        payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "repository_root": str(self.repository_root),
            "workspace_root": str(self.workspace_root),
            "navigation": self._navigation(),
            "home": self._home_payload(repository, workspace, session, reports),
            "workspace": workspace,
            "session": session,
            "reports": reports,
            "capabilities": capabilities,
        }
        self._cached_payload = payload
        self._cache_expires_at = now + self.cache_ttl_seconds
        return payload

    def render_home(self, payload: Optional[Dict[str, Any]] = None) -> str:
        data = payload or self.build()
        home = data["home"]
        return self._page(
            "Engineering Operating System",
            data,
            [
                self._summary_grid(home["summary_cards"]),
                self._section("Recent Activity", self._activity_table(home["recent_activity"])),
                self._section("Recent Reports", self._report_table(home["recent_reports"])),
                self._section("Repository Health", self._health_checks(home["repository_health"])),
                self._section("Repository Statistics", self._metrics_table(home["repository_statistics"])),
                self._section("Latest Repository Inspection", self._inspection_panel(home["latest_repository_inspection"])),
            ],
        )

    def render_projects(self, payload: Optional[Dict[str, Any]] = None) -> str:
        data = payload or self.build()
        workspace = data["workspace"]
        return self._page(
            "Project Manager",
            data,
            [
                self._summary_grid(workspace["summary_cards"]),
                self._section("Managed Repositories", self._repository_table(workspace["repositories"])),
            ],
        )

    def render_session(self, payload: Optional[Dict[str, Any]] = None) -> str:
        data = payload or self.build()
        session = data["session"]
        return self._page(
            "Engineering Session",
            data,
            [
                self._summary_grid(session["summary_cards"]),
                self._section("Session History", self._session_history(session["session_history"])),
                self._section("Recent Activity", self._activity_table(session["recent_activity"])),
            ],
        )

    def render_explorer(self, payload: Optional[Dict[str, Any]] = None) -> str:
        data = payload or self.build()
        rows = []
        for capability in data["capabilities"]["items"]:
            rows.append(
                "<tr>"
                f"<td><a href=\"/capabilities/{escape(capability['slug'])}\">{escape(capability['title'])}</a></td>"
                f"<td>{escape(capability['status'])}</td>"
                f"<td>{capability['implementation_percentage']}%</td>"
                f"<td>{escape(capability['target_epic'])}</td>"
                f"<td>{escape(', '.join(capability.get('blocking_dependencies') or []) or 'None')}</td>"
                "</tr>"
            )
        table = (
            "<table><thead><tr><th>Capability</th><th>Status</th><th>Progress</th><th>Target Epic</th><th>Blocking Dependencies</th></tr></thead>"
            f"<tbody>{''.join(rows)}</tbody></table>"
        )
        return self._page(
            "Engineering Explorer",
            data,
            [
                self._summary_grid(data["capabilities"]["summary_cards"]),
                self._section("Capability Matrix", table),
            ],
        )

    def render_reports(self, payload: Optional[Dict[str, Any]] = None) -> str:
        data = payload or self.build()
        return self._page(
            "Reports",
            data,
            [
                self._summary_grid(data["reports"]["summary_cards"]),
                self._section("Generated Reports", self._report_table(data["reports"]["items"])),
            ],
        )

    def render_capability(self, slug: str, payload: Optional[Dict[str, Any]] = None) -> Optional[str]:
        data = payload or self.build()
        capability = next(
            (item for item in data["capabilities"]["items"] if item["slug"] == slug),
            None,
        )
        if capability is None:
            return None
        details = (
            self._definition_list(
                [
                    ("Status", capability["status"]),
                    ("Purpose", capability["purpose"]),
                    ("Description", capability["description"]),
                    ("Architecture", capability["architecture"]),
                    ("Inputs", ", ".join(capability["inputs"])),
                    ("Outputs", ", ".join(capability["outputs"])),
                    ("Dependencies", ", ".join(capability["dependencies"]) or "None"),
                    ("Current implementation", capability["current_implementation"]),
                    ("Current implementation percentage", f"{capability['implementation_percentage']}%"),
                    ("Current Epic", capability["current_epic"]),
                    ("Current Pull Request", capability["current_pull_request"] or "None"),
                    ("Related Files", ", ".join(capability["related_files"]) or "None"),
                    ("Related Tests", ", ".join(capability["related_tests"]) or "None"),
                    ("CLI Commands", ", ".join(capability["cli_commands"]) or "None"),
                    ("Dashboard Pages", ", ".join(capability["dashboard_pages"]) or "None"),
                    ("Repository Usage", ", ".join(capability["repository_usage"]) or "None"),
                    ("Future Roadmap", capability["future_roadmap"]),
                    ("Known Limitations", capability["known_limitations"]),
                    ("Next Milestone", capability["next_milestone"]),
                    ("Engineering Decisions", "; ".join(capability["engineering_decisions"]) or "None"),
                    ("Unlock Conditions", "; ".join(capability["unlock_conditions"]) or "None"),
                    ("Blocking Dependencies", ", ".join(capability["blocking_dependencies"]) or "None"),
                    ("Related Issues", ", ".join(capability["related_issues"]) or "None"),
                    ("Justification Documents", ", ".join(capability["justification_documents"]) or "None"),
                ]
            )
        )
        why = self._definition_list(
            [
                ("Why does this capability exist?", capability["why"]["existence"]),
                ("Which engineering problem does it solve?", capability["why"]["problem"]),
                ("Why was this architecture chosen?", capability["why"]["architecture"]),
                ("Which future engines depend on it?", ", ".join(capability["why"]["future_dependencies"]) or "None"),
                ("Which repositories currently use it?", ", ".join(capability["why"]["repositories"]) or "None"),
                ("What would break if it disappeared?", capability["why"]["breakage"]),
                ("Which documents justify its existence?", ", ".join(capability["why"]["documents"]) or "None"),
            ]
        )
        return self._page(
            capability["title"],
            data,
            [
                self._summary_grid(
                    [
                        {"label": "Status", "value": capability["status"]},
                        {"label": "Implementation", "value": f"{capability['implementation_percentage']}%"},
                        {"label": "Target Epic", "value": capability["target_epic"]},
                    ]
                ),
                self._section("Capability Detail", details),
                self._section("WHY", why),
            ],
        )

    def _load_repository_profile(self) -> Dict[str, Any]:
        inspection = self._latest_json(self.repository_root / ".ai" / "reports", "inspect-*.json")
        if inspection is None:
            profile = RepositoryEngine(self.repository_root).profile()
            inspection = RepositoryProfileSerializer.to_dict(profile)
        metrics = inspection.get("metrics", {})
        health = inspection.get("health_summary", {})
        dependencies = inspection.get("dependencies", {})
        return {
            "name": inspection.get("name", self.repository_root.name),
            "path": inspection.get("path", str(self.repository_root)),
            "metrics": metrics,
            "health_summary": health,
            "languages": metrics.get("language_distribution", {}),
            "tech_stack": inspection.get("tech_stack", []),
            "dependency_manifests": list((dependencies.get("manifests", {}) or {}).keys()),
            "latest_inspection": inspection,
        }

    def _load_workspace_summary(self) -> Dict[str, Any]:
        orchestrator = WorkspaceOrchestrator(
            workspace_root=str(self.workspace_root),
            output_dir=str(self.workspace_root),
            persist=True,
        )
        persistence = WorkspacePersistence(str(self.workspace_root))
        if not persistence.exists():
            orchestrator.scan()
        repositories = persistence.load_repositories()
        if not any(
            Path(repo.repository_root).resolve() == self.repository_root
            for repo in repositories
        ):
            orchestrator.register_repository(str(self.repository_root))
            repositories = persistence.load_repositories()
        dashboard_result = orchestrator.dashboard()["dashboard_dict"]
        summary = dashboard_result.get("workspace_summary", {})
        repos = []
        for repo in repositories:
            repos.append(
                {
                    "name": repo.name,
                    "health": repo.repository_health,
                    "current_branch": repo.current_branch or repo.default_branch,
                    "last_inspection": repo.last_scan or repo.last_refresh or "n/a",
                    "active_sprint": repo.current_milestone or repo.current_batch or repo.current_epic or "n/a",
                    "active_issue": repo.current_issue or "n/a",
                    "repository_statistics": f"readiness {repo.readiness:.1f}%",
                    "implementation_progress": f"{repo.readiness:.1f}%",
                    "root": repo.repository_root,
                }
            )
        return {
            "workspace_id": dashboard_result.get("workspace_id", ""),
            "workspace_root": dashboard_result.get("workspace_root", str(self.workspace_root)),
            "summary": summary,
            "repositories": repos,
            "dashboard": dashboard_result,
            "summary_cards": [
                {"label": "Current Project", "value": self.repository_root.name},
                {"label": "Repositories", "value": str(summary.get("total_repositories", len(repos)))},
                {"label": "Repository Health", "value": str(summary.get("overall_health", "unknown")).upper()},
                {"label": "Implementation Progress", "value": f"{summary.get('overall_readiness', 0.0):.1f}%"},
            ],
        }

    def _load_session(self) -> Dict[str, Any]:
        state = self._read_json(self.repository_root / ".ai" / "development_state" / "current_state.json") or {}
        snapshot = self._read_json(self.repository_root / ".ai" / "development_state" / "executive_snapshot.json") or {}
        events = self._read_json(self.repository_root / ".ai" / "development_state" / "events.json") or {}
        git_context = GitContextProvider(str(self.repository_root)).collect()
        planning_state = state.get("planning_state", {})
        workspace_state = state.get("workspace_state", {})
        repository_state = state.get("repository_state", {})
        execution_state = state.get("execution_state", {})
        current_context = snapshot.get("current_context", {})
        ai_provider = self._detect_ai_provider()
        session_history = []
        sessions_dir = self.repository_root / ".ai" / "sessions"
        if sessions_dir.is_dir():
            for path in sorted(sessions_dir.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
                session_payload = self._read_json(path) or {}
                session_history.append(
                    {
                        "identifier": session_payload.get("identifier", path.stem),
                        "status": session_payload.get("status", "UNKNOWN"),
                        "repository": session_payload.get("repository", "."),
                        "completed_steps": session_payload.get("completed_steps", []),
                    }
                )
        recent_activity = []
        for event in (events.get("events") or [])[-8:]:
            recent_activity.append(
                {
                    "timestamp": event.get("timestamp", ""),
                    "title": event.get("event_type", "event"),
                    "details": ", ".join(
                        f"{key}={value}"
                        for key, value in list((event.get("context") or {}).items())[:3]
                    ),
                }
            )
        return {
            "current_project": workspace_state.get("active_project", self.repository_root.name),
            "current_repository": repository_state.get("repository", self.repository_root.name),
            "current_branch": repository_state.get("branch", git_context.get("current_branch", "")),
            "current_workspace": workspace_state.get("active_workspace", str(self.workspace_root)),
            "current_sprint": planning_state.get("current_sprint", current_context.get("current_epic", "")),
            "current_epic": current_context.get("current_epic", workspace_state.get("current_objective", "")),
            "current_issue": current_context.get("current_issue", ""),
            "current_engineering_task": workspace_state.get("current_task", current_context.get("current_task", "")),
            "current_runtime": execution_state.get("current_executor", "runtime"),
            "current_runtime_status": repository_state.get("repository_health", "unknown"),
            "current_ai_provider": ai_provider,
            "session_history": session_history,
            "recent_activity": recent_activity,
            "summary_cards": [
                {"label": "Current Project", "value": workspace_state.get("active_project", self.repository_root.name)},
                {"label": "Current Repository", "value": repository_state.get("repository", self.repository_root.name)},
                {"label": "Current Branch", "value": repository_state.get("branch", git_context.get("current_branch", ""))},
                {"label": "Current Workspace", "value": workspace_state.get("active_workspace", str(self.workspace_root))},
                {"label": "Current Sprint", "value": planning_state.get("current_sprint", "n/a")},
                {"label": "Current Epic", "value": current_context.get("current_epic", "n/a")},
                {"label": "Current Issue", "value": current_context.get("current_issue", "n/a")},
                {"label": "Current Engineering Task", "value": workspace_state.get("current_task", "n/a")},
                {"label": "Current Runtime", "value": execution_state.get("current_executor", "runtime")},
                {"label": "Current AI Provider", "value": ai_provider},
            ],
        }

    def _load_reports(self) -> Dict[str, Any]:
        report_specs = [
            ("Repository Inspection", self._latest_json_path(self.repository_root / ".ai" / "reports", "inspect-*.json")),
            ("Executive Briefing", self.repository_root / ".ai" / "executive" / "briefing.json"),
            ("Planning", self.repository_root / ".ai" / "planning" / "planning.json"),
            ("Execution", self.repository_root / ".ai" / "execution" / "execution.json"),
            ("Self Evaluation", self.repository_root / ".ai" / "self_evaluation" / "evaluation.json"),
            ("Self Improvement", self.repository_root / ".ai" / "self_improvement" / "improvements.json"),
            ("Workspace Dashboard", self.workspace_root / ".ai" / "workspace" / "dashboard.json"),
        ]
        available_report_specs = [path for _, path in report_specs if path is not None]
        items = []
        for title, path in report_specs:
            if path is None or not path.exists():
                continue
            payload = self._read_json(path) or {}
            items.append(
                {
                    "title": title,
                    "path": str(path),
                    "generated_at": payload.get("generated_at", self._iso_from_timestamp(path.stat().st_mtime)),
                    "description": self._report_description(title, payload),
                }
            )
        return {
            "items": items,
            "summary_cards": [
                {"label": "Recent Reports", "value": str(len(items))},
                {"label": "Latest Report", "value": items[0]["title"] if items else "None"},
                {"label": "Report Coverage", "value": f"{len(items)}/{len(available_report_specs)}"},
            ],
        }

    def _load_capabilities(self, workspace: Mapping[str, Any], session: Mapping[str, Any]) -> Dict[str, Any]:
        statuses: Dict[str, str] = {}
        items: List[Dict[str, Any]] = []
        for definition in CAPABILITY_DEFINITIONS:
            resolved_paths = self._resolve_related_paths(definition.related_paths)
            resolved_tests = self._resolve_related_paths(definition.related_tests)
            file_ratio = len(resolved_paths) / len(definition.related_paths) if definition.related_paths else 1.0
            test_ratio = len(resolved_tests) / len(definition.related_tests) if definition.related_tests else 1.0
            implementation_percentage = int(round(((file_ratio * 0.75) + (test_ratio * 0.25)) * 100))
            status = "Planned"
            if implementation_percentage >= 85:
                status = "Available"
            elif implementation_percentage > 0:
                status = "In Development"
            statuses[definition.slug] = status
            items.append(
                {
                    "slug": definition.slug,
                    "title": definition.title,
                    "status": status,
                    "purpose": definition.purpose,
                    "description": definition.description,
                    "architecture": definition.architecture,
                    "inputs": definition.inputs,
                    "outputs": definition.outputs,
                    "dependencies": definition.dependencies,
                    "implementation_percentage": implementation_percentage,
                    "current_implementation": f"{len(resolved_paths)} related path(s) and {len(resolved_tests)} related test(s) detected.",
                    "current_epic": definition.target_epic,
                    "current_pull_request": session.get("current_branch", "") if session.get("current_branch", "") not in {"main", "master"} else "",
                    "related_files": [self._relative_path(path) for path in resolved_paths],
                    "related_tests": [self._relative_path(path) for path in resolved_tests],
                    "cli_commands": definition.cli_commands,
                    "dashboard_pages": definition.dashboard_pages,
                    "future_roadmap": definition.future_roadmap,
                    "known_limitations": definition.known_limitations,
                    "next_milestone": definition.next_milestone,
                    "engineering_decisions": definition.engineering_decisions,
                    "unlock_conditions": self._unlock_conditions(definition, resolved_paths, resolved_tests),
                    "blocking_dependencies": [],
                    "target_epic": definition.target_epic,
                    "related_issues": [session.get("current_issue", "")] if session.get("current_issue") else [],
                    "repository_usage": self._repository_usage(definition, workspace),
                    "justification_documents": definition.justification_documents,
                    "why": {
                        "existence": definition.purpose,
                        "problem": definition.why_problem,
                        "architecture": definition.why_architecture,
                        "future_dependencies": definition.dependencies,
                        "repositories": self._repository_usage(definition, workspace),
                        "breakage": f"Navigation, reports, or engineering context for {definition.title} would disappear from the operating system.",
                        "documents": definition.justification_documents,
                    },
                }
            )
        for item in items:
            blocking = [dependency for dependency in item["dependencies"] if statuses.get(dependency) not in {None, "Available"}]
            item["blocking_dependencies"] = blocking
            if item["status"] == "Planned" and blocking:
                item["status"] = "Blocked"
        available = sum(1 for item in items if item["status"] == "Available")
        in_development = sum(1 for item in items if item["status"] == "In Development")
        planned = sum(1 for item in items if item["status"] == "Planned")
        blocked = sum(1 for item in items if item["status"] == "Blocked")
        return {
            "items": items,
            "summary_cards": [
                {"label": "Capabilities", "value": str(len(items))},
                {"label": "Available", "value": str(available)},
                {"label": "In Development", "value": str(in_development)},
                {"label": "Planned", "value": str(planned)},
                {"label": "Blocked", "value": str(blocked)},
            ],
        }

    def _home_payload(
        self,
        repository: Mapping[str, Any],
        workspace: Mapping[str, Any],
        session: Mapping[str, Any],
        reports: Mapping[str, Any],
    ) -> Dict[str, Any]:
        latest_inspection = repository["latest_inspection"]
        return {
            "summary_cards": [
                {"label": "Current Project", "value": session["current_project"]},
                {"label": "Current Repository", "value": session["current_repository"]},
                {"label": "Current Branch", "value": session["current_branch"]},
                {"label": "Current Sprint", "value": session["current_sprint"]},
                {"label": "Current Epic", "value": session["current_epic"]},
                {"label": "Current Issue", "value": session["current_issue"] or "n/a"},
                {"label": "Current Engineering Task", "value": session["current_engineering_task"]},
                {"label": "Current AI Provider", "value": session["current_ai_provider"]},
                {"label": "Current Runtime Status", "value": session["current_runtime_status"]},
                {"label": "Repository Health", "value": str(repository["health_summary"].get("status", "unknown"))},
                {"label": "Repository Statistics", "value": f"{repository['metrics'].get('total_files', 0)} files"},
                {"label": "Latest Repository Inspection", "value": latest_inspection.get("name", repository["name"])},
            ],
            "recent_activity": session["recent_activity"],
            "recent_reports": reports["items"][:5],
            "repository_health": repository["health_summary"],
            "repository_statistics": repository["metrics"],
            "latest_repository_inspection": {
                "languages": repository["languages"],
                "tech_stack": repository["tech_stack"],
                "dependency_manifests": repository["dependency_manifests"],
                "workspace_health": workspace["summary"].get("overall_health", "unknown"),
            },
        }

    def _navigation(self) -> List[Dict[str, str]]:
        return [
            {"href": "/", "label": "Home"},
            {"href": "/projects", "label": "Project Manager"},
            {"href": "/session", "label": "Engineering Session"},
            {"href": "/explorer", "label": "Engineering Explorer"},
            {"href": "/reports", "label": "Reports"},
        ]

    def _resolve_related_paths(self, relative_paths: Iterable[str]) -> List[Path]:
        resolved = []
        for relative_path in relative_paths:
            path = self.repository_root / relative_path
            if path.exists():
                resolved.append(path)
        return resolved

    def _unlock_conditions(
        self,
        definition: CapabilityDefinition,
        resolved_paths: List[Path],
        resolved_tests: List[Path],
    ) -> List[str]:
        conditions = []
        missing_paths = [path for path in definition.related_paths if not (self.repository_root / path).exists()]
        missing_tests = [path for path in definition.related_tests if not (self.repository_root / path).exists()]
        if missing_paths:
            conditions.append(f"implement {len(missing_paths)} missing related path(s)")
        if missing_tests:
            conditions.append(f"add {len(missing_tests)} missing related test(s)")
        if not conditions and resolved_paths:
            conditions.append("maintain current implementation and validation coverage")
        return conditions

    def _repository_usage(self, definition: CapabilityDefinition, workspace: Mapping[str, Any]) -> List[str]:
        repositories = [repo["name"] for repo in workspace.get("repositories", [])]
        if not repositories:
            return list(definition.repository_usage)
        return [name for name in repositories if name in definition.repository_usage or name == self.repository_root.name] or repositories[:1]

    def _latest_json(self, directory: Path, pattern: str) -> Optional[Dict[str, Any]]:
        path = self._latest_json_path(directory, pattern)
        return self._read_json(path) if path else None

    def _latest_json_path(self, directory: Path, pattern: str) -> Optional[Path]:
        if not directory.exists():
            return None
        matches = sorted(directory.glob(pattern), key=lambda item: item.stat().st_mtime, reverse=True)
        return matches[0] if matches else None

    def _read_json(self, path: Optional[Path]) -> Optional[Dict[str, Any]]:
        if path is None or not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def _detect_ai_provider(self) -> str:
        providers = []
        for env_name, label in [
            ("ANTHROPIC_API_KEY", "Anthropic"),
            ("OPENAI_API_KEY", "OpenAI"),
            ("GEMINI_API_KEY", "Gemini"),
            ("GOOGLE_API_KEY", "Google"),
            ("MISTRAL_API_KEY", "Mistral"),
        ]:
            if os.environ.get(env_name):
                providers.append(label)
        return ", ".join(providers) if providers else "Not configured"

    def _report_description(self, title: str, payload: Mapping[str, Any]) -> str:
        if title == "Repository Inspection":
            metrics = payload.get("metrics", {})
            return f"{metrics.get('total_files', 0)} files, {metrics.get('entry_point_count', 0)} entry points."
        if title == "Executive Briefing":
            return str(payload.get("executive_summary", "Executive summary available."))
        if title == "Workspace Dashboard":
            summary = payload.get("workspace_summary", {})
            return f"{summary.get('total_repositories', 0)} repositories, health={summary.get('overall_health', 'unknown')}."
        if isinstance(payload, Mapping) and payload:
            first_key = next(iter(payload.keys()))
            return f"Contains {len(payload.keys())} top-level field(s); starts with '{first_key}'."
        return "Generated artifact."

    def _page(self, title: str, payload: Mapping[str, Any], sections: List[str]) -> str:
        nav = "".join(
            f"<a href=\"{escape(item['href'])}\">{escape(item['label'])}</a>"
            for item in payload["navigation"]
        )
        capability_links = "".join(
            f"<li><a href=\"/capabilities/{escape(item['slug'])}\">{escape(item['title'])}</a> <span class=\"status\">{escape(item['status'])}</span></li>"
            for item in payload["capabilities"]["items"]
        )
        return (
            "<!doctype html><html><head><meta charset=\"utf-8\">"
            f"<title>{escape(title)} — AI-Toolkit</title>"
            "<style>"
            "body{font-family:Arial,sans-serif;margin:0;background:#0b1020;color:#e5e7eb;}"
            "a{color:#93c5fd;text-decoration:none;}a:hover{text-decoration:underline;}"
            ".layout{display:grid;grid-template-columns:280px 1fr;min-height:100vh;}"
            "aside{background:#111827;padding:24px;border-right:1px solid #1f2937;}"
            "main{padding:24px;}"
            "nav a{display:block;padding:8px 0;}"
            ".panel{background:#111827;border:1px solid #1f2937;border-radius:12px;padding:16px;margin:0 0 20px 0;}"
            ".grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;}"
            ".card{background:#111827;border:1px solid #1f2937;border-radius:12px;padding:14px;}"
            ".label{font-size:12px;color:#9ca3af;text-transform:uppercase;letter-spacing:.08em;}"
            ".value{font-size:18px;font-weight:700;margin-top:6px;word-break:break-word;}"
            "table{width:100%;border-collapse:collapse;}th,td{padding:10px;border-bottom:1px solid #1f2937;text-align:left;vertical-align:top;}"
            "dt{font-weight:700;margin-top:10px;}dd{margin:4px 0 10px 0;color:#d1d5db;}"
            "ul{padding-left:18px;}li{margin:6px 0;}.status{color:#9ca3af;font-size:12px;margin-left:4px;}"
            "h1,h2,h3{margin-top:0;} code{background:#1f2937;padding:2px 6px;border-radius:6px;}"
            "</style></head><body>"
            "<div class=\"layout\">"
            "<aside>"
            "<h2>AI-Toolkit</h2>"
            "<p>Engineering Operating System</p>"
            f"<nav>{nav}</nav>"
            "<div class=\"panel\"><h3>Capabilities</h3><ul>"
            f"{capability_links}</ul></div>"
            "</aside>"
            f"<main><h1>{escape(title)}</h1>{''.join(sections)}</main>"
            "</div></body></html>"
        )

    def _summary_grid(self, cards: Iterable[Mapping[str, Any]]) -> str:
        items = []
        for card in cards:
            items.append(
                "<div class=\"card\">"
                f"<div class=\"label\">{escape(str(card['label']))}</div>"
                f"<div class=\"value\">{escape(str(card['value']))}</div>"
                "</div>"
            )
        return f"<section class=\"grid\">{''.join(items)}</section>"

    def _section(self, title: str, content: str) -> str:
        return f"<section class=\"panel\"><h2>{escape(title)}</h2>{content}</section>"

    def _activity_table(self, items: Iterable[Mapping[str, Any]]) -> str:
        rows = []
        for item in items:
            rows.append(
                "<tr>"
                f"<td>{escape(str(item.get('timestamp', '')))}</td>"
                f"<td>{escape(str(item.get('title', '')))}</td>"
                f"<td>{escape(str(item.get('details', '')))}</td>"
                "</tr>"
            )
        if not rows:
            rows.append("<tr><td colspan=\"3\">No recent activity available.</td></tr>")
        return "<table><thead><tr><th>Timestamp</th><th>Activity</th><th>Details</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"

    def _report_table(self, items: Iterable[Mapping[str, Any]]) -> str:
        rows = []
        for item in items:
            rows.append(
                "<tr>"
                f"<td>{escape(str(item.get('title', '')))}</td>"
                f"<td><code>{escape(str(item.get('path', '')))}</code></td>"
                f"<td>{escape(str(item.get('generated_at', '')))}</td>"
                f"<td>{escape(str(item.get('description', '')))}</td>"
                "</tr>"
            )
        if not rows:
            rows.append("<tr><td colspan=\"4\">No reports available.</td></tr>")
        return "<table><thead><tr><th>Report</th><th>Path</th><th>Generated</th><th>Description</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"

    def _health_checks(self, health: Mapping[str, Any]) -> str:
        checks = health.get("checks", [])
        rows = []
        for check in checks:
            rows.append(
                "<tr>"
                f"<td>{escape(str(check.get('name', '')))}</td>"
                f"<td>{'PASS' if check.get('passed') else 'FAIL'}</td>"
                f"<td>{escape(str(check.get('message', '')))}</td>"
                "</tr>"
            )
        if not rows:
            rows.append("<tr><td colspan=\"3\">No health checks available.</td></tr>")
        score = health.get("score", 0)
        summary = escape(str(health.get("summary", "")))
        return f"<p><strong>Status:</strong> {escape(str(health.get('status', 'unknown')))} · <strong>Score:</strong> {score}%</p><p>{summary}</p><table><thead><tr><th>Check</th><th>Result</th><th>Details</th></tr></thead><tbody>{''.join(rows)}</tbody></table>"

    def _metrics_table(self, metrics: Mapping[str, Any]) -> str:
        rows = []
        for key, value in metrics.items():
            if isinstance(value, Mapping):
                value = ", ".join(f"{inner_key}={inner_value}" for inner_key, inner_value in value.items())
            rows.append(
                "<tr>"
                f"<td>{escape(str(key).replace('_', ' ').title())}</td>"
                f"<td>{escape(str(value))}</td>"
                "</tr>"
            )
        return "<table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"

    def _inspection_panel(self, inspection: Mapping[str, Any]) -> str:
        return self._definition_list(
            [
                ("Languages", ", ".join(f"{key}={value}" for key, value in inspection.get("languages", {}).items()) or "None"),
                ("Technology Stack", ", ".join(inspection.get("tech_stack", [])) or "None"),
                ("Dependency Manifests", ", ".join(inspection.get("dependency_manifests", [])) or "None"),
                ("Workspace Health", inspection.get("workspace_health", "unknown")),
            ]
        )

    def _repository_table(self, items: Iterable[Mapping[str, Any]]) -> str:
        rows = []
        for item in items:
            rows.append(
                "<tr>"
                f"<td>{escape(str(item.get('name', '')))}</td>"
                f"<td>{escape(str(item.get('health', '')))}</td>"
                f"<td>{escape(str(item.get('current_branch', '')))}</td>"
                f"<td>{escape(str(item.get('last_inspection', '')))}</td>"
                f"<td>{escape(str(item.get('active_sprint', '')))}</td>"
                f"<td>{escape(str(item.get('active_issue', '')))}</td>"
                f"<td>{escape(str(item.get('repository_statistics', '')))}</td>"
                f"<td>{escape(str(item.get('implementation_progress', '')))}</td>"
                "</tr>"
            )
        return "<table><thead><tr><th>Repository</th><th>Health</th><th>Current Branch</th><th>Last Inspection</th><th>Active Sprint</th><th>Active Issue</th><th>Repository Statistics</th><th>Implementation Progress</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"

    def _session_history(self, items: Iterable[Mapping[str, Any]]) -> str:
        rows = []
        for item in items:
            rows.append(
                "<tr>"
                f"<td>{escape(str(item.get('identifier', '')))}</td>"
                f"<td>{escape(str(item.get('status', '')))}</td>"
                f"<td>{escape(str(item.get('repository', '')))}</td>"
                f"<td>{escape(', '.join(item.get('completed_steps', [])) or 'None')}</td>"
                "</tr>"
            )
        if not rows:
            rows.append("<tr><td colspan=\"4\">No session history available.</td></tr>")
        return "<table><thead><tr><th>Session</th><th>Status</th><th>Repository</th><th>Completed Steps</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"

    def _definition_list(self, rows: Iterable[tuple[str, str]]) -> str:
        html = ["<dl>"]
        for key, value in rows:
            html.append(f"<dt>{escape(str(key))}</dt><dd>{escape(str(value))}</dd>")
        html.append("</dl>")
        return "".join(html)

    def _iso_from_timestamp(self, timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()

    def _relative_path(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.repository_root))
        except ValueError:
            return str(path)
