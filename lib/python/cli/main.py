#!/usr/bin/env python3

import argparse
import json
import os
import sys

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


def cmd_plan():

    plan = PlanningEngine(".").build_plan()

    print("Execution Plan:", plan.identifier)
    print()

    for task in plan.tasks:

        print(
            f"[{task.priority}] {task.identifier} -> {task.title}"
        )


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
    "plan",
]:
    sub.add_parser(command)

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

args = parser.parse_args()

if args.command == "inventory":

    cmd_inventory()

elif args.command == "dependencies":

    cmd_dependencies()

elif args.command == "validate":

    cmd_validate()

elif args.command == "plan":

    cmd_plan()

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

else:

    parser.print_help()
    sys.exit(1)
