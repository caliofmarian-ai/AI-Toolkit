"""
Workspace Orchestrator — Persistence Layer
CORE-012

Persists all workspace artifacts to .ai/workspace/:

  workspace.json          workspace identity and metadata
  repositories.json       all registered repositories
  relationships.json      cross-repository relationships
  dependencies.json       cross-repository dependency edges
  health.json             aggregated workspace health
  priorities.json         ranked priorities for the owner
  recommendations.json    evidence-based workspace recommendations
  dashboard.json          workspace dashboard summary
  history.json            scan history entries
  statistics.json         aggregate statistics

All writes are atomic (write to temp, then rename) and deterministic
(JSON keys sorted, no floating timestamps outside the data model).
"""

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from .models import (
    WorkspaceDependencyEdge,
    WorkspaceHealth,
    WorkspacePriority,
    WorkspaceRecommendation,
    WorkspaceRelationship,
    WorkspaceRepository,
    WorkspaceRisk,
    WorkspaceScanResult,
    WorkspaceStatistics,
    WORKSPACE_SCHEMA_VERSION,
)
from .registry import RepositoryRegistry


class WorkspacePersistence:
    """
    Persists and loads workspace orchestrator artifacts under .ai/workspace/.

    All methods are safe to call even when the .ai/workspace/ directory does
    not yet exist — it is created on demand.
    """

    WORKSPACE_DIR = "workspace"

    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root).resolve()
        self.base_dir = self.workspace_root / ".ai" / self.WORKSPACE_DIR

    # ------------------------------------------------------------------
    # Atomic write helpers
    # ------------------------------------------------------------------

    def _ensure_dir(self) -> None:
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _write_json(self, filename: str, data: Any) -> str:
        """Write *data* atomically to base_dir/filename.  Returns the path."""
        self._ensure_dir()
        target = self.base_dir / filename
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=str(self.base_dir),
            delete=False,
            suffix=".tmp",
        ) as tmp:
            json.dump(data, tmp, indent=2, sort_keys=True, ensure_ascii=False)
            tmp_path = tmp.name
        os.replace(tmp_path, str(target))
        return str(target)

    def _read_json(self, filename: str) -> Optional[Any]:
        """Return parsed JSON from base_dir/filename, or None if missing."""
        path = self.base_dir / filename
        if not path.exists():
            return None
        with open(str(path), encoding="utf-8") as fh:
            return json.load(fh)

    # ------------------------------------------------------------------
    # Save — full scan result
    # ------------------------------------------------------------------

    def save(self, result: WorkspaceScanResult, statistics: WorkspaceStatistics) -> Dict[str, str]:
        """
        Persist all workspace artifacts from a scan result.

        Returns a dict mapping artifact name -> absolute file path.
        """
        self._ensure_dir()
        now = result.generated_at
        paths: Dict[str, str] = {}

        # workspace.json
        paths["workspace"] = self._write_json("workspace.json", {
            "schema_version": WORKSPACE_SCHEMA_VERSION,
            "workspace_id": result.workspace_id,
            "workspace_root": result.workspace_root,
            "generated_at": now,
            "total_repositories": result.total_repositories,
            "scanned_repositories": result.scanned_repositories,
            "failed_repositories": result.failed_repositories,
        })

        # repositories.json
        paths["repositories"] = self._write_json(
            "repositories.json",
            {
                "schema_version": WORKSPACE_SCHEMA_VERSION,
                "workspace_id": result.workspace_id,
                "generated_at": now,
                "count": len(result.repositories),
                "repositories": [r.to_dict() for r in result.repositories],
            },
        )

        # dependencies.json
        paths["dependencies"] = self._write_json(
            "dependencies.json",
            {
                "schema_version": WORKSPACE_SCHEMA_VERSION,
                "workspace_id": result.workspace_id,
                "generated_at": now,
                "count": len(result.dependencies),
                "dependencies": [d.to_dict() for d in result.dependencies],
            },
        )

        # relationships.json
        paths["relationships"] = self._write_json(
            "relationships.json",
            {
                "schema_version": WORKSPACE_SCHEMA_VERSION,
                "workspace_id": result.workspace_id,
                "generated_at": now,
                "count": len(result.relationships),
                "relationships": [r.to_dict() for r in result.relationships],
            },
        )

        # health.json
        paths["health"] = self._write_json(
            "health.json",
            {
                "schema_version": WORKSPACE_SCHEMA_VERSION,
                "workspace_id": result.workspace_id,
                "generated_at": now,
                **result.health.to_dict(),
            },
        )

        # priorities.json
        paths["priorities"] = self._write_json(
            "priorities.json",
            {
                "schema_version": WORKSPACE_SCHEMA_VERSION,
                "workspace_id": result.workspace_id,
                "generated_at": now,
                "count": len(result.priorities),
                "priorities": [p.to_dict() for p in result.priorities],
            },
        )

        # recommendations.json
        paths["recommendations"] = self._write_json(
            "recommendations.json",
            {
                "schema_version": WORKSPACE_SCHEMA_VERSION,
                "workspace_id": result.workspace_id,
                "generated_at": now,
                "count": len(result.recommendations),
                "recommendations": [r.to_dict() for r in result.recommendations],
            },
        )

        # risks (inside recommendations.json-adjacent file)
        paths["risks"] = self._write_json(
            "risks.json",
            {
                "schema_version": WORKSPACE_SCHEMA_VERSION,
                "workspace_id": result.workspace_id,
                "generated_at": now,
                "count": len(result.risks),
                "risks": [r.to_dict() for r in result.risks],
            },
        )

        # statistics.json
        paths["statistics"] = self._write_json(
            "statistics.json",
            {
                "schema_version": WORKSPACE_SCHEMA_VERSION,
                "workspace_id": result.workspace_id,
                "generated_at": now,
                **statistics.to_dict(),
            },
        )

        # history.json — append to rolling history
        paths["history"] = self._append_history({
            "workspace_id": result.workspace_id,
            "generated_at": now,
            "total_repositories": result.total_repositories,
            "scanned_repositories": result.scanned_repositories,
            "failed_repositories": result.failed_repositories,
            "overall_health": result.health.overall_health,
            "overall_readiness": round(result.health.overall_readiness, 4),
            "scan_duration": round(statistics.scan_duration, 4),
        })

        return paths

    def _append_history(self, entry: Dict[str, Any]) -> str:
        existing = self._read_json("history.json")
        if existing is None:
            existing = {"schema_version": WORKSPACE_SCHEMA_VERSION, "history": []}
        history = existing.get("history", [])
        history.append(entry)
        # Keep only the last 100 entries
        history = history[-100:]
        return self._write_json("history.json", {
            "schema_version": WORKSPACE_SCHEMA_VERSION,
            "count": len(history),
            "history": history,
        })

    # ------------------------------------------------------------------
    # Save — dashboard separately (may be called without a full scan)
    # ------------------------------------------------------------------

    def save_dashboard(self, workspace_id: str, generated_at: str, dashboard_dict: Dict[str, Any]) -> str:
        return self._write_json("dashboard.json", {
            "schema_version": WORKSPACE_SCHEMA_VERSION,
            "workspace_id": workspace_id,
            "generated_at": generated_at,
            **dashboard_dict,
        })

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    def load_workspace(self) -> Optional[Dict[str, Any]]:
        return self._read_json("workspace.json")

    def load_repositories(self) -> List[WorkspaceRepository]:
        data = self._read_json("repositories.json")
        if data is None:
            return []
        return [WorkspaceRepository.from_dict(r) for r in data.get("repositories", [])]

    def load_dependencies(self) -> List[WorkspaceDependencyEdge]:
        data = self._read_json("dependencies.json")
        if data is None:
            return []
        return [WorkspaceDependencyEdge.from_dict(d) for d in data.get("dependencies", [])]

    def load_relationships(self) -> List[WorkspaceRelationship]:
        data = self._read_json("relationships.json")
        if data is None:
            return []
        return [WorkspaceRelationship.from_dict(r) for r in data.get("relationships", [])]

    def load_health(self) -> Optional[WorkspaceHealth]:
        data = self._read_json("health.json")
        if data is None:
            return None
        return WorkspaceHealth.from_dict(data)

    def load_priorities(self) -> List[WorkspacePriority]:
        data = self._read_json("priorities.json")
        if data is None:
            return []
        return [WorkspacePriority.from_dict(p) for p in data.get("priorities", [])]

    def load_recommendations(self) -> List[WorkspaceRecommendation]:
        data = self._read_json("recommendations.json")
        if data is None:
            return []
        return [WorkspaceRecommendation.from_dict(r) for r in data.get("recommendations", [])]

    def load_risks(self) -> List[WorkspaceRisk]:
        data = self._read_json("risks.json")
        if data is None:
            return []
        return [WorkspaceRisk.from_dict(r) for r in data.get("risks", [])]

    def load_statistics(self) -> Optional[WorkspaceStatistics]:
        data = self._read_json("statistics.json")
        if data is None:
            return None
        return WorkspaceStatistics.from_dict(data)

    def load_history(self) -> List[Dict[str, Any]]:
        data = self._read_json("history.json")
        if data is None:
            return []
        return data.get("history", [])

    def load_dashboard(self) -> Optional[Dict[str, Any]]:
        return self._read_json("dashboard.json")

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def exists(self) -> bool:
        """Return True if the workspace persistence directory exists."""
        return (self.base_dir / "workspace.json").exists()

    def artifact_paths(self) -> Dict[str, str]:
        """Return all existing artifact paths."""
        artifacts = [
            "workspace.json", "repositories.json", "dependencies.json",
            "relationships.json", "health.json", "priorities.json",
            "recommendations.json", "risks.json", "statistics.json",
            "history.json", "dashboard.json",
        ]
        return {
            a.replace(".json", ""): str(self.base_dir / a)
            for a in artifacts
            if (self.base_dir / a).exists()
        }
