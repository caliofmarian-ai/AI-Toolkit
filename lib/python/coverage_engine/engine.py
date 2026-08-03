from pathlib import Path

from python.canonical_entities import CoverageMetric


class CoverageEngine:
    """Compute coverage metrics across dimensions."""

    def __init__(self, repository=".", workspace_index=None):
        self.root = Path(repository).resolve()
        self._workspace_index = workspace_index

    def _get_index(self):
        if self._workspace_index is not None:
            return self._workspace_index
        from python.workspace_index import WorkspaceIndexBuilder
        return WorkspaceIndexBuilder(self.root).build()

    def compute(self, canonical_repo, matches):
        """Compute coverage metrics across repository dimensions."""
        index = self._get_index()
        metrics = []
        documents = canonical_repo.all_documents()
        total_docs = len(documents)

        documentation_covered = sum(1 for doc in documents if self._best_confidence(matches.get(doc.id, [])) >= 0.5)
        implementation_covered = sum(1 for doc in documents if self._best_confidence(matches.get(doc.id, [])) >= 0.75)
        metrics.append(self._metric("Documentation", total_docs, documentation_covered, [], [doc.id for doc in documents if self._best_confidence(matches.get(doc.id, [])) >= 0.5]))
        metrics.append(self._metric("Implementation", total_docs, implementation_covered, [doc.id for doc in documents if 0.3 <= self._best_confidence(matches.get(doc.id, [])) < 0.75], [doc.id for doc in documents if self._best_confidence(matches.get(doc.id, [])) >= 0.75]))

        python_modules = len(index.python_files())
        test_files = [wf.path for wf in index.files if "test" in wf.path.lower() and wf.extension in (".py", ".sh")]
        testing_total = max(1, python_modules)
        testing_covered = min(testing_total, len(test_files))
        metrics.append(self._metric("Testing", testing_total, testing_covered, [], test_files[:10]))

        metrics.append(self._architecture_metric(index, canonical_repo, matches))
        metrics.append(self._keyword_metric("Runtime", index, ["runtime", "execution", "coordinator"]))
        metrics.append(self._keyword_metric("Configuration", index, ["config", "configuration", "settings", "policy"]))
        metrics.append(self._keyword_metric("Observability", index, ["observability", "monitor", "metrics", "progress", "profiler"]))
        metrics.append(self._keyword_metric("Security", index, ["security", "auth", "secret", "permission"]))
        metrics.append(self._keyword_metric("Planning", index, ["planning", "roadmap", "planner", "batch"]))
        return metrics

    def summary(self, metrics):
        overall = 0.0
        if metrics:
            overall = sum(metric.score for metric in metrics) / float(len(metrics))
        return {"overall": overall, "categories": dict((metric.category, metric.score) for metric in metrics)}

    def _best_confidence(self, matches):
        if not matches:
            return 0.0
        return max(match.confidence for match in matches)

    def _metric(self, category, total, covered, partial_items, evidence):
        total = int(total)
        covered = int(min(total, covered))
        partial = len(partial_items)
        missing = max(total - covered, 0)
        score = float(covered) / float(total) if total else 0.0
        score = max(0.0, min(1.0, score))
        return CoverageMetric(
            category=category,
            score=score,
            total=total,
            covered=covered,
            missing=missing,
            partial=partial,
            evidence=list(evidence)[:10],
        )

    def _architecture_metric(self, index, canonical_repo, matches):
        architecture_doc = canonical_repo.get_by_id("CANON-001")
        layers = [
            "workspace", "repository", "analysis", "intelligence", "planning",
            "execution", "review", "observability", "persistence", "autonomous",
        ]
        if architecture_doc is not None:
            discovered = []
            for section in architecture_doc.sections:
                lowered = section.title.lower()
                if lowered.endswith("layer"):
                    discovered.append(lowered.replace(" layer", ""))
            if discovered:
                layers = discovered
        corpus = []
        for wf in index.files:
            corpus.append(wf.path.lower())
        for doc_matches in matches.values():
            for match in doc_matches:
                corpus.append(match.implementation_ref.lower())
        corpus_text = "\n".join(corpus)
        found = [layer for layer in layers if layer in corpus_text]
        return self._metric("Architecture", len(layers), len(found), [], found)

    def _keyword_metric(self, category, index, keywords):
        joined = "\n".join(wf.path.lower() for wf in index.files)
        found = [keyword for keyword in keywords if keyword in joined]
        return self._metric(category, len(keywords), len(found), [], found)
