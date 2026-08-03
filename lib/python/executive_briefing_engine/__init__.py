"""
Executive Briefing Engine — CORE-010

Primary interface between AI CTO and the Owner.

Transforms repository state into executive decisions, priorities,
and recommendations using existing CORE engine intelligence.
"""

from .engine import ExecutiveBriefingEngine
from .generator import ExecutiveBriefingGenerator
from .recommendation_engine import ExecutiveRecommendationEngine
from .priority_engine import ExecutivePriorityEngine
from .risk_analyzer import ExecutiveRiskAnalyzer
from .decision_tracker import ExecutiveDecisionTracker
from .insight_generator import ExecutiveInsightGenerator
from .persistence import ExecutiveBriefingPersistence
from .models import (
    BRIEFING_VERSION,
    ExecutiveBriefing,
    ExecutiveRecommendation,
    ExecutiveRisk,
    ExecutivePriorityItem,
    ExecutiveDecision,
    OwnerDashboard,
)

__all__ = [
    "BRIEFING_VERSION",
    "ExecutiveBriefingEngine",
    "ExecutiveBriefingGenerator",
    "ExecutiveRecommendationEngine",
    "ExecutivePriorityEngine",
    "ExecutiveRiskAnalyzer",
    "ExecutiveDecisionTracker",
    "ExecutiveInsightGenerator",
    "ExecutiveBriefingPersistence",
    "ExecutiveBriefing",
    "ExecutiveRecommendation",
    "ExecutiveRisk",
    "ExecutivePriorityItem",
    "ExecutiveDecision",
    "OwnerDashboard",
]
