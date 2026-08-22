# FUSION-02 — AI Partner Real Session Reattachment Anatomy

Generated: 2026-08-21T05:42:34.837620+00:00

## Purpose

Recover the exact production anatomy required to connect
the browser-visible AI Partner conversation to the durable
AISessionEngine identity.

This report is inspection authority only.

It does not yet certify browser reattachment.

## Demonstrated baseline

- Full FUSION regression before this recovery: 229 passed.
- EngineeringDashboardService is the real dashboard service.
- POST /api/ai/chat is the real owner AI chat HTTP boundary.
- The HTTP boundary already accepts session_id.
- The HTTP boundary passes session_id to AIPlatformService.
- Existing browser mutation attempts durable session identity.
- No DashboardService abstraction is authorized.

## Current worktree

BEGIN CURRENT WORKTREE
 M lib/python/dashboard/service.py
 M work/implementation-reports/FUSION/FUSION_02_TERMUX_EXECUTION_ERROR_MEMORY.md
END CURRENT WORKTREE

## Existing dashboard service mutation

BEGIN SERVICE DIFF
diff --git a/lib/python/dashboard/service.py b/lib/python/dashboard/service.py
index e560a93..bd31df6 100644
--- a/lib/python/dashboard/service.py
+++ b/lib/python/dashboard/service.py
@@ -933,8 +933,17 @@ class EngineeringDashboardService:
     def _load_ai_control_center(self) -> Dict[str, Any]:
         return self.ai_platform.control_center()

-    def ask_repository(self, question: str, prompt_name: str = "") -> Dict[str, Any]:
-        return self.ai_platform.ask_repository(question=question, prompt_name=prompt_name)
+    def ask_repository(
+        self,
+        question: str,
+        prompt_name: str = "",
+        session_id: str = "",
+    ) -> Dict[str, Any]:
+        return self.ai_platform.ask_repository(
+            question=question,
+            prompt_name=prompt_name,
+            session_id=session_id,
+        )

     def _load_capabilities(
         self,
@@ -1558,12 +1567,12 @@ class EngineeringDashboardService:
             'e.preventDefault();const q=question.value.trim();if(!q)return;'
             'send.disabled=true;question.disabled=true;'
             'status.className="chat-status working";'
-            'status.textContent="AI Partner is working…";'
+            'const storedSession=localStorage.getItem("ai_toolkit_partner_session_id");''if(storedSession&&session){session.value=storedSession;}''status.textContent="AI Partner is working…";'
             'try{const data=await jsonFetch("/api/ai/chat",{'
             'method:"POST",headers:{"Content-Type":"application/json"},'
             'body:JSON.stringify({question:q,session_id:session.value,'
             'provider_id:provider.value,model:model.value})});'
-            'const sid=data.session_id||session.value;question.value="";'
+            'const sid=data.session_id||session.value;''if(sid){session.value=sid;localStorage.setItem("ai_toolkit_partner_session_id",sid);}''question.value="";'
             'await loadSessions(sid);session.value=sid;await loadSession();'
             'status.className="chat-status";'
             'status.textContent="AI response received and persisted.";}'
END SERVICE DIFF

## Dashboard service anatomy

BEGIN DASHBOARD SERVICE
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
    CapabilityDefinition(
        slug="css-engine",
        title="CSS Engine",
        purpose="Validate canonical standards against the Canonical Specification Standard.",
        description="Loads canonical standard documents and validates them for metadata completeness, version format, required sections, normative language, and cross-reference integrity.",
        architecture="Pure Python engine that parses markdown-based canonical standard files and applies CSS-000 through CSS-005 validation rules.",
        inputs=["canonical standard markdown files", "standards root directory"],
        outputs=["CSSValidationResult per standard", "diagnostics report", "structured JSON output"],
        dependencies=["canonical standards (standards/)"],
        related_paths=["lib/python/css_engine", "standards/css"],
        related_tests=["tests/test_canonical_execution_stack.sh"],
        cli_commands=[],
        dashboard_pages=["/explorer/css-engine"],
        future_roadmap="Full CSS compliance scoring and automated standard quality gates.",
        known_limitations="Validates structure and metadata; does not evaluate semantic correctness of specification prose.",
        next_milestone="CSS validation integrated into CI pipeline.",
        engineering_decisions=["Derive validation rules directly from CSS-000 through CSS-005 without redesigning the standard."],
        why_problem="Canonical standards must be self-validating to remain authoritative.",
        why_architecture="Markdown-native approach keeps the engine aligned with the existing standard authoring format.",
        why_dependencies="The CSS Engine validates the foundation on which CDM and CSL depend.",
        repository_usage=["AI-Toolkit"],
        justification_documents=["standards/css/CSS-000_SPECIFICATION_MODEL.md"],
    ),
    CapabilityDefinition(
        slug="cdm-engine",
        title="CDM Engine",
        purpose="Load, parse, and materialize canonical documents into structured objects.",
        description="Transforms canonical markdown documents into CdmDocumentObject instances with full metadata extraction, section parsing, dependency extraction, and traceability link discovery.",
        architecture="Pure Python engine with markdown header parsing, section tree construction, canonical reference extraction, and CDM-000 validation.",
        inputs=["canonical document markdown files", "documents directory"],
        outputs=["CdmDocumentObject per document", "validation results", "dependency graph"],
        dependencies=["canonical standards (CDM-000 through CDM-019)"],
        related_paths=["lib/python/cdm_engine", "standards/cdm"],
        related_tests=["tests/test_canonical_execution_stack.sh"],
        cli_commands=[],
        dashboard_pages=["/explorer/cdm-engine"],
        future_roadmap="Document query language (CDM-012) and document namespace resolution (CDM-014).",
        known_limitations="Section nesting is currently limited to two levels.",
        next_milestone="CDM Engine feeding the Knowledge Graph automatically.",
        engineering_decisions=["Implement CDM-000 materialization without re-parsing canonical specs."],
        why_problem="Canonical documents must be executable objects, not static text.",
        why_architecture="Direct markdown parsing avoids dependency on external document frameworks.",
        why_dependencies="CDM Engine is the foundation for Knowledge Materialization and Repository Intelligence.",
        repository_usage=["AI-Toolkit"],
        justification_documents=["standards/cdm/CDM-000_DOCUMENT_MODEL.md"],
    ),
    CapabilityDefinition(
        slug="csl-engine",
        title="CSL Engine",
        purpose="Execute the Canonical Specification Language pipeline.",
        description="Provides a unified Lexer → Parser → AST → SemanticAnalyzer → Validator → CompilerInterface pipeline for CSL source files.",
        architecture="Wraps the existing canonical_parser (CslLexer, CslParser, SemanticAnalyzer) in a single executable engine interface.",
        inputs=["CSL source text", "CSL source files", "CSL directories"],
        outputs=["CslExecutionResult with tokens, AST, semantic result, diagnostics", "CslCompileResult with structured entities"],
        dependencies=["canonical_parser", "canonical standards (CSL)"],
        related_paths=["lib/python/csl_engine", "lib/python/canonical_parser", "standards/csl"],
        related_tests=["tests/test_canonical_execution_stack.sh"],
        cli_commands=[],
        dashboard_pages=["/explorer/csl-engine"],
        future_roadmap="Full CSL code generation and canonical standard compilation to executable artifacts.",
        known_limitations="Compiler interface produces structured JSON; binary code generation is not yet implemented.",
        next_milestone="CSL documents compiled into Knowledge Objects automatically.",
        engineering_decisions=["Wrap existing canonical_parser rather than rewrite to preserve continuity."],
        why_problem="CSL must be executable, not merely a specification language.",
        why_architecture="Engine wrapper keeps the architecture clean: one execution interface over all CSL pipeline stages.",
        why_dependencies="Derives from CslLexer and CslParser already present in canonical_parser.",
        repository_usage=["AI-Toolkit"],
        justification_documents=["standards/csl/core/CSL_CONSTITUTION.md"],
    ),
    CapabilityDefinition(
        slug="knowledge-materialization",
        title="Knowledge Materialization Engine",
        purpose="Transform canonical documents into executable knowledge.",
        description="Materializes CDM documents and CSS standards into Knowledge Objects, Knowledge Relationships, a Knowledge Graph, a Dependency Graph, and a Traceability Graph.",
        architecture="Consumes CDM Engine and CSS Engine outputs and builds a CanonicalKnowledgeGraph with full node and edge materialization.",
        inputs=["CdmDocumentObject list", "CSSStandardRecord list", "standards root directory"],
        outputs=["MaterializedKnowledge with knowledge_graph, dependency_graph, traceability_graph"],
        dependencies=["cdm-engine", "css-engine", "knowledge_graph", "canonical_entities"],
        related_paths=["lib/python/knowledge_materialization", "lib/python/knowledge_graph"],
        related_tests=["tests/test_canonical_execution_stack.sh"],
        cli_commands=[],
        dashboard_pages=["/explorer/knowledge-materialization"],
        future_roadmap="Reasoning graph, live graph query interface, canonical entity graph diff.",
        known_limitations="Reasoning graph is not yet implemented.",
        next_milestone="Repository Intelligence consuming the Knowledge Graph instead of file scanning.",
        engineering_decisions=["Build on existing CanonicalKnowledgeGraph rather than introduce a new graph library."],
        why_problem="Canonical Knowledge must be queryable and navigable at runtime.",
        why_architecture="Extending the existing graph architecture ensures compatibility with all existing graph consumers.",
        why_dependencies="Directly consumes CDM Engine and CSS Engine to form the full execution pipeline.",
        repository_usage=["AI-Toolkit"],
        justification_documents=["standards/cdm/CDM-011_DOCUMENT_GRAPH.md"],
    ),
]


class EngineeringDashboardService:
    def __init__(
        self,
        repository_root: str = ".",
        workspace_root: Optional[str] = None,
        cache_ttl_seconds: float = 5.0,
        organism_service: Optional[Any] = None,
    ) -> None:
        self.repository_root = Path(repository_root).resolve()
        self.workspace_root = (
            Path(workspace_root).resolve()
            if workspace_root
            else self.repository_root.parent
        )
        self.cache_ttl_seconds = cache_ttl_seconds
        self.organism_service = organism_service
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
        organism = (
            self.organism_service.state()
            if self.organism_service is not None
            else {
                "state": "UNKNOWN",
                "reason": (
                    "Dashboard is not attached to "
                    "RuntimeBootstrap organism boundary."
                ),
            }
        )
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
            "organism": organism,
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
                self._section(
                    "Owner AI Chat",
                    self._owner_ai_chat_panel(control),
                ),
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
                    "engineering_context_initialized": bool(runtime_payload.get("engineering_context")),
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

    def ask_repository(
        self,
        question: str,
        prompt_name: str = "",
        session_id: str = "",
    ) -> Dict[str, Any]:
        return self.ai_platform.ask_repository(
            question=question,
            prompt_name=prompt_name,
            session_id=session_id,
        )

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
                status in {"Implemented", "Validated"}
                and definition.slug in {"dashboard", "runtime", "engineering-session", "project-manager"}
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

    def seed_engineering_context(
        self,
        engineering_context: Mapping[str, Any],
    ) -> None:
        """Reuse engineering context reconstructed by the owning runtime.

        This prevents the dashboard from synchronously invoking the same
        ContextSynchronizationEngine again during one RuntimeBootstrap cycle.
        Human Authority and canonical persistence remain unchanged.
        """
        self._runtime_engineering_context = dict(engineering_context)

    def _load_engineering_context(self, *, refresh: bool = False) -> Dict[str, Any]:
        if not refresh:
            runtime_context = getattr(
                self,
                "_runtime_engineering_context",
                None,
            )
            if runtime_context is not None:
                return dict(runtime_context)

        path = self.repository_root / ".ai" / "context" / "engineering_context.json"
        if refresh or not path.exists():
            try:
                return ContextSynchronizationEngine(
                    repository=str(self.repository_root),
                    workspace_root=str(self.workspace_root),
                ).synchronize(refresh=refresh).get("engineering_context", {})
            except Exception:
                return {}
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
            ".ai-chat{display:flex;flex-direction:column;gap:14px;}"
            ".chat-toolbar{display:flex;justify-content:space-between;gap:12px;align-items:center;}"
            ".chat-muted{font-size:12px;color:#9ca3af;margin-top:4px;}"
            ".chat-controls{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;}"
            ".chat-controls label{font-size:12px;color:#9ca3af;}"
            ".chat-controls select,.chat-controls input,.chat-composer textarea{width:100%;box-sizing:border-box;margin-top:5px;background:#0b1020;color:#e5e7eb;border:1px solid #374151;border-radius:8px;padding:10px;}"
            ".chat-history{height:420px;overflow:auto;background:#080d19;border:1px solid #1f2937;border-radius:12px;padding:14px;}"
            ".chat-message{max-width:82%;padding:12px 14px;border-radius:12px;margin:10px 0;white-space:pre-wrap;word-break:break-word;}"
            ".chat-message.human{margin-left:auto;background:#1d4ed8;}"
            ".chat-message.ai{margin-right:auto;background:#1f2937;}"
            ".chat-actor{font-size:11px;font-weight:700;text-transform:uppercase;opacity:.75;margin-bottom:5px;}"
            ".chat-empty,.chat-status{color:#9ca3af;}"
            ".chat-status.error{color:#fca5a5;}.chat-status.working{color:#93c5fd;}"
            ".chat-composer{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:end;}"
            ".chat-composer button{background:#2563eb;color:white;border:0;border-radius:8px;padding:12px 20px;font-weight:700;cursor:pointer;}"
            ".chat-composer button:disabled{opacity:.55;cursor:wait;}"
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

    def _owner_ai_chat_panel(
        self,
        control: Mapping[str, Any],
    ) -> str:
        providers = [
            item
            for item in control.get("providers", [])
            if item.get("connection")
        ]

        provider_options = []
        for item in providers:
            provider_id = escape(
                str(
                    item.get("id")
                    or item.get("provider_id")
                    or item.get("name", "")
                ).lower()
            )
            name = escape(str(item.get("name", provider_id)))
            models = item.get("models", []) or []
            model = escape(str(models[0] if models else ""))
            provider_options.append(
                f'<option value="{provider_id}" '
                f'data-model="{model}">{name}</option>'
            )

        options = "".join(provider_options)

        return (
            '<div id="owner-ai-chat" class="ai-chat">'
            '<div class="chat-toolbar">'
            '<div><strong>Owner AI Chat</strong>'
            '<div class="chat-muted">'
            'Persistent RAW conversation · '
            'not automatically Evidence or Canon'
            '</div></div>'
            '<a href="/owner/logout">Owner logout</a>'
            '</div>'
            '<div class="chat-controls">'
            '<label>AI Partner / Provider'
            f'<select id="chat-provider">{options}</select>'
            '</label>'
            '<label>Model'
            '<input id="chat-model" type="text" '
            'placeholder="provider default">'
            '</label>'
            '<label>Session'
            '<select id="chat-session">'
            '<option value="">New conversation</option>'
            '</select></label>'
            '</div>'
            '<div id="chat-history" class="chat-history">'
            '<div class="chat-empty">'
            'Select a session or send the first message.'
            '</div></div>'
            '<div id="chat-status" class="chat-status" '
            'aria-live="polite"></div>'
            '<form id="chat-form" class="chat-composer">'
            '<textarea id="chat-question" rows="4" '
            'placeholder="Talk to your AI Partner..." '
            'required></textarea>'
            '<button id="chat-send" type="submit">Send</button>'
            '</form>'
            '</div>'
            '<script>'
            '(()=>{'
            'const $=id=>document.getElementById(id);'
            'const history=$("chat-history"),'
            'session=$("chat-session"),'
            'provider=$("chat-provider"),'
            'model=$("chat-model"),'
            'status=$("chat-status"),'
            'form=$("chat-form"),'
            'question=$("chat-question"),'
            'send=$("chat-send");'
            'function esc(v){const d=document.createElement("div");'
            'd.textContent=v==null?"":String(v);return d.innerHTML;}'
            'function actorName(v){'
            'return String(v||"").toUpperCase()==="HUMAN"'
            '?"You":"AI Partner";}'
            'function renderSources(items){'
            'if(!items||!items.length){history.innerHTML='
            '"<div class=\\"chat-empty\\">No messages yet.</div>";'
            'return;}'
            'history.innerHTML=items.map(x=>{'
            'const actor=String(x.actor||"").toUpperCase();'
            'const cls=actor==="HUMAN"?"human":"ai";'
            'return "<article class=\\"chat-message "+cls+"\\">"'
            '+"<div class=\\"chat-actor\\">"+esc(actorName(actor))'
            '+"</div><div>"+esc(x.content||"")+"</div></article>";'
            '}).join("");history.scrollTop=history.scrollHeight;}'
            'async function jsonFetch(url,opts={}){'
            'const r=await fetch(url,{credentials:"same-origin",...opts});'
            'let data={};try{data=await r.json();}catch(_e){}'
            'if(r.status===401){location.href="/owner/login";'
            'throw new Error("Owner authentication required");}'
            'if(!r.ok)throw new Error(data.detail||data.error||'
            '("HTTP "+r.status));return data;}'
            'async function loadSessions(preferred=""){'
            'const data=await jsonFetch("/api/ai/sessions");'
            'const items=data.sessions||[];'
            'const current=preferred||session.value;'
            'session.innerHTML="<option value=\\"\\">New conversation</option>"'
            '+items.map(s=>"<option value=\\""+esc(s.id)+"\\">"'
            '+esc((s.project||"AI-Toolkit")+" · "+s.id)'
            '+"</option>").join("");'
            'if(current&&items.some(s=>s.id===current))session.value=current;'
            '}'
            'async function loadSession(){'
            'if(!session.value){renderSources([]);return;}'
            'status.textContent="Loading conversation…";'
            'try{const data=await jsonFetch("/api/ai/sessions/"'
            '+encodeURIComponent(session.value));'
            'const s=data.session||{};renderSources(s.raw_sources||[]);'
            'if(s.selected_provider)provider.value=s.selected_provider;'
            'if(s.selected_model)model.value=s.selected_model;'
            'status.textContent="Conversation recovered.";}'
            'catch(e){status.textContent=e.message;status.className='
            '"chat-status error";}}'
            'provider.addEventListener("change",()=>{'
            'const o=provider.options[provider.selectedIndex];'
            'if(o&&o.dataset.model)model.value=o.dataset.model;});'
            'session.addEventListener("change",loadSession);'
            'form.addEventListener("submit",async e=>{'
            'e.preventDefault();const q=question.value.trim();if(!q)return;'
            'send.disabled=true;question.disabled=true;'
            'status.className="chat-status working";'
            'const storedSession=localStorage.getItem("ai_toolkit_partner_session_id");''if(storedSession&&session){session.value=storedSession;}''status.textContent="AI Partner is working…";'
            'try{const data=await jsonFetch("/api/ai/chat",{'
            'method:"POST",headers:{"Content-Type":"application/json"},'
            'body:JSON.stringify({question:q,session_id:session.value,'
            'provider_id:provider.value,model:model.value})});'
            'const sid=data.session_id||session.value;''if(sid){session.value=sid;localStorage.setItem("ai_toolkit_partner_session_id",sid);}''question.value="";'
            'await loadSessions(sid);session.value=sid;await loadSession();'
            'status.className="chat-status";'
            'status.textContent="AI response received and persisted.";}'
            'catch(e){status.className="chat-status error";'
            'status.textContent=e.message;}finally{send.disabled=false;'
            'question.disabled=false;question.focus();}});'
            'const first=provider.options[provider.selectedIndex];'
            'if(first&&first.dataset.model)model.value=first.dataset.model;'
            'loadSessions().then(()=>{'
            'if(session.options.length>1){session.selectedIndex=1;'
            'loadSession();}}).catch(e=>{status.textContent=e.message;});'
            '})();'
            '</script>'
        )

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

END DASHBOARD SERVICE

## Dashboard HTTP server anatomy

BEGIN DASHBOARD HTTP SERVER
from __future__ import annotations

import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlparse

from .service import EngineeringDashboardService


class _DashboardRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = self._normalize_path(parsed.path)
        query = parse_qs(parsed.query)
        server = self.server._dashboard_server  # type: ignore[attr-defined]
        if path == "/health":
            self._send_json({"ok": True, "service": "dashboard"})
            return
        if path == "/api/dashboard":
            self._send_json(server.service.build(refresh="refresh=1" in parsed.query))
            return
        if path == "/api/capabilities":
            payload = server.service.build(refresh="refresh=1" in parsed.query)
            self._send_json(payload["capabilities"])
            return
        if path == "/api/runtime":
            payload = server.service.build(refresh="refresh=1" in parsed.query)
            self._send_json(payload["runtime"])
            return
        if path == "/api/diagnostics":
            payload = server.service.build(refresh="refresh=1" in parsed.query)
            self._send_json(payload["diagnostics"])
            return
        if path == "/api/ai/control-center":
            payload = server.service.build(refresh="refresh=1" in parsed.query)
            self._send_json(payload["ai_control_center"])
            return
        if path == "/api/ai/ask":
            question = (query.get("q") or [""])[0].strip()
            prompt_name = (query.get("prompt") or [""])[0].strip()
            if not question and not prompt_name:
                self._send_json({"error": "missing query"}, status=400)
                return
            self._send_json(server.service.ask_repository(question=question, prompt_name=prompt_name))
            return
        payload = server.service.build(refresh="refresh=1" in parsed.query)
        if path == "/":
            self._send_html(server.service.render_home(payload))
            return
        if path == "/projects":
            self._send_html(server.service.render_projects(payload))
            return
        if path == "/repository":
            question = (query.get("q") or [""])[0].strip()
            prompt_name = (query.get("prompt") or [""])[0].strip()
            self._send_html(server.service.render_repository(payload, question=question, prompt_name=prompt_name))
            return
        if path == "/session":
            self._send_html(server.service.render_session(payload))
            return
        if path == "/ai-control-center":
            self._send_html(server.service.render_ai_control_center(payload))
            return
        if path == "/knowledge":
            self._send_html(server.service.render_explorer(payload))
            return
        if path == "/validation":
            self._send_html(server.service.render_diagnostics(payload))
            return
        if path == "/settings":
            self._send_html(server.service.render_runtime(payload))
            return
        if path == "/explorer":
            self._send_html(server.service.render_explorer(payload))
            return
        if path == "/reports":
            self._send_html(server.service.render_reports(payload))
            return
        if path == "/runtime":
            self._send_html(server.service.render_runtime(payload))
            return
        if path == "/diagnostics":
            self._send_html(server.service.render_diagnostics(payload))
            return
        if path.startswith("/capabilities/"):
            slug = path.rsplit("/", 1)[-1]
            page = server.service.render_capability(slug, payload)
            if page is None:
                self._send_json({"error": "not found"}, status=404)
                return
            self._send_html(page)
            return
        self._send_json({"error": "not found"}, status=404)

    def _normalize_path(self, path: str) -> str:
        aliases = {
            "/dashboard": "/",
            "/project-manager": "/projects",
            "/engineering-session": "/session",
        }
        return aliases.get(path, path)

    def _send_html(self, html: str, status: int = 200) -> None:
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, payload: Dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class DashboardHttpServer:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8081,
        repository_root: str = ".",
        workspace_root: Optional[str] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.service = EngineeringDashboardService(
            repository_root=repository_root,
            workspace_root=workspace_root,
        )
        self._server: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}/"

    def start(self) -> None:
        self.service.build(refresh=True)
        self._server = self._build_server()
        self._thread = threading.Thread(
            target=self._server.serve_forever,
            daemon=True,
            name="EngineeringDashboardHttpServer",
        )
        self._thread.start()

    def serve_forever(self) -> None:
        self.service.build(refresh=True)
        self._server = self._build_server()
        self._server.serve_forever()

    def stop(self) -> None:
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
        if self._thread is not None:
            self._thread.join(timeout=5)

    def _handler_class(self):
        return type(
            "EngineeringDashboardHandler",
            (_DashboardRequestHandler,),
            {},
        )

    def _build_server(self) -> HTTPServer:
        server = HTTPServer((self.host, self.port), self._handler_class())
        server._dashboard_server = self  # type: ignore[attr-defined]
        return server


def serve_dashboard(
    host: str = "127.0.0.1",
    port: int = 8081,
    repository_root: str = ".",
    workspace_root: Optional[str] = None,
    open_browser: bool = False,
) -> None:
    server = DashboardHttpServer(
        host=host,
        port=port,
        repository_root=repository_root,
        workspace_root=workspace_root,
    )
    print(f"AI-Toolkit Dashboard running at {server.url}")
    if open_browser:
        webbrowser.open(server.url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()

END DASHBOARD HTTP SERVER

## Runtime HTTP interface anatomy

BEGIN RUNTIME HTTP INTERFACE
"""
CORE-021 — Runtime HTTP Server
CANON-055 §5, CANON-056

Minimal HTTP server (stdlib only) that exposes:

    GET  /health    — liveness check
    GET  /ready     — readiness check
    GET  /metrics   — metrics snapshot
    GET  /status    — full Runtime status report
    POST /webhook/github  — GitHub webhook receiver
    POST /webhook/telegram — Telegram update receiver (fallback to polling)

Uses Python's built-in http.server so no third-party HTTP framework
is required.
"""

import json
import logging
import threading
from lib.python.runtime.interfaces.runtime_api import RuntimeApiRouter

from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional
from urllib.parse import parse_qs, urlparse

from python.runtime.owner_access import (
    OWNER_SESSION_COOKIE,
    OwnerAccessBoundary,
)

logger = logging.getLogger(__name__)


class _RuntimeHandler(BaseHTTPRequestHandler):
    """Request handler that delegates to the RuntimeHttpServer callbacks."""

    # These are set by RuntimeHttpServer before creating instances.
    _server_ref: "RuntimeHttpServer" = None  # type: ignore[assignment]

    def log_message(self, fmt, *args):
        logger.debug("HTTP %s", fmt % args)

    def _send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html: str, status: int = 200) -> None:
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _redirect(
        self,
        location: str,
        *,
        cookie: str = "",
    ) -> None:
        self.send_response(303)
        self.send_header("Location", location)
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _owner_login_page(
        self,
        *,
        rejected: bool = False,
    ) -> str:
        message = (
            "<p class=\"error\">Owner credential rejected.</p>"
            if rejected
            else ""
        )
        return (
            "<!doctype html><html><head>"
            "<meta charset=\"utf-8\">"
            "<meta name=\"viewport\" "
            "content=\"width=device-width,initial-scale=1\">"
            "<title>Owner Access — AI-Toolkit</title>"
            "<style>"
            "body{font-family:Arial,sans-serif;background:#0b1020;"
            "color:#e5e7eb;display:grid;place-items:center;"
            "min-height:100vh;margin:0}"
            ".box{width:min(92vw,460px);background:#111827;"
            "border:1px solid #1f2937;border-radius:14px;"
            "padding:24px}"
            "input,button{box-sizing:border-box;width:100%;"
            "padding:12px;margin-top:10px;border-radius:8px}"
            "input{background:#0b1020;color:#fff;"
            "border:1px solid #374151}"
            "button{background:#2563eb;color:#fff;border:0;"
            "font-weight:700;cursor:pointer}"
            ".muted{color:#9ca3af}.error{color:#fca5a5}"
            "</style></head><body><main class=\"box\">"
            "<h1>AI-Toolkit Owner Access</h1>"
            "<p class=\"muted\">Private · Single Owner · "
            "Human Authority</p>"
            + message
            + "<form method=\"post\" action=\"/owner/login\">"
            "<label for=\"owner-token\">Owner credential</label>"
            "<input id=\"owner-token\" name=\"owner_token\" "
            "type=\"password\" autocomplete=\"current-password\" "
            "required autofocus>"
            "<button type=\"submit\">Enter AI-Toolkit</button>"
            "</form></main></body></html>"
        )

    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length) if length else b""

    def _require_owner(self) -> bool:
        srv = self.__class__._server_ref
        decision = srv.owner_access.authenticate_request(self.headers)

        if decision.authenticated:
            return True

        self._send_json(
            {
                "error": "owner authentication required",
                "access": decision.as_dict(),
            },
            401,
        )
        return False

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        srv = self.__class__._server_ref
        normalized_dashboard_path = srv.normalize_dashboard_path(path)
        prefer_json = query.get("format", [""])[0] == "json" or "application/json" in self.headers.get("Accept", "")
        if path == "/owner/login":
            decision = srv.owner_access.authenticate_request(
                self.headers
            )
            if decision.authenticated:
                self._redirect("/ai-control-center")
            else:
                self._send_html(self._owner_login_page())
            return

        if path == "/owner/logout":
            self._redirect(
                "/owner/login",
                cookie=(
                    f"{OWNER_SESSION_COOKIE}=; Path=/; "
                    "Max-Age=0; HttpOnly; Secure; SameSite=Strict"
                ),
            )
            return

        if path == "/api/ai/sessions":
            if not self._require_owner():
                return
            if srv.dashboard_service is None:
                self._send_json(
                    {"error": "AI dashboard service unavailable"},
                    503,
                )
                return
            sessions = (
                srv.dashboard_service.ai_platform.sessions.list_sessions()
            )
            self._send_json({"sessions": sessions})
            return

        if path.startswith("/api/ai/sessions/"):
            if not self._require_owner():
                return
            if srv.dashboard_service is None:
                self._send_json(
                    {"error": "AI dashboard service unavailable"},
                    503,
                )
                return
            session_id = path.rsplit("/", 1)[-1].strip()
            session = (
                srv.dashboard_service.ai_platform.sessions.get(
                    session_id
                )
            )
            if not session:
                self._send_json(
                    {"error": "AI session not found"},
                    404,
                )
                return
            self._send_json({"session": session})
            return

        if normalized_dashboard_path == "/" and not prefer_json and srv.dashboard_service is not None:
            self._send_html(srv.render_dashboard(path, query))

        elif normalized_dashboard_path == "/" and prefer_json:
            data = srv.api.status()
            self._send_json(data)
        elif path in ("/health", "/api/v1/health"):
            data = srv.api.health()
            self._send_json(data, 200 if data.get("healthy") else 503)
        elif path == "/api/v1/runtime":
            self._send_json(srv.api.runtime())
        elif path in ("/organism", "/api/v1/organism"):
            status = srv.api.status()
            organism = status.get("organism")

            if organism is None:
                self._send_json(
                    {
                        "state": "UNKNOWN",
                        "reason": (
                            "Organism state is not available "
                            "from RuntimeBootstrap."
                        ),
                    },
                    503,
                )
            else:
                self._send_json(organism)
        elif path == "/runtime":
            if srv.dashboard_service is not None and not prefer_json:
                self._send_html(srv.render_dashboard(path, query))
            else:
                self._send_json(srv.api.runtime())
        elif path == "/diagnostics":
            if srv.dashboard_service is not None and not prefer_json:
                self._send_html(srv.render_dashboard(path, query))
            else:
                self._send_json(srv.api.status().get("diagnostics", {}))
        elif path == "/ready":
            data = srv.handle_ready()
            status = 200 if data.get("ready") else 503
            self._send_json(data, status)
        elif path in ("/metrics", "/api/v1/metrics"):
            self._send_json(srv.api.metrics())
        elif path in ("/status", "/api/v1/status"):
            self._send_json(srv.api.status())
        elif srv.dashboard_service is not None and normalized_dashboard_path in (
            "/",
            "/projects",
            "/session",
            "/repository",
            "/ai-control-center",
            "/explorer",
            "/reports",
            "/runtime",
            "/diagnostics",
        ):
            if normalized_dashboard_path == "/ai-control-center":
                decision = srv.owner_access.authenticate_request(
                    self.headers
                )
                if not decision.authenticated:
                    self._redirect("/owner/login")
                    return
            if normalized_dashboard_path == "/repository":
                privileged_query = bool(
                    (query.get("q") or [""])[0].strip()
                    or (query.get("prompt") or [""])[0].strip()
                )
                if privileged_query and not self._require_owner():
                    return
            self._send_html(srv.render_dashboard(path, query))
        elif srv.dashboard_service is not None and path == "/api/ai/control-center":
            if not self._require_owner():
                return
            payload = srv.dashboard_payload(refresh="1" in query.get("refresh", []))
            self._send_json(payload.get("ai_control_center", {}))
        elif srv.dashboard_service is not None and path == "/api/ai/ask":
            if not self._require_owner():
                return
            question = (query.get("q") or [""])[0].strip()
            prompt_name = (query.get("prompt") or [""])[0].strip()
            if not question and not prompt_name:
                self._send_json({"error": "missing query"}, 400)
                return
            self._send_json(srv.dashboard_service.ask_repository(question=question, prompt_name=prompt_name))
        elif srv.dashboard_service is not None and path == "/api/dashboard":
            self._send_json(srv.dashboard_payload(refresh="1" in query.get("refresh", [])))
        elif srv.dashboard_service is not None and path == "/api/capabilities":
            payload = srv.dashboard_payload(refresh="1" in query.get("refresh", []))
            self._send_json(payload.get("capabilities", {}))
        elif srv.dashboard_service is not None and path.startswith("/capabilities/"):
            page = srv.render_dashboard(path, query)
            if page is None:
                self._send_json({"error": "not found"}, 404)
            else:
                self._send_html(page)
        else:
            self._send_json({"error": "not found"}, 404)

    def do_POST(self) -> None:
        path = self.path.split("?")[0]
        srv = self.__class__._server_ref
        body = self._read_body()

        if path == "/owner/login":
            try:
                form = parse_qs(
                    body.decode("utf-8"),
                    keep_blank_values=True,
                )
            except UnicodeDecodeError:
                self._send_html(
                    self._owner_login_page(rejected=True),
                    400,
                )
                return

            supplied = (
                form.get("owner_token", [""])[0].strip()
            )
            decision = srv.owner_access.authenticate(
                {"Authorization": f"Bearer {supplied}"}
            )

            if not decision.authenticated:
                self._send_html(
                    self._owner_login_page(rejected=True),
                    401,
                )
                return

            session_value = (
                srv.owner_access.session_cookie_value()
            )
            self._redirect(
                "/ai-control-center",
                cookie=(
                    f"{OWNER_SESSION_COOKIE}={session_value}; "
                    "Path=/; HttpOnly; Secure; SameSite=Strict"
                ),
            )
            return

        if path == "/webhook/github":
            sig = self.headers.get("X-Hub-Signature-256", "")
            event_type = self.headers.get("X-GitHub-Event", "unknown")
            result = srv.handle_github_webhook(event_type, sig, body)
            self._send_json(result)
        elif path == "/webhook/telegram":
            result = srv.handle_telegram_update(body)
            self._send_json(result)
        elif path == "/api/ai/chat":
            if not self._require_owner():
                return
            if srv.dashboard_service is None:
                self._send_json(
                    {"error": "AI dashboard service unavailable"},
                    503,
                )
                return
            try:
                payload = json.loads(body.decode("utf-8") or "{}")
            except (UnicodeDecodeError, json.JSONDecodeError):
                self._send_json({"error": "invalid JSON body"}, 400)
                return

            question = str(payload.get("question", "")).strip()
            session_id = str(payload.get("session_id", "")).strip()
            provider_id = str(payload.get("provider_id", "")).strip()
            model = str(payload.get("model", "")).strip()
            prompt_name = str(payload.get("prompt_name", "")).strip()

            if not question and not prompt_name:
                self._send_json({"error": "missing question"}, 400)
                return

            try:
                result = srv.dashboard_service.ai_platform.ask_repository(
                    question=question,
                    session_id=session_id,
                    provider_id=provider_id,
                    model=model,
                    prompt_name=prompt_name,
                )
            except ValueError as exc:
                self._send_json({"error": str(exc)}, 400)
                return
            except Exception as exc:
                logger.exception("Owner AI chat failed")
                self._send_json(
                    {
                        "error": "AI chat execution failed",
                        "detail": f"{type(exc).__name__}: {exc}",
                    },
                    500,
                )
                return

            self._send_json(result)
        else:
            self._send_json({"error": "not found"}, 404)


class RuntimeHttpServer:
    """
    Minimal HTTP server for the Runtime Server.

    All route handlers are injectable so callers can wire in the
    real Health, Metrics, and Webhook implementations.
    """

    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        self._host = host
        self._port = port
        self._server: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None
        self.dashboard_service = None
        self.owner_access = OwnerAccessBoundary()

        # Default no-op handlers (replaced by bootstrap)
        self._health_handler: Callable[[], dict] = lambda: {"healthy": True}
        self._ready_handler: Callable[[], dict] = lambda: {"ready": True}
        self._runtime_handler: Callable[[], dict] = lambda: {"state": "BOOT"}
        self._metrics_handler: Callable[[], dict] = lambda: {}
        self._status_handler: Callable[[], dict] = lambda: {}
        self._github_handler: Callable[[str, str, bytes], dict] = lambda et, sig, b: {"ok": True}
        self._telegram_handler: Callable[[bytes], dict] = lambda b: {"ok": True}
        self.api = RuntimeApiRouter(
            health=self.handle_health,
            runtime=self.handle_runtime,
            status=self.handle_status,
            metrics=self.handle_metrics,
        )

    # ------------------------------------------------------------------ #
    # Handler injection
    # ------------------------------------------------------------------ #

    def set_health_handler(self, fn: Callable[[], dict]) -> None:
        self._health_handler = fn

    def set_ready_handler(self, fn: Callable[[], dict]) -> None:
        self._ready_handler = fn

    def set_runtime_handler(self, fn: Callable[[], dict]) -> None:
        self._runtime_handler = fn

    def set_metrics_handler(self, fn: Callable[[], dict]) -> None:
        self._metrics_handler = fn

    def set_status_handler(self, fn: Callable[[], dict]) -> None:
        self._status_handler = fn

    def set_github_webhook_handler(self, fn: Callable[[str, str, bytes], dict]) -> None:
        self._github_handler = fn

    def set_telegram_update_handler(self, fn: Callable[[bytes], dict]) -> None:
        self._telegram_handler = fn

    def set_dashboard_service(self, service: Any) -> None:
        self.dashboard_service = service

    # ------------------------------------------------------------------ #
    # Internal dispatch (called from _RuntimeHandler)
    # ------------------------------------------------------------------ #

    def handle_health(self) -> dict:
        try:
            return self._health_handler()
        except Exception as exc:
            logger.error("Health handler error: %s", exc)
            return {"healthy": True, "error": str(exc)}

    def handle_ready(self) -> dict:
        try:
            return self._ready_handler()
        except Exception as exc:
            logger.error("Ready handler error: %s", exc)
            return {"ready": False, "error": str(exc)}

    def handle_runtime(self) -> dict:
        try:
            return self._runtime_handler()
        except Exception as exc:
            logger.error("Runtime handler error: %s", exc)
            return {"state": "FAILED", "error": str(exc)}

    def handle_metrics(self) -> dict:
        try:
            return self._metrics_handler()
        except Exception as exc:
            return {"error": str(exc)}

    def handle_status(self) -> dict:
        try:
            return self._status_handler()
        except Exception as exc:
            return {"error": str(exc)}

    def handle_github_webhook(self, event_type: str, signature: str, body: bytes) -> dict:
        try:
            return self._github_handler(event_type, signature, body)
        except Exception as exc:
            logger.error("GitHub webhook handler error: %s", exc)
            return {"ok": False, "error": str(exc)}

    def handle_telegram_update(self, body: bytes) -> dict:
        try:
            return self._telegram_handler(body)
        except Exception as exc:
            logger.error("Telegram update handler error: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------ #
    # Lifecycle
    # ------------------------------------------------------------------ #

    def start(self) -> None:
        # Give the handler class a reference to this server instance
        # using a class-level attribute (one server per process).
        _RuntimeHandler._server_ref = self

        self._server = HTTPServer((self._host, self._port), _RuntimeHandler)
        self._thread = threading.Thread(
            target=self._server.serve_forever,
            name="RuntimeHttpServer",
            daemon=True,
        )
        self._thread.start()
        logger.info("RuntimeHttpServer listening on %s:%s", self._host, self._port)

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server.server_close()
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("RuntimeHttpServer stopped")

    def dashboard_payload(self, *, refresh: bool = False) -> dict:
        if self.dashboard_service is None:
            return {}
        return self.dashboard_service.build(refresh=refresh)

    def render_dashboard(self, path: str, query: Dict[str, Any]) -> Optional[str]:
        if self.dashboard_service is None:
            return None
        refresh = "1" in query.get("refresh", [])
        payload = self.dashboard_service.build(refresh=refresh)
        normalized_path = self.normalize_dashboard_path(path)
        if normalized_path == "/":
            return self.dashboard_service.render_home(payload)
        if normalized_path == "/projects":
            return self.dashboard_service.render_projects(payload)
        if normalized_path == "/session":
            return self.dashboard_service.render_session(payload)
        if normalized_path == "/repository":
            question = (query.get("q") or [""])[0].strip()
            prompt_name = (query.get("prompt") or [""])[0].strip()
            return self.dashboard_service.render_repository(payload, question=question, prompt_name=prompt_name)
        if normalized_path == "/ai-control-center":
            return self.dashboard_service.render_ai_control_center(payload)
        if normalized_path == "/explorer":
            return self.dashboard_service.render_explorer(payload)
        if normalized_path == "/reports":
            return self.dashboard_service.render_reports(payload)
        if normalized_path == "/runtime":
            return self.dashboard_service.render_runtime(payload)
        if normalized_path == "/diagnostics":
            return self.dashboard_service.render_diagnostics(payload)
        if normalized_path.startswith("/capabilities/"):
            slug = normalized_path.rsplit("/", 1)[-1]
            return self.dashboard_service.render_capability(slug, payload)
        return None

    def normalize_dashboard_path(self, path: str) -> str:
        aliases = {
            "/dashboard": "/",
            "/project-manager": "/projects",
            "/engineering-session": "/session",
            "/knowledge": "/explorer",
            "/validation": "/diagnostics",
            "/settings": "/runtime",
        }
        return aliases.get(path, path)

END RUNTIME HTTP INTERFACE

## AISessionEngine anatomy

BEGIN AI SESSION ENGINE
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping
from uuid import uuid4


class AISessionEngine:
    def __init__(
        self,
        repository_root: str = ".",
        *,
        state_root: str | None = None,
    ) -> None:
        self.root = Path(repository_root).resolve()

        configured_state_root = (
            state_root
            if state_root is not None
            else os.environ.get("AI_TOOLKIT_STATE_ROOT", "")
        )

        if configured_state_root:
            self.state_root = Path(
                configured_state_root
            ).expanduser().resolve()
        else:
            # Historical/local compatibility:
            # without an explicit durable root, preserve the established
            # repository-local state anatomy.
            self.state_root = self.root

        self.dir = (
            self.state_root
            / ".ai"
            / "ai_sessions"
        )

    def create(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        session = {
            "id": payload.get("id", f"AI-SESSION-{uuid4().hex[:12].upper()}"),
            "project": payload.get("project", self.root.name),
            "repository": payload.get("repository", self.root.name),
            "branch": payload.get("branch", ""),
            "issue": payload.get("issue", ""),
            "epic": payload.get("epic", ""),
            "sprint": payload.get("sprint", ""),
            "workspace": payload.get("workspace", ""),
            "repository_profile": payload.get("repository_profile", {}),
            "engineering_context": payload.get("engineering_context", {}),
            "selected_provider": payload.get("selected_provider", ""),
            "selected_model": payload.get("selected_model", ""),
            "prompt_history": list(payload.get("prompt_history", [])),
            "conversation_history": list(payload.get("conversation_history", [])),
            "raw_sources": list(payload.get("raw_sources", [])),
            "experience_id": payload.get("experience_id", ""),
            "journey_reference": dict(
                payload.get("journey_reference", {})
            ),
            "token_usage": list(payload.get("token_usage", [])),
            "created_at": payload.get("created_at", now),
            "updated_at": now,
        }
        self._save(session)
        return session

    def list_sessions(self) -> List[Dict[str, Any]]:
        if not self.dir.exists():
            return []
        items = []
        for path in sorted(self.dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            session = self._read(path)
            if session:
                items.append(session)
        return items

    def get(self, session_id: str) -> Dict[str, Any]:
        path = self.dir / f"{session_id}.json"
        return self._read(path)

    def bind_experience(
        self,
        session_id: str,
        experience_id: str,
    ) -> Dict[str, Any]:
        session = self.get(session_id)
        if not session:
            raise ValueError(f"unknown session {session_id}")

        existing = str(session.get("experience_id", "")).strip()
        if existing and existing != experience_id:
            raise ValueError(
                f"session {session_id} already belongs to Experience {existing}"
            )

        session["experience_id"] = experience_id
        session["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._save(session)
        return session

    def bind_journey(
        self,
        session_id: str,
        journey: Mapping[str, Any],
    ) -> Dict[str, Any]:
        """Persist only the cognitive Journey reference owned by a session."""
        session = self.get(session_id)

        if not session:
            raise ValueError(f"unknown session {session_id}")

        if not isinstance(journey, Mapping):
            raise TypeError("journey must be a mapping")

        journey_id = str(
            journey.get("journey_id", "")
        ).strip()

        need_id = str(
            journey.get("need_id", "")
        ).strip()

        if not journey_id:
            raise ValueError("journey_id must not be empty")

        if not need_id:
            raise ValueError("journey need_id must not be empty")

        reference = {
            "journey_id": journey_id,
            "need_id": need_id,
            "status": str(
                journey.get("status", "UNKNOWN")
            ).strip() or "UNKNOWN",
            "step_count": int(
                journey.get("step_count", 0)
            ),
            "epistemic_gain": bool(
                journey.get("epistemic_gain", False)
            ),
            "stopping_reason": str(
                journey.get("stopping_reason", "")
            ),
        }

        # A Conversation is durable across multiple human requests.
        # Each request may legitimately begin a new Journey.
        # The session therefore owns the CURRENT Journey reference;
        # Journey identity is not the lifetime identity of Conversation.
        session["journey_reference"] = reference
        session["updated_at"] = (
            datetime.now(timezone.utc).isoformat()
        )

        self._save(session)

        return session

    def mark_journey_interruption(
        self,
        session_id: str,
        *,
        reason: str,
    ) -> Dict[str, Any]:
        """Persist a non-authoritative interruption checkpoint."""
        session = self.get(session_id)

        if not session:
            raise ValueError(f"unknown session {session_id}")

        reference = session.get(
            "journey_reference",
            {},
        )

        if not isinstance(reference, Mapping) or not reference:
            return session

        reason = str(reason).strip()

        if not reason:
            reason = "runtime-interruption"

        checkpoint = dict(reference)
        checkpoint["status"] = "INTERRUPTED"
        checkpoint["stopping_reason"] = reason
        checkpoint["authority_conferred"] = False
        checkpoint["human_authority_preserved"] = True
        checkpoint["restart_recoverable"] = True

        session["journey_reference"] = checkpoint
        session["updated_at"] = (
            datetime.now(timezone.utc).isoformat()
        )

        self._save(session)

        return session

    def journey_reference(
        self,
        session_id: str,
    ) -> Dict[str, Any]:
        """Read the compact Journey reference owned by a session."""
        session = self.get(session_id)

        if not session:
            raise ValueError(f"unknown session {session_id}")

        reference = session.get(
            "journey_reference",
            {},
        )

        if not isinstance(reference, Mapping):
            return {}

        return dict(reference)

    def append_raw_source(
        self,
        session_id: str,
        source: Mapping[str, Any],
    ) -> Dict[str, Any]:
        session = self.get(session_id)
        if not session:
            raise ValueError(f"unknown session {session_id}")

        item = dict(source)

        if item.get("session_id") != session_id:
            raise ValueError("raw source session identity mismatch")

        sources = session.setdefault("raw_sources", [])
        expected_sequence = len(sources) + 1

        if item.get("sequence") != expected_sequence:
            raise ValueError(
                "raw source temporal sequence does not continue session order"
            )

        sources.append(item)
        session["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._save(session)
        return session

    def conversation_sources(
        self,
        session_id: str,
    ) -> List[Dict[str, Any]]:
        session = self.get(session_id)
        if not session:
            raise ValueError(f"unknown session {session_id}")
        return list(session.get("raw_sources", []))

    def append_interaction(self, session_id: str, question: str, answer: str, usage: Mapping[str, Any]) -> Dict[str, Any]:
        session = self.get(session_id)
        if not session:
            raise ValueError(f"unknown session {session_id}")
        now = datetime.now(timezone.utc).isoformat()
        session.setdefault("prompt_history", []).append(question)
        session.setdefault("conversation_history", []).append({"question": question, "answer": answer, "timestamp": now})
        session.setdefault("token_usage", []).append(dict(usage))
        session["updated_at"] = now
        self._save(session)
        return session

    def _save(self, session: Mapping[str, Any]) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        path = self.dir / f"{session['id']}.json"
        path.write_text(json.dumps(dict(session), indent=2), encoding="utf-8")

    def _read(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}

END AI SESSION ENGINE

## AIPlatformService anatomy

BEGIN AI PLATFORM SERVICE
from __future__ import annotations
import logging

from collections import defaultdict
from typing import Any, Dict, Mapping, Optional

from .adapters import builtin_adapters
from .context_builder import AIContextBuilder
from .conversation_experience import ConversationExperienceBridge
from .conversation_context import ConversationContextReconstructor
from .cognitive_coordination import (
    EpistemicCognitiveCoordinator,
    InformationNeed,
    JourneyState,
    NavigationPlan,
)
from python.evidence_engine.engine import EvidenceEngine
from .model_manager import ModelManager
from .pipeline import AIRequestPipeline
from .prompt_library import PromptLibrary
from .registry import ProviderRegistry
from .sessions import AISessionEngine
from .settings import AISettingsStore, masked_provider_settings

logger = logging.getLogger(__name__)



def _fusion02_context_anatomy(context):
    """Return structural size metadata, never context values."""
    import json

    def serialized_bytes(value):
        return len(
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                default=str,
            ).encode("utf-8")
        )

    total = serialized_bytes(context)
    branches = {}

    if isinstance(context, dict):
        for key, value in context.items():
            branch_bytes = serialized_bytes(value)

            branches[str(key)] = {
                "bytes": branch_bytes,
                "percent": round(
                    (
                        branch_bytes
                        / total
                        * 100.0
                    )
                    if total
                    else 0.0,
                    2,
                ),
                "kind": (
                    "object"
                    if isinstance(value, dict)
                    else "array"
                    if isinstance(value, list)
                    else "string"
                    if isinstance(value, str)
                    else type(value).__name__
                ),
                "children": (
                    len(value)
                    if isinstance(
                        value,
                        (dict, list),
                    )
                    else 0
                ),
            }

    return {
        "total_serialized_bytes": total,
        "estimated_tokens_at_4_bytes": (
            (total + 3) // 4
        ),
        "branch_count": len(branches),
        "branches": branches,
    }


def _fusion02_log_context_anatomy(context):
    """Log structural measurements only."""
    anatomy = _fusion02_context_anatomy(
        context
    )

    ordered = sorted(
        anatomy["branches"].items(),
        key=lambda item: (
            item[1]["bytes"]
        ),
        reverse=True,
    )

    branch_summary = ",".join(
        (
            f"{name}="
            f"{data['bytes']}"
            f"({data['percent']}%)"
        )
        for name, data in ordered
    )

    logger.info(
        "FUSION-02 reconstructed context anatomy: "
        "total_serialized_bytes=%s, "
        "estimated_tokens_at_4_bytes=%s, "
        "branch_count=%s, "
        "branches=%s",
        anatomy[
            "total_serialized_bytes"
        ],
        anatomy[
            "estimated_tokens_at_4_bytes"
        ],
        anatomy[
            "branch_count"
        ],
        branch_summary,
        extra={
            "fusion02_context_anatomy":
                anatomy,
        },
    )

    return anatomy


class AIPlatformService:
    def __init__(self, repository_root: str = ".", workspace_root: Optional[str] = None) -> None:
        self.settings = AISettingsStore(repository_root)
        self.registry = ProviderRegistry()
        self.model_manager = ModelManager()
        self.context_builder = AIContextBuilder(repository_root, workspace_root)
        self.sessions = AISessionEngine(repository_root)
        self.conversation_experience = ConversationExperienceBridge(repository_root)
        self.conversation_context = ConversationContextReconstructor(
            repository_root,
            workspace_root,
        )
        self.cognitive_coordinator = EpistemicCognitiveCoordinator()
        self.evidence_engine = EvidenceEngine(repository_root)
        self.prompt_library = PromptLibrary()
        self.pipeline = AIRequestPipeline(
            registry=self.registry,
            model_manager=self.model_manager,
            context_builder=self.context_builder,
        )
        for adapter in builtin_adapters():
            self.registry.register(adapter)

    def configure_provider(self, provider_id: str, **kwargs: Any) -> Dict[str, Any]:
        settings = self.settings.configure_provider(provider_id, **kwargs)
        return masked_provider_settings(settings)

    def configure_models(self, roles: Mapping[str, str]) -> Dict[str, Any]:
        settings = self.settings.configure_models(roles)
        return masked_provider_settings(settings)

    def configure_routing(self, default_provider: str = "", fallback_provider: str = "") -> Dict[str, Any]:
        settings = self.settings.configure_routing(
            default_provider=default_provider or None,
            fallback_provider=fallback_provider or None,
        )
        return masked_provider_settings(settings)

    def test_connection(self, provider_id: str) -> Dict[str, Any]:
        settings = self.settings.load()
        provider_settings = dict(settings.get("providers", {})).get(provider_id, {})
        return self.registry.test_connection(provider_id, provider_settings)

    def connect(self, provider_id: str) -> Dict[str, Any]:
        result = self.test_connection(provider_id)
        result["action"] = "connect"
        return result

    def disconnect(self, provider_id: str) -> Dict[str, Any]:
        result = {
            "provider": provider_id,
            "status": "disconnected",
            "connection": False,
            "action": "disconnect",
        }
        return result

    def create_session(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self.sessions.create(payload)

    def ask_repository(
        self,
        question: str,
        *,
        session_id: str = "",
        provider_id: str = "",
        model: str = "",
        prompt_name: str = "",
    ) -> Dict[str, Any]:
        settings = self.settings.load()
        prompt = self.prompt_library.resolve(
            prompt_name,
            fallback=question,
        )
        effective_question = question.strip() or prompt

        if session_id:
            session = self.sessions.get(session_id)
            if not session:
                raise ValueError(f"unknown session {session_id}")
        else:
            session = self.sessions.create(
                {
                    "project": self.sessions.root.name,
                    "repository": self.sessions.root.name,
                    "selected_provider": provider_id,
                    "selected_model": model,
                }
            )

        experience, binding = (
            self.conversation_experience.ensure_experience(session)
        )

        session = self.sessions.bind_experience(
            session["id"],
            str(experience.experience_id),
        )

        human_sequence = len(
            session.get("raw_sources", [])
        ) + 1

        human_source = self.conversation_experience.raw_source(
            session=session,
            experience=experience,
            actor="HUMAN",
            content=effective_question,
            sequence=human_sequence,
        )

        session = self.sessions.append_raw_source(
            session["id"],
            human_source,
        )

        cognitive_coordination = self.cognitive_coordinator.initialize(
            effective_question,
            session_id=session["id"],
        )

        need_data = cognitive_coordination["information_need"]
        journey_data = cognitive_coordination["journey"]
        navigation_plan_data = cognitive_coordination.get(
            "navigation_plan"
        )

        information_need = InformationNeed(
            schema=need_data["schema"],
            need_id=need_data["need_id"],
            question=need_data["question"],
            objective=need_data["objective"],
            epistemic_status=need_data["epistemic_status"],
            research_required=need_data["research_required"],
            requested_capabilities=tuple(
                need_data["requested_capabilities"]
            ),
            constraints=dict(need_data["constraints"]),
        )

        journey_state = JourneyState(
            schema=journey_data["schema"],
            journey_id=journey_data["journey_id"],
            need_id=journey_data["need_id"],
            status=journey_data["status"],
            step_count=journey_data["step_count"],
            epistemic_gain=journey_data["epistemic_gain"],
            visited=tuple(journey_data["visited"]),
            stopping_reason=journey_data["stopping_reason"],
        )

        search_navigation = None
        retrieval = None

        if (
            navigation_plan_data is not None
            and navigation_plan_data["required"] is True
            and "search" in navigation_plan_data["capabilities"]
        ):
            navigation_plan = NavigationPlan(
                schema=navigation_plan_data["schema"],
                need_id=navigation_plan_data["need_id"],
                required=navigation_plan_data["required"],
                capabilities=tuple(
                    navigation_plan_data["capabilities"]
                ),
                read_only=navigation_plan_data["read_only"],
                authority_preserved=navigation_plan_data[
                    "authority_preserved"
                ],
                working_context_materialized=(
                    navigation_plan_data[
                        "working_context_materialized"
                    ]
                ),
                retrieval_executed=navigation_plan_data[
                    "retrieval_executed"
                ],
                stopping_conditions=tuple(
                    navigation_plan_data["stopping_conditions"]
                ),
            )

            search_navigation = (
                self.cognitive_coordinator.execute_search_navigation(
                    plan=navigation_plan,
                    journey=journey_state,
                    keyword=effective_question,
                    search=self.evidence_engine.find,
                )
            )

            retrieval = search_navigation.get("retrieval")

            navigation_journey = search_navigation.get("journey")

            if navigation_journey is not None:
                journey_state = JourneyState(
                    schema=navigation_journey["schema"],
                    journey_id=navigation_journey["journey_id"],
                    need_id=navigation_journey["need_id"],
                    status=navigation_journey["status"],
                    step_count=navigation_journey["step_count"],
                    epistemic_gain=navigation_journey[
                        "epistemic_gain"
                    ],
                    visited=tuple(
                        navigation_journey["visited"]
                    ),
                    stopping_reason=navigation_journey[
                        "stopping_reason"
                    ],
                )

        read_navigation = None

        if isinstance(retrieval, dict):
            source_paths = retrieval.get(
                "source_paths",
                (),
            )

            if source_paths:
                selected_source_path = source_paths[0]

                def _bounded_repository_read(
                    repository_root,
                    relative_path,
                ):
                    target = (
                        repository_root / relative_path
                    ).resolve()

                    target.relative_to(
                        repository_root.resolve()
                    )

                    return target.read_text(
                        encoding="utf-8",
                    )

                read_navigation = (
                    self.cognitive_coordinator.execute_read_navigation(
                        selected_source_path,
                        read=_bounded_repository_read,
                        repository_root=self.sessions.root,
                    )
                )

                retrieval = (
                    self.cognitive_coordinator.attach_read_evidence(
                        retrieval=retrieval,
                        read_navigation=read_navigation,
                    )
                )

        working_context = (
            self.cognitive_coordinator.materialize_working_context(
                need=information_need,
                journey=journey_state,
                retrieval=retrieval,
            )
        )

        working_context_data = working_context.to_dict()

        # Bind the current Journey when the session is owned by the
        # persistent AISessionEngine. Synthetic/test-double sessions may
        # intentionally exist only at the service boundary.
        persisted_session = self.sessions.get(
            session["id"]
        )

        if persisted_session:
            session = self.sessions.bind_journey(
                session["id"],
                journey_state.to_dict(),
            )

        reconstructed_context = self.conversation_context.build(
            session["id"],
            partner_identity={
                "provider": provider_id or session.get(
                    "selected_provider", ""
                ),
                "model": model or session.get(
                    "selected_model", ""
                ),
            },
        )

        provider_cognitive_context = dict(
            reconstructed_context
        )
        provider_cognitive_context[
            "working_context"
        ] = working_context_data

        if read_navigation is not None:
            provider_cognitive_context[
                "read_navigation"
            ] = read_navigation

        _fusion02_log_context_anatomy(
            provider_cognitive_context
        )

        use_cognitive_working_context = getattr(
            self.pipeline,
            "use_cognitive_working_context",
            None,
        )

        if callable(use_cognitive_working_context):
            use_cognitive_working_context(
                working_context
            )

        try:
            result = self.pipeline.run(
                prompt,
                settings,
                provider_id=provider_id,
                model=model,
                context_override=provider_cognitive_context,
            )
        except Exception as exc:
            persisted_session = self.sessions.get(
                session["id"]
            )

            if persisted_session:
                self.sessions.mark_journey_interruption(
                    session["id"],
                    reason=(
                        "provider-failure:"
                        + type(exc).__name__
                    ),
                )

            raise

        session = self.sessions.append_interaction(
            session["id"],
            effective_question,
            result["answer"],
            result["usage"],
        )

        ai_sequence = len(
            session.get("raw_sources", [])
        ) + 1

        ai_source = self.conversation_experience.raw_source(
            session=session,
            experience=experience,
            actor="AI",
            content=result["answer"],
            sequence=ai_sequence,
            provider=result["provider"],
            model=result["model"],
        )

        session = self.sessions.append_raw_source(
            session["id"],
            ai_source,
        )

        return {
            "session_id": session["id"],
            "experience_id": str(experience.experience_id),
            "question": effective_question,
            "answer": result["answer"],
            "provider": result["provider"],
            "model": result["model"],
            "usage": result["usage"],
            "raw_source_count": len(
                session.get("raw_sources", [])
            ),
            "information_need": cognitive_coordination[
                "information_need"
            ],
            "journey": journey_state.to_dict(),
            "search_navigation": search_navigation,
            "read_navigation": read_navigation,
            "working_context": working_context_data,
            "context": provider_cognitive_context,
            "context_schema": provider_cognitive_context.get(
                "schema"
            ),
            "epistemic_status": {
                "conversation_is_raw_source": True,
                "conversation_is_evidence": False,
                "conversation_is_canon": False,
                "automatic_sedimentation": False,
                "retrieval_confers_authority": False,
                "human_authority_preserved": True,
                "unknown_is_valid": True,
            },
        }

    def usage_summary(self) -> Dict[str, Any]:
        sessions = self.sessions.list_sessions()
        total = {
            "tokens": 0,
            "estimated_cost": 0.0,
            "latency_ms": 0,
            "requests": 0,
            "success": 0,
            "errors": 0,
        }
        by_provider: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                "tokens": 0,
                "estimated_cost": 0.0,
                "latency_ms": 0,
                "requests": 0,
                "success": 0,
                "errors": 0,
            }
        )
        for session in sessions:
            for usage in session.get("token_usage", []):
                provider = usage.get("provider", "unknown")
                tokens = int(usage.get("input_tokens", 0)) + int(usage.get("output_tokens", 0))
                cost = float(usage.get("estimated_cost", 0.0))
                latency = int(usage.get("latency_ms", 0))
                success = bool(usage.get("success", False))

                total["tokens"] += tokens
                total["estimated_cost"] += cost
                total["latency_ms"] += latency
                total["requests"] += 1
                total["success"] += 1 if success else 0
                total["errors"] += 0 if success else 1

                by_provider[provider]["tokens"] += tokens
                by_provider[provider]["estimated_cost"] += cost
                by_provider[provider]["latency_ms"] += latency
                by_provider[provider]["requests"] += 1
                by_provider[provider]["success"] += 1 if success else 0
                by_provider[provider]["errors"] += 0 if success else 1

        success_rate = (total["success"] / total["requests"] * 100.0) if total["requests"] else 0.0
        avg_latency = (total["latency_ms"] / total["requests"]) if total["requests"] else 0.0
        return {
            "total": {
                **total,
                "estimated_cost": round(total["estimated_cost"], 6),
                "success_rate": round(success_rate, 2),
                "average_latency_ms": round(avg_latency, 2),
            },
            "by_provider": {
                provider: {
                    **stats,
                    "estimated_cost": round(float(stats["estimated_cost"]), 6),
                    "success_rate": round((stats["success"] / stats["requests"] * 100.0) if stats["requests"] else 0.0, 2),
                    "average_latency_ms": round((stats["latency_ms"] / stats["requests"]) if stats["requests"] else 0.0, 2),
                }
                for provider, stats in by_provider.items()
            },
        }

    def control_center(self) -> Dict[str, Any]:
        settings = self.settings.load()
        providers = self.registry.list_providers(settings)
        discovered = self.model_manager.discover_models(providers)
        role_models = self.model_manager.resolve_roles(settings, discovered)
        usage = self.usage_summary()
        return {
            "providers": providers,
            "connections": [
                {
                    "provider": item["id"],
                    "connect": True,
                    "disconnect": True,
                    "test_connection": True,
                    "last_success": item.get("last_success", ""),
                    "last_failure": item.get("last_failure", ""),
                    "last_response_time": item.get("last_response_time", 0),
                    "health_status": item.get("health", "unknown"),
                }
                for item in providers
            ],
            "model_manager": {
                "discovered_models": discovered,
                "role_models": role_models,
            },
            "settings": masked_provider_settings(settings),
            "prompt_library": self.prompt_library.list_categories(),
            "usage": usage,
            "recent_sessions": [
                {
                    "id": item.get("id", ""),
                    "project": item.get("project", ""),
                    "repository": item.get("repository", ""),
                    "branch": item.get("branch", ""),
                    "issue": item.get("issue", ""),
                    "epic": item.get("epic", ""),
                    "sprint": item.get("sprint", ""),
                    "workspace": item.get("workspace", ""),
                    "selected_provider": item.get("selected_provider", ""),
                    "selected_model": item.get("selected_model", ""),
                    "prompt_count": len(item.get("prompt_history", [])),
                    "conversation_count": len(item.get("conversation_history", [])),
                }
                for item in self.sessions.list_sessions()[:10]
            ],
        }

END AI PLATFORM SERVICE

## Existing owner chat acceptance

BEGIN OWNER CHAT TEST
from __future__ import annotations

import os

from python.dashboard.service import EngineeringDashboardService
from python.runtime.owner_access import (
    OWNER_SESSION_COOKIE,
    OwnerAccessBoundary,
)


def test_owner_web_session_is_derived_not_raw_secret(monkeypatch):
    monkeypatch.setenv(
        "AI_TOOLKIT_OWNER_TOKEN",
        "fusion-02-test-owner-secret",
    )
    boundary = OwnerAccessBoundary()
    cookie_value = boundary.session_cookie_value()

    assert cookie_value
    assert cookie_value != "fusion-02-test-owner-secret"
    assert "fusion-02-test-owner-secret" not in cookie_value


def test_owner_cookie_authenticates_existing_boundary(monkeypatch):
    monkeypatch.setenv(
        "AI_TOOLKIT_OWNER_TOKEN",
        "fusion-02-test-owner-secret",
    )
    boundary = OwnerAccessBoundary()
    cookie = (
        f"{OWNER_SESSION_COOKIE}="
        f"{boundary.session_cookie_value()}"
    )

    decision = boundary.authenticate_request(
        {"Cookie": cookie}
    )

    assert decision.authenticated is True
    assert decision.role == "OWNER"
    assert decision.human_authority is True


def test_invalid_owner_cookie_fails_closed(monkeypatch):
    monkeypatch.setenv(
        "AI_TOOLKIT_OWNER_TOKEN",
        "fusion-02-test-owner-secret",
    )
    boundary = OwnerAccessBoundary()

    decision = boundary.authenticate_request(
        {
            "Cookie": (
                f"{OWNER_SESSION_COOKIE}=not-valid"
            )
        }
    )

    assert decision.authenticated is False
    assert decision.human_authority is False


def test_existing_bearer_contract_remains_valid(monkeypatch):
    monkeypatch.setenv(
        "AI_TOOLKIT_OWNER_TOKEN",
        "fusion-02-test-owner-secret",
    )
    boundary = OwnerAccessBoundary()

    decision = boundary.authenticate_request(
        {
            "Authorization": (
                "Bearer fusion-02-test-owner-secret"
            )
        }
    )

    assert decision.authenticated is True
    assert decision.role == "OWNER"


def test_ai_control_center_contains_real_chat_surface(tmp_path):
    service = EngineeringDashboardService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    control = {
        "providers": [
            {
                "id": "openai",
                "provider_id": "openai",
                "name": "OpenAI",
                "connection": True,
                "models": ["gpt-4.1"],
            }
        ]
    }

    html = service._owner_ai_chat_panel(control)

    assert 'id="chat-form"' in html
    assert 'id="chat-question"' in html
    assert 'id="chat-session"' in html
    assert 'id="chat-provider"' in html
    assert "/api/ai/chat" in html
    assert "/api/ai/sessions" in html
    assert "AI Partner is working" in html
    assert "RAW conversation" in html
    assert "Evidence or Canon" in html


def test_chat_ui_does_not_embed_owner_secret(
    tmp_path,
    monkeypatch,
):
    secret = "MUST-NOT-APPEAR-IN-HTML"
    monkeypatch.setenv(
        "AI_TOOLKIT_OWNER_TOKEN",
        secret,
    )

    service = EngineeringDashboardService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    html = service._owner_ai_chat_panel(
        {
            "providers": [
                {
                    "id": "openai",
                    "name": "OpenAI",
                    "connection": True,
                    "models": ["gpt-4.1"],
                }
            ]
        }
    )

    assert secret not in html
    assert "AI_TOOLKIT_OWNER_TOKEN" not in html


def test_chat_uses_same_origin_cookie_not_js_owner_token(
    tmp_path,
):
    service = EngineeringDashboardService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    html = service._owner_ai_chat_panel(
        {
            "providers": [
                {
                    "id": "openai",
                    "name": "OpenAI",
                    "connection": True,
                    "models": ["gpt-4.1"],
                }
            ]
        }
    )

    assert 'credentials:"same-origin"' in html
    assert "Authorization" not in html
    assert "Bearer " not in html


def test_session_readback_uses_existing_ai_session_engine():
    from python.ai_platform.sessions import AISessionEngine

    assert hasattr(AISessionEngine, "list_sessions")
    assert hasattr(AISessionEngine, "get")
    assert hasattr(AISessionEngine, "conversation_sources")

END OWNER CHAT TEST

## Browser frontend candidates

BEGIN FRONTEND PATHS
NONE FOUND
END FRONTEND PATHS

## Recovered real physiological chain

Browser AI Partner
-> POST /api/ai/chat
-> session_id from browser
-> dashboard_service.ai_platform.ask_repository
-> AIPlatformService
-> AISessionEngine
-> AI_TOOLKIT_STATE_ROOT
-> durable session state

## Required acceptance

1. AI Partner creates or continues a session.
2. Response returns the actual session_id.
3. Browser stores that session_id.
4. Page reload restores that session_id.
5. Next message sends the same session_id.
6. AISessionEngine resolves the same durable session.
7. Conversation history remains continuous.
8. Railway redeploy occurs.
9. Browser reconnects to the same durable session.
10. Conversation continues after redeployment.
11. Full FUSION regression remains green.

## Conservation

- No reset.
- No restore.
- No force push.
- Existing production mutation preserved.
- Durable state-root physiology preserved.
- Human authority preserved.

## Status

REAL SESSION REATTACHMENT ANATOMY RECOVERED.

IMPLEMENTATION NOT YET CERTIFIED.
