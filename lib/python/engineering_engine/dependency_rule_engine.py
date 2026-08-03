from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class DependencyResult:
    component: str
    status: str
    missing: list[str]


class DependencyRuleEngine:

    def __init__(self, root: Path):
        self.root = root
        self.rules = self._load()

    def _load(self):

        rules = {}

        path = self.root / "engineering-rules" / "dependencies.yaml"

        if not path.exists():
            return rules

        current = None

        for line in path.read_text(encoding="utf-8").splitlines():

            if not line.strip():
                continue

            if not line.startswith(" "):
                current = line.rstrip(":")
                rules[current] = []

            elif "- " in line and current:
                rules[current].append(line.split("- ", 1)[1].strip())

        return rules

    def evaluate(self, component: str):

        deps = self.rules.get(component, [])

        missing = list(deps)

        if not deps:
            status = "READY"
        elif component == "Runtime REST API":
            status = "BLOCKED"
        else:
            status = "WAITING"

        return DependencyResult(
            component=component,
            status=status,
            missing=missing,
        )
