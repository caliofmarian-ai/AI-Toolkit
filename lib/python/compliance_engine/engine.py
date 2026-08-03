from pathlib import Path

from python.canonical_entities import ComplianceMetric, ComplianceState


class ComplianceEngine:
    """Evaluate canonical compliance across categories."""

    def __init__(self, repository=".", workspace_index=None):
        self.root = Path(repository).resolve()
        self._workspace_index = workspace_index

    def _get_index(self):
        if self._workspace_index is not None:
            return self._workspace_index
        from python.workspace_index import WorkspaceIndexBuilder
        return WorkspaceIndexBuilder(self.root).build()

    def evaluate(self, canonical_repo, matches, coverage_metrics):
        """Evaluate repository compliance against canonical expectations."""
        index = self._get_index()
        coverage_lookup = dict((metric.category, metric) for metric in coverage_metrics)
        metrics = []
        docs = canonical_repo.all_documents()
        best_matches = dict((doc.id, self._best_confidence(matches.get(doc.id, []))) for doc in docs)

        canonical_score = self._average([
            coverage_lookup.get("Documentation").score if coverage_lookup.get("Documentation") else 0.0,
            coverage_lookup.get("Implementation").score if coverage_lookup.get("Implementation") else 0.0,
        ])
        metrics.append(self._metric("Canonical Compliance", canonical_score, ["Documentation and implementation coverage considered"]))
        metrics.append(self._metric("Architecture Compliance", self._score_from_metric(coverage_lookup, "Architecture"), self._metric_evidence(coverage_lookup, "Architecture")))

        package_files = [wf.path for wf in index.python_files() if wf.name == "__init__.py" and wf.path.startswith("lib/python/")]
        python_dirs = set(Path(wf.path).parent.as_posix() for wf in index.python_files() if wf.path.startswith("lib/python/"))
        structural_score = float(len(package_files)) / float(len(python_dirs)) if python_dirs else 0.0
        structural_score = max(structural_score, self._score_from_metric(coverage_lookup, "Implementation") * 0.5)
        metrics.append(self._metric("Structural Compliance", min(1.0, structural_score), package_files[:10]))

        interface_hits = [wf.path for wf in index.python_files() if "interface" in wf.path.lower() or wf.name == "base.py"]
        interface_score = min(1.0, float(len(interface_hits)) / 3.0) if interface_hits else 0.0
        metrics.append(self._metric("Interface Compliance", interface_score, interface_hits[:10]))

        dependency_graph = canonical_repo.dependency_graph()
        dep_total = sum(1 for deps in dependency_graph.values() if deps)
        dep_ok = 0
        evidence = []
        for doc_id, deps in dependency_graph.items():
            if not deps:
                continue
            if best_matches.get(doc_id, 0.0) < 0.5:
                continue
            if all(best_matches.get(dep, 0.0) >= 0.3 for dep in deps):
                dep_ok += 1
                evidence.append(doc_id)
        dependency_score = float(dep_ok) / float(dep_total) if dep_total else 0.0
        metrics.append(self._metric("Dependency Compliance", dependency_score, evidence[:10]))

        metrics.append(self._metric("Runtime Compliance", self._score_from_metric(coverage_lookup, "Runtime"), self._metric_evidence(coverage_lookup, "Runtime")))
        metrics.append(self._metric("Configuration Compliance", self._score_from_metric(coverage_lookup, "Configuration"), self._metric_evidence(coverage_lookup, "Configuration")))
        metrics.append(self._metric("Testing Compliance", self._score_from_metric(coverage_lookup, "Testing"), self._metric_evidence(coverage_lookup, "Testing")))
        return metrics

    def overall_score(self, metrics):
        return self._average([metric.score for metric in metrics])

    def _metric(self, category, score, evidence):
        return ComplianceMetric(
            category=category,
            state=self._state_for_score(score),
            score=max(0.0, min(1.0, score)),
            evidence=list(evidence)[:10],
        )

    def _state_for_score(self, score):
        if score >= 0.8:
            return ComplianceState.COMPLIANT
        if score >= 0.5:
            return ComplianceState.CONDITIONALLY_COMPLIANT
        if score > 0.0:
            return ComplianceState.NON_COMPLIANT
        return ComplianceState.UNKNOWN

    def _average(self, values):
        values = [value for value in values if value is not None]
        return (sum(values) / float(len(values))) if values else 0.0

    def _best_confidence(self, matches):
        if not matches:
            return 0.0
        return max(match.confidence for match in matches)

    def _score_from_metric(self, lookup, name):
        metric = lookup.get(name)
        return metric.score if metric else 0.0

    def _metric_evidence(self, lookup, name):
        metric = lookup.get(name)
        return metric.evidence if metric else []
