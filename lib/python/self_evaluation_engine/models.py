"""
Self Evaluation Engine — Canonical Models
CORE-016A

All evaluation artifacts are deterministic, serialisable, and versioned.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

EVALUATION_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Quality Gate constants
# ---------------------------------------------------------------------------

GATE_PASS = "PASS"
GATE_WARNING = "WARNING"
GATE_FAILED = "FAILED"
GATE_BLOCKED = "BLOCKED"
GATE_MANUAL_REVIEW = "MANUAL_REVIEW"

QUALITY_GATES = (GATE_PASS, GATE_WARNING, GATE_FAILED, GATE_BLOCKED, GATE_MANUAL_REVIEW)

# ---------------------------------------------------------------------------
# Score dimension constants
# ---------------------------------------------------------------------------

DIMENSION_CANONICAL_COMPLIANCE = "canonical_compliance"
DIMENSION_ARCHITECTURE_QUALITY = "architecture_quality"
DIMENSION_REPOSITORY_HEALTH = "repository_health"
DIMENSION_EXECUTION_QUALITY = "execution_quality"
DIMENSION_PLANNING_QUALITY = "planning_quality"
DIMENSION_WORKSPACE_QUALITY = "workspace_quality"
DIMENSION_MAINTAINABILITY = "maintainability"
DIMENSION_DOCUMENTATION_QUALITY = "documentation_quality"
DIMENSION_TESTING_QUALITY = "testing_quality"
DIMENSION_CONFIDENCE = "confidence"
DIMENSION_OVERALL = "overall_engineering_quality"

ALL_DIMENSIONS = (
    DIMENSION_CANONICAL_COMPLIANCE,
    DIMENSION_ARCHITECTURE_QUALITY,
    DIMENSION_REPOSITORY_HEALTH,
    DIMENSION_EXECUTION_QUALITY,
    DIMENSION_PLANNING_QUALITY,
    DIMENSION_WORKSPACE_QUALITY,
    DIMENSION_MAINTAINABILITY,
    DIMENSION_DOCUMENTATION_QUALITY,
    DIMENSION_TESTING_QUALITY,
    DIMENSION_CONFIDENCE,
    DIMENSION_OVERALL,
)


# ---------------------------------------------------------------------------
# EvaluationContext
# ---------------------------------------------------------------------------

@dataclass
class EvaluationContext:
    """Records all context used during a self-evaluation run."""

    evaluation_id: str
    repository: str
    workspace: str
    generated_at: str
    schema_version: str
    planning_id: str
    execution_id: str
    briefing_id: str
    synchronization_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evaluation_id": self.evaluation_id,
            "repository": self.repository,
            "workspace": self.workspace,
            "generated_at": self.generated_at,
            "schema_version": self.schema_version,
            "planning_id": self.planning_id,
            "execution_id": self.execution_id,
            "briefing_id": self.briefing_id,
            "synchronization_id": self.synchronization_id,
        }


# ---------------------------------------------------------------------------
# QualityScore
# ---------------------------------------------------------------------------

@dataclass
class QualityScore:
    """A single scored quality dimension with evidence."""

    dimension: str
    score: float
    gate: str
    evidence: List[str]
    findings: List[str]
    recommendation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dimension": self.dimension,
            "score": self.score,
            "gate": self.gate,
            "evidence": self.evidence,
            "findings": self.findings,
            "recommendation": self.recommendation,
        }


# ---------------------------------------------------------------------------
# RegressionFinding
# ---------------------------------------------------------------------------

@dataclass
class RegressionFinding:
    """A single detected regression."""

    severity: str
    component: str
    finding: str
    impact: str
    affected_modules: List[str]
    confidence: float
    recommendation: str
    evidence: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "severity": self.severity,
            "component": self.component,
            "finding": self.finding,
            "impact": self.impact,
            "affected_modules": self.affected_modules,
            "confidence": self.confidence,
            "recommendation": self.recommendation,
            "evidence": self.evidence,
        }


# ---------------------------------------------------------------------------
# ArchitectureFinding
# ---------------------------------------------------------------------------

@dataclass
class ArchitectureFinding:
    """A detected architecture compliance issue."""

    category: str
    component: str
    description: str
    severity: str
    evidence: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "component": self.component,
            "description": self.description,
            "severity": self.severity,
            "evidence": self.evidence,
        }


# ---------------------------------------------------------------------------
# EvaluationResult
# ---------------------------------------------------------------------------

@dataclass
class EvaluationResult:
    """Deterministic summary of a complete self-evaluation run."""

    evaluation_id: str
    generated_at: str
    repository: str
    schema_version: str
    context: Optional[EvaluationContext] = None
    quality_scores: List[QualityScore] = field(default_factory=list)
    regression_findings: List[RegressionFinding] = field(default_factory=list)
    architecture_findings: List[ArchitectureFinding] = field(default_factory=list)
    overall_gate: str = GATE_PASS
    overall_score: float = 0.0
    overall_confidence: float = 0.0
    summary: str = ""
    recommendations: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evaluation_id": self.evaluation_id,
            "generated_at": self.generated_at,
            "repository": self.repository,
            "schema_version": self.schema_version,
            "context": self.context.to_dict() if self.context else {},
            "quality_scores": [s.to_dict() for s in self.quality_scores],
            "regression_findings": [r.to_dict() for r in self.regression_findings],
            "architecture_findings": [a.to_dict() for a in self.architecture_findings],
            "overall_gate": self.overall_gate,
            "overall_score": self.overall_score,
            "overall_confidence": self.overall_confidence,
            "summary": self.summary,
            "recommendations": self.recommendations,
            "errors": self.errors,
            "warnings": self.warnings,
        }
