"""
Autonomous Execution Engine — Evidence Collector and Snapshot
CORE-015D

Collects deterministic, evidence-based execution artefacts.
"""

import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


class ExecutionEvidenceCollector:
    """
    CORE-015D — Execution Evidence Collector.

    Collects observable evidence from each execution stage without
    duplicating analysis responsibilities held by other COREs.
    """

    def __init__(self) -> None:
        self._items: List[Dict[str, Any]] = []

    def record(self, source: str, category: str, data: Dict[str, Any]) -> None:
        """Record a piece of evidence."""
        self._items.append(
            {
                "source": source,
                "category": category,
                "timestamp": _utcnow(),
                "data": data,
            }
        )

    def collect(self) -> Dict[str, Any]:
        """Return all collected evidence as a deterministic dict."""
        return {
            "evidence_count": len(self._items),
            "items": sorted(
                self._items,
                key=lambda x: (x["source"], x["category"]),
            ),
        }

    def reset(self) -> None:
        self._items.clear()


class ExecutionSnapshot:
    """
    CORE-015D — Execution Snapshot.

    Captures a frozen, reproducible snapshot of the execution context.
    """

    @staticmethod
    def capture(
        execution_id: str,
        context: Mapping[str, Any],
        planning_queue: Mapping[str, Any],
        development_state: Mapping[str, Any],
        briefing: Mapping[str, Any],
        live_context: Mapping[str, Any],
        schema_version: str,
    ) -> Dict[str, Any]:
        """Return a snapshot dict."""
        captured_at = _utcnow()
        content = f"{execution_id}{captured_at}"
        snapshot_id = "ATK-SNAP-" + hashlib.sha1(
            content.encode("utf-8")
        ).hexdigest()[:8].upper()

        return {
            "snapshot_id": snapshot_id,
            "execution_id": execution_id,
            "captured_at": captured_at,
            "context": dict(context),
            "planning_queue": dict(planning_queue),
            "development_state": dict(development_state),
            "briefing": dict(briefing),
            "live_context": dict(live_context),
            "schema_version": schema_version,
        }
