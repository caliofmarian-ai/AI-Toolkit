"""
Autonomous Execution Engine — Logger and Reporter
CORE-015E

Structured log recording and execution report generation.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


class ExecutionLogger:
    """
    CORE-015E — Execution Logger.

    Records structured log entries for every pipeline stage.
    All entries are deterministic — no floating timestamps in tests.
    """

    def __init__(self) -> None:
        self._entries: List[Dict[str, Any]] = []

    def log(self, level: str, stage: str, message: str, data: Dict[str, Any] = None) -> None:
        self._entries.append(
            {
                "timestamp": _utcnow(),
                "level": level.upper(),
                "stage": stage,
                "message": message,
                "data": data or {},
            }
        )

    def info(self, stage: str, message: str, data: Dict[str, Any] = None) -> None:
        self.log("INFO", stage, message, data)

    def warning(self, stage: str, message: str, data: Dict[str, Any] = None) -> None:
        self.log("WARNING", stage, message, data)

    def error(self, stage: str, message: str, data: Dict[str, Any] = None) -> None:
        self.log("ERROR", stage, message, data)

    def entries(self) -> List[Dict[str, Any]]:
        return list(self._entries)

    def to_dict(self) -> Dict[str, Any]:
        return {"entry_count": len(self._entries), "entries": list(self._entries)}


class ExecutionReporter:
    """
    CORE-015E — Execution Reporter.

    Produces structured execution reports from ExecutionResult.
    """

    def report(self, result_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Return a structured report dict from a serialised ExecutionResult."""
        stage_results = result_dict.get("stage_results", [])
        validation_results = result_dict.get("validation_results", [])
        metrics = result_dict.get("metrics", {})
        errors = result_dict.get("errors", [])
        warnings = result_dict.get("warnings", [])

        passed = sum(1 for v in validation_results if v.get("status") == "PASS")
        failed = sum(1 for v in validation_results if v.get("status") == "FAIL")
        avg_score = (
            sum(v.get("score", 0.0) for v in validation_results) / len(validation_results)
            if validation_results
            else 0.0
        )

        return {
            "execution_id": result_dict.get("execution_id", ""),
            "generated_at": result_dict.get("generated_at", ""),
            "repository": result_dict.get("repository", ""),
            "mode": result_dict.get("mode", ""),
            "approval": result_dict.get("approval", ""),
            "status": result_dict.get("status", ""),
            "stage_count": len(stage_results),
            "validation_passed": passed,
            "validation_failed": failed,
            "average_validation_score": round(avg_score, 3),
            "error_count": len(errors),
            "warning_count": len(warnings),
            "total_duration_ms": metrics.get("total_duration_ms", 0.0),
            "confidence": result_dict.get("context", {}).get("confidence", 0.0),
            "summary": result_dict.get("summary", ""),
            "next_actions": result_dict.get("next_actions", []),
        }
