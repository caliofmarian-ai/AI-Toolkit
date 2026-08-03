from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass
class GapItem:
    name: str
    status: str


class GapAnalysis:

    DEFAULT_ITEMS = [
        "Runtime REST API",
        "API Versioning",
        "API Authentication",
        "OpenAPI Specification",
        "GraphQL Preparation",
        "MCP Preparation",
        "Runtime API Client",
        "API Error Contract",
        "API Response Contract",
        "API Validation Layer",
        "API Middleware",
        "API Rate Limiting",
    ]

    def __init__(self, repository_root: Path):
        self.root = repository_root

    def analyse(self):
        implemented = {
            "Runtime REST API": False,
            "API Versioning": False,
            "API Authentication": False,
            "OpenAPI Specification": False,
            "GraphQL Preparation": False,
            "MCP Preparation": False,
            "Runtime API Client": False,
            "API Error Contract": False,
            "API Response Contract": False,
            "API Validation Layer": False,
            "API Middleware": False,
            "API Rate Limiting": False,
        }

        return [
            GapItem(
                name=item,
                status="IMPLEMENTED" if implemented[item] else "MISSING"
            )
            for item in self.DEFAULT_ITEMS
        ]

    def write_markdown(self, output: Path):

        output.parent.mkdir(parents=True, exist_ok=True)

        items = self.analyse()

        with output.open("w", encoding="utf-8") as md:

            md.write("# Gap Analysis\n\n")

            md.write(
                f"Generated: {datetime.now(UTC).isoformat()}\n\n"
            )

            md.write("| Component | Status |\n")
            md.write("|-----------|--------|\n")

            for item in items:
                md.write(f"| {item.name} | {item.status} |\n")

            md.write("\n## Summary\n\n")

            missing = sum(1 for x in items if x.status == "MISSING")

            md.write(f"- Missing Components: {missing}\n")
            md.write("- Repository ready for Implementation Planning.\n")
