"""
AI CTO Integration Scanner Engine — CORE-008A / CORE-008B

Orchestrates the full integration scan pipeline:
  WorkspaceIndex → Detectors → CanonicalIntelligence → Scoring
  → SemanticRepositoryIntelligence → Report
"""

from pathlib import Path

from python.workspace_index import WorkspaceIndexBuilder
from python.batch_planner import BatchPlanner
from python.canonical_repository import CanonicalRepository
from python.canonical_intelligence.engine import CanonicalIntelligenceEngine
from python.compliance_engine import ComplianceEngine
from python.coverage_engine import CoverageEngine
from python.drift_engine import DriftEngine
from python.knowledge_graph import CanonicalKnowledgeGraphBuilder
from python.reporting_engine import ReportingEngine
from python.semantic_matching import SemanticMatcher
from python.semantic_repository_intelligence import SemanticRepositoryEngine

from .detectors import (
    TelegramDetector,
    OwnerControlDetector,
    RuntimeDetector,
    StateDetector,
    ConfigurationDetector,
    CanonicalDetector,
    ProjectMemoryDetector,
)
from .scoring import ReadinessScorer
from .report import AICTOReportGenerator


class AICTOScannerEngine:
    """
    AI CTO Integration Scanner.

    Inspects an arbitrary software repository and produces an
    AI_CTO_INTEGRATION_REPORT.md covering all architectural dimensions.
    """

    _DETECTORS = [
        TelegramDetector(),
        OwnerControlDetector(),
        RuntimeDetector(),
        StateDetector(),
        ConfigurationDetector(),
        CanonicalDetector(),
        ProjectMemoryDetector(),
    ]

    def __init__(self, repository=".", output_dir=None):
        self.root = Path(repository).resolve()
        self.output_dir = Path(output_dir).resolve() if output_dir else Path(".").resolve()

    def scan(self):
        """
        Execute the full scan pipeline and return the complete result dict.
        """
        # ------------------------------------------------------------------
        # Phase 1 — Workspace index (CORE-007 reuse)
        # ------------------------------------------------------------------
        index = WorkspaceIndexBuilder(self.root).build()

        # ------------------------------------------------------------------
        # Phase 2 — Component detection
        # ------------------------------------------------------------------
        detection_results = {}
        for detector in self._DETECTORS:
            result = detector.detect(index, self.root)
            detection_results[result.category] = result

        detection_data = {
            cat: result.to_dict()
            for cat, result in detection_results.items()
        }

        # ------------------------------------------------------------------
        # Phase 3 — Canonical intelligence (CORE-007 reuse)
        # ------------------------------------------------------------------
        canonical_stats = None
        canonical_reports = None
        canonical_docs_path = self.root / "docs" / "canonical"

        if canonical_docs_path.is_dir() and any(canonical_docs_path.glob("CANON-*.md")):
            try:
                canonical_stats, canonical_reports = self._run_canonical_intelligence(index, canonical_docs_path)
            except Exception:
                canonical_stats = None
                canonical_reports = None

        # ------------------------------------------------------------------
        # Phase 4 — Readiness scoring
        # ------------------------------------------------------------------
        scorer = ReadinessScorer()
        scores = scorer.compute(detection_results, canonical_stats)

        # ------------------------------------------------------------------
        # Phase 5 — Assemble result
        # ------------------------------------------------------------------
        scan_result = {
            "repository": str(self.root),
            "repository_name": self.root.name,
            "detection": detection_data,
            "canonical_stats": canonical_stats or {},
            "canonical_reports": canonical_reports or {},
            "scores": scores,
            "workspace": {
                "total_files": index.statistics.total_files,
                "total_directories": index.statistics.total_directories,
            },
        }

        # ------------------------------------------------------------------
        # Phase 6 — Semantic repository intelligence (CORE-008B)
        # ------------------------------------------------------------------
        semantic_result = None
        try:
            semantic_engine = SemanticRepositoryEngine(
                repository=str(self.root),
                workspace_index=index,
                persist=True,
            )
            semantic_result = semantic_engine.analyze()
        except Exception:
            semantic_result = None

        scan_result["semantic"] = semantic_result or {}

        # ------------------------------------------------------------------
        # Phase 7 — Report generation
        # ------------------------------------------------------------------
        report_path = self.output_dir / "AI_CTO_INTEGRATION_REPORT.md"
        generator = AICTOReportGenerator()
        generator.generate(scan_result, report_path)
        scan_result["report_path"] = str(report_path)

        return scan_result

    def _run_canonical_intelligence(self, workspace_index, canonical_docs_path):
        """Run the CORE-007 canonical intelligence pipeline on the target repo."""
        canonical_repo = CanonicalRepository.load_from_directory(canonical_docs_path)
        if not canonical_repo.all_documents():
            return None, None

        graph = CanonicalKnowledgeGraphBuilder().build(canonical_repo)

        matcher = SemanticMatcher(self.root, workspace_index=workspace_index)
        matches = matcher.match_all(canonical_repo)

        coverage_engine = CoverageEngine(self.root, workspace_index=workspace_index)
        coverage = coverage_engine.compute(canonical_repo, matches)

        compliance_engine = ComplianceEngine(self.root, workspace_index=workspace_index)
        compliance = compliance_engine.evaluate(canonical_repo, matches, coverage)

        drift_engine = DriftEngine(self.root, workspace_index=workspace_index)
        findings = drift_engine.detect(canonical_repo, matches, coverage)

        planner = BatchPlanner()
        batches = planner.generate(canonical_repo, findings, coverage)

        reporter = ReportingEngine()
        reports = reporter.generate(canonical_repo, graph, matches, coverage, compliance, findings, batches)

        intel_engine = CanonicalIntelligenceEngine.__new__(CanonicalIntelligenceEngine)
        stats = intel_engine.statistics({
            "canonical_repository": canonical_repo,
            "graph": graph,
            "coverage": coverage,
            "compliance": compliance,
            "drift": findings,
            "batches": batches,
        })

        return stats, reports.get("markdown", {})


# Backward-compatible public alias.
AICTOScanner = AICTOScannerEngine
