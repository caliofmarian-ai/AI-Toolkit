from pathlib import Path
from typing import Any, Dict

from python.batch_planner import BatchPlanner
from python.canonical_repository import CanonicalRepository
from python.compliance_engine import ComplianceEngine
from python.coverage_engine import CoverageEngine
from python.drift_engine import DriftEngine
from python.knowledge_graph import CanonicalKnowledgeGraphBuilder
from python.reporting_engine import ReportingEngine
from python.semantic_matching import SemanticMatcher


class CanonicalIntelligenceEngine:
    """Main entry point for CORE-007 Canonical Intelligence."""

    def __init__(self, repository=".", workspace_index=None, canonical_docs_path=None):
        self.root = Path(repository).resolve()
        self._workspace_index = workspace_index
        self._canonical_docs_path = Path(canonical_docs_path) if canonical_docs_path is not None else (self.root / "docs" / "canonical")

    def _get_index(self):
        if self._workspace_index is not None:
            return self._workspace_index
        from python.workspace_index import WorkspaceIndexBuilder
        return WorkspaceIndexBuilder(self.root).build()

    def run(self):
        """Execute the full canonical intelligence pipeline."""
        index = self._get_index()
        canonical_repo = CanonicalRepository.load_from_directory(self._canonical_docs_path)
        graph = CanonicalKnowledgeGraphBuilder().build(canonical_repo)
        matcher = SemanticMatcher(self.root, workspace_index=index)
        matches = matcher.match_all(canonical_repo)
        coverage_engine = CoverageEngine(self.root, workspace_index=index)
        coverage = coverage_engine.compute(canonical_repo, matches)
        compliance_engine = ComplianceEngine(self.root, workspace_index=index)
        compliance = compliance_engine.evaluate(canonical_repo, matches, coverage)
        drift_engine = DriftEngine(self.root, workspace_index=index)
        findings = drift_engine.detect(canonical_repo, matches, coverage)
        planner = BatchPlanner()
        batches = planner.generate(canonical_repo, findings, coverage)
        reporter = ReportingEngine()
        reports = reporter.generate(canonical_repo, graph, matches, coverage, compliance, findings, batches)
        return {
            "canonical_repository": canonical_repo,
            "graph": graph,
            "matches": matches,
            "coverage": coverage,
            "compliance": compliance,
            "drift": findings,
            "batches": batches,
            "reports": reports,
        }

    def analyze(self) -> Dict[str, Any]:
        """Backward-compatible alias for callers expecting analyze()."""
        return self.run()

    def statistics(self, result):
        coverage_scores = [metric.score for metric in result.get("coverage", [])]
        compliance_scores = [metric.score for metric in result.get("compliance", [])]
        canonical_repo = result.get("canonical_repository")
        graph = result.get("graph")
        return {
            "canonical_documents": len(canonical_repo.all_documents()) if canonical_repo is not None else 0,
            "graph_nodes": graph.node_count() if graph is not None else 0,
            "overall_coverage": sum(coverage_scores) / float(len(coverage_scores)) if coverage_scores else 0.0,
            "overall_compliance": sum(compliance_scores) / float(len(compliance_scores)) if compliance_scores else 0.0,
            "drift_findings": len(result.get("drift", [])),
            "batches": len(result.get("batches", [])),
        }
