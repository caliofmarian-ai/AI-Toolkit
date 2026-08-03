#!/usr/bin/env python3

import argparse
import json
import sys

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

    cmd_agent("inspect", repository=args.path, output_dir=args.output)

else:

    parser.print_help()
    sys.exit(1)
