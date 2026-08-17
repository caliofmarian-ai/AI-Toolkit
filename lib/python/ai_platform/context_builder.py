from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from python.context_synchronization_engine.engine import (
    DevelopmentContextProvider,
    GitContextProvider,
    WorkspaceContextProvider,
)
from python.repository_engine.engine import RepositoryEngine
from python.repository_engine.serializer import RepositoryProfileSerializer


class AIContextBuilder:
    def __init__(self, repository_root: str = ".", workspace_root: str | None = None) -> None:
        self.repository_root = Path(repository_root).resolve()
        self.workspace_root = Path(workspace_root).resolve() if workspace_root else self.repository_root.parent

    def build_permanent_orientation(self) -> Dict[str, Any]:
        """Build bounded read-only orientation without repository profiling.

        Permanent orientation tells the AI where it is operating and which
        high-level epistemic manifestations are visible.  It deliberately
        does not materialize repository knowledge.  Task-specific knowledge
        belongs to later cognitive retrieval and Working Context assembly.
        """
        git = GitContextProvider(str(self.repository_root)).collect()
        development = DevelopmentContextProvider(str(self.repository_root)).collect()
        runtime_payload = self._read_json(
            self.repository_root / ".ai" / "runtime" / "state" / "runtime_status.json"
        )
        runtime_status = runtime_payload.get("runtime", runtime_payload)

        return {
            "schema": "ai-toolkit/permanent-epistemic-orientation/v1",
            "organism": "AI-Toolkit",
            "project": self.repository_root.name,
            "human_authority": {
                "authority": "human",
                "ai_may_promote_authority": False,
            },
            "epistemic_classes": [
                "canon",
                "evidence",
                "conversation",
                "error_memory",
                "persistent_experience",
                "runtime",
                "repository",
            ],
            "available_organs": [
                "csl_uem",
                "canon",
                "knowledge_graph",
                "repository",
                "provenance",
                "layered_memory",
                "persistent_experience",
            ],
            "navigation_capabilities": [
                "search",
                "resolve",
                "read",
                "inspect",
                "traverse",
                "trace_provenance",
            ],
            "current_branch": git.get("current_branch", ""),
            "current_sprint": (development.get("planning", {}) or {}).get(
                "current_sprint",
                "",
            ),
            "current_epic": (development.get("current_context", {}) or {}).get(
                "current_epic",
                "",
            ),
            "current_issue": (development.get("current_context", {}) or {}).get(
                "current_issue",
                "",
            ),
            "runtime_status": runtime_status,
            "constraints": {
                "knowledge_availability_is_not_working_context": True,
                "retrieval_confers_authority": False,
                "semantic_identity_is_physical_location": False,
                "navigation_read_only": True,
                "unknown_is_valid": True,
                "full_repository_profile_default_payload": False,
            },
        }

    def build(self) -> Dict[str, Any]:
        git = GitContextProvider(str(self.repository_root)).collect()
        development = DevelopmentContextProvider(str(self.repository_root)).collect()
        workspace = WorkspaceContextProvider(str(self.repository_root), str(self.workspace_root)).collect()
        context_path = self.repository_root / ".ai" / "context" / "live_context.json"
        live_context = self._read_json(context_path)
        runtime_status = self._read_json(self.repository_root / ".ai" / "runtime" / "state" / "runtime_status.json")
        reports = self._recent_reports(limit=5)
        profile = RepositoryProfileSerializer.to_dict(RepositoryEngine(self.repository_root).profile())
        return {
            "repository_profile": profile,
            "repository_health": profile.get("health_summary", {}),
            "technology_stack": profile.get("tech_stack", []),
            "dependencies": profile.get("dependencies", {}),
            "current_branch": git.get("current_branch", ""),
            "current_sprint": (development.get("planning", {}) or {}).get("current_sprint", ""),
            "current_epic": (development.get("current_context", {}) or {}).get("current_epic", ""),
            "current_issue": (development.get("current_context", {}) or {}).get("current_issue", ""),
            "engineering_session": self._read_json(self.repository_root / ".ai" / "development_state" / "current_state.json"),
            "runtime_status": runtime_status.get("runtime", runtime_status),
            "canonical_documents": self._canonical_documents(limit=12),
            "recent_reports": reports,
            "context": live_context,
            "workspace": workspace,
        }

    def _recent_reports(self, limit: int = 5) -> list[dict[str, Any]]:
        reports_dir = self.repository_root / ".ai" / "reports"
        if not reports_dir.exists():
            return []
        paths = sorted(reports_dir.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True)[:limit]
        result = []
        for path in paths:
            payload = self._read_json(path)
            result.append({"path": str(path), "generated_at": payload.get("generated_at", "")})
        return result

    def _canonical_documents(self, limit: int = 12) -> list[str]:
        docs_dir = self.repository_root / "docs" / "canonical"
        if not docs_dir.exists():
            return []
        paths = sorted(docs_dir.glob("*.md"))[:limit]
        return [str(path.relative_to(self.repository_root)) for path in paths]

    def _read_json(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
