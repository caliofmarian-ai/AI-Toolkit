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


def cmd_agent(agent_name):

    runtime = build_runtime()

    result = runtime.execute(
        agent_name,
        AgentContext(repository=".")
    )

    print(json.dumps(
        result.data,
        indent=2
    ))


parser = argparse.ArgumentParser(
    prog="ai"
)

sub = parser.add_subparsers(dest="command")

for command in [
    "inventory",
    "dependencies",
    "validate",
    "plan",
    "inspect",
]:
    sub.add_parser(command)

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

    cmd_agent("inspect")

else:

    parser.print_help()
    sys.exit(1)
