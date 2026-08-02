#!/usr/bin/env python3

import argparse
import json
import sys

from python.repository_engine.engine import RepositoryEngine
from python.dependency_engine.engine import DependencyEngine
from python.validation_engine.engine import ValidationEngine
from python.planning_engine.engine import PlanningEngine
from python.repository_inspector_v2.engine import RepositoryInspectorV2


def cmd_inventory(args):
    engine = RepositoryEngine(".")
    print(json.dumps(engine.statistics(), indent=2))


def cmd_dependencies(args):
    engine = DependencyEngine(".")
    print(json.dumps(engine.statistics(), indent=2))


def cmd_validate(args):
    engine = ValidationEngine(".")
    print(json.dumps(engine.statistics(), indent=2))


def cmd_plan(args):
    engine = PlanningEngine(".")
    plan = engine.build_plan()

    print("Execution Plan:", plan.identifier)
    print()

    for task in plan.tasks:
        print(f"[{task.priority}] {task.identifier} -> {task.title}")


def main():

    parser = argparse.ArgumentParser(
        prog="ai",
        description="AI Toolkit CLI"
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("inventory")
    sub.add_parser("dependencies")
    sub.add_parser("validate")
    sub.add_parser("plan")
    sub.add_parser("inspect")

    args = parser.parse_args()

    if args.command == "inventory":
        cmd_inventory(args)

    elif args.command == "dependencies":
        cmd_dependencies(args)

    elif args.command == "validate":
        cmd_validate(args)

    elif args.command == "plan":
        cmd_plan(args)

    elif args.command == "inspect":
        agent = RepositoryInspectorV2(".")
        import json
        print(json.dumps(agent.inspect(), indent=2))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
