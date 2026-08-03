from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlanningRule:
    keyword: str
    status: str
    risk: str
    priority: str


class RuleEngine:

    DEFAULT_RULES = (
        PlanningRule("REST API", "BLOCKED", "HIGH", "HIGH"),
        PlanningRule("OpenAPI", "WAITING", "MEDIUM", "HIGH"),
        PlanningRule("Authentication", "WAITING", "HIGH", "HIGH"),
        PlanningRule("GraphQL", "WAITING", "LOW", "MEDIUM"),
        PlanningRule("MCP", "WAITING", "LOW", "MEDIUM"),
    )

    def classify(self, component: str):

        for rule in self.DEFAULT_RULES:
            if rule.keyword.lower() in component.lower():
                return rule

        return PlanningRule(
            keyword="default",
            status="TODO",
            risk="MEDIUM",
            priority="MEDIUM",
        )
