"""
Executive Briefing Engine — Canonical Models
CORE-010A
"""

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Tuple

BRIEFING_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Priority / severity constants
# ---------------------------------------------------------------------------

PRIORITY_CRITICAL = "critical"
PRIORITY_HIGH = "high"
PRIORITY_MEDIUM = "medium"
PRIORITY_LOW = "low"
PRIORITY_BLOCKED = "blocked"
PRIORITY_WAITING = "waiting"
PRIORITY_COMPLETED = "completed"

SEVERITY_CRITICAL = "critical"
SEVERITY_HIGH = "high"
SEVERITY_MEDIUM = "medium"
SEVERITY_LOW = "low"

RISK_ARCHITECTURE = "architecture"
RISK_CANONICAL_DRIFT = "canonical_drift"
RISK_MISSING_COMPONENTS = "missing_components"
RISK_BROKEN_DEPENDENCIES = "broken_dependencies"
RISK_REPOSITORY_INTEGRITY = "repository_integrity"
RISK_REGRESSION = "regression"
RISK_TECHNICAL_DEBT = "technical_debt"


# ---------------------------------------------------------------------------
# ExecutiveRecommendation
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ExecutiveRecommendation:
    """Evidence-based executive recommendation."""

    id: str
    title: str
    description: str
    priority: str
    impact: str
    confidence: float
    required_effort: str  # low | medium | high
    dependencies: Tuple[str, ...]
    affected_components: Tuple[str, ...]
    reasoning: str
    evidence: Tuple[str, ...]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "impact": self.impact,
            "confidence": round(self.confidence, 4),
            "required_effort": self.required_effort,
            "dependencies": list(self.dependencies),
            "affected_components": list(self.affected_components),
            "reasoning": self.reasoning,
            "evidence": list(self.evidence),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ExecutiveRecommendation":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            priority=data.get("priority", PRIORITY_MEDIUM),
            impact=data.get("impact", ""),
            confidence=float(data.get("confidence", 0.5)),
            required_effort=data.get("required_effort", "medium"),
            dependencies=tuple(data.get("dependencies", [])),
            affected_components=tuple(data.get("affected_components", [])),
            reasoning=data.get("reasoning", ""),
            evidence=tuple(data.get("evidence", [])),
        )


# ---------------------------------------------------------------------------
# ExecutiveRisk
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ExecutiveRisk:
    """Detected executive-level risk."""

    id: str
    category: str
    severity: str
    title: str
    description: str
    evidence: Tuple[str, ...]
    affected_components: Tuple[str, ...]
    remediation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
            "evidence": list(self.evidence),
            "affected_components": list(self.affected_components),
            "remediation": self.remediation,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ExecutiveRisk":
        return cls(
            id=data.get("id", ""),
            category=data.get("category", RISK_ARCHITECTURE),
            severity=data.get("severity", SEVERITY_MEDIUM),
            title=data.get("title", ""),
            description=data.get("description", ""),
            evidence=tuple(data.get("evidence", [])),
            affected_components=tuple(data.get("affected_components", [])),
            remediation=data.get("remediation", ""),
        )


# ---------------------------------------------------------------------------
# ExecutivePriorityItem
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ExecutivePriorityItem:
    """A classified work item."""

    id: str
    title: str
    classification: str
    category: str
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "classification": self.classification,
            "category": self.category,
            "rationale": self.rationale,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ExecutivePriorityItem":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            classification=data.get("classification", PRIORITY_MEDIUM),
            category=data.get("category", ""),
            rationale=data.get("rationale", ""),
        )


# ---------------------------------------------------------------------------
# ExecutiveDecision
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ExecutiveDecision:
    """A pending decision requiring owner action."""

    id: str
    title: str
    description: str
    options: Tuple[str, ...]
    recommended_option: str
    impact: str
    urgency: str
    context: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "options": list(self.options),
            "recommended_option": self.recommended_option,
            "impact": self.impact,
            "urgency": self.urgency,
            "context": self.context,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ExecutiveDecision":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            options=tuple(data.get("options", [])),
            recommended_option=data.get("recommended_option", ""),
            impact=data.get("impact", ""),
            urgency=data.get("urgency", PRIORITY_MEDIUM),
            context=data.get("context", ""),
        )


# ---------------------------------------------------------------------------
# OwnerDashboard
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class OwnerDashboard:
    """Concise owner-facing summary dashboard."""

    overall_health: str
    repository_readiness: str
    current_progress: str
    open_risks: int
    recommended_actions: Tuple[str, ...]
    blocked_items: Tuple[str, ...]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_health": self.overall_health,
            "repository_readiness": self.repository_readiness,
            "current_progress": self.current_progress,
            "open_risks": self.open_risks,
            "recommended_actions": list(self.recommended_actions),
            "blocked_items": list(self.blocked_items),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "OwnerDashboard":
        return cls(
            overall_health=data.get("overall_health", "unknown"),
            repository_readiness=data.get("repository_readiness", "unknown"),
            current_progress=data.get("current_progress", ""),
            open_risks=int(data.get("open_risks", 0)),
            recommended_actions=tuple(data.get("recommended_actions", [])),
            blocked_items=tuple(data.get("blocked_items", [])),
        )


# ---------------------------------------------------------------------------
# ExecutiveBriefing
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ExecutiveBriefing:
    """Complete executive briefing produced by CORE-010."""

    briefing_id: str
    generated_at: str
    schema_version: str
    repository: str

    # Status
    executive_summary: str
    current_branch: str
    current_issue: str
    current_pull_request: str
    current_batch: str
    current_milestone: str
    current_epic: str
    current_recommendation: str

    # Health dimensions
    architecture_health: str
    canonical_health: str
    development_health: str
    repository_health: str
    runtime_health: str

    # Intelligence outputs
    recommendations: Tuple[ExecutiveRecommendation, ...]
    critical_risks: Tuple[ExecutiveRisk, ...]
    all_risks: Tuple[ExecutiveRisk, ...]
    pending_decisions: Tuple[ExecutiveDecision, ...]
    priorities: Tuple[ExecutivePriorityItem, ...]

    # Suggested next
    suggested_next_core: str
    suggested_next_batch: str
    suggested_next_pr: str
    estimated_completion: str

    # Dashboard
    owner_dashboard: OwnerDashboard

    def to_dict(self) -> Dict[str, Any]:
        return {
            "briefing_id": self.briefing_id,
            "generated_at": self.generated_at,
            "schema_version": self.schema_version,
            "repository": self.repository,
            "executive_summary": self.executive_summary,
            "current_branch": self.current_branch,
            "current_issue": self.current_issue,
            "current_pull_request": self.current_pull_request,
            "current_batch": self.current_batch,
            "current_milestone": self.current_milestone,
            "current_epic": self.current_epic,
            "current_recommendation": self.current_recommendation,
            "architecture_health": self.architecture_health,
            "canonical_health": self.canonical_health,
            "development_health": self.development_health,
            "repository_health": self.repository_health,
            "runtime_health": self.runtime_health,
            "recommendations": [r.to_dict() for r in self.recommendations],
            "critical_risks": [r.to_dict() for r in self.critical_risks],
            "all_risks": [r.to_dict() for r in self.all_risks],
            "pending_decisions": [d.to_dict() for d in self.pending_decisions],
            "priorities": [p.to_dict() for p in self.priorities],
            "suggested_next_core": self.suggested_next_core,
            "suggested_next_batch": self.suggested_next_batch,
            "suggested_next_pr": self.suggested_next_pr,
            "estimated_completion": self.estimated_completion,
            "owner_dashboard": self.owner_dashboard.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ExecutiveBriefing":
        return cls(
            briefing_id=data.get("briefing_id", ""),
            generated_at=data.get("generated_at", ""),
            schema_version=data.get("schema_version", BRIEFING_VERSION),
            repository=data.get("repository", ""),
            executive_summary=data.get("executive_summary", ""),
            current_branch=data.get("current_branch", ""),
            current_issue=data.get("current_issue", ""),
            current_pull_request=data.get("current_pull_request", ""),
            current_batch=data.get("current_batch", ""),
            current_milestone=data.get("current_milestone", ""),
            current_epic=data.get("current_epic", ""),
            current_recommendation=data.get("current_recommendation", ""),
            architecture_health=data.get("architecture_health", "unknown"),
            canonical_health=data.get("canonical_health", "unknown"),
            development_health=data.get("development_health", "unknown"),
            repository_health=data.get("repository_health", "unknown"),
            runtime_health=data.get("runtime_health", "unknown"),
            recommendations=tuple(
                ExecutiveRecommendation.from_dict(r)
                for r in data.get("recommendations", [])
            ),
            critical_risks=tuple(
                ExecutiveRisk.from_dict(r)
                for r in data.get("critical_risks", [])
            ),
            all_risks=tuple(
                ExecutiveRisk.from_dict(r)
                for r in data.get("all_risks", [])
            ),
            pending_decisions=tuple(
                ExecutiveDecision.from_dict(d)
                for d in data.get("pending_decisions", [])
            ),
            priorities=tuple(
                ExecutivePriorityItem.from_dict(p)
                for p in data.get("priorities", [])
            ),
            suggested_next_core=data.get("suggested_next_core", ""),
            suggested_next_batch=data.get("suggested_next_batch", ""),
            suggested_next_pr=data.get("suggested_next_pr", ""),
            estimated_completion=data.get("estimated_completion", ""),
            owner_dashboard=OwnerDashboard.from_dict(
                data.get("owner_dashboard", {})
            ),
        )
