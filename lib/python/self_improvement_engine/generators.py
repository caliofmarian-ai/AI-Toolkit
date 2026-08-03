"""
Self Improvement Engine — Issue, Batch and CORE Proposal Generators
CORE-017C

Generates actionable Issues, Batches and CORE proposals from
improvement analysis findings.

Proposals always require Owner approval before execution.
"""

import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List

from .models import (
    EFFORT_LOW,
    EFFORT_MEDIUM,
    EFFORT_HIGH,
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    PRIORITY_LOW,
    CapabilityGap,
    CoreProposal,
    ProposedBatch,
    ProposedIssue,
    TechnicalDebt,
)


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _short_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:6].upper()


class IssueGenerator:
    """
    CORE-017C — Issue Generator.

    Generates Issues from technical debt, capability gaps,
    and evaluation findings.
    """

    def generate_from_debt(self, debt_items: List[TechnicalDebt]) -> List[ProposedIssue]:
        issues: List[ProposedIssue] = []
        for debt in debt_items:
            issue_id = f"ISS-{_short_hash(debt.debt_id)}"
            issues.append(
                ProposedIssue(
                    issue_id=issue_id,
                    title=f"Fix technical debt: {debt.component}",
                    description=debt.description,
                    objective=f"Eliminate {debt.category} debt in {debt.component}",
                    motivation=debt.recommendation,
                    dependencies=[],
                    acceptance_criteria=[
                        f"{debt.component} no longer contains {debt.category}",
                        "All existing tests continue to pass",
                    ],
                    priority=debt.severity if debt.severity in (
                        PRIORITY_CRITICAL, PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW
                    ) else PRIORITY_LOW,
                    estimated_effort=debt.estimated_effort,
                    estimated_risk="low",
                    affected_components=[debt.component],
                    canonical_references=[],
                    evidence=debt.evidence,
                    implementation_strategy=debt.recommendation,
                    validation_strategy="Run full regression test suite after changes.",
                )
            )
        return issues

    def generate_from_gaps(self, gaps: List[CapabilityGap]) -> List[ProposedIssue]:
        issues: List[ProposedIssue] = []
        for gap in gaps:
            issue_id = f"ISS-{_short_hash(gap.gap_id)}"
            issues.append(
                ProposedIssue(
                    issue_id=issue_id,
                    title=f"Add missing capability: {gap.description}",
                    description=gap.description,
                    objective=f"Implement missing {gap.category}",
                    motivation=(
                        "This capability is required for a complete AI CTO implementation."
                    ),
                    dependencies=[],
                    acceptance_criteria=[
                        f"{gap.gap_id} is resolved",
                        "All existing tests continue to pass",
                        "New tests cover the added capability",
                    ],
                    priority=gap.priority,
                    estimated_effort=EFFORT_MEDIUM,
                    estimated_risk="low",
                    affected_components=[gap.category],
                    canonical_references=[],
                    evidence=gap.evidence,
                    implementation_strategy=f"Implement the missing {gap.category}.",
                    validation_strategy="Verify the capability is present and tested.",
                )
            )
        return issues


class BatchGenerator:
    """
    CORE-017C — Batch Generator.

    Groups related Issues into executable Batches.
    Batches always require Owner approval before execution.
    """

    def generate(self, issues: List[ProposedIssue]) -> List[ProposedBatch]:
        if not issues:
            return []

        batches: List[ProposedBatch] = []

        # Group by category (priority)
        by_priority: Dict[str, List[ProposedIssue]] = {}
        for issue in issues:
            by_priority.setdefault(issue.priority, []).append(issue)

        priority_order = [PRIORITY_CRITICAL, PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW]
        for priority in priority_order:
            group = by_priority.get(priority, [])
            if not group:
                continue
            batch_id = f"BATCH-IMP-{_short_hash(priority + str(len(group)))}"
            batches.append(
                ProposedBatch(
                    batch_id=batch_id,
                    title=f"Improvement Batch: {priority.upper()} priority issues",
                    objectives=[i.objective for i in group],
                    issue_ids=[i.issue_id for i in group],
                    dependencies=[],
                    execution_order=[i.issue_id for i in group],
                    acceptance_criteria=[
                        "All issues in the batch are resolved",
                        "All regression tests pass",
                        "No new technical debt introduced",
                    ],
                    regression_strategy="Run full test suite before and after batch execution.",
                    validation_strategy="Run `ai evaluate` after batch completion.",
                    owner_approval_required=True,
                    evidence={"issue_count": len(group), "priority": priority},
                )
            )

        return batches


class CoreProposalEngine:
    """
    CORE-017C — CORE Proposal Engine.

    Generates new CORE proposals when justified by analysis findings.
    Never generates duplicate COREs.
    """

    # COREs that are already documented/implemented
    _EXISTING_CORES = {
        "CORE-007", "CORE-008A", "CORE-008B", "CORE-008C",
        "CORE-009", "CORE-010", "CORE-011", "CORE-012",
        "CORE-013", "CORE-014", "CORE-015", "CORE-016", "CORE-017",
    }

    def generate(
        self,
        capability_gaps: List[CapabilityGap],
        evaluation_score: float,
    ) -> List[CoreProposal]:
        """
        Generate CORE proposals only when the evidence justifies them.

        Does not propose COREs that already exist.
        Only proposes when evaluation_score indicates real gaps.
        """
        proposals: List[CoreProposal] = []

        # Only propose new COREs if there are significant missing capabilities
        significant_gaps = [g for g in capability_gaps if g.priority in (PRIORITY_CRITICAL, PRIORITY_HIGH)]
        if not significant_gaps or evaluation_score > 0.85:
            return proposals

        # Example: propose CORE-018 for automated testing orchestration if coverage is low
        coverage_gaps = [g for g in significant_gaps if "test" in g.description.lower()]
        if coverage_gaps and "CORE-018" not in self._EXISTING_CORES:
            proposal_id = f"PROP-{_short_hash('CORE-018-testing')}"
            proposals.append(
                CoreProposal(
                    proposal_id=proposal_id,
                    core_id="CORE-018",
                    problem_statement=(
                        "AI Toolkit lacks automated test orchestration capability."
                    ),
                    current_limitation=(
                        "Tests must be manually triggered. No automated CI integration exists."
                    ),
                    architectural_motivation=(
                        "An autonomous AI CTO requires automated test validation "
                        "as part of the execution lifecycle."
                    ),
                    expected_benefits=[
                        "Automated regression detection",
                        "Continuous quality assurance",
                        "Reduced manual testing burden",
                    ],
                    affected_engines=[
                        "autonomous_execution_engine",
                        "self_evaluation_engine",
                    ],
                    required_changes=[
                        "Implement test orchestration engine",
                        "Integrate with execution pipeline",
                        "Expose `ai test` CLI command",
                    ],
                    estimated_complexity=EFFORT_MEDIUM,
                    implementation_order=18,
                    regression_risk="low",
                    canonical_impact="Extends AI CTO with test automation authority.",
                    roadmap_position="after CORE-017",
                    evidence={
                        "triggered_by": [g.gap_id for g in coverage_gaps],
                        "evaluation_score": evaluation_score,
                    },
                )
            )

        return proposals


class RoadmapEvolutionEngine:
    """
    CORE-017C — Roadmap Evolution Engine.

    Recommends roadmap updates based on analysis findings.
    Never rewrites the roadmap automatically — Owner approval is required.
    """

    def generate_updates(
        self,
        capability_gaps: List[CapabilityGap],
        technical_debt: List[TechnicalDebt],
        evaluation_score: float,
    ) -> List[Any]:
        from .models import RoadmapUpdate
        updates: List[RoadmapUpdate] = []

        if evaluation_score < 0.7:
            update_id = f"RU-{_short_hash('quality-improvement')}"
            updates.append(
                RoadmapUpdate(
                    update_id=update_id,
                    category="quality_improvement",
                    description=(
                        f"Overall engineering quality ({evaluation_score:.0%}) is below target (70%). "
                        "Add a quality improvement milestone to the roadmap."
                    ),
                    reason=f"Evaluation score {evaluation_score:.0%} is below threshold.",
                    priority=PRIORITY_HIGH,
                    owner_approval_required=True,
                    evidence={"evaluation_score": evaluation_score},
                )
            )

        high_debt = [d for d in technical_debt if d.severity in ("high", "critical")]
        if high_debt:
            update_id = f"RU-{_short_hash('debt-reduction')}"
            updates.append(
                RoadmapUpdate(
                    update_id=update_id,
                    category="technical_debt",
                    description=(
                        f"Detected {len(high_debt)} high-severity technical debt item(s). "
                        "Consider adding a debt reduction milestone."
                    ),
                    reason=f"{len(high_debt)} high-severity debt items detected.",
                    priority=PRIORITY_MEDIUM,
                    owner_approval_required=True,
                    evidence={"debt_count": len(high_debt)},
                )
            )

        high_gaps = [g for g in capability_gaps if g.priority in (PRIORITY_CRITICAL, PRIORITY_HIGH)]
        if high_gaps:
            update_id = f"RU-{_short_hash('capability-gap')}"
            updates.append(
                RoadmapUpdate(
                    update_id=update_id,
                    category="capability_gap",
                    description=(
                        f"Detected {len(high_gaps)} high-priority capability gap(s). "
                        "Update roadmap to include missing capabilities."
                    ),
                    reason=f"{len(high_gaps)} high-priority capability gaps detected.",
                    priority=PRIORITY_HIGH,
                    owner_approval_required=True,
                    evidence={"gap_ids": [g.gap_id for g in high_gaps]},
                )
            )

        return updates
