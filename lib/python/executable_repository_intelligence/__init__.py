"""
Executable Repository Intelligence — CORE-008C

Determines which files participate in runtime execution vs. documentation,
generated artifacts, and informational content.

Builds on top of CORE-008B (SemanticRepositoryEngine) without duplication.

Public API::

    from python.executable_repository_intelligence import ExecutableRepositoryEngine
    result = ExecutableRepositoryEngine(repository="/path").analyze()
"""

from .engine import ExecutableRepositoryEngine
from .file_classifier import FileClassifier
from .runtime_map import RuntimeMapBuilder
from .executable_dep_graph import ExecutableDependencyGraphBuilder
from .injection_safety import InjectionSafetyClassifier
from .zone_classifier import ZoneClassifier
from .recommendations import ExecutableRecommendationEngine
from .persistence import ExecutablePersistence
from .report import ExecutionModelReportGenerator

__all__ = [
    "ExecutableRepositoryEngine",
    "FileClassifier",
    "RuntimeMapBuilder",
    "ExecutableDependencyGraphBuilder",
    "InjectionSafetyClassifier",
    "ZoneClassifier",
    "ExecutableRecommendationEngine",
    "ExecutablePersistence",
    "ExecutionModelReportGenerator",
]
