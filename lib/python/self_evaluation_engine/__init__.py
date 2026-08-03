"""
Self Evaluation Engine — CORE-016

The AI CTO quality assurance layer.

Evaluates every implementation against canonical architecture, repository
standards, and engineering quality.

Public API::

    from python.self_evaluation_engine import SelfEvaluationEngine

    engine = SelfEvaluationEngine(repository="/path/to/repo")
    result = engine.evaluate()
"""

from .engine import EvaluationCoordinator, SelfEvaluationEngine
from .analyzers import (
    ArchitectureComplianceAnalyzer,
    CanonicalComplianceAnalyzer,
    CoverageAnalyzer,
    EvidenceAnalyzer,
    ImprovementAnalyzer,
    RegressionAnalyzer,
    RepositoryComplianceAnalyzer,
)
from .models import (
    ALL_DIMENSIONS,
    DIMENSION_ARCHITECTURE_QUALITY,
    DIMENSION_CANONICAL_COMPLIANCE,
    DIMENSION_CONFIDENCE,
    DIMENSION_DOCUMENTATION_QUALITY,
    DIMENSION_EXECUTION_QUALITY,
    DIMENSION_MAINTAINABILITY,
    DIMENSION_OVERALL,
    DIMENSION_PLANNING_QUALITY,
    DIMENSION_REPOSITORY_HEALTH,
    DIMENSION_TESTING_QUALITY,
    DIMENSION_WORKSPACE_QUALITY,
    EVALUATION_VERSION,
    GATE_BLOCKED,
    GATE_FAILED,
    GATE_MANUAL_REVIEW,
    GATE_PASS,
    GATE_WARNING,
    QUALITY_GATES,
    ArchitectureFinding,
    EvaluationContext,
    EvaluationResult,
    QualityScore,
    RegressionFinding,
)
from .persistence import EvaluationPersistence
from .report import EvaluationReportGenerator
from .scoring import ConfidenceScorer, QualityScorer

__all__ = [
    # Main engine
    "SelfEvaluationEngine",
    "EvaluationCoordinator",
    # Analyzers
    "CanonicalComplianceAnalyzer",
    "ArchitectureComplianceAnalyzer",
    "RepositoryComplianceAnalyzer",
    "RegressionAnalyzer",
    "CoverageAnalyzer",
    "EvidenceAnalyzer",
    "ImprovementAnalyzer",
    # Scorers
    "QualityScorer",
    "ConfidenceScorer",
    # Persistence
    "EvaluationPersistence",
    # Report
    "EvaluationReportGenerator",
    # Version
    "EVALUATION_VERSION",
    # Gate constants
    "GATE_PASS",
    "GATE_WARNING",
    "GATE_FAILED",
    "GATE_BLOCKED",
    "GATE_MANUAL_REVIEW",
    "QUALITY_GATES",
    # Dimension constants
    "DIMENSION_CANONICAL_COMPLIANCE",
    "DIMENSION_ARCHITECTURE_QUALITY",
    "DIMENSION_REPOSITORY_HEALTH",
    "DIMENSION_EXECUTION_QUALITY",
    "DIMENSION_PLANNING_QUALITY",
    "DIMENSION_WORKSPACE_QUALITY",
    "DIMENSION_MAINTAINABILITY",
    "DIMENSION_DOCUMENTATION_QUALITY",
    "DIMENSION_TESTING_QUALITY",
    "DIMENSION_CONFIDENCE",
    "DIMENSION_OVERALL",
    "ALL_DIMENSIONS",
    # Models
    "EvaluationContext",
    "QualityScore",
    "RegressionFinding",
    "ArchitectureFinding",
    "EvaluationResult",
]
