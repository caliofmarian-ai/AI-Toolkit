"""
Self Evaluation Engine — Persistence Layer
CORE-016D

Writes all evaluation artifacts to .ai/self_evaluation/ atomically.

Artifacts produced:
  evaluation.json
  quality.json
  confidence.json
  compliance.json
  architecture.json
  coverage.json
  regressions.json
  evidence.json
  history.json
  snapshot.json
  AI_CTO_SELF_EVALUATION.md
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List


class EvaluationPersistence:
    """
    CORE-016D — Evaluation Persistence.

    All writes are atomic and deterministic.
    """

    EVALUATION_DIR = "self_evaluation"

    def __init__(self, repository_root: str = ".") -> None:
        self.repository_root = Path(repository_root).resolve()
        self.base_dir = self.repository_root / ".ai" / self.EVALUATION_DIR

    def save(
        self,
        evaluation_result: Any,
        markdown: str = "",
    ) -> Dict[str, str]:
        """
        Persist all evaluation artifacts.

        Returns a dict mapping artifact name → absolute file path.
        """
        self.base_dir.mkdir(parents=True, exist_ok=True)
        d = evaluation_result.to_dict()
        paths: Dict[str, str] = {}

        # evaluation.json — full result
        paths["evaluation"] = self._write("evaluation.json", d)

        # quality.json — quality scores
        paths["quality"] = self._write(
            "quality.json",
            {
                "evaluation_id": d.get("evaluation_id", ""),
                "generated_at": d.get("generated_at", ""),
                "quality_scores": d.get("quality_scores", []),
                "overall_score": d.get("overall_score", 0.0),
                "overall_gate": d.get("overall_gate", ""),
            },
        )

        # confidence.json — confidence score
        confidence_scores = [
            s for s in d.get("quality_scores", []) if s.get("dimension") == "confidence"
        ]
        paths["confidence"] = self._write(
            "confidence.json",
            {
                "evaluation_id": d.get("evaluation_id", ""),
                "generated_at": d.get("generated_at", ""),
                "confidence_score": confidence_scores[0] if confidence_scores else {},
                "overall_confidence": d.get("overall_confidence", 0.0),
            },
        )

        # compliance.json — canonical compliance
        compliance_scores = [
            s for s in d.get("quality_scores", []) if s.get("dimension") == "canonical_compliance"
        ]
        paths["compliance"] = self._write(
            "compliance.json",
            {
                "evaluation_id": d.get("evaluation_id", ""),
                "generated_at": d.get("generated_at", ""),
                "compliance_scores": compliance_scores,
            },
        )

        # architecture.json
        paths["architecture"] = self._write(
            "architecture.json",
            {
                "evaluation_id": d.get("evaluation_id", ""),
                "generated_at": d.get("generated_at", ""),
                "architecture_findings": d.get("architecture_findings", []),
            },
        )

        # coverage.json
        coverage_scores = [
            s for s in d.get("quality_scores", []) if s.get("dimension") == "testing_quality"
        ]
        paths["coverage"] = self._write(
            "coverage.json",
            {
                "evaluation_id": d.get("evaluation_id", ""),
                "generated_at": d.get("generated_at", ""),
                "coverage_scores": coverage_scores,
            },
        )

        # regressions.json
        paths["regressions"] = self._write(
            "regressions.json",
            {
                "evaluation_id": d.get("evaluation_id", ""),
                "generated_at": d.get("generated_at", ""),
                "regression_findings": d.get("regression_findings", []),
                "regression_count": len(d.get("regression_findings", [])),
            },
        )

        # evidence.json
        paths["evidence"] = self._write(
            "evidence.json",
            {
                "evaluation_id": d.get("evaluation_id", ""),
                "generated_at": d.get("generated_at", ""),
                "quality_scores": d.get("quality_scores", []),
            },
        )

        # history.json — append current run
        paths["history"] = self._append_history(d)

        # snapshot.json
        paths["snapshot"] = self._write(
            "snapshot.json",
            {
                "evaluation_id": d.get("evaluation_id", ""),
                "captured_at": d.get("generated_at", ""),
                "context": d.get("context", {}),
                "overall_score": d.get("overall_score", 0.0),
                "overall_gate": d.get("overall_gate", ""),
                "schema_version": d.get("schema_version", ""),
            },
        )

        # Markdown report
        if markdown:
            md_path = self.base_dir / "AI_CTO_SELF_EVALUATION.md"
            md_content = markdown if markdown.endswith("\n") else markdown + "\n"
            self._atomic_write_text(md_path, md_content)
            paths["markdown"] = str(md_path)

        return paths

    def load_evaluation(self) -> Dict[str, Any]:
        return self._read("evaluation.json")

    def exists(self) -> bool:
        return (self.base_dir / "evaluation.json").exists()

    # ------------------------------------------------------------------

    def _append_history(self, d: Dict[str, Any]) -> str:
        history = self._read("history.json")
        entries: List[Dict[str, Any]] = list(history.get("entries", []))
        entries.append({
            "evaluation_id": d.get("evaluation_id", ""),
            "timestamp": d.get("generated_at", ""),
            "repository": d.get("repository", ""),
            "overall_score": d.get("overall_score", 0.0),
            "overall_gate": d.get("overall_gate", ""),
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
