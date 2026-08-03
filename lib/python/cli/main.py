#!/usr/bin/env python3

import argparse
import json
import os
import sys
from pathlib import Path

# Ensure lib/ is in sys.path so that `from python.xxx` imports work regardless
# of how this module is invoked (e.g. `python3 -m lib.python.cli.main` or
# `PYTHONPATH=lib python3 -m python.cli.main`).
_lib_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
if _lib_dir not in sys.path:
    sys.path.insert(0, _lib_dir)

from python.agent_runtime.models import AgentContext
from python.agent_runtime.registry import build_runtime

from python.repository_engine.engine import RepositoryEngine
from python.dependency_engine.engine import DependencyEngine
from python.validation_engine.engine import ValidationEngine
from python.planning_engine.engine import PlanningEngine


def cmd_inventory():

    print(json.dumps(
        RepositoryEngine(".").statistics(),
        indent=2
    ))


def cmd_dependencies():

    print(json.dumps(
        DependencyEngine(".").statistics(),
        indent=2
    ))


def cmd_validate():

    print(json.dumps(
        ValidationEngine(".").statistics(),
        indent=2
    ))


def cmd_plan(repository=".", workspace=None, as_json=False, refresh=False):
    """
    Autonomous Planning Engine (CORE-014).

    Falls back to the legacy PlanningEngine summary when the
    AutonomousPlanningEngine is unavailable.
    """
    import json as _json
    try:
        from python.autonomous_planning_engine import AutonomousPlanningEngine
        engine = AutonomousPlanningEngine(
            repository=repository,
            workspace_root=workspace,
            persist=True,
            refresh_integrations=refresh,
        )
        result = engine.plan()
        if as_json:
            print(_json.dumps(result["planning_dict"], indent=2))
        else:
            d = result["planning_dict"]
            rp = d.get("roadmap_progress", {})
            na = d.get("next_actions", {})
            queue = d.get("execution_queue", {})
            print(f"AI CTO Autonomous Planning — {repository}")
            print(f"  Planning ID:  {d.get('planning_id', '')}")
            print(f"  Phase:        {rp.get('current_phase', '')}")
            print(f"  Maturity:     {rp.get('repository_maturity', '')}")
            print(f"  Progress:     {rp.get('completion_percentage', 0.0):.1f}%")
            print(f"  COREs done:   {len(rp.get('completed_cores', []))}")
            print(f"  COREs left:   {len(rp.get('incomplete_cores', []))}")
            print()
            nc = na.get("next_core")
            if nc:
                print(f"  Next CORE:    {nc.get('id', '')} — {nc.get('reason', '')}")
            ni = na.get("next_issue")
            if ni:
                print(f"  Next Issue:   {ni.get('title', '')}")
            nb = na.get("next_batch")
            if nb:
                print(f"  Next Batch:   {nb.get('title', nb.get('id', ''))}")
            npr = na.get("next_pr")
            if npr:
                print(f"  Next PR:      {npr.get('title', '')}")
            nm = na.get("next_milestone")
            if nm:
                print(f"  Next MS:      {nm.get('title', '')}")
            print()
            print(f"  Queue:        {queue.get('entry_count', 0)} items")
            paths = result.get("paths", {})
            if paths.get("markdown"):
                print(f"  Report:       {paths['markdown']}")
            if paths.get("planning"):
                print(f"  Plan JSON:    {paths['planning']}")
    except Exception:
        # Graceful fallback to legacy plan engine
        plan = PlanningEngine(".").build_plan()
        print("Execution Plan:", plan.identifier)
        print()
        for task in plan.tasks:
            print(f"[{task.priority}] {task.identifier} -> {task.title}")


def cmd_agent(agent_name, repository=".", output_dir="."):

    runtime = build_runtime()

    result = runtime.execute(
        agent_name,
        AgentContext(
            repository=repository,
            metadata={"output_dir": output_dir},
        )
    )

    print(json.dumps(
        result.data,
        indent=2
    ))

    for message in result.messages:
        print(message)


parser = argparse.ArgumentParser(
    prog="ai"
)

sub = parser.add_subparsers(dest="command")

for command in [
    "inventory",
    "dependencies",
    "validate",
]:
    sub.add_parser(command)

plan_parser = sub.add_parser(
    "plan",
    help="Autonomous Planning Engine (CORE-014)",
)
plan_parser.add_argument(
    "--json",
    action="store_true",
    dest="plan_json",
    help="Output planning result as JSON",
)
plan_parser.add_argument(
    "--refresh",
    action="store_true",
    dest="plan_refresh",
    help="Refresh all intelligence integrations before planning",
)
plan_parser.add_argument(
    "--repository",
    default=".",
    metavar="PATH",
    dest="plan_repository",
    help="Path to the repository (default: current directory)",
)
plan_parser.add_argument(
    "--workspace",
    default=None,
    metavar="PATH",
    dest="plan_workspace",
    help="Path to the workspace root (default: parent of repository)",
)

inspect_parser = sub.add_parser(
    "inspect",
    help="Scan a repository and generate AI_CTO_INTEGRATION_REPORT.md",
)
inspect_parser.add_argument(
    "path",
    nargs="?",
    default=".",
    help="Path to the repository to inspect (default: current directory)",
)
inspect_parser.add_argument(
    "--output",
    default=".",
    metavar="DIR",
    help="Directory where AI_CTO_INTEGRATION_REPORT.md will be written (default: current directory)",
)
inspect_parser.add_argument(
    "--semantic-only",
    action="store_true",
    dest="semantic_only",
    help="Run semantic analysis only and print a JSON summary (no full report)",
)
inspect_parser.add_argument(
    "--runtime",
    action="store_true",
    dest="runtime",
    help="Run executable repository intelligence (CORE-008C) and print a JSON summary",
)
inspect_parser.add_argument(
    "--execution-model",
    action="store_true",
    dest="execution_model",
    help=(
        "Run full executable intelligence pipeline (CORE-008C), persist "
        ".ai/runtime_repository_model.json, .ai/executable_repository_map.json, "
        "and generate AI_CTO_EXECUTION_MODEL.md"
    ),
)

briefing_parser = sub.add_parser(
    "briefing",
    help="Generate AI CTO Executive Briefing (CORE-010)",
)
briefing_parser.add_argument(
    "--repository",
    default=".",
    metavar="PATH",
    dest="briefing_repository",
    help="Path to the repository (default: current directory)",
)
briefing_parser.add_argument(
    "--json",
    action="store_true",
    dest="briefing_json",
    help="Output briefing as JSON instead of the markdown summary",
)
briefing_parser.add_argument(
    "--refresh",
    action="store_true",
    dest="briefing_refresh",
    help="Refresh all intelligence integrations before generating the briefing",
)

workspace_parser = sub.add_parser(
    "workspace",
    help="Multi-Repository Workspace Orchestrator (CORE-012)",
)
workspace_parser.add_argument(
    "--scan",
    action="store_true",
    dest="workspace_scan",
    help="Scan all repositories in the workspace and generate the dashboard",
)
workspace_parser.add_argument(
    "--refresh",
    action="store_true",
    dest="workspace_refresh",
    help="Re-scan all repositories (full refresh, ignores cache)",
)
workspace_parser.add_argument(
    "--repository",
    default=None,
    metavar="PATH",
    dest="workspace_repository",
    help="Register or re-scan a single repository and update workspace state",
)
workspace_parser.add_argument(
    "--dashboard",
    action="store_true",
    dest="workspace_dashboard",
    help="Generate (or reload) the AI_CTO_WORKSPACE_DASHBOARD.md",
)
workspace_parser.add_argument(
    "--json",
    action="store_true",
    dest="workspace_json",
    help="Output workspace scan result as JSON",
)
workspace_parser.add_argument(
    "--workspace",
    default=".",
    metavar="PATH",
    dest="workspace_root",
    help=(
        "Path to the workspace root directory containing multiple repositories "
        "(default: parent of current directory)"
    ),
)

context_parser = sub.add_parser(
    "context",
    help="Synchronize AI CTO live context (CORE-013)",
)
context_parser.add_argument(
    "--refresh",
    action="store_true",
    dest="context_refresh",
    help="Refresh synchronized context and downstream artifacts",
)
context_parser.add_argument(
    "--json",
    action="store_true",
    dest="context_json",
    help="Output synchronized context as JSON",
)
context_parser.add_argument(
    "--repository",
    default=".",
    metavar="PATH",
    dest="context_repository",
    help="Path to the repository (default: current directory)",
)
context_parser.add_argument(
    "--workspace",
    default=None,
    metavar="PATH",
    dest="context_workspace",
    help="Path to the workspace root (default: parent of repository)",
)

args = parser.parse_args()

if args.command == "inventory":

    cmd_inventory()

elif args.command == "dependencies":

    cmd_dependencies()

elif args.command == "validate":

    cmd_validate()

elif args.command == "plan":

    cmd_plan(
        repository=getattr(args, "plan_repository", "."),
        workspace=getattr(args, "plan_workspace", None),
        as_json=getattr(args, "plan_json", False),
        refresh=getattr(args, "plan_refresh", False),
    )

elif args.command == "inspect":

    if getattr(args, "runtime", False) or getattr(args, "execution_model", False):
        import json as _json
        from python.executable_repository_intelligence import ExecutableRepositoryEngine
        persist = getattr(args, "execution_model", False)
        engine = ExecutableRepositoryEngine(repository=args.path, persist=persist)
        result = engine.analyze()
        summary = {
            "repository": result["repository"],
            "executable_file_count": result["executable_file_count"],
            "non_executable_file_count": result["non_executable_file_count"],
            "category_distribution": result["category_distribution"],
            "zone_distribution": result["zone_distribution"],
            "safety_distribution": result["safety_distribution"],
            "main_entry_point": result["runtime_map"]["main_entry_point"],
            "execution_chain": result["runtime_map"]["execution_chain"][:5],
            "bootstrap_sequence": result["runtime_map"]["bootstrap_sequence"][:5],
            "runtime_component_count": len(result["runtime_map"]["runtime_components"]),
            "executable_dep_nodes": result["executable_dependency_graph"]["node_count"],
            "executable_dep_edges": result["executable_dependency_graph"]["edge_count"],
            "recommendation_count": len(result["recommendations"]),
            "zone_count": len(result["zones"]),
        }
        print(_json.dumps(summary, indent=2))
    elif getattr(args, "semantic_only", False):
        import json as _json
        from python.semantic_repository_intelligence import SemanticRepositoryEngine
        engine = SemanticRepositoryEngine(repository=args.path, persist=False)
        result = engine.analyze()
        summary = {
            "repository": result["repository"],
            "file_count": result["file_count"],
            "import_graph": result["import_graph"],
            "architecture_graph": {
                "node_count": result["architecture_graph"]["node_count"],
                "edge_count": result["architecture_graph"]["edge_count"],
                "hotspots": result["architecture_graph"]["hotspots"],
                "extension_points": result["architecture_graph"]["extension_points"],
                "risk_count": len(result["architecture_graph"]["risks"]),
            },
            "injection_point_count": len(result["injection_points"]),
            "recommendation_count": len(result["recommendations"]),
            "complexity": result["complexity"],
            "next_core": result["next_core"],
        }
        print(_json.dumps(summary, indent=2))
    else:
        cmd_agent("inspect", repository=args.path, output_dir=args.output)

elif args.command == "briefing":

    import json as _json
    from python.executive_briefing_engine import ExecutiveBriefingEngine

    repository = getattr(args, "briefing_repository", ".")
    as_json = getattr(args, "briefing_json", False)
    refresh = getattr(args, "briefing_refresh", False)

    engine = ExecutiveBriefingEngine(
        repository=repository,
        output_dir=repository,
        persist=True,
        refresh_integrations=refresh,
    )
    result = engine.generate()

    if as_json:
        print(_json.dumps(result["briefing_dict"], indent=2))
    else:
        briefing = result["briefing"]
        print(result["markdown"])
        print()
        print(f"Briefing ID:  {briefing.briefing_id}")
        print(f"Generated:    {briefing.generated_at}")
        print(f"Repository:   {briefing.repository}")
        paths = result.get("paths", {})
        if paths.get("markdown"):
            print(f"Markdown:     {paths['markdown']}")
        if paths.get("briefing"):
            print(f"JSON:         {paths['briefing']}")

elif args.command == "workspace":

    import json as _json
    from python.workspace_orchestrator import WorkspaceOrchestrator

    workspace_root = getattr(args, "workspace_root", ".")
    do_scan = getattr(args, "workspace_scan", False)
    do_refresh = getattr(args, "workspace_refresh", False)
    repo_path = getattr(args, "workspace_repository", None)
    do_dashboard = getattr(args, "workspace_dashboard", False)
    as_json = getattr(args, "workspace_json", False)

    orchestrator = WorkspaceOrchestrator(
        workspace_root=workspace_root,
        output_dir=workspace_root,
        persist=True,
    )

    if repo_path is not None:
        repo = orchestrator.register_repository(repo_path)
        if as_json:
            print(_json.dumps(repo.to_dict(), indent=2))
        else:
            print(f"Repository registered: {repo.name}")
            print(f"  Root:     {repo.repository_root}")
            print(f"  Health:   {repo.repository_health.upper()}")
            print(f"  Readiness:{repo.readiness:.0f}%")

    elif do_scan or do_refresh:
        result = orchestrator.scan(refresh=do_refresh)
        if as_json:
            print(_json.dumps(result.to_dict(), indent=2))
        else:
            print(f"Workspace scan complete.")
            print(f"  Workspace:     {result.workspace_root}")
            print(f"  Repositories:  {result.total_repositories}")
            print(f"  Scanned:       {result.scanned_repositories}")
            print(f"  Failed:        {result.failed_repositories}")
            print(f"  Health:        {result.health.overall_health.upper()}")
            print(f"  Readiness:     {result.health.overall_readiness:.0f}%")
            print(f"  Risks:         {len(result.risks)}")
            print(f"  Recommendations: {len(result.recommendations)}")
            if result.priorities:
                top = result.priorities[0]
                print(f"  Suggested Next: {top.repository}")
            paths = {
                "dashboard_md": str(
                    __import__("pathlib").Path(workspace_root) / "AI_CTO_WORKSPACE_DASHBOARD.md"
                ),
                "workspace_json": str(
                    __import__("pathlib").Path(workspace_root) / ".ai" / "workspace" / "workspace.json"
                ),
            }
            print(f"  Dashboard:     {paths['dashboard_md']}")
            print(f"  Workspace JSON:{paths['workspace_json']}")

    elif do_dashboard:
        dashboard_result = orchestrator.dashboard()
        if as_json:
            print(_json.dumps(dashboard_result["dashboard_dict"], indent=2))
        else:
            print(dashboard_result["markdown"])
            paths = dashboard_result.get("paths", {})
            if paths.get("dashboard_md"):
                print(f"\nDashboard written: {paths['dashboard_md']}")

    else:
        # Default: show a brief workspace summary
        dashboard_result = orchestrator.dashboard()
        if as_json:
            print(_json.dumps(dashboard_result["dashboard_dict"], indent=2))
        else:
            dd = dashboard_result["dashboard_dict"]
            summary = dd.get("workspace_summary", {})
            print(f"AI CTO Workspace — {workspace_root}")
            print(f"  Repositories:  {summary.get('total_repositories', 0)}")
            print(f"  Health:        {summary.get('overall_health', 'unknown').upper()}")
            print(f"  Readiness:     {summary.get('overall_readiness', 0):.1f}%")
            nr = dd.get("suggested_next_repository", "")
            if nr:
                print(f"  Next Repo:     {nr}")

elif args.command == "context":

    import json as _json
    from python.context_synchronization_engine import ContextSynchronizationEngine

    repository = getattr(args, "context_repository", ".")
    workspace_root = getattr(args, "context_workspace", None)
    as_json = getattr(args, "context_json", False)
    refresh = getattr(args, "context_refresh", False)

    engine = ContextSynchronizationEngine(
        repository=repository,
        workspace_root=workspace_root,
        persist=True,
    )
    result = engine.synchronize(refresh=refresh)

    if as_json:
        print(_json.dumps(result, indent=2, sort_keys=True))
    else:
        live = result.get("live_context", {})
        report = result.get("synchronization_report", {})
        paths = result.get("paths", {})
        print("AI CTO Context Synchronization complete.")
        print(f"  Repository:     {live.get('repository', '')}")
        print(f"  Root:           {live.get('repository_root', '')}")
        print(f"  Workspace:      {live.get('workspace', '')}")
        print(f"  Branch:         {live.get('current_branch', '')}")
        print(f"  Commit:         {live.get('current_commit', '')}")
        print(f"  Issue:          {live.get('current_issue', '')}")
        print(f"  Batch:          {live.get('current_batch', '')}")
        print(f"  Recommendation: {live.get('current_recommendation', '')}")
        print(f"  Findings:       {report.get('finding_count', 0)}")
        print(f"  Context JSON:   {paths.get('live_context', str(Path(repository).resolve() / '.ai' / 'context' / 'live_context.json'))}")
        print(f"  Report:         {paths.get('markdown', str(Path(repository).resolve() / '.ai' / 'context' / 'AI_CTO_CONTEXT_REPORT.md'))}")

else:

    parser.print_help()
    sys.exit(1)
