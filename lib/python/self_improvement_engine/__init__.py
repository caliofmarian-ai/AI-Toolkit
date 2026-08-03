"""
Self Improvement Engine — CORE-017

The AI CTO continuous improvement layer.

Continuously analyzes every repository, execution, and evaluation to
determine how AI Toolkit can become a better AI CTO.

Public API::

    from python.self_improvement_engine import SelfImprovementEngine

    engine = SelfImprovementEngine(repository="/path/to/repo")
    result = engine.improve()
"""

from .engine import (
    EvolutionPlanner,
    ImprovementCoordinator,
    OptimizationPlanner,
    SelfImprovementEngine,
)
from .analyzers import CapabilityAnalyzer, PerformanceAnalyzer, TechnicalDebtAnalyzer
from .generators import (
    BatchGenerator,
    CoreProposalEngine,
    IssueGenerator,
    RoadmapEvolutionEngine,
)
from .models import (
    EFFORT_HIGH,
    EFFORT_LOW,
    EFFORT_MEDIUM,
    IMPROVEMENT_VERSION,
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_LOW,
    PRIORITY_MEDIUM,
    CapabilityGap,
    CoreProposal,
    OptimizationPlan,
    PerformanceMetric,
    ProposedBatch,
    ProposedIssue,
    RoadmapUpdate,
    TechnicalDebt,
)
from .persistence import ImprovementPersistence
from .report import ImprovementReportGenerator

__all__ = [
    # Main engine
    "SelfImprovementEngine",
    "ImprovementCoordinator",
    "OptimizationPlanner",
    "EvolutionPlanner",
    # Analyzers
    "TechnicalDebtAnalyzer",
    "PerformanceAnalyzer",
    "CapabilityAnalyzer",
    # Generators
    "IssueGenerator",
    "BatchGenerator",
    "CoreProposalEngine",
    "RoadmapEvolutionEngine",
    # Persistence
    "ImprovementPersistence",
    # Report
    "ImprovementReportGenerator",
    # Version
    "IMPROVEMENT_VERSION",
    # Priority constants
    "PRIORITY_CRITICAL",
    "PRIORITY_HIGH",
    "PRIORITY_MEDIUM",
    "PRIORITY_LOW",
    # Effort constants
    "EFFORT_LOW",
    "EFFORT_MEDIUM",
    "EFFORT_HIGH",
    # Models
    "TechnicalDebt",
    "PerformanceMetric",
    "CapabilityGap",
    "ProposedIssue",
    "ProposedBatch",
    "CoreProposal",
    "RoadmapUpdate",
    "OptimizationPlan",
]
