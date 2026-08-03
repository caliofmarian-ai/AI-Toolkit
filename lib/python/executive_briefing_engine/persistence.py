"""
Executive Briefing Engine — Persistence Layer
CORE-010H

Writes executive briefing outputs to .ai/executive/:
  briefing.json
  recommendations.json
  priorities.json
  risks.json
  owner_actions.json
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Mapping

from .models import ExecutiveBriefing


class ExecutiveBriefingPersistence:
    """
    Persists executive briefing artifacts to .ai/executive/.

    All writes are atomic (write to temp then rename) and deterministic
    (keys sorted, no timestamps in JSON except in briefing.json itself).
    """

    EXECUTIVE_DIR = "executive"

    def __init__(self, repository_root: str = "."):
        self.repository_root = Path(repository_root).resolve()
        self.base_dir = self.repository_root / ".ai" / self.EXECUTIVE_DIR

    def save(self, briefing: ExecutiveBriefing) -> Dict[str, str]:
        """
        Persist all executive briefing artifacts.

        Returns a dict mapping artifact name to absolute file path.
        """
        self.base_dir.mkdir(parents=True, exist_ok=True)
        briefing_dict = briefing.to_dict()

        paths: Dict[str, str] = {}
        paths["briefing"] = self._write("briefing.json", briefing_dict)
        paths["recommendations"] = self._write(
            "recommendations.json",
            {
                "briefing_id": briefing.briefing_id,
                "generated_at": briefing.generated_at,
                "recommendations": [r.to_dict() for r in briefing.recommendations],
            },
        )
        paths["priorities"] = self._write(
            "priorities.json",
            {
                "briefing_id": briefing.briefing_id,
                "generated_at": briefing.generated_at,
                "priorities": [p.to_dict() for p in briefing.priorities],
            },
        )
        paths["risks"] = self._write(
            "risks.json",
            {
                "briefing_id": briefing.briefing_id,
                "generated_at": briefing.generated_at,
                "critical_risks": [r.to_dict() for r in briefing.critical_risks],
                "all_risks": [r.to_dict() for r in briefing.all_risks],
            },
        )
        paths["owner_actions"] = self._write(
            "owner_actions.json",
            {
                "briefing_id": briefing.briefing_id,
                "generated_at": briefing.generated_at,
                "pending_decisions": [d.to_dict() for d in briefing.pending_decisions],
                "owner_dashboard": briefing.owner_dashboard.to_dict(),
                "recommended_actions": briefing.owner_dashboard.recommended_actions,
            },
        )
        return paths

    def load_briefing(self) -> Dict[str, Any]:
        """Load the most recent briefing from .ai/executive/briefing.json."""
        path = self.base_dir / "briefing.json"
        if not path.exists():
            return {}
        return self._read(path)

    def exists(self) -> bool:
        """Return True if .ai/executive/briefing.json exists."""
        return (self.base_dir / "briefing.json").exists()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _write(self, filename: str, payload: Mapping[str, Any]) -> str:
        path = self.base_dir / filename
        self._atomic_write(path, payload)
        return str(path)

    def _atomic_write(self, path: Path, payload: Mapping[str, Any]):
        content = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
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

    def _read(self, path: Path) -> Dict[str, Any]:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
