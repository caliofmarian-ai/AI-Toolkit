"""
Semantic Repository Intelligence — CORE-008B

Upgrades AI CTO from a pattern-based repository scanner into a semantic
software intelligence platform.

Public API::

    from python.semantic_repository_intelligence import SemanticRepositoryEngine
    result = SemanticRepositoryEngine(repository="/path").analyze()
"""

from .engine import SemanticRepositoryEngine
from .ast_analyzer import ASTAnalyzer
from .import_graph import ImportGraphBuilder
from .call_graph import CallGraphBuilder
from .dependency_graph import DependencyGraphBuilder
from .architecture_graph import ArchitectureGraphBuilder
from .injection_point_analyzer import InjectionPointAnalyzer
from .relationship_resolver import RelationshipResolver
from .confidence_engine import ConfidenceEngine
from .recommendation_engine import SemanticRecommendationEngine
from .persistence import SemanticPersistence

__all__ = [
    "SemanticRepositoryEngine",
    "ASTAnalyzer",
    "ImportGraphBuilder",
    "CallGraphBuilder",
    "DependencyGraphBuilder",
    "ArchitectureGraphBuilder",
    "InjectionPointAnalyzer",
    "RelationshipResolver",
    "ConfidenceEngine",
    "SemanticRecommendationEngine",
    "SemanticPersistence",
]
