from __future__ import annotations

from typing import Dict, List


PROMPT_LIBRARY: Dict[str, List[Dict[str, str]]] = {
    "Engineering": [
        {"name": "implementation_strategy", "prompt": "Generate an implementation strategy for the current repository context."},
    ],
    "Architecture": [
        {"name": "architecture_review", "prompt": "Explain the repository architecture and identify extension points."},
    ],
    "Repository Audit": [
        {"name": "audit_risks", "prompt": "Find architectural and delivery risks in the repository."},
    ],
    "Canonical Review": [
        {"name": "canonical_alignment", "prompt": "Review alignment between implementation and canonical documents."},
    ],
    "Runtime Diagnostics": [
        {"name": "runtime_health", "prompt": "Analyze runtime diagnostics and propose prioritized fixes."},
    ],
    "Implementation Planning": [
        {"name": "next_steps", "prompt": "Propose next implementation steps based on current context."},
    ],
    "Security Review": [
        {"name": "security_review", "prompt": "Review the current context for security risks and mitigations."},
    ],
    "Documentation": [
        {"name": "docs_update", "prompt": "Summarize documentation updates required for current implementation."},
    ],
    "Executive Briefing": [
        {"name": "exec_brief", "prompt": "Create an executive engineering briefing for current status and risks."},
    ],
}


class PromptLibrary:
    def list_categories(self) -> Dict[str, List[Dict[str, str]]]:
        return {category: list(items) for category, items in PROMPT_LIBRARY.items()}

    def resolve(self, name: str, fallback: str = "") -> str:
        for items in PROMPT_LIBRARY.values():
            for item in items:
                if item["name"] == name:
                    return item["prompt"]
        return fallback
