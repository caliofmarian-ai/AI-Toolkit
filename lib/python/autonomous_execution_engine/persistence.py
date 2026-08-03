"""
Autonomous Execution Engine — Persistence Layer
CORE-015G

Writes all execution artifacts to .ai/execution/ atomically.

Artifacts produced:
  execution.json
  execution_context.json
  execution_queue.json
  execution_history.json
  execution_metrics.json
  execution_results.json
  execution_snapshot.json
  execution_evidence.json
  execution_log.json
  execution_report.json
  AI_CTO_EXECUTION_REPORT.md
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Mapping


class ExecutionPersistence:
    """
    CORE-015G — Execution Persistence.

    All writes are atomic (write to temp file, then rename) and
    deterministic (JSON keys sorted, stable ordering).
    """

    EXECUTION_DIR = "execution"

    def __init__(self, repository_root: str = ".") -> None:
        self.repository_root = Path(repository_root).resolve()
        self.base_dir = self.repository_root / ".ai" / self.EXECUTION_DIR

    def save(
        self,
        execution_result: Any,
        log_entries: List[Dict[str, Any]] = None,
        report_dict: Dict[str, Any] = None,
        markdown: str = "",
    ) -> Dict[str, str]:
        """
        Persist all execution artifacts.

        ``execution_result`` must expose a ``to_dict()`` method.

        Returns a dict mapping artifact name → absolute file path.
        """
        self.base_dir.mkdir(parents=True, exist_ok=True)
        d = execution_result.to_dict()
        paths: Dict[str, str] = {}

        # execution.json — full result
        paths["execution"] = self._write("execution.json", d)

        # execution_context.json
        paths["execution_context"] = self._write(
            "execution_context.json", d.get("context", {})
        )

        # execution_queue.json — planning queue from snapshot
        snapshot = d.get("snapshot", {})
        paths["execution_queue"] = self._write(
            "execution_queue.json",
            snapshot.get("planning_queue", {}),
        )

        # execution_metrics.json
        paths["execution_metrics"] = self._write(
            "execution_metrics.json", d.get("metrics", {})
        )

        # execution_results.json — validation results
        paths["execution_results"] = self._write(
            "execution_results.json",
            {
                "execution_id": d.get("execution_id", ""),
                "validation_results": d.get("validation_results", []),
            },
        )

        # execution_snapshot.json
        paths["execution_snapshot"] = self._write(
            "execution_snapshot.json", snapshot
        )

        # execution_evidence.json
        paths["execution_evidence"] = self._write(
            "execution_evidence.json", d.get("evidence", {})
        )

        # execution_log.json
        log_data = {
            "execution_id": d.get("execution_id", ""),
            "entry_count": len(log_entries or []),
            "entries": log_entries or [],
        }
        paths["execution_log"] = self._write("execution_log.json", log_data)

        # execution_report.json
        paths["execution_report"] = self._write(
            "execution_report.json", report_dict or {}
        )

        # execution_history.json — append current run
        paths["execution_history"] = self._append_history(d)

        # Markdown report
        if markdown:
            md_path = self.base_dir / "AI_CTO_EXECUTION_REPORT.md"
            md_content = markdown if markdown.endswith("\n") else markdown + "\n"
            self._atomic_write_text(md_path, md_content)
            paths["markdown"] = str(md_path)

        return paths

    def load_execution(self) -> Dict[str, Any]:
        """Load the most recent execution.json, or return {}."""
        return self._read("execution.json")

    def load_history(self) -> Dict[str, Any]:
        """Load the current execution_history.json, or return empty history."""
        return self._read("execution_history.json")

    def exists(self) -> bool:
        return (self.base_dir / "execution.json").exists()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _append_history(self, d: Dict[str, Any]) -> str:
        """Append the current execution to execution_history.json."""
        history = self._read("execution_history.json")
        entries: List[Dict[str, Any]] = list(history.get("entries", []))
        entry = {
            "execution_id": d.get("execution_id", ""),
            "timestamp": d.get("generated_at", ""),
            "repository": d.get("repository", ""),
            "mode": d.get("mode", ""),
            "approval": d.get("approval", ""),
            "status": d.get("status", ""),
            "duration_ms": d.get("metrics", {}).get("total_duration_ms", 0.0),
            "confidence": d.get("context", {}).get("confidence", 0.0),
            "summary": d.get("summary", ""),
        }
        entries.append(entry)
        history_dict = {
            "repository": d.get("repository", ""),
            "generated_at": d.get("generated_at", ""),
            "schema_version": d.get("schema_version", ""),
            "entry_count": len(entries),
            "entries": entries,
        }
        return self._write("execution_history.json", history_dict)

    def _write(self, filename: str, payload: Any) -> str:
        path = self.base_dir / filename
        content = (
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        )
        self._atomic_write_text(path, content)
        return str(path)

    def _atomic_write_text(self, path: Path, content: str) -> None:
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
