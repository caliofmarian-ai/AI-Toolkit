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
    def semantic_title(self) -> str:
        """
        Return the human-readable semantic identity of the Transformation.

        Need already states what this Transformation is about. Reusing it
        avoids introducing a second mutable source of semantic truth.
        """

        return self.need

    @property
    def human_identity(self) -> str:
        """
        Combine stable machine identity with human-readable meaning.
        """

        return f"{self.identifier} — {self.semantic_title}"

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
            f"Transformation: {transformation.human_identity}",
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

    @staticmethod
    def _parse_artifact(text: str) -> dict[str, str]:
        """
        Recover semantic sections from a Transformation evidence artifact.

        The Markdown representation remains the persisted representation;
        recovery does not introduce a parallel persistence format.
        """

        sections: dict[str, list[str]] = {}
        current: str | None = None

        for raw_line in text.splitlines():
            if raw_line.startswith("## "):
                current = raw_line[3:].strip()
                sections[current] = []
                continue

            if current is not None:
                sections[current].append(raw_line)

        def body(name: str) -> str:
            if name not in sections:
                raise TransformationError(
                    f"Transformation artifact missing section: {name}"
                )

            value = "\n".join(sections[name]).strip()

            if not value:
                raise TransformationError(
                    f"Transformation artifact has empty section: {name}"
                )

            return value

        identity_lines = [
            line.strip()
            for line in sections.get("Identity", [])
            if line.strip()
        ]

        identity: dict[str, str] = {}

        for line in identity_lines:
            if ": " not in line:
                raise TransformationError(
                    "Malformed Transformation identity metadata"
                )

            key, value = line.split(": ", 1)
            identity[key] = value

        required_identity = {
            "Transformation ID",
            "Parent Transformation",
            "Started",
            "Ended",
            "Status",
        }

        if not required_identity.issubset(identity):
            missing = sorted(required_identity - set(identity))
            raise TransformationError(
                "Transformation identity metadata missing: "
                + ", ".join(missing)
            )

        result = {
            "identifier": identity["Transformation ID"],
            "parent_transformation": identity["Parent Transformation"],
            "started_at": identity["Started"],
            "ended_at": identity["Ended"],
            "status": identity["Status"],
            "need": body("Need"),
            "research": body("Research"),
            "hypothesis": body("Hypothesis"),
            "owner_decision": body("Owner Decision"),
            "implementation": body("Implementation"),
            "execution": body("Execution"),
            "artifacts_effects": body("Artifacts / Effects"),
            "evidence": body("Evidence"),
            "verification": body("Verification"),
            "knowledge": body("Knowledge"),
            "evolution": body("Evolution"),
            "next_transformation": body("Next Transformation"),
        }

        return result

    def get(self, identifier: str) -> Transformation:
        """
        Recover a persisted Transformation by stable identity.

        Recovery reconstructs the immutable epistemic value from its
        persisted human-readable evidence representation.
        """

        path = self._artifact_path(identifier)

        if not path.is_file():
            raise TransformationError(
                f"Transformation does not exist: {identifier}"
            )

        data = self._parse_artifact(
            path.read_text(encoding="utf-8")
        )

        if data["identifier"] != identifier:
            raise TransformationError(
                "Transformation artifact identity does not match "
                "requested identity"
            )

        parent = data["parent_transformation"]
        ended = data["ended_at"]

        return Transformation(
            identifier=data["identifier"],
            need=data["need"],
            started_at=data["started_at"],
            status=data["status"],
            research=data["research"],
            hypothesis=data["hypothesis"],
            owner_decision=data["owner_decision"],
            implementation=data["implementation"],
            execution=data["execution"],
            artifacts_effects=data["artifacts_effects"],
            evidence=data["evidence"],
            verification=data["verification"],
            knowledge=data["knowledge"],
            evolution=data["evolution"],
            next_transformation=data["next_transformation"],
            parent_transformation=(
                None if parent == "NONE" else parent
            ),
            ended_at=(
                None if ended == "NOT ENDED" else ended
            ),
        )

    def list_transformations(self) -> tuple[Transformation, ...]:
        """
        Recover all locally persisted Transformations in stable identity order.

        A malformed artifact matching the TR-NNNNNN identity family is
        surfaced as an error rather than silently omitted.
        """

        if not self.root.exists():
            return ()

        identities: list[str] = []

        for path in self.root.glob("TR-*.md"):
            match = re.fullmatch(r"TR-(\d{6})\.md", path.name)

            if match:
                identities.append(f"TR-{match.group(1)}")

        identities.sort()

        return tuple(
            self.get(identifier)
            for identifier in identities
        )

    def children(
        self,
        identifier: str,
    ) -> tuple[Transformation, ...]:
        """
        Return locally persisted direct descendants of identifier.

        The parent identity itself may refer to a Transformation whose
        artifact is external or no longer locally available. This preserves
        the established Transformation reference contract.
        """

        _validate_identifier(identifier)

        return tuple(
            transformation
            for transformation in self.list_transformations()
            if transformation.parent_transformation == identifier
        )

    def lineage(
        self,
        identifier: str,
    ) -> tuple[Transformation, ...]:
        """
        Reconstruct locally demonstrable ancestry from ancestor to current.

        Parent references are allowed to exist without a local parent
        artifact. However, lineage reconstruction cannot invent the missing
        ancestor: traversal fails explicitly when required evidence is absent.

        Cycles are rejected explicitly.
        """

        current = self.get(identifier)
        reverse_chain: list[Transformation] = []
        visited: set[str] = set()

        while True:
            if current.identifier in visited:
                raise TransformationError(
                    "Transformation lineage contains a cycle"
                )

            visited.add(current.identifier)
            reverse_chain.append(current)

            parent = current.parent_transformation

            if parent is None:
                break

            parent_path = self._artifact_path(parent)

            if not parent_path.is_file():
                raise TransformationError(
                    "Transformation lineage is incomplete; "
                    f"parent artifact is not locally available: {parent}"
                )

            current = self.get(parent)

        reverse_chain.reverse()

        return tuple(reverse_chain)

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
