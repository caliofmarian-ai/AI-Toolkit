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

execute_parser = sub.add_parser(
    "execute",
    help="Autonomous Execution Engine (CORE-015)",
)
execute_parser.add_argument(
    "--repository",
    default=".",
    metavar="PATH",
    dest="execute_repository",
    help="Path to the repository (default: current directory)",
)
execute_parser.add_argument(
    "--workspace",
    default=None,
    metavar="PATH",
    dest="execute_workspace",
    help="Path to the workspace root (default: parent of repository)",
)
execute_parser.add_argument(
    "--json",
    action="store_true",
    dest="execute_json",
    help="Output execution result as JSON",
)
execute_parser.add_argument(
    "--refresh",
    action="store_true",
    dest="execute_refresh",
    help="Refresh all intelligence integrations before execution",
)
execute_parser.add_argument(
    "--simulate",
    action="store_true",
    dest="execute_simulate",
    help="Run in SIMULATION mode (no mutations)",
)
execute_parser.add_argument(
    "--dry-run",
    action="store_true",
    dest="execute_dry_run",
    help="Run in DRY_RUN mode (describe actions without executing)",
)
execute_parser.add_argument(
    "--validate",
    action="store_true",
    dest="execute_validate",
    help="Run in VALIDATION_ONLY mode",
)

evaluate_parser = sub.add_parser(
    "evaluate",
    help="Self Evaluation Engine (CORE-016)",
)
evaluate_parser.add_argument(
    "--repository",
    default=".",
    metavar="PATH",
    dest="evaluate_repository",
    help="Path to the repository (default: current directory)",
)
evaluate_parser.add_argument(
    "--workspace",
    default=None,
    metavar="PATH",
    dest="evaluate_workspace",
    help="Path to the workspace root (default: parent of repository)",
)
evaluate_parser.add_argument(
    "--json",
    action="store_true",
    dest="evaluate_json",
    help="Output evaluation result as JSON",
)
evaluate_parser.add_argument(
    "--refresh",
    action="store_true",
    dest="evaluate_refresh",
    help="Refresh integrations before evaluation",
)
evaluate_parser.add_argument(
    "--regressions",
    action="store_true",
    dest="evaluate_regressions",
    help="Show only regression findings",
)
evaluate_parser.add_argument(
    "--quality",
    action="store_true",
    dest="evaluate_quality",
    help="Show only quality scores",
)

improve_parser = sub.add_parser(
    "improve",
    help="Self Improvement Engine (CORE-017)",
)
improve_parser.add_argument(
    "--repository",
    default=".",
    metavar="PATH",
    dest="improve_repository",
    help="Path to the repository (default: current directory)",
)
improve_parser.add_argument(
    "--workspace",
    default=None,
    metavar="PATH",
    dest="improve_workspace",
    help="Path to the workspace root (default: parent of repository)",
)
improve_parser.add_argument(
    "--json",
    action="store_true",
    dest="improve_json",
    help="Output improvement plan as JSON",
)
improve_parser.add_argument(
    "--refresh",
    action="store_true",
    dest="improve_refresh",
    help="Refresh integrations before improvement analysis",
)
improve_parser.add_argument(
    "--technical-debt",
    action="store_true",
    dest="improve_technical_debt",
    help="Show only technical debt findings",
)
improve_parser.add_argument(
    "--performance",
    action="store_true",
    dest="improve_performance",
    help="Show only performance metrics",
)
improve_parser.add_argument(
    "--roadmap",
    action="store_true",
    dest="improve_roadmap",
    help="Show only roadmap update recommendations",
)

dashboard_parser = sub.add_parser(
    "dashboard",
    help="Serve the Engineering Operating System dashboard",
)
dashboard_parser.add_argument(
    "dashboard_action",
    nargs="?",
    default="serve",
    choices=["serve"],
    help="Dashboard action to execute (default: serve)",
)
dashboard_parser.add_argument(
    "--host",
    default="127.0.0.1",
    help="HTTP host to bind (default: 127.0.0.1)",
)
dashboard_parser.add_argument(
    "--port",
    type=int,
    default=8081,
    help="HTTP port to bind (default: 8081)",
)
dashboard_parser.add_argument(
    "--repository",
    default=".",
    metavar="PATH",
    dest="dashboard_repository",
    help="Path to the repository (default: current directory)",
)
dashboard_parser.add_argument(
    "--workspace",
    default=None,
    metavar="PATH",
    dest="dashboard_workspace",
    help="Path to the workspace root (default: parent of repository)",
)
dashboard_parser.add_argument(
    "--open-browser",
    action="store_true",
    dest="dashboard_open_browser",
    help="Open the dashboard URL in the default browser",
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

elif args.command == "execute":

    import json as _json
    from python.autonomous_execution_engine import AutonomousExecutionEngine

    repository = getattr(args, "execute_repository", ".")
    workspace_root = getattr(args, "execute_workspace", None)
    as_json = getattr(args, "execute_json", False)
    refresh = getattr(args, "execute_refresh", False)
    simulate = getattr(args, "execute_simulate", False)
    dry_run = getattr(args, "execute_dry_run", False)
    validate_only = getattr(args, "execute_validate", False)

    if validate_only:
        mode = "VALIDATION_ONLY"
    elif simulate:
        mode = "SIMULATION"
    elif dry_run:
        mode = "DRY_RUN"
    else:
        mode = "READ_ONLY"

    engine = AutonomousExecutionEngine(
        repository=repository,
        workspace_root=workspace_root,
        mode=mode,
        persist=True,
        refresh_integrations=refresh,
    )
    result = engine.execute()

    if as_json:
        print(_json.dumps(result["execution_dict"], indent=2))
    else:
        d = result["execution_dict"]
        ctx = d.get("context", {})
        metrics = d.get("metrics", {})
        paths = result.get("paths", {})
        print(f"AI CTO Autonomous Execution — {repository}")
        print(f"  Execution ID: {d.get('execution_id', '')}")
        print(f"  Mode:         {d.get('mode', '')}")
        print(f"  Approval:     {d.get('approval', '')}")
        print(f"  Status:       {d.get('status', '')}")
        print(f"  Confidence:   {ctx.get('confidence', 0.0):.0%}")
        print(f"  Duration:     {metrics.get('total_duration_ms', 0.0):.1f} ms")
        print(f"  Branch:       {ctx.get('branch', '')}")
        print()
        na = d.get("next_actions", [])
        if na:
            print("  Next Actions:")
            for action in na:
                print(f"    - {action}")
        if paths.get("markdown"):
            print(f"  Report:       {paths['markdown']}")

elif args.command == "evaluate":

    import json as _json
    from python.self_evaluation_engine import SelfEvaluationEngine

    repository = getattr(args, "evaluate_repository", ".")
    workspace_root = getattr(args, "evaluate_workspace", None)
    as_json = getattr(args, "evaluate_json", False)
    refresh = getattr(args, "evaluate_refresh", False)
    regressions_only = getattr(args, "evaluate_regressions", False)
    quality_only = getattr(args, "evaluate_quality", False)

    engine = SelfEvaluationEngine(
        repository=repository,
        workspace_root=workspace_root,
        persist=True,
        refresh_integrations=refresh,
    )
    result = engine.evaluate()

    if as_json:
        print(_json.dumps(result["evaluation_dict"], indent=2))
    else:
        d = result["evaluation_dict"]
        paths = result.get("paths", {})
        print(f"AI CTO Self Evaluation — {repository}")
        print(f"  Evaluation ID:   {d.get('evaluation_id', '')}")
        print(f"  Overall Gate:    {d.get('overall_gate', '')}")
        print(f"  Overall Score:   {d.get('overall_score', 0.0):.0%}")
        print(f"  Confidence:      {d.get('overall_confidence', 0.0):.0%}")
        print(f"  Regressions:     {len(d.get('regression_findings', []))}")
        print(f"  Architecture:    {len(d.get('architecture_findings', []))} findings")
        print()
        if regressions_only:
            for r in d.get("regression_findings", []):
                print(f"  [{r.get('severity', '').upper()}] {r.get('component', '')}: {r.get('finding', '')}")
        elif quality_only:
            for s in d.get("quality_scores", []):
                print(f"  {s.get('dimension', '')}: {s.get('score', 0.0):.0%} ({s.get('gate', '')})")
        else:
            recs = d.get("recommendations", [])
            if recs:
                print("  Recommendations:")
                for rec in recs[:5]:
                    print(f"    - {rec}")
        if paths.get("markdown"):
            print(f"  Report:          {paths['markdown']}")

elif args.command == "improve":

    import json as _json
    from python.self_improvement_engine import SelfImprovementEngine

    repository = getattr(args, "improve_repository", ".")
    workspace_root = getattr(args, "improve_workspace", None)
    as_json = getattr(args, "improve_json", False)
    refresh = getattr(args, "improve_refresh", False)
    debt_only = getattr(args, "improve_technical_debt", False)
    perf_only = getattr(args, "improve_performance", False)
    roadmap_only = getattr(args, "improve_roadmap", False)

    engine = SelfImprovementEngine(
        repository=repository,
        workspace_root=workspace_root,
        persist=True,
        refresh_integrations=refresh,
    )
    result = engine.improve()

    if as_json:
        print(_json.dumps(result["plan_dict"], indent=2))
    else:
        d = result["plan_dict"]
        paths = result.get("paths", {})
        print(f"AI CTO Self Improvement — {repository}")
        print(f"  Plan ID:         {d.get('plan_id', '')}")
        print(f"  Technical Debt:  {d.get('technical_debt_count', 0)} items")
        print(f"  Capability Gaps: {d.get('capability_gap_count', 0)} gaps")
        print(f"  Proposed Issues: {d.get('proposed_issue_count', 0)} issues")
        print(f"  Proposed Batches:{d.get('proposed_batch_count', 0)} batches")
        print(f"  CORE Proposals:  {d.get('core_proposal_count', 0)} proposals")
        print(f"  Roadmap Updates: {d.get('roadmap_update_count', 0)} updates")
        print()
        if debt_only:
            for item in d.get("technical_debt", []):
                print(f"  [{item.get('severity', '').upper()}] {item.get('component', '')}: {item.get('description', '')}")
        elif perf_only:
            for m in d.get("performance_metrics", []):
                print(f"  {m.get('name', '')}: {m.get('value', 0)} {m.get('unit', '')} ({m.get('trend', '')})")
        elif roadmap_only:
            for u in d.get("roadmap_updates", []):
                print(f"  [{u.get('priority', '').upper()}] {u.get('description', '')}")
        else:
            print(f"  Summary: {d.get('summary', '')}")
        if paths.get("markdown"):
            print(f"  Report:          {paths['markdown']}")

elif args.command == "dashboard":

    from python.dashboard import serve_dashboard

    repository = getattr(args, "dashboard_repository", ".")
    workspace_root = getattr(args, "dashboard_workspace", None)
    host = getattr(args, "host", os.environ.get("HOST", "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"))
    port = getattr(args, "port", int(os.environ.get("PORT", "8081")))
    open_browser = getattr(args, "dashboard_open_browser", False)

    serve_dashboard(
        host=host,
        port=port,
        repository_root=repository,
        workspace_root=workspace_root,
        open_browser=open_browser,
    )

else:

    parser.print_help()
    sys.exit(1)
