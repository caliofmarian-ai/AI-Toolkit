"""
Semantic Repository Intelligence — Project Memory Persistence
CORE-008B

Persists and loads semantic analysis results to/from the repository's
``.ai/semantic_knowledge.json`` file to enable future incremental scanning
and integration with the Development State Engine (CORE-009).
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


_KNOWLEDGE_DIR = ".ai"
_KNOWLEDGE_FILE = "semantic_knowledge.json"


class SemanticPersistence:
    """
    Saves and loads semantic analysis snapshots to ``<repo>/.ai/semantic_knowledge.json``.

    The knowledge file is a JSON document that stores:
    - The repository identity and analysis timestamp
    - A compact summary of all graph results
    - A version field for future schema migrations
    """

    SCHEMA_VERSION = "1.0.0"

    def __init__(self, root: Path):
        self.root = root
        self._knowledge_path = root / _KNOWLEDGE_DIR / _KNOWLEDGE_FILE

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save(self, analysis_result: Dict[str, Any]) -> Path:
        """
        Persist *analysis_result* to the knowledge file.

        Returns the absolute path where the file was written.
        Raises IOError if the file cannot be written.
        """
        knowledge_dir = self.root / _KNOWLEDGE_DIR
        knowledge_dir.mkdir(parents=True, exist_ok=True)

        snapshot = {
            "schema_version": self.SCHEMA_VERSION,
            "repository": str(self.root),
            "captured_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "analysis": self._compact(analysis_result),
        }

        with self._knowledge_path.open("w", encoding="utf-8") as fh:
            json.dump(snapshot, fh, indent=2, ensure_ascii=False)

        return self._knowledge_path

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    def load(self) -> Optional[Dict[str, Any]]:
        """
        Load a previously saved knowledge snapshot.

        Returns the raw dict or None if no snapshot exists.
        """
        if not self._knowledge_path.exists():
            return None
        try:
            with self._knowledge_path.open(encoding="utf-8") as fh:
                data = json.load(fh)
            if data.get("schema_version") != self.SCHEMA_VERSION:
                return None
            return data
        except (json.JSONDecodeError, OSError):
            return None

    def exists(self) -> bool:
        """Return True if a knowledge snapshot exists."""
        return self._knowledge_path.exists()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _compact(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract a compact summary of the analysis result for storage.

        We deliberately store only aggregate statistics (not the full AST
        analysis) to keep the file small and shareable.
        """
        import_graph = result.get("import_graph", {})
        call_graph = result.get("call_graph", {})
        arch_graph = result.get("architecture_graph", {})
        dep_graph = result.get("dependency_graph", {})
        complexity = result.get("complexity", {})

        return {
            "import_graph": {
                "node_count": import_graph.get("node_count", 0),
                "edge_count": import_graph.get("edge_count", 0),
                "circular_dependency_count": import_graph.get("circular_dependency_count", 0),
                "critical_modules": import_graph.get("critical_modules", [])[:10],
                "orphan_modules": import_graph.get("orphan_modules", [])[:10],
            },
            "call_graph": {
                "edge_count": call_graph.get("edge_count", 0),
                "entry_points": call_graph.get("entry_points", [])[:10],
            },
            "architecture_graph": {
                "node_count": arch_graph.get("node_count", 0),
                "edge_count": arch_graph.get("edge_count", 0),
                "hotspots": arch_graph.get("hotspots", [])[:5],
                "extension_points": arch_graph.get("extension_points", [])[:5],
                "risk_count": len(arch_graph.get("risks", [])),
            },
            "dependency_graph": {
                "external_dependency_count": dep_graph.get("external_dependency_count", 0),
                "internal_module_count": dep_graph.get("internal_module_count", 0),
            },
            "complexity": complexity,
            "recommendation_count": len(result.get("recommendations", [])),
            "injection_point_count": len(result.get("injection_points", [])),
            "next_core": result.get("next_core", ""),
        }
