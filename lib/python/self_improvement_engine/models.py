"""
Self Improvement Engine — Canonical Models
CORE-017A

All improvement artifacts are deterministic, serialisable, and versioned.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

IMPROVEMENT_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Priority constants
# ---------------------------------------------------------------------------

PRIORITY_CRITICAL = "critical"
PRIORITY_HIGH = "high"
PRIORITY_MEDIUM = "medium"
PRIORITY_LOW = "low"

# ---------------------------------------------------------------------------
# Effort constants
# ---------------------------------------------------------------------------

EFFORT_LOW = "low"
EFFORT_MEDIUM = "medium"
EFFORT_HIGH = "high"


# ---------------------------------------------------------------------------
# TechnicalDebt
# ---------------------------------------------------------------------------

@dataclass
class TechnicalDebt:
    """A single detected technical debt item."""

    debt_id: str
    category: str
    component: str
    description: str
    severity: str
    estimated_effort: str
    evidence: Dict[str, Any]
    recommendation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "debt_id": self.debt_id,
            "category": self.category,
            "component": self.component,
            "description": self.description,
            "severity": self.severity,
            "estimated_effort": self.estimated_effort,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
        }


# ---------------------------------------------------------------------------
# PerformanceMetric
# ---------------------------------------------------------------------------

@dataclass
class PerformanceMetric:
    """A single measured performance metric."""

    metric_id: str
    name: str
    value: float
    unit: str
    baseline: float
    trend: str
    evidence: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_id": self.metric_id,
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "baseline": self.baseline,
            "trend": self.trend,
            "evidence": self.evidence,
        }


# ---------------------------------------------------------------------------
# CapabilityGap
# ---------------------------------------------------------------------------

@dataclass
class CapabilityGap:
    """A missing capability detected in AI Toolkit."""

    gap_id: str
    category: str
    description: str
    priority: str
    evidence: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gap_id": self.gap_id,
            "category": self.category,
            "description": self.description,
            "priority": self.priority,
            "evidence": self.evidence,
        }


# ---------------------------------------------------------------------------
# ProposedIssue
# ---------------------------------------------------------------------------

@dataclass
class ProposedIssue:
    """An automatically generated Issue proposal."""

    issue_id: str
    title: str
    description: str
    objective: str
    motivation: str
    dependencies: List[str]
    acceptance_criteria: List[str]
    priority: str
    estimated_effort: str
    estimated_risk: str
    affected_components: List[str]
    canonical_references: List[str]
    evidence: Dict[str, Any]
    implementation_strategy: str
    validation_strategy: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "issue_id": self.issue_id,
            "title": self.title,
            "description": self.description,
            "objective": self.objective,
            "motivation": self.motivation,
            "dependencies": self.dependencies,
            "acceptance_criteria": self.acceptance_criteria,
            "priority": self.priority,
            "estimated_effort": self.estimated_effort,
            "estimated_risk": self.estimated_risk,
            "affected_components": self.affected_components,
            "canonical_references": self.canonical_references,
            "evidence": self.evidence,
            "implementation_strategy": self.implementation_strategy,
            "validation_strategy": self.validation_strategy,
        }


# ---------------------------------------------------------------------------
# ProposedBatch
# ---------------------------------------------------------------------------

@dataclass
class ProposedBatch:
    """An automatically generated Batch proposal."""

    batch_id: str
    title: str
    objectives: List[str]
    issue_ids: List[str]
    dependencies: List[str]
    execution_order: List[str]
    acceptance_criteria: List[str]
    regression_strategy: str
    validation_strategy: str
    owner_approval_required: bool
    evidence: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "batch_id": self.batch_id,
            "title": self.title,
            "objectives": self.objectives,
            "issue_ids": self.issue_ids,
            "dependencies": self.dependencies,
            "execution_order": self.execution_order,
            "acceptance_criteria": self.acceptance_criteria,
            "regression_strategy": self.regression_strategy,
            "validation_strategy": self.validation_strategy,
            "owner_approval_required": self.owner_approval_required,
            "evidence": self.evidence,
        }


# ---------------------------------------------------------------------------
# CoreProposal
# ---------------------------------------------------------------------------

@dataclass
class CoreProposal:
    """A proposed new CORE engine."""

    proposal_id: str
    core_id: str
    problem_statement: str
    current_limitation: str
    architectural_motivation: str
    expected_benefits: List[str]
    affected_engines: List[str]
    required_changes: List[str]
    estimated_complexity: str
    implementation_order: int
    regression_risk: str
    canonical_impact: str
    roadmap_position: str
    evidence: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "core_id": self.core_id,
            "problem_statement": self.problem_statement,
            "current_limitation": self.current_limitation,
            "architectural_motivation": self.architectural_motivation,
            "expected_benefits": self.expected_benefits,
            "affected_engines": self.affected_engines,
            "required_changes": self.required_changes,
            "estimated_complexity": self.estimated_complexity,
            "implementation_order": self.implementation_order,
            "regression_risk": self.regression_risk,
            "canonical_impact": self.canonical_impact,
            "roadmap_position": self.roadmap_position,
            "evidence": self.evidence,
        }


# ---------------------------------------------------------------------------
# RoadmapUpdate
# ---------------------------------------------------------------------------

@dataclass
class RoadmapUpdate:
    """A recommended roadmap update."""

    update_id: str
    category: str
    description: str
    reason: str
    priority: str
    owner_approval_required: bool
    evidence: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "update_id": self.update_id,
            "category": self.category,
            "description": self.description,
            "reason": self.reason,
            "priority": self.priority,
            "owner_approval_required": self.owner_approval_required,
            "evidence": self.evidence,
        }


# ---------------------------------------------------------------------------
# OptimizationPlan
# ---------------------------------------------------------------------------

@dataclass
class OptimizationPlan:
    """A structured optimization plan."""

    plan_id: str
    generated_at: str
    repository: str
    schema_version: str
    technical_debt_items: List[TechnicalDebt] = field(default_factory=list)
    performance_metrics: List[PerformanceMetric] = field(default_factory=list)
    capability_gaps: List[CapabilityGap] = field(default_factory=list)
    proposed_issues: List[ProposedIssue] = field(default_factory=list)
    proposed_batches: List[ProposedBatch] = field(default_factory=list)
    core_proposals: List[CoreProposal] = field(default_factory=list)
    roadmap_updates: List[RoadmapUpdate] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "generated_at": self.generated_at,
            "repository": self.repository,
            "schema_version": self.schema_version,
            "technical_debt_count": len(self.technical_debt_items),
            "performance_metric_count": len(self.performance_metrics),
            "capability_gap_count": len(self.capability_gaps),
            "proposed_issue_count": len(self.proposed_issues),
            "proposed_batch_count": len(self.proposed_batches),
            "core_proposal_count": len(self.core_proposals),
            "roadmap_update_count": len(self.roadmap_updates),
            "technical_debt": [d.to_dict() for d in self.technical_debt_items],
            "performance_metrics": [m.to_dict() for m in self.performance_metrics],
            "capability_gaps": [g.to_dict() for g in self.capability_gaps],
            "proposed_issues": [i.to_dict() for i in self.proposed_issues],
            "proposed_batches": [b.to_dict() for b in self.proposed_batches],
            "core_proposals": [c.to_dict() for c in self.core_proposals],
            "roadmap_updates": [r.to_dict() for r in self.roadmap_updates],
            "summary": self.summary,
        }
