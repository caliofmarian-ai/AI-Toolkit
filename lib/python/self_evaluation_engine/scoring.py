"""
Self Evaluation Engine — Quality Scorer and Confidence Scorer
CORE-016C

Produces numerical scores from evaluation findings.
All scoring is deterministic and evidence-based.
"""

from typing import Any, Dict, List, Mapping

from .models import (
    ALL_DIMENSIONS,
    DIMENSION_OVERALL,
    GATE_FAILED,
    GATE_MANUAL_REVIEW,
    GATE_PASS,
    GATE_WARNING,
    QualityScore,
)

# Dimension weights for the overall score
_DIMENSION_WEIGHTS: Dict[str, float] = {
    "canonical_compliance": 0.15,
    "architecture_quality": 0.15,
    "repository_health": 0.10,
    "execution_quality": 0.15,
    "planning_quality": 0.10,
    "workspace_quality": 0.05,
    "maintainability": 0.10,
    "documentation_quality": 0.05,
    "testing_quality": 0.10,
    "confidence": 0.05,
}


class QualityScorer:
    """
    CORE-016C — Quality Scorer.

    Aggregates individual dimension scores into a weighted overall score.
    """

    def score_overall(self, quality_scores: List[QualityScore]) -> QualityScore:
        """Compute the weighted overall engineering quality score."""
        if not quality_scores:
            return QualityScore(
                dimension=DIMENSION_OVERALL,
                score=0.0,
                gate=GATE_FAILED,
                evidence=["No quality scores provided"],
                findings=["Cannot evaluate without individual dimension scores"],
                recommendation="Run self-evaluation with all analyzers enabled.",
            )

        score_map = {s.dimension: s.score for s in quality_scores}
        weighted_sum = 0.0
        weight_total = 0.0
        evidence: List[str] = []

        for dim, weight in _DIMENSION_WEIGHTS.items():
            dim_score = score_map.get(dim)
            if dim_score is not None:
                weighted_sum += dim_score * weight
                weight_total += weight
                evidence.append(f"{dim}: {dim_score:.0%} (weight={weight:.0%})")

        overall = weighted_sum / weight_total if weight_total > 0 else 0.0
        gate = self._gate(overall, quality_scores)

        return QualityScore(
            dimension=DIMENSION_OVERALL,
            score=round(overall, 3),
            gate=gate,
            evidence=evidence,
            findings=[],
            recommendation=self._recommendation(overall, gate),
        )

    def _gate(self, overall: float, scores: List[QualityScore]) -> str:
        has_failed = any(s.gate == GATE_FAILED for s in scores)
        if has_failed or overall < 0.5:
            return GATE_FAILED
        if overall < 0.7:
            return GATE_WARNING
        return GATE_PASS

    def _recommendation(self, score: float, gate: str) -> str:
        if gate == GATE_FAILED:
            return f"Critical quality issues detected (score={score:.0%}). Immediate attention required."
        if gate == GATE_WARNING:
            return f"Quality is acceptable but below target (score={score:.0%}). Improvements recommended."
        return f"Engineering quality is good (score={score:.0%}). Continue current practices."


class ConfidenceScorer:
    """
    CORE-016C — Confidence Scorer.

    Computes an evaluation confidence score based on available data sources.
    """

    def score(
        self,
        has_planning: bool,
        has_execution: bool,
        has_context: bool,
        has_briefing: bool,
        has_workspace: bool,
    ) -> QualityScore:
        sources = [has_planning, has_execution, has_context, has_briefing, has_workspace]
        available = sum(1 for s in sources if s)
        total = len(sources)
        confidence = available / total

        gate = GATE_PASS if confidence >= 0.8 else (GATE_WARNING if confidence >= 0.5 else GATE_FAILED)
        evidence = [
            f"Planning data: {'available' if has_planning else 'missing'}",
            f"Execution data: {'available' if has_execution else 'missing'}",
            f"Context data: {'available' if has_context else 'missing'}",
            f"Briefing data: {'available' if has_briefing else 'missing'}",
            f"Workspace data: {'available' if has_workspace else 'missing'}",
        ]

        return QualityScore(
            dimension="confidence",
            score=round(confidence, 3),
            gate=gate,
            evidence=evidence,
            findings=(
                [f"Only {available}/{total} data sources available"]
                if confidence < 1.0
                else []
            ),
            recommendation=(
                "Synchronize all data sources for maximum confidence."
                if confidence < 1.0
                else "All data sources available."
            ),
        )
