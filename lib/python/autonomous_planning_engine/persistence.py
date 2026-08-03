"""
Autonomous Planning Engine — Persistence Layer
CORE-014K

Writes all planning artifacts to .ai/planning/ atomically.

Artifacts produced:
  planning.json
  execution_queue.json
  next_actions.json
  roadmap_progress.json
  recommended_pr.json
  recommended_issue.json
  recommended_batch.json
  recommended_milestone.json
  recommended_core.json
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Mapping, Optional


class PlanningPersistence:
    """
    CORE-014K — Planning Persistence.

    All writes are atomic (write to temp file, then rename) and
    deterministic (JSON keys sorted).
    """

    PLANNING_DIR = "planning"

    def __init__(self, repository_root: str = ".") -> None:
        self.repository_root = Path(repository_root).resolve()
        self.base_dir = self.repository_root / ".ai" / self.PLANNING_DIR

    def save(self, planning_result: Any) -> Dict[str, str]:
        """
        Persist all planning artifacts.

        ``planning_result`` must be a PlanningResult (or any object with
        a ``to_dict()`` method).

        Returns a dict mapping artifact name → absolute file path.
        """
        self.base_dir.mkdir(parents=True, exist_ok=True)
        d = planning_result.to_dict()
        paths: Dict[str, str] = {}

        # planning.json — full result
        paths["planning"] = self._write("planning.json", d)

        # execution_queue.json
        paths["execution_queue"] = self._write(
            "execution_queue.json", d.get("execution_queue", {})
        )

        # next_actions.json
        paths["next_actions"] = self._write(
            "next_actions.json", d.get("next_actions", {})
        )

        # roadmap_progress.json
        paths["roadmap_progress"] = self._write(
            "roadmap_progress.json", d.get("roadmap_progress", {})
        )

        # individual recommendations
        for key in (
            "recommended_core",
            "recommended_issue",
            "recommended_batch",
            "recommended_pr",
            "recommended_milestone",
        ):
            value = d.get(key)
            filename = f"{key}.json"
            paths[key] = self._write(filename, value or {})

        return paths

    def load_planning(self) -> Dict[str, Any]:
        """Load the most recent planning.json, or return {}."""
        return self._read("planning.json")

    def exists(self) -> bool:
        """Return True if .ai/planning/planning.json exists."""
        return (self.base_dir / "planning.json").exists()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _write(self, filename: str, payload: Any) -> str:
        path = self.base_dir / filename
        content = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        self._atomic_write(path, content)
        return str(path)

    def _atomic_write(self, path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(content)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp_path, path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def _read(self, filename: str) -> Dict[str, Any]:
        path = self.base_dir / filename
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
