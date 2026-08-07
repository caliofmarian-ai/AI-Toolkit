from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

from python.ai_platform import AIPlatformService
from python.context_synchronization_engine import ContextSynchronizationEngine
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
    target_epic: str = "EPIC-004"


CAPABILITY_DEFINITIONS: List[CapabilityDefinition] = [
    CapabilityDefinition(
        slug="dashboard",
        title="Dashboard",
        purpose="Provide the primary Engineering Operating System interface.",
        description="Aggregates repository, workspace, reports, and engineering-session context into a single local application.",
        architecture="A stdlib HTTP server renders HTML pages from existing repository artifacts and engines without adding a frontend framework.",
        inputs=["repository state", "workspace state", "reports", "capability metadata"],
        outputs=["home page", "project manager page", "engineering explorer pages", "runtime pages", "JSON endpoints"],
        dependencies=["repository-engine", "engineering-session", "project-manager"],
        related_paths=["bin/ai", "lib/python/dashboard", "lib/python/cli/main.py"],
        related_tests=["tests/test_dashboard.sh", "tests/test_dashboard_navigation.sh"],
        cli_commands=["bin/ai dashboard serve"],
        dashboard_pages=["/", "/projects", "/session", "/explorer", "/reports", "/runtime", "/diagnostics"],
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
        dashboard_pages=["/", "/session", "/runtime", "/diagnostics"],
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
        self.ai_platform = AIPlatformService(
            repository_root=str(self.repository_root),
            workspace_root=str(self.workspace_root),
        )

    def build(self, refresh: bool = False) -> Dict[str, Any]:
        now = time.time()
        if (
            not refresh
            and self._cached_payload is not None
            and now < self._cache_expires_at
        ):
            return self._cached_payload

        engineering_context = self._load_engineering_context(refresh=refresh)
        ai_control_center = self._load_ai_control_center()
        session = self._load_session(
            engineering_context=engineering_context,
            ai_control_center=ai_control_center,
        )
        repository = self._load_repository_profile()
        workspace = self._load_workspace_summary()
        reports = self._load_reports(engineering_context=engineering_context)
        runtime = self._load_runtime(session, workspace, engineering_context=engineering_context)
        diagnostics = self._load_diagnostics(runtime)
        capabilities = self._load_capabilities(
            workspace,
            session,
            runtime,
            engineering_context=engineering_context,
        )

        payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "repository_root": str(self.repository_root),
            "workspace_root": str(self.workspace_root),
            "navigation": self._navigation(),
            "home": self._home_payload(repository, workspace, session, reports, runtime, diagnostics),
            "workspace": workspace,
            "session": session,
            "reports": reports,
            "runtime": runtime,
            "diagnostics": diagnostics,
            "capabilities": capabilities,
            "ai_control_center": ai_control_center,
            "engineering_context": engineering_context,
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
                self._section("Engineering Session", self._definition_list(home["session_overview"])),
                self._section("Runtime Status", self._definition_list(home["runtime_overview"])),
                self._section("Product Status", self._definition_list(home["product_status"])),
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

    def render_repository(
        self,
        payload: Optional[Dict[str, Any]] = None,
        *,
        question: str = "",
        prompt_name: str = "",
    ) -> str:
        data = payload or self.build()
        result = self.ask_repository(question=question, prompt_name=prompt_name) if (question or prompt_name) else {}
        ai_control_center = data["ai_control_center"]
        usage = ai_control_center["usage"]["total"]
        response_section = "<p>Use <code>?q=Your%20question</code> on this page URL to ask repository-aware questions.</p>"
        if result:
            response_section = self._definition_list(
                [
                    ("Question", result.get("question", "")),
                    ("Provider", result.get("provider", "")),
                    ("Model", result.get("model", "")),
                    ("Session", result.get("session_id", "")),
                    ("Answer", result.get("answer", "")),
                ]
            )
        return self._page(
            "Repository",
            data,
            [
                self._summary_grid(
                    [
                        {"label": "Ask AI Requests", "value": str(usage.get("requests", 0))},
                        {"label": "Tokens", "value": str(usage.get("tokens", 0))},
                        {"label": "Success Rate", "value": f"{usage.get('success_rate', 0.0):.2f}%"},
                        {"label": "Estimated Cost", "value": f"{usage.get('estimated_cost', 0.0):.6f}"},
                    ]
                ),
                self._section("Repository-aware Engineering Chat", response_section),
                self._section("Prompt Library", self._prompt_library_table(ai_control_center["prompt_library"])),
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

    def render_ai_control_center(self, payload: Optional[Dict[str, Any]] = None) -> str:
        data = payload or self.build()
        control = data["ai_control_center"]
        usage = control["usage"]["total"]
        return self._page(
            "AI Control Center",
            data,
            [
                self._summary_grid(
                    [
                        {"label": "Providers", "value": str(len(control["providers"]))},
                        {"label": "Connected Providers", "value": str(sum(1 for item in control["providers"] if item.get("connection")))},
                        {"label": "Requests", "value": str(usage.get("requests", 0))},
                        {"label": "Success Rate", "value": f"{usage.get('success_rate', 0.0):.2f}%"},
                    ]
                ),
                self._section("Providers", self._provider_table(control["providers"])),
                self._section("Model Manager", self._model_manager_panel(control["model_manager"])),
                self._section("Connections", self._connection_table(control["connections"])),
                self._section("Usage Monitoring", self._usage_panel(control["usage"])),
                self._section("Recent AI Sessions", self._ai_sessions_table(control["recent_sessions"])),
                self._section("AI Settings", self._metrics_table(control["settings"])),
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

    def render_runtime(self, payload: Optional[Dict[str, Any]] = None) -> str:
        data = payload or self.build()
        runtime = data["runtime"]
        return self._page(
            "Runtime",
            data,
            [
                self._summary_grid(runtime["summary_cards"]),
                self._section("Runtime Overview", self._definition_list(runtime["overview"])),
                self._section("Health Checks", self._health_matrix(runtime["health"])),
                self._section("Loaded Services", self._bullet_list(runtime["loaded_services"])),
                self._section("Loaded Engines", self._bullet_list(runtime["loaded_engines"])),
                self._section("Registered CLI Commands", self._bullet_list(runtime["registered_cli_commands"])),
                self._section("Registered Providers", self._bullet_list(runtime["registered_providers"])),
            ],
        )

    def render_diagnostics(self, payload: Optional[Dict[str, Any]] = None) -> str:
        data = payload or self.build()
        diagnostics = data["diagnostics"]
        return self._page(
            "Diagnostics",
            data,
            [
                self._summary_grid(diagnostics["summary_cards"]),
                self._section("Runtime Issues", self._issue_table(diagnostics["issues"])),
                self._section("Warnings", self._bullet_list(diagnostics["warnings"])),
                self._section("Configuration", self._metrics_table(diagnostics["configuration"])),
                self._section("Recent Startup Log", self._startup_log(diagnostics["recent_startup_log"])),
                self._section("Health Checks", self._health_matrix(diagnostics["health_checks"])),
                self._section("Recommendations", self._bullet_list(diagnostics["recommendations"])),
                self._section("Future Improvements", self._bullet_list(diagnostics["future_improvements"])),
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

    def _load_session(
        self,
        *,
        engineering_context: Optional[Mapping[str, Any]] = None,
        ai_control_center: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        state = self._read_json(self.repository_root / ".ai" / "development_state" / "current_state.json") or {}
        snapshot = self._read_json(self.repository_root / ".ai" / "development_state" / "executive_snapshot.json") or {}
        events = self._read_json(self.repository_root / ".ai" / "development_state" / "events.json") or {}
        git_context = GitContextProvider(str(self.repository_root)).collect()
        planning_state = state.get("planning_state", {})
        workspace_state = state.get("workspace_state", {})
        repository_state = state.get("repository_state", {})
        execution_state = state.get("execution_state", {})
        current_context = snapshot.get("current_context", {})
        live_context = (engineering_context or {}).get("implementation_context", {}).get("traceability", {})
        project_data = (engineering_context or {}).get("project_context", {}).get("data", {})
        ai_provider = self._detect_ai_provider(ai_control_center=ai_control_center)
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
            "current_project": project_data.get("repository_context", {}).get("name", "") or workspace_state.get("active_project", self.repository_root.name),
            "current_repository": repository_state.get("repository", self.repository_root.name),
            "current_branch": repository_state.get("branch", git_context.get("current_branch", "")),
            "current_workspace": workspace_state.get("active_workspace", str(self.workspace_root)),
            "current_sprint": planning_state.get("current_sprint", current_context.get("current_epic", "")),
            "current_epic": live_context.get("current_epic", "") or current_context.get("current_epic", workspace_state.get("current_objective", "")),
            "current_issue": live_context.get("current_issue", "") or current_context.get("current_issue", ""),
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
                {"label": "Current Epic", "value": live_context.get("current_epic", "") or current_context.get("current_epic", "n/a")},
                {"label": "Current Issue", "value": live_context.get("current_issue", "") or current_context.get("current_issue", "n/a")},
                {"label": "Current Engineering Task", "value": workspace_state.get("current_task", "n/a")},
                {"label": "Current Runtime", "value": execution_state.get("current_executor", "runtime")},
                {"label": "Current AI Provider", "value": ai_provider},
            ],
        }

    def _load_reports(self, *, engineering_context: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        report_specs = [
            ("Repository Inspection", self._latest_json_path(self.repository_root / ".ai" / "reports", "inspect-*.json")),
            ("Executive Briefing", self.repository_root / ".ai" / "executive" / "briefing.json"),
            ("Planning", self.repository_root / ".ai" / "planning" / "planning.json"),
            ("Execution", self.repository_root / ".ai" / "execution" / "execution.json"),
            ("Self Evaluation", self.repository_root / ".ai" / "self_evaluation" / "evaluation.json"),
            ("Self Improvement", self.repository_root / ".ai" / "self_improvement" / "improvements.json"),
            ("Workspace Dashboard", self.workspace_root / ".ai" / "workspace" / "dashboard.json"),
            ("Engineering Context", self.repository_root / ".ai" / "context" / "engineering_context.json"),
            ("Decision History", self.repository_root / ".ai" / "context" / "decision_history.json"),
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

    def _load_runtime(
        self,
        session: Mapping[str, Any],
        workspace: Mapping[str, Any],
        *,
        engineering_context: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        persisted = self._read_json(self.repository_root / ".ai" / "runtime" / "state" / "runtime_status.json") or {}
        runtime_payload = persisted.get("runtime", {})
        health = persisted.get("health", {})
        if not runtime_payload:
            provider_value = self._detect_ai_provider()
            runtime_payload = {
                "state": "BOOT",
                "uptime_seconds": 0.0,
                "startup_duration_seconds": 0.0,
                "port": int(os.environ.get("PORT", "8081")),
                "environment": os.environ.get("RAILWAY_ENVIRONMENT", os.environ.get("ENVIRONMENT", "local")),
                "loaded_services": ["dashboard"],
                "loaded_engines": ["repository", "workspace"],
                "registered_cli_commands": ["bin/ai dashboard serve"],
                "registered_providers": provider_value.split(", ") if provider_value != "Not configured" else [],
                "current_repository": str(self.repository_root),
                "current_workspace": str(self.workspace_root),
                "current_project": session.get("current_project", self.repository_root.name),
                "current_session": {
                    "project": session.get("current_project", self.repository_root.name),
                    "repository": session.get("current_repository", self.repository_root.name),
                    "branch": session.get("current_branch", ""),
                    "task": session.get("current_engineering_task", ""),
                    "identifier": session.get("session_history", [{}])[0].get("identifier", "") if session.get("session_history") else "",
                    "status": session.get("session_history", [{}])[0].get("status", "") if session.get("session_history") else "",
                },
                "runtime_configuration": {
                    "http_port": int(os.environ.get("PORT", "8081")),
                    "environment": os.environ.get("ENVIRONMENT", "local"),
                },
                "dashboard_initialized": True,
                "repository_detected": True,
                "workspace_detected": True,
            }
        runtime_payload["engineering_context"] = engineering_context or self._read_json(
            self.repository_root / ".ai" / "context" / "engineering_context.json"
        ) or {}
        if not health:
            health = {
                "healthy": bool(runtime_payload.get("dashboard_initialized", True)),
                "ready": runtime_payload.get("state") == "READY",
                "checks": {
                    "runtime_alive": True,
                    "dashboard_initialized": bool(runtime_payload.get("dashboard_initialized", True)),
                    "engineering_context_initialized": bool(runtime_payload.get("engineering_context", {})),
                    "repository_loaded": bool(runtime_payload.get("repository_detected", True)),
                    "session_initialized": bool(runtime_payload.get("current_session", {}).get("project")),
                },
            }
        providers = runtime_payload.get("registered_providers") or []
        summary_cards = [
            {"label": "Runtime State", "value": runtime_payload.get("state", "unknown")},
            {"label": "Uptime", "value": f"{runtime_payload.get('uptime_seconds', 0.0):.1f}s"},
            {"label": "Port", "value": runtime_payload.get("port", "n/a")},
            {"label": "Environment", "value": runtime_payload.get("environment", "unknown")},
            {"label": "Health", "value": "HEALTHY" if health.get("healthy") else "UNHEALTHY"},
            {"label": "Loaded Engines", "value": str(len(runtime_payload.get("loaded_engines", [])))},
        ]
        overview = [
            ("Runtime State", runtime_payload.get("state", "unknown")),
            ("Uptime", f"{runtime_payload.get('uptime_seconds', 0.0):.1f}s"),
            ("Startup Duration", f"{runtime_payload.get('startup_duration_seconds', 0.0):.3f}s"),
            ("Port", str(runtime_payload.get("port", "n/a"))),
            ("Environment", runtime_payload.get("environment", "unknown")),
            ("Loaded Services", ", ".join(runtime_payload.get("loaded_services", [])) or "None"),
            ("Loaded Engines", ", ".join(runtime_payload.get("loaded_engines", [])) or "None"),
            ("Registered Commands", ", ".join(runtime_payload.get("registered_cli_commands", [])) or "None"),
            ("Registered Providers", ", ".join(providers) or "None"),
            ("Current Repository", runtime_payload.get("current_repository", str(self.repository_root))),
            ("Current Workspace", runtime_payload.get("current_workspace", str(self.workspace_root))),
            ("Current Project", runtime_payload.get("current_project", self.repository_root.name)),
            ("Current Session", runtime_payload.get("current_session", {}).get("identifier", "") or runtime_payload.get("current_session", {}).get("task", "") or "n/a"),
            ("Engineering Context", "LOADED" if runtime_payload.get("engineering_context") else "MISSING"),
        ]
        return {
            **runtime_payload,
            "health": health,
            "summary_cards": summary_cards,
            "overview": overview,
        }

    def _load_diagnostics(self, runtime: Mapping[str, Any]) -> Dict[str, Any]:
        persisted = self._read_json(self.repository_root / ".ai" / "runtime" / "state" / "runtime_diagnostics.json") or {}
        diagnostics_payload = persisted.get("diagnostics", {})
        if not diagnostics_payload:
            diagnostics_payload = {
                "issues": [],
                "warnings": [] if runtime.get("health", {}).get("healthy") else ["Runtime health is degraded."],
                "configuration": runtime.get("runtime_configuration", {}),
                "recent_startup_log": [{"state": runtime.get("state", "unknown"), "message": "Dashboard-only runtime view.", "timestamp": self._iso_from_timestamp(time.time())}],
                "health_checks": runtime.get("health", {}),
                "recommendations": ["Start the runtime server to collect live diagnostics."],
                "future_improvements": ["Add live runtime telemetry to this page."],
            }
        return {
            **diagnostics_payload,
            "summary_cards": [
                {"label": "Issues", "value": str(len(diagnostics_payload.get("issues", [])))},
                {"label": "Warnings", "value": str(len(diagnostics_payload.get("warnings", [])))},
                {"label": "Health", "value": "HEALTHY" if runtime.get("health", {}).get("healthy") else "UNHEALTHY"},
                {"label": "Recommendations", "value": str(len(diagnostics_payload.get("recommendations", [])))},
            ],
        }

    def _load_ai_control_center(self) -> Dict[str, Any]:
        return self.ai_platform.control_center()

    def ask_repository(self, question: str, prompt_name: str = "") -> Dict[str, Any]:
        return self.ai_platform.ask_repository(question=question, prompt_name=prompt_name)

    def _load_capabilities(
        self,
        workspace: Mapping[str, Any],
        session: Mapping[str, Any],
        runtime: Mapping[str, Any],
        *,
        engineering_context: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        statuses: Dict[str, str] = {}
        items: List[Dict[str, Any]] = []
        runtime_healthy = bool((runtime.get("health", {}) or {}).get("healthy"))
        engineering_context_loaded = bool(engineering_context)
        for definition in CAPABILITY_DEFINITIONS:
            resolved_paths = self._resolve_related_paths(definition.related_paths)
            resolved_tests = self._resolve_related_paths(definition.related_tests)
            file_ratio = len(resolved_paths) / len(definition.related_paths) if definition.related_paths else 1.0
            test_ratio = len(resolved_tests) / len(definition.related_tests) if definition.related_tests else 1.0
            implementation_percentage = int(round(((file_ratio * 0.75) + (test_ratio * 0.25)) * 100))
            status = "Planned"
            if implementation_percentage >= 85:
                status = "Implemented"
            elif implementation_percentage > 0:
                status = "In Progress"
            if status == "Implemented" and resolved_tests:
                status = "Validated"
            if (
                definition.slug in {"dashboard", "runtime", "engineering-session", "project-manager"}
                and engineering_context_loaded
                and runtime_healthy
            ):
                status = "Operational"
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
            blocking = [
                dependency
                for dependency in item["dependencies"]
                if statuses.get(dependency) not in {None, "Implemented", "Validated", "Operational"}
            ]
            item["blocking_dependencies"] = blocking
            if item["status"] == "Planned" and blocking:
                item["status"] = "Blocked"
        implemented = sum(1 for item in items if item["status"] == "Implemented")
        in_progress = sum(1 for item in items if item["status"] == "In Progress")
        planned = sum(1 for item in items if item["status"] == "Planned")
        blocked = sum(1 for item in items if item["status"] == "Blocked")
        validated = sum(1 for item in items if item["status"] == "Validated")
        operational = sum(1 for item in items if item["status"] == "Operational")
        return {
            "items": items,
            "summary_cards": [
                {"label": "Capabilities", "value": str(len(items))},
                {"label": "Implemented", "value": str(implemented)},
                {"label": "In Progress", "value": str(in_progress)},
                {"label": "Planned", "value": str(planned)},
                {"label": "Blocked", "value": str(blocked)},
                {"label": "Validated", "value": str(validated)},
                {"label": "Operational", "value": str(operational)},
            ],
        }

    def _load_engineering_context(self, *, refresh: bool = False) -> Dict[str, Any]:
        path = self.repository_root / ".ai" / "context" / "engineering_context.json"
        if not path.exists():
            try:
                return ContextSynchronizationEngine(
                    repository=str(self.repository_root),
                    workspace_root=str(self.workspace_root),
                ).synchronize(refresh=False).get("engineering_context", {})
            except Exception:
                return self._read_json(path) or {}
        return self._read_json(path) or {}

    def _home_payload(
        self,
        repository: Mapping[str, Any],
        workspace: Mapping[str, Any],
        session: Mapping[str, Any],
        reports: Mapping[str, Any],
        runtime: Mapping[str, Any],
        diagnostics: Mapping[str, Any],
    ) -> Dict[str, Any]:
        latest_inspection = repository["latest_inspection"]
        return {
            "summary_cards": [
                {"label": "Welcome", "value": f"Engineering Operating System · {session['current_project']}"},
                {"label": "Current Engineering Session", "value": runtime.get("current_session", {}).get("identifier", "") or session["current_engineering_task"] or "n/a"},
                {"label": "Current Project", "value": session["current_project"]},
                {"label": "Current Repository", "value": session["current_repository"]},
                {"label": "Current Branch", "value": session["current_branch"] or "n/a"},
                {"label": "Current Engineering Task", "value": session["current_engineering_task"] or "n/a"},
                {"label": "Repository Health", "value": str(repository["health_summary"].get("status", "unknown"))},
                {"label": "Current Runtime Status", "value": runtime.get("state", session["current_runtime_status"])},
                {"label": "Current Sprint", "value": session["current_sprint"] or "n/a"},
                {"label": "Current Epic", "value": session["current_epic"] or "n/a"},
                {"label": "Current Issue", "value": session["current_issue"] or "n/a"},
                {"label": "Current AI Provider", "value": session["current_ai_provider"]},
                {"label": "Recent Reports", "value": str(len(reports["items"]))},
                {"label": "Recent Activity", "value": str(len(session["recent_activity"]))},
                {"label": "Implementation Progress", "value": f"{workspace['summary'].get('overall_readiness', 0.0):.1f}%"},
                {"label": "Repository Statistics", "value": f"files={repository['metrics'].get('total_files', 0)}, entries={repository['metrics'].get('entry_point_count', 0)}"},
                {"label": "Latest Repository Inspection", "value": ", ".join(repository["tech_stack"][:3]) or "n/a"},
            ],
            "session_overview": [
                ("Current Project", session["current_project"]),
                ("Current Repository", session["current_repository"]),
                ("Current Workspace", session["current_workspace"]),
                ("Current Branch", session["current_branch"]),
                ("Current Engineering Session", runtime.get("current_session", {}).get("identifier", "") or "n/a"),
                ("Current Sprint", session["current_sprint"] or "n/a"),
                ("Current Epic", session["current_epic"] or "n/a"),
                ("Current Issue", session["current_issue"] or "n/a"),
                ("Current AI Provider", session["current_ai_provider"]),
                ("Next Recommended Action", (diagnostics.get("recommendations") or ["Review runtime diagnostics and continue implementation."])[0]),
            ],
            "runtime_overview": [
                ("Runtime State", runtime.get("state", "unknown")),
                ("Health", "HEALTHY" if runtime.get("health", {}).get("healthy") else "UNHEALTHY"),
                ("Ready", "YES" if runtime.get("health", {}).get("ready") else "NO"),
                ("Port", runtime.get("port", "n/a")),
                ("Environment", runtime.get("environment", "unknown")),
                ("Loaded Services", ", ".join(runtime.get("loaded_services", [])) or "None"),
                ("Loaded Engines", ", ".join(runtime.get("loaded_engines", [])) or "None"),
            ],
            "product_status": [
                ("Current Project", session["current_project"]),
                ("Repository Health", str(repository["health_summary"].get("status", "unknown"))),
                ("Runtime Status", runtime.get("state", session["current_runtime_status"])),
                ("Current Sprint", session["current_sprint"] or "n/a"),
                ("Current Epic", session["current_epic"] or "n/a"),
                ("Current Issue", session["current_issue"] or "n/a"),
                ("Current AI Provider", session["current_ai_provider"]),
                ("Recent Reports", str(len(reports["items"]))),
                ("Implementation Progress", f"{workspace['summary'].get('overall_readiness', 0.0):.1f}%"),
                ("Next Recommended Action", (diagnostics.get("recommendations") or ["Review runtime diagnostics and continue implementation."])[0]),
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
            {"href": "/dashboard", "label": "Dashboard"},
            {"href": "/project-manager", "label": "Projects"},
            {"href": "/repository", "label": "Repository"},
            {"href": "/engineering-session", "label": "Engineering Session"},
            {"href": "/ai-control-center", "label": "AI Control Center"},
            {"href": "/knowledge", "label": "Knowledge"},
            {"href": "/validation", "label": "Validation"},
            {"href": "/reports", "label": "Reports"},
            {"href": "/settings", "label": "Settings"},
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

    def _detect_ai_provider(self, ai_control_center: Optional[Mapping[str, Any]] = None) -> str:
        cached = (self._cached_payload or {}).get("ai_control_center", {})
        source = ai_control_center or cached or self.ai_platform.control_center()
        providers = [
            item.get("name", "")
            for item in source.get("providers", [])
            if item.get("status") == "configured" or item.get("connection")
        ]
        if not providers:
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

    def _health_matrix(self, health: Mapping[str, Any]) -> str:
        checks = health.get("checks", {})
        rows = []
        for name, ok in checks.items():
            rows.append(
                "<tr>"
                f"<td>{escape(str(name))}</td>"
                f"<td>{'PASS' if ok else 'FAIL'}</td>"
                "</tr>"
            )
        if not rows:
            rows.append("<tr><td colspan=\"2\">No health checks available.</td></tr>")
        return (
            f"<p><strong>Healthy:</strong> {'YES' if health.get('healthy') else 'NO'} · "
            f"<strong>Ready:</strong> {'YES' if health.get('ready') else 'NO'}</p>"
            "<table><thead><tr><th>Check</th><th>Result</th></tr></thead><tbody>"
            + "".join(rows)
            + "</tbody></table>"
        )

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

    def _provider_table(self, providers: Iterable[Mapping[str, Any]]) -> str:
        rows = []
        for item in providers:
            rows.append(
                "<tr>"
                f"<td>{escape(str(item.get('name', '')))}</td>"
                f"<td>{escape(str(item.get('status', '')))}</td>"
                f"<td>{'YES' if item.get('connection') else 'NO'}</td>"
                f"<td>{escape(', '.join(item.get('models', [])) or 'None')}</td>"
                f"<td>{escape(', '.join(item.get('capabilities', [])) or 'None')}</td>"
                f"<td>{escape(str(item.get('latency', 0)))}</td>"
                f"<td>{escape(str(item.get('health', 'unknown')))}</td>"
                "</tr>"
            )
        if not rows:
            rows.append("<tr><td colspan=\"7\">No providers available.</td></tr>")
        return "<table><thead><tr><th>Provider</th><th>Status</th><th>Connected</th><th>Models</th><th>Capabilities</th><th>Latency (ms)</th><th>Health</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"

    def _connection_table(self, connections: Iterable[Mapping[str, Any]]) -> str:
        rows = []
        for item in connections:
            rows.append(
                "<tr>"
                f"<td>{escape(str(item.get('provider', '')))}</td>"
                f"<td>{escape(str(item.get('health_status', 'unknown')))}</td>"
                f"<td>{escape(str(item.get('last_success', '')))}</td>"
                f"<td>{escape(str(item.get('last_failure', '')))}</td>"
                f"<td>{escape(str(item.get('last_response_time', 0)))}</td>"
                "</tr>"
            )
        if not rows:
            rows.append("<tr><td colspan=\"5\">No connection data available.</td></tr>")
        return "<table><thead><tr><th>Provider</th><th>Health</th><th>Last Success</th><th>Last Failure</th><th>Last Response Time (ms)</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"

    def _model_manager_panel(self, model_manager: Mapping[str, Any]) -> str:
        discovered = model_manager.get("discovered_models", {})
        roles = model_manager.get("role_models", {})
        discovered_rows = []
        for provider, models in discovered.items():
            discovered_rows.append((provider, ", ".join(models) or "None"))
        role_rows = [(key, value or "n/a") for key, value in roles.items()]
        return self._definition_list(discovered_rows + role_rows)

    def _usage_panel(self, usage: Mapping[str, Any]) -> str:
        total = usage.get("total", {})
        return self._definition_list(
            [
                ("Requests", str(total.get("requests", 0))),
                ("Tokens", str(total.get("tokens", 0))),
                ("Estimated Cost", f"{total.get('estimated_cost', 0.0):.6f}"),
                ("Average Latency (ms)", str(total.get("average_latency_ms", 0.0))),
                ("Success Rate", f"{total.get('success_rate', 0.0):.2f}%"),
                ("Errors", str(total.get("errors", 0))),
            ]
        )

    def _ai_sessions_table(self, sessions: Iterable[Mapping[str, Any]]) -> str:
        rows = []
        for item in sessions:
            rows.append(
                "<tr>"
                f"<td>{escape(str(item.get('id', '')))}</td>"
                f"<td>{escape(str(item.get('project', '')))}</td>"
                f"<td>{escape(str(item.get('repository', '')))}</td>"
                f"<td>{escape(str(item.get('branch', '')))}</td>"
                f"<td>{escape(str(item.get('selected_provider', '')))}</td>"
                f"<td>{escape(str(item.get('selected_model', '')))}</td>"
                f"<td>{escape(str(item.get('conversation_count', 0)))}</td>"
                "</tr>"
            )
        if not rows:
            rows.append("<tr><td colspan=\"7\">No AI sessions available.</td></tr>")
        return "<table><thead><tr><th>Session</th><th>Project</th><th>Repository</th><th>Branch</th><th>Provider</th><th>Model</th><th>Messages</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"

    def _prompt_library_table(self, prompt_library: Mapping[str, Iterable[Mapping[str, Any]]]) -> str:
        rows = []
        for category, items in prompt_library.items():
            for item in items:
                rows.append(
                    "<tr>"
                    f"<td>{escape(str(category))}</td>"
                    f"<td>{escape(str(item.get('name', '')))}</td>"
                    f"<td>{escape(str(item.get('prompt', '')))}</td>"
                    "</tr>"
                )
        if not rows:
            rows.append("<tr><td colspan=\"3\">No prompts registered.</td></tr>")
        return "<table><thead><tr><th>Category</th><th>Name</th><th>Prompt</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"

    def _definition_list(self, rows: Iterable[tuple[str, str]]) -> str:
        html = ["<dl>"]
        for key, value in rows:
            html.append(f"<dt>{escape(str(key))}</dt><dd>{escape(str(value))}</dd>")
        html.append("</dl>")
        return "".join(html)

    def _bullet_list(self, items: Iterable[Any]) -> str:
        values = list(items)
        if not values:
            return "<p>None.</p>"
        return "<ul>" + "".join(f"<li>{escape(str(item))}</li>" for item in values) + "</ul>"

    def _issue_table(self, items: Iterable[Mapping[str, Any]]) -> str:
        rows = []
        for item in items:
            rows.append(
                "<tr>"
                f"<td>{escape(str(item.get('timestamp', '')))}</td>"
                f"<td>{escape(str(item.get('severity', '')))}</td>"
                f"<td>{escape(str(item.get('source', '')))}</td>"
                f"<td>{escape(str(item.get('message', '')))}</td>"
                f"<td>{escape(str(item.get('details', '')))}</td>"
                "</tr>"
            )
        if not rows:
            rows.append("<tr><td colspan=\"5\">No runtime issues detected.</td></tr>")
        return "<table><thead><tr><th>Timestamp</th><th>Severity</th><th>Source</th><th>Message</th><th>Details</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"

    def _startup_log(self, entries: Iterable[Mapping[str, Any]]) -> str:
        rows = []
        for entry in entries:
            rows.append(
                "<tr>"
                f"<td>{escape(str(entry.get('timestamp', '')))}</td>"
                f"<td>{escape(str(entry.get('state', '')))}</td>"
                f"<td>{escape(str(entry.get('message', '')))}</td>"
                "</tr>"
            )
        if not rows:
            rows.append("<tr><td colspan=\"3\">No startup events recorded.</td></tr>")
        return "<table><thead><tr><th>Timestamp</th><th>State</th><th>Message</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"

    def _iso_from_timestamp(self, timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()

    def _relative_path(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.repository_root))
        except ValueError:
            return str(path)
