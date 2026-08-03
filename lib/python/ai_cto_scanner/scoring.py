"""
AI CTO Integration Scanner — Readiness Scoring

Computes AI CTO readiness scores for each architectural dimension.
"""


class ReadinessScorer:
    """Compute readiness scores from detection results and canonical analysis."""

    # Score weights per dimension (detection_weight, canonical_bonus)
    _WEIGHTS = {
        "Telegram": 1.0,
        "Runtime": 1.0,
        "State": 1.0,
        "Persistence": 0.8,
        "OwnerControl": 1.0,
        "Canonical": 1.0,
        "Development": 0.8,
        "ProjectMemory": 1.0,
        "ContextIntegrity": 0.6,
        "Overall": 1.0,
    }

    def compute(self, detection_results, canonical_stats=None):
        """
        Compute readiness scores from detection results dict.

        detection_results: dict[category_name -> DetectionResult]
        canonical_stats: optional dict from CanonicalIntelligenceEngine.statistics()
        Returns: dict[dimension -> score_0_to_100]
        """
        scores = {}

        # Telegram Readiness
        telegram = detection_results.get("Telegram")
        scores["Telegram Readiness"] = self._score(telegram)

        # Runtime Readiness
        runtime = detection_results.get("Runtime")
        scores["Runtime Readiness"] = self._score(runtime)

        # State Readiness
        state = detection_results.get("State")
        scores["State Readiness"] = self._score(state)

        # Persistence Readiness (derived from State + Configuration)
        config = detection_results.get("Configuration")
        persist_components = self._filter_components(state, ["Persistence", "State Store", "Session Management"])
        config_components = self._filter_components(config, ["Configuration Files", "Environment Variables"])
        persist_count = persist_components + config_components
        persist_total = 5
        scores["Persistence Readiness"] = min(100, int((persist_count / persist_total) * 100))

        # Owner Readiness
        owner = detection_results.get("OwnerControl")
        scores["Owner Readiness"] = self._score(owner)

        # Canonical Readiness
        canonical = detection_results.get("Canonical")
        canon_score = self._score(canonical)
        if canonical_stats:
            canon_bonus = int(
                canonical_stats.get("overall_coverage", 0.0) * 30
                + canonical_stats.get("overall_compliance", 0.0) * 20
            )
            canon_score = min(100, canon_score + canon_bonus)
        scores["Canonical Readiness"] = canon_score

        # Development Readiness (composite)
        dev_score = self._compute_development_readiness(detection_results, canonical_stats)
        scores["Development Readiness"] = dev_score

        # Project Memory Readiness
        memory = detection_results.get("ProjectMemory")
        scores["Project Memory Readiness"] = self._score(memory)

        # Context Integrity Readiness (subset of Project Memory)
        integrity_components = self._filter_components(memory, ["Context Integrity", "Snapshot Engine", "Context Persistence"])
        scores["Context Integrity Readiness"] = min(100, int((integrity_components / 3) * 100))

        # Overall AI CTO Readiness (weighted average)
        dimension_scores = [
            scores["Telegram Readiness"] * 1.0,
            scores["Runtime Readiness"] * 1.0,
            scores["State Readiness"] * 1.0,
            scores["Owner Readiness"] * 1.0,
            scores["Canonical Readiness"] * 1.2,
            scores["Development Readiness"] * 0.8,
            scores["Project Memory Readiness"] * 1.0,
        ]
        total_weight = 1.0 + 1.0 + 1.0 + 1.0 + 1.2 + 0.8 + 1.0
        scores["Overall AI CTO Readiness"] = int(sum(dimension_scores) / total_weight)

        return scores

    def _score(self, result):
        if result is None:
            return 0
        return int(result.score * 100)

    def _filter_components(self, result, names):
        if result is None:
            return 0
        return sum(1 for m in result.matches if m.name in names and m.confidence > 0.0)

    def _compute_development_readiness(self, detection_results, canonical_stats):
        scores = []
        for category in ("Runtime", "Configuration", "State"):
            result = detection_results.get(category)
            if result:
                scores.append(result.score)
        if canonical_stats:
            scores.append(canonical_stats.get("overall_coverage", 0.0))
            scores.append(canonical_stats.get("overall_compliance", 0.0))
        if not scores:
            return 0
        return int((sum(scores) / len(scores)) * 100)
