"""
PCC-02 Transformation.

Executable Transformation anatomy for the AI-Toolkit Epistemic Organism.

This module matures the inherited TransformationLifecycle rather than
creating a parallel Transformation organ.

The model preserves explicit epistemic absence. Unknown, unexecuted,
unverified, or undecided matters are represented as such and are never
silently invented.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Final
import re


ROOT: Final[Path] = Path("work/transformation-evidence")

UNKNOWN: Final[str] = "UNKNOWN"
NOT_EXECUTED: Final[str] = "NOT EXECUTED"
NOT_VERIFIED: Final[str] = "NOT VERIFIED"
NO_OWNER_DECISION: Final[str] = "NO OWNER DECISION RECORDED"

_IDENTIFIER_PATTERN: Final[re.Pattern[str]] = re.compile(r"^TR-\d{6}$")


class TransformationError(ValueError):
    """Raised when Transformation anatomy or lifecycle is invalid."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _require_text(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TransformationError(f"{name} must be non-empty text")
    return value.strip()


def _validate_identifier(identifier: str) -> str:
    if not _IDENTIFIER_PATTERN.fullmatch(identifier):
        raise TransformationError(
            "Transformation identifier must use TR-NNNNNN form"
        )
    return identifier


@dataclass(frozen=True)
class Transformation:
    """
    One meaningful unit of project evolution.

    The twelve epistemic dimensions are:

    1. Need
    2. Research
    3. Hypothesis
    4. Owner Decision
    5. Implementation
    6. Execution
    7. Artifacts / Effects
    8. Evidence
    9. Verification
    10. Knowledge
    11. Evolution
    12. Next Transformation

    Stable identity and lifecycle metadata remain separate from those
    twelve dimensions.
    """

    identifier: str
    need: str
    started_at: str
    status: str

    research: str = UNKNOWN
    hypothesis: str = UNKNOWN
    owner_decision: str = NO_OWNER_DECISION
    implementation: str = UNKNOWN
    execution: str = NOT_EXECUTED
    artifacts_effects: str = UNKNOWN
    evidence: str = UNKNOWN
    verification: str = NOT_VERIFIED
    knowledge: str = UNKNOWN
    evolution: str = UNKNOWN
    next_transformation: str = UNKNOWN

    parent_transformation: str | None = None
    ended_at: str | None = None

    def __post_init__(self) -> None:
        _validate_identifier(self.identifier)
        _require_text("need", self.need)
        _require_text("started_at", self.started_at)
        _require_text("status", self.status)

        if self.parent_transformation is not None:
            _validate_identifier(self.parent_transformation)

    @property
    def dimensions(self) -> tuple[tuple[str, str], ...]:
        """Return the twelve PCC-02 dimensions in epistemic order."""

        return (
            ("Need", self.need),
            ("Research", self.research),
            ("Hypothesis", self.hypothesis),
            ("Owner Decision", self.owner_decision),
            ("Implementation", self.implementation),
            ("Execution", self.execution),
            ("Artifacts / Effects", self.artifacts_effects),
            ("Evidence", self.evidence),
            ("Verification", self.verification),
            ("Knowledge", self.knowledge),
            ("Evolution", self.evolution),
            ("Next Transformation", self.next_transformation),
        )


class TransformationLifecycle:
    """
    Begin and complete Transformations through the inherited executable organ.

    Existing begin()/complete() entry points are preserved.
    """

    def __init__(self, root: Path | None = None):
        self.root = Path(root) if root is not None else ROOT

    def _artifact_path(self, identifier: str) -> Path:
        _validate_identifier(identifier)
        return self.root / f"{identifier}.md"

    def _next_identifier(self) -> str:
        """
        Derive the next local TR-NNNNNN identity from existing evidence.

        Existing Transformation evidence is inspected rather than replacing
        the historical TR identity family with a new namespace.
        """

        self.root.mkdir(parents=True, exist_ok=True)

        highest = 0

        for path in self.root.glob("TR-*.md"):
            match = re.fullmatch(r"TR-(\d{6})\.md", path.name)
            if match:
                highest = max(highest, int(match.group(1)))

        return f"TR-{highest + 1:06d}"

    def _render(self, transformation: Transformation) -> str:
        lines = [
            "# Transformation Evidence",
            "",
            "## Identity",
            "",
            f"Transformation ID: {transformation.identifier}",
            f"Parent Transformation: "
            f"{transformation.parent_transformation or 'NONE'}",
            f"Started: {transformation.started_at}",
            f"Ended: {transformation.ended_at or 'NOT ENDED'}",
            f"Status: {transformation.status}",
            "",
        ]

        for title, value in transformation.dimensions:
            lines.extend(
                [
                    f"## {title}",
                    "",
                    value,
                    "",
                ]
            )

        return "\n".join(lines)

    def _write(self, transformation: Transformation) -> None:
        self.root.mkdir(parents=True, exist_ok=True)

        self._artifact_path(transformation.identifier).write_text(
            self._render(transformation),
            encoding="utf-8",
        )

    def begin(
        self,
        need: str,
        *,
        parent_transformation: str | None = None,
        research: str = UNKNOWN,
        hypothesis: str = UNKNOWN,
        owner_decision: str = NO_OWNER_DECISION,
    ) -> Transformation:
        """
        Begin a Transformation from a concrete Need.

        Information not yet established remains explicit rather than being
        invented.
        """

        need = _require_text("need", need)

        if parent_transformation is not None:
            _validate_identifier(parent_transformation)

        transformation = Transformation(
            identifier=self._next_identifier(),
            need=need,
            started_at=_utc_now(),
            status="RUNNING",
            research=research,
            hypothesis=hypothesis,
            owner_decision=owner_decision,
            parent_transformation=parent_transformation,
        )

        self._write(transformation)
        return transformation

    def complete(
        self,
        transformation: Transformation,
        *,
        implementation: str = UNKNOWN,
        execution: str = NOT_EXECUTED,
        artifacts_effects: str = UNKNOWN,
        evidence: str = UNKNOWN,
        verification: str = NOT_VERIFIED,
        knowledge: str = UNKNOWN,
        evolution: str = UNKNOWN,
        next_transformation: str = UNKNOWN,
    ) -> Transformation:
        """
        Complete a Transformation without manufacturing missing knowledge.

        Completion records the supplied epistemic state. It does not imply
        that execution occurred or verification succeeded.
        """

        if transformation.status != "RUNNING":
            raise TransformationError(
                "Only a RUNNING Transformation may be completed"
            )

        completed = replace(
            transformation,
            status="COMPLETED",
            implementation=implementation,
            execution=execution,
            artifacts_effects=artifacts_effects,
            evidence=evidence,
            verification=verification,
            knowledge=knowledge,
            evolution=evolution,
            next_transformation=next_transformation,
            ended_at=_utc_now(),
        )

        self._write(completed)
        return completed


if __name__ == "__main__":
    lifecycle = TransformationLifecycle()

    tr = lifecycle.begin(
        "Create the first executable lifecycle."
    )

    tr = lifecycle.complete(tr)

    print()
    print("Transformation")
    print(tr.identifier)
    print("Completed.")
