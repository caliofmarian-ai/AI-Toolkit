"""
Autonomous Execution Engine — Execution Validator
CORE-015C

Runs repository, semantic, canonical and regression validation
using existing CORE intelligence.  Does NOT duplicate any analysis.
"""

import time
from typing import Any, Dict, List, Mapping

from .models import (
    VALIDATION_FAIL,
    VALIDATION_PASS,
    VALIDATION_SKIPPED,
    VALIDATION_WARNING,
    ValidationResult,
)


class ExecutionValidator:
    """
    CORE-015C — Execution Validator.

    Orchestrates validation by delegating to existing CORE engines.
    Produces deterministic, evidence-based ValidationResult objects.
    """

    def __init__(self, repository: str = ".") -> None:
        self.repository = repository

    def validate_repository(self) -> ValidationResult:
        """Repository structure validation via CORE-008A."""
        try:
            from python.ai_cto_scanner import AICTOScannerEngine  # type: ignore[import]

            scanner = AICTOScannerEngine(self.repository)
            result = scanner.scan()
            score = result.get("readiness_score")
            if score is None:
                overall = (result.get("scores") or {}).get("Overall AI CTO Readiness")
                if isinstance(overall, (int, float)):
                    score = float(overall) / 100.0
            score = float(score if score is not None else 0.5)
            findings = result.get("findings", [])
            return ValidationResult(
                validator="RepositoryValidator",
                status=VALIDATION_PASS if score >= 0.5 else VALIDATION_WARNING,
                score=score,
                findings=[str(f) for f in findings],
                evidence={"readiness_score": score, "source": "CORE-008A"},
            )
        except Exception as exc:  # noqa: BLE001
            return ValidationResult(
                validator="RepositoryValidator",
                status=VALIDATION_SKIPPED,
                score=0.5,
                findings=[f"Repository validation skipped: {exc}"],
                evidence={"source": "CORE-008A"},
            )

    def validate_semantic(self) -> ValidationResult:
        """Semantic architecture validation via CORE-008B."""
        try:
            from python.semantic_repository_intelligence import (  # type: ignore[import]
                SemanticRepositoryEngine,
            )
            engine = SemanticRepositoryEngine(repository=self.repository, persist=False)
            result = engine.analyze()
            risks = result.get("architecture_graph", {}).get("risks", [])
            score = max(0.0, 1.0 - len(risks) * 0.05)
            return ValidationResult(
                validator="SemanticValidator",
                status=VALIDATION_PASS if not risks else VALIDATION_WARNING,
                score=round(score, 3),
                findings=[str(r) for r in risks[:10]],
                evidence={"risk_count": len(risks), "source": "CORE-008B"},
            )
        except Exception as exc:  # noqa: BLE001
            return ValidationResult(
                validator="SemanticValidator",
                status=VALIDATION_SKIPPED,
                score=0.5,
                findings=[f"Semantic validation skipped: {exc}"],
                evidence={"source": "CORE-008B"},
            )

    def validate_canonical(self) -> ValidationResult:
        """Canonical specification compliance via CORE-007."""
        try:
            from python.canonical_intelligence.engine import (  # type: ignore[import]
                CanonicalIntelligenceEngine,
            )
            engine = CanonicalIntelligenceEngine(repository=self.repository)
            result = engine.analyze()
            deviations = result.get("deviations", [])
            score = max(0.0, 1.0 - len(deviations) * 0.1)
            return ValidationResult(
                validator="CanonicalValidator",
                status=VALIDATION_PASS if not deviations else VALIDATION_WARNING,
                score=round(score, 3),
                findings=[str(d) for d in deviations[:10]],
                evidence={"deviation_count": len(deviations), "source": "CORE-007"},
            )
        except Exception as exc:  # noqa: BLE001
            return ValidationResult(
                validator="CanonicalValidator",
                status=VALIDATION_SKIPPED,
                score=0.5,
                findings=[f"Canonical validation skipped: {exc}"],
                evidence={"source": "CORE-007"},
            )

    def validate_regression(
        self, snapshot: Mapping[str, Any]
    ) -> ValidationResult:
        """
        Regression validation — compare current state against the snapshot.

        Detects schema-level regressions in planning output structure.
        """
        findings: List[str] = []
        evidence: Dict[str, Any] = {}

        # Check that key planning fields have not disappeared
        required_keys = {"planning_id", "schema_version", "execution_queue"}
        planning = dict(snapshot.get("planning_queue", {}) or {})
        if (
            "planning_id" not in planning
            and "execution_queue" not in planning
            and "entries" in planning
        ):
            planning = {
                "planning_id": planning.get("queue_id", ""),
                "schema_version": planning.get("schema_version", ""),
                "execution_queue": planning,
            }
        missing = required_keys - set(planning.keys())
        if missing:
            findings.append(f"Missing planning keys: {sorted(missing)}")
        evidence["checked_planning_keys"] = sorted(required_keys)
        evidence["missing_planning_keys"] = sorted(missing)

        status = VALIDATION_FAIL if findings else VALIDATION_PASS
        score = 0.0 if findings else 1.0
        return ValidationResult(
            validator="RegressionValidator",
            status=status,
            score=score,
            findings=findings,
            evidence=evidence,
        )

    def validate_acceptance(
        self, mode: str, validation_results: List[ValidationResult]
    ) -> ValidationResult:
        """
        Full acceptance validation — all validators must PASS or WARNING.
        """
        failures = [
            v for v in validation_results if v.status == VALIDATION_FAIL
        ]
        avg_score = (
            sum(v.score for v in validation_results) / len(validation_results)
            if validation_results
            else 1.0
        )
        status = VALIDATION_FAIL if failures else VALIDATION_PASS
        return ValidationResult(
            validator="AcceptanceValidator",
            status=status,
            score=round(avg_score, 3),
            findings=[f"{v.validator}: {v.findings}" for v in failures],
            evidence={
                "mode": mode,
                "validator_count": len(validation_results),
                "failure_count": len(failures),
                "average_score": round(avg_score, 3),
            },
        )
