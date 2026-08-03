"""
Executable Repository Intelligence — Persistence
CORE-008C

Persists the executable repository model to:
  .ai/runtime_repository_model.json
  .ai/executable_repository_map.json
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


_AI_DIR = ".ai"
_RUNTIME_MODEL_FILE = "runtime_repository_model.json"
_EXEC_MAP_FILE = "executable_repository_map.json"

SCHEMA_VERSION = "1.0.0"


class ExecutablePersistence:
    """
    Saves CORE-008C analysis results to the repository's .ai directory.
    """

    def __init__(self, root: Path):
        self.root = root
        self._ai_dir = root / _AI_DIR
        self._runtime_model_path = self._ai_dir / _RUNTIME_MODEL_FILE
        self._exec_map_path = self._ai_dir / _EXEC_MAP_FILE

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save_runtime_model(self, result_dict: Dict[str, Any]) -> Path:
        """
        Save the full executable repository result as runtime_repository_model.json.
        Returns the path written.
        """
        self._ai_dir.mkdir(parents=True, exist_ok=True)
        snapshot = {
            "schema_version": SCHEMA_VERSION,
            "repository": str(self.root),
            "captured_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "model": result_dict,
        }
        with self._runtime_model_path.open("w", encoding="utf-8") as fh:
            json.dump(snapshot, fh, indent=2, ensure_ascii=False)
        return self._runtime_model_path

    def save_executable_map(self, result_dict: Dict[str, Any]) -> Path:
        """
        Save a compact executable map as executable_repository_map.json.
        Returns the path written.
        """
        self._ai_dir.mkdir(parents=True, exist_ok=True)
        compact = self._build_compact_map(result_dict)
        snapshot = {
            "schema_version": SCHEMA_VERSION,
            "repository": str(self.root),
            "captured_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "executable_map": compact,
        }
        with self._exec_map_path.open("w", encoding="utf-8") as fh:
            json.dump(snapshot, fh, indent=2, ensure_ascii=False)
        return self._exec_map_path

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    def load_runtime_model(self) -> Optional[Dict[str, Any]]:
        """Load runtime_repository_model.json or return None."""
        return self._load(self._runtime_model_path)

    def load_executable_map(self) -> Optional[Dict[str, Any]]:
        """Load executable_repository_map.json or return None."""
        return self._load(self._exec_map_path)

    def runtime_model_exists(self) -> bool:
        return self._runtime_model_path.exists()

    def executable_map_exists(self) -> bool:
        return self._exec_map_path.exists()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load(self, path: Path) -> Optional[Dict[str, Any]]:
        if not path.exists():
            return None
        try:
            with path.open(encoding="utf-8") as fh:
                data = json.load(fh)
            if data.get("schema_version") != SCHEMA_VERSION:
                return None
            return data
        except (json.JSONDecodeError, OSError):
            return None

    def _build_compact_map(self, result_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Build a compact summary of the executable analysis for the map file."""
        runtime_map = result_dict.get("runtime_map", {})
        dep_graph = result_dict.get("executable_dependency_graph", {})
        zones = result_dict.get("zones", [])

        return {
            "executable_file_count": result_dict.get("executable_file_count", 0),
            "non_executable_file_count": result_dict.get("non_executable_file_count", 0),
            "category_distribution": result_dict.get("category_distribution", {}),
            "zone_distribution": result_dict.get("zone_distribution", {}),
            "safety_distribution": result_dict.get("safety_distribution", {}),
            "main_entry_point": runtime_map.get("main_entry_point"),
            "execution_chain": runtime_map.get("execution_chain", [])[:10],
            "bootstrap_sequence": runtime_map.get("bootstrap_sequence", [])[:10],
            "scheduler_entry": runtime_map.get("scheduler_entry"),
            "runtime_component_count": len(runtime_map.get("runtime_components", [])),
            "executable_dep_nodes": dep_graph.get("node_count", 0),
            "executable_dep_edges": dep_graph.get("edge_count", 0),
            "excluded_file_count": dep_graph.get("excluded_count", 0),
            "zone_count": len(zones),
            "recommendation_count": len(result_dict.get("recommendations", [])),
        }
