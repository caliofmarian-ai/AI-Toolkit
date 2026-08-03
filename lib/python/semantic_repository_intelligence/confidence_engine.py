"""
Semantic Repository Intelligence — Confidence Engine
CORE-008B

Computes confidence scores for semantic findings based on the quality and
quantity of supporting evidence.
"""

from typing import Any, Dict, List


class ConfidenceEngine:
    """
    Assigns calibrated confidence scores to semantic findings.

    Confidence is a float in [0.0, 1.0] derived from:

    - Number of evidence pieces (more = higher confidence)
    - Source diversity (AST vs. text-match vs. heuristic)
    - Cross-reference count (finding corroborated by multiple files)
    - Base confidence supplied by the detector

    The engine is intentionally simple and stateless so that scores are
    deterministic across runs.
    """

    # Weights per evidence tier
    _TIER_WEIGHTS = {
        "ast": 1.0,        # direct AST parse result
        "text_match": 0.7, # regex / text scan result
        "heuristic": 0.4,  # naming / path heuristic
    }

    def score(
        self,
        base_confidence: float,
        evidence: List[str],
        cross_reference_count: int = 0,
        evidence_tier: str = "text_match",
    ) -> float:
        """
        Compute a confidence score.

        Parameters
        ----------
        base_confidence:
            Detector-supplied initial confidence (0.0–1.0).
        evidence:
            List of evidence strings (more items → higher score).
        cross_reference_count:
            How many independent files corroborate this finding.
        evidence_tier:
            Quality tier of evidence: 'ast', 'text_match', or 'heuristic'.
        """
        tier_weight = self._TIER_WEIGHTS.get(evidence_tier, 0.5)

        # Evidence bonus: logarithmic to avoid trivially hitting 1.0
        n = max(0, len(evidence))
        if n == 0:
            evidence_bonus = 0.0
        elif n == 1:
            evidence_bonus = 0.05
        elif n <= 3:
            evidence_bonus = 0.10
        elif n <= 10:
            evidence_bonus = 0.15
        else:
            evidence_bonus = 0.20

        # Cross-reference bonus
        xref_bonus = min(0.15, cross_reference_count * 0.03)

        raw = base_confidence * tier_weight + evidence_bonus + xref_bonus
        return round(min(1.0, max(0.0, raw)), 3)

    def score_batch(
        self, findings: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Apply confidence scoring to a list of finding dicts in-place.

        Each dict must contain at minimum:
          - ``base_confidence`` (float)
          - ``evidence`` (list[str])
        Optionally:
          - ``cross_reference_count`` (int)
          - ``evidence_tier`` (str)

        The updated ``confidence`` key is written back to each dict.
        """
        scored = []
        for finding in findings:
            confidence = self.score(
                base_confidence=finding.get("base_confidence", 0.5),
                evidence=finding.get("evidence", []),
                cross_reference_count=finding.get("cross_reference_count", 0),
                evidence_tier=finding.get("evidence_tier", "text_match"),
            )
            updated = dict(finding)
            updated["confidence"] = confidence
            scored.append(updated)
        return scored

    def aggregate(self, confidences: List[float]) -> float:
        """
        Aggregate multiple confidence scores into a single score using the
        conservative minimum-weighted average (geometric mean of sorted top-half).
        """
        if not confidences:
            return 0.0
        sorted_conf = sorted(confidences)
        # Use the lower half to stay conservative
        n = max(1, len(sorted_conf) // 2 + 1)
        subset = sorted_conf[:n]
        product = 1.0
        for c in subset:
            product *= max(0.01, c)
        return round(product ** (1.0 / n), 3)
