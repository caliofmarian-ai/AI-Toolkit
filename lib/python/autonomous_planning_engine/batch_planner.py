"""
Autonomous Planning Engine — Batch Planner
CORE-014G

Recommends the next batch to execute by consulting:
  - Development state current_batch and recommended_batch
  - Batch documents in development/ directory
  - Executive Briefing suggested_next_batch
  - Canonical compliance gaps → batch generation triggers

This is a *planning* BatchPlanner (recommends which batch to run next),
distinct from lib/python/batch_planner/planner.py (generates batch documents
from canonical findings).  No batch decisions are hardcoded.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from .models import EFFORT_MEDIUM, TYPE_BATCH, PlanningEntry

_EMPTY = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})
_BATCH_RE = re.compile(r"\bBATCH-(\d+)\b", re.IGNORECASE)
_STATUS_RE = re.compile(r"^Status:\s*(.+)$", re.MULTILINE | re.IGNORECASE)


def _is_set(v: Any) -> bool:
    return bool(v) and str(v).strip() not in _EMPTY


def _batch_sort_key(batch_id: str) -> int:
    m = _BATCH_RE.search(batch_id)
    return int(m.group(1)) if m else 9999


def _load_batch_status(md_file: Path) -> str:
    """Return the Status field from a batch Markdown file."""
    try:
        content = md_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "UNKNOWN"
    m = _STATUS_RE.search(content)
    return m.group(1).strip().upper() if m else "UNKNOWN"


class BatchPlanner:
    """
    CORE-014G — Batch Planner.

    Recommends the next batch to execute from repository intelligence.
    """

    def __init__(self, repository_root: str = ".") -> None:
        self.root = Path(repository_root).resolve()
        self._dev_dir = self.root / "development"

    def recommend_next_batch(
        self,
        decision_context: Mapping[str, Any],
        snapshot: Mapping[str, Any],
        briefing: Mapping[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """Return the highest-priority batch recommendation, or None."""
        candidates = self._collect_candidates(decision_context, snapshot, briefing)
        return candidates[0] if candidates else None

    def build_batch_entries(
        self,
        decision_context: Mapping[str, Any],
        snapshot: Mapping[str, Any],
        briefing: Mapping[str, Any],
    ) -> List[PlanningEntry]:
        """Return PlanningEntry objects for the top batch recommendations."""
        candidates = self._collect_candidates(decision_context, snapshot, briefing)
        entries: List[PlanningEntry] = []
        for i, c in enumerate(candidates[:5]):
            entries.append(
                PlanningEntry(
                    entry_id=c.get("id", f"BATCH-{i + 1:03d}"),
                    title=c["title"],
                    type=TYPE_BATCH,
                    priority=c.get("priority", "medium"),
                    reason=c.get("reason", ""),
                    dependencies=tuple(c.get("dependencies", [])),
                    estimated_effort=c.get("estimated_effort", EFFORT_MEDIUM),
                    confidence=c.get("confidence", 0.7),
                    blocked_by=(),
                    metadata=c,
                )
            )
        return entries

    # ------------------------------------------------------------------
    # Candidate generation
    # ------------------------------------------------------------------

    def _collect_candidates(
        self,
        decision_context: Mapping[str, Any],
        snapshot: Mapping[str, Any],
        briefing: Mapping[str, Any],
    ) -> List[Dict[str, Any]]:
        candidates: List[Dict[str, Any]] = []

        # 1. Executive Briefing suggested_next_batch
        suggested = decision_context.get("suggested_next_batch", "")
        if _is_set(suggested):
            candidates.append({
                "id": suggested,
                "title": f"Execute {suggested}",
                "priority": "high",
                "reason": (
                    f"Executive Briefing recommends {suggested} as the next "
                    "batch to execute."
                ),
                "dependencies": [],
                "estimated_effort": EFFORT_MEDIUM,
                "confidence": 0.85,
            })

        # 2. Batch documents in development/ with IN DEVELOPMENT status
        in_dev = self._find_in_development_batches()
        for batch_id, md_path in sorted(in_dev.items(), key=lambda t: _batch_sort_key(t[0])):
            if not any(c.get("id") == batch_id for c in candidates):
                candidates.append({
                    "id": batch_id,
                    "title": f"Complete {batch_id}",
                    "priority": "medium",
                    "reason": f"{batch_id} has status IN DEVELOPMENT in {md_path.name}.",
                    "dependencies": [],
                    "estimated_effort": EFFORT_MEDIUM,
                    "confidence": 0.75,
                })

        # 3. Next CORE → needs a corresponding batch
        next_core = decision_context.get("next_core")
        if next_core and not any(next_core in c.get("reason", "") for c in candidates):
            batch_title = f"Execute batch for {next_core}"
            candidates.append({
                "id": f"BATCH-{next_core}",
                "title": batch_title,
                "priority": "high",
                "reason": f"A new batch is needed to implement {next_core}.",
                "dependencies": [],
                "estimated_effort": EFFORT_MEDIUM,
                "confidence": 0.70,
            })

        return candidates

    def _find_in_development_batches(self) -> Dict[str, Path]:
        """Return {batch_id: path} for all IN DEVELOPMENT batch documents."""
        result: Dict[str, Path] = {}
        if not self._dev_dir.is_dir():
            return result
        for md_file in sorted(self._dev_dir.glob("*.md")):
            status = _load_batch_status(md_file)
            if "IN DEVELOPMENT" in status or "IN_DEVELOPMENT" in status:
                m = _BATCH_RE.search(md_file.stem)
                if m:
                    batch_id = f"BATCH-{m.group(1).zfill(3)}"
                    result[batch_id] = md_file
        return result
