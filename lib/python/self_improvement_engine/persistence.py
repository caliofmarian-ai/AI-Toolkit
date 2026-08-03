"""
Self Improvement Engine — Persistence Layer
CORE-017D

Writes all improvement artifacts to .ai/self_improvement/ atomically.

Artifacts produced:
  improvements.json
  technical_debt.json
  performance.json
  optimization_plan.json
  proposed_issues.json
  proposed_batches.json
  proposed_cores.json
  roadmap_updates.json
  capability_analysis.json
  history.json
  snapshot.json
  AI_CTO_SELF_IMPROVEMENT.md
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List


class ImprovementPersistence:
    """
    CORE-017D — Improvement Persistence.

    All writes are atomic and deterministic.
    """

    IMPROVEMENT_DIR = "self_improvement"

    def __init__(self, repository_root: str = ".") -> None:
        self.repository_root = Path(repository_root).resolve()
        self.base_dir = self.repository_root / ".ai" / self.IMPROVEMENT_DIR

    def save(
        self,
        optimization_plan: Any,
        markdown: str = "",
    ) -> Dict[str, str]:
        """
        Persist all improvement artifacts.

        Returns a dict mapping artifact name → absolute file path.
        """
        self.base_dir.mkdir(parents=True, exist_ok=True)
        d = optimization_plan.to_dict()
        paths: Dict[str, str] = {}

        # improvements.json — full plan
        paths["improvements"] = self._write("improvements.json", d)

        # technical_debt.json
        paths["technical_debt"] = self._write(
            "technical_debt.json",
            {
                "plan_id": d.get("plan_id", ""),
                "generated_at": d.get("generated_at", ""),
                "technical_debt_count": d.get("technical_debt_count", 0),
                "technical_debt": d.get("technical_debt", []),
            },
        )

        # performance.json
        paths["performance"] = self._write(
            "performance.json",
            {
                "plan_id": d.get("plan_id", ""),
                "generated_at": d.get("generated_at", ""),
                "performance_metric_count": d.get("performance_metric_count", 0),
                "performance_metrics": d.get("performance_metrics", []),
            },
        )

        # optimization_plan.json — full plan (alias)
        paths["optimization_plan"] = self._write("optimization_plan.json", d)

        # proposed_issues.json
        paths["proposed_issues"] = self._write(
            "proposed_issues.json",
            {
                "plan_id": d.get("plan_id", ""),
                "generated_at": d.get("generated_at", ""),
                "proposed_issue_count": d.get("proposed_issue_count", 0),
                "proposed_issues": d.get("proposed_issues", []),
            },
        )

        # proposed_batches.json
        paths["proposed_batches"] = self._write(
            "proposed_batches.json",
            {
                "plan_id": d.get("plan_id", ""),
                "generated_at": d.get("generated_at", ""),
                "proposed_batch_count": d.get("proposed_batch_count", 0),
                "proposed_batches": d.get("proposed_batches", []),
            },
        )

        # proposed_cores.json
        paths["proposed_cores"] = self._write(
            "proposed_cores.json",
            {
                "plan_id": d.get("plan_id", ""),
                "generated_at": d.get("generated_at", ""),
                "core_proposal_count": d.get("core_proposal_count", 0),
                "core_proposals": d.get("core_proposals", []),
            },
        )

        # roadmap_updates.json
        paths["roadmap_updates"] = self._write(
            "roadmap_updates.json",
            {
                "plan_id": d.get("plan_id", ""),
                "generated_at": d.get("generated_at", ""),
                "roadmap_update_count": d.get("roadmap_update_count", 0),
                "roadmap_updates": d.get("roadmap_updates", []),
                "note": "All roadmap updates require Owner approval before implementation.",
            },
        )

        # capability_analysis.json
        paths["capability_analysis"] = self._write(
            "capability_analysis.json",
            {
                "plan_id": d.get("plan_id", ""),
                "generated_at": d.get("generated_at", ""),
                "capability_gap_count": d.get("capability_gap_count", 0),
                "capability_gaps": d.get("capability_gaps", []),
            },
        )

        # history.json
        paths["history"] = self._append_history(d)

        # snapshot.json
        paths["snapshot"] = self._write(
            "snapshot.json",
            {
                "plan_id": d.get("plan_id", ""),
                "captured_at": d.get("generated_at", ""),
                "repository": d.get("repository", ""),
                "schema_version": d.get("schema_version", ""),
                "technical_debt_count": d.get("technical_debt_count", 0),
                "capability_gap_count": d.get("capability_gap_count", 0),
                "proposed_issue_count": d.get("proposed_issue_count", 0),
            },
        )

        # Markdown report
        if markdown:
            md_path = self.base_dir / "AI_CTO_SELF_IMPROVEMENT.md"
            md_content = markdown if markdown.endswith("\n") else markdown + "\n"
            self._atomic_write_text(md_path, md_content)
            paths["markdown"] = str(md_path)

        return paths

    def load_improvements(self) -> Dict[str, Any]:
        return self._read("improvements.json")

    def exists(self) -> bool:
        return (self.base_dir / "improvements.json").exists()

    # ------------------------------------------------------------------

    def _append_history(self, d: Dict[str, Any]) -> str:
        history = self._read("history.json")
        entries: List[Dict[str, Any]] = list(history.get("entries", []))
        entries.append({
            "plan_id": d.get("plan_id", ""),
            "timestamp": d.get("generated_at", ""),
            "repository": d.get("repository", ""),
            "technical_debt_count": d.get("technical_debt_count", 0),
            "capability_gap_count": d.get("capability_gap_count", 0),
            "proposed_issue_count": d.get("proposed_issue_count", 0),
            "core_proposal_count": d.get("core_proposal_count", 0),
        })
        history_dict = {
            "repository": d.get("repository", ""),
            "generated_at": d.get("generated_at", ""),
            "schema_version": d.get("schema_version", ""),
            "entry_count": len(entries),
            "entries": entries,
        }
        return self._write("history.json", history_dict)

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
