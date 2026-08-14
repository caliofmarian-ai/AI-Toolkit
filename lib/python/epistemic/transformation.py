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
class EpistemicReference:
    """
    One explicit relation from a Transformation to another epistemic artifact.

    The reference maps identity, meaning, relation, and resolvable location.
    It does not copy the target artifact and does not claim that the target
    belongs to an organ that has not yet been implemented.
    """

    relation: str
    target_identity: str
    target_title: str
    target_reference: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "relation",
            _require_text("relation", self.relation),
        )
        object.__setattr__(
            self,
            "target_identity",
            _require_text("target_identity", self.target_identity),
        )
        object.__setattr__(
            self,
            "target_title",
            _require_text("target_title", self.target_title),
        )
        object.__setattr__(
            self,
            "target_reference",
            _require_text("target_reference", self.target_reference),
        )

    @property
    def human_identity(self) -> str:
        return f"{self.target_identity} — {self.target_title}"


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
    relations: tuple[EpistemicReference, ...] = ()

    def __post_init__(self) -> None:
        _validate_identifier(self.identifier)
        _require_text("need", self.need)
        _require_text("started_at", self.started_at)
        _require_text("status", self.status)

        if self.parent_transformation is not None:
            _validate_identifier(self.parent_transformation)

        if not isinstance(self.relations, tuple):
            raise TransformationError(
                "relations must be an immutable tuple"
            )

        if not all(
            isinstance(reference, EpistemicReference)
            for reference in self.relations
        ):
            raise TransformationError(
                "relations must contain EpistemicReference values"
            )

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
            "## Epistemic Relations",
            "",
        ]

        if transformation.relations:
            for reference in transformation.relations:
                lines.extend(
                    [
                        f"- Relation: {reference.relation}",
                        f"  Target: {reference.human_identity}",
                        f"  Reference: {reference.target_reference}",
                    ]
                )
        else:
            lines.append("NONE")

        lines.append("")

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

        relation_lines = [
            line.rstrip()
            for line in sections.get("Epistemic Relations", [])
            if line.strip()
        ]

        relations: list[EpistemicReference] = []

        if relation_lines and relation_lines != ["NONE"]:
            current_relation: dict[str, str] = {}

            for line in relation_lines:
                stripped = line.strip()

                if stripped.startswith("- Relation: "):
                    if current_relation:
                        raise TransformationError(
                            "Malformed epistemic relation block"
                        )

                    current_relation["relation"] = stripped[
                        len("- Relation: "):
                    ]

                elif stripped.startswith("Target: "):
                    target = stripped[len("Target: "):]

                    if " — " not in target:
                        raise TransformationError(
                            "Epistemic relation Target must contain "
                            "identity and semantic title"
                        )

                    target_identity, target_title = target.split(
                        " — ",
                        1,
                    )

                    current_relation["target_identity"] = target_identity
                    current_relation["target_title"] = target_title

                elif stripped.startswith("Reference: "):
                    current_relation["target_reference"] = stripped[
                        len("Reference: "):
                    ]

                    required = {
                        "relation",
                        "target_identity",
                        "target_title",
                        "target_reference",
                    }

                    if not required.issubset(current_relation):
                        raise TransformationError(
                            "Incomplete epistemic relation block"
                        )

                    relations.append(
                        EpistemicReference(**current_relation)
                    )
                    current_relation = {}

                else:
                    raise TransformationError(
                        "Malformed epistemic relation metadata"
                    )

            if current_relation:
                raise TransformationError(
                    "Incomplete epistemic relation block"
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
            "relations": tuple(relations),
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
            relations=data["relations"],
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

    def resolve_reference(
        self,
        reference: EpistemicReference,
    ) -> Path | None:
        """
        Resolve a repository-relative manifestation when one exists locally.

        Identity remains independent of location. A missing or non-file
        reference is represented explicitly as unresolved rather than being
        invented or treated as proof of non-existence.
        """

        if not isinstance(reference, EpistemicReference):
            raise TransformationError(
                "reference must be an EpistemicReference"
            )

        raw = reference.target_reference

        # Git identities, URLs, database keys, and other non-filesystem
        # manifestations remain explicit references but are not falsely
        # resolved as local files.
        if (
            "://" in raw
            or raw.startswith("git:")
            or raw.startswith("urn:")
        ):
            return None

        candidate = Path(raw)

        if candidate.is_absolute():
            return candidate if candidate.is_file() else None

        candidate = Path.cwd() / candidate

        return candidate if candidate.is_file() else None

    def inspect(
        self,
        identifier: str,
    ) -> dict[str, object]:
        """
        Reconstruct one Transformation as a human-auditable epistemic view.

        The view is derived from persisted Transformation truth. It does not
        become a second persistence authority.
        """

        transformation = self.get(identifier)

        lineage_state: tuple[Transformation, ...] | None
        lineage_error: str | None

        try:
            lineage_state = self.lineage(identifier)
            lineage_error = None
        except TransformationError as exc:
            lineage_state = None
            lineage_error = str(exc)

        relation_views: list[dict[str, object]] = []

        for reference in transformation.relations:
            resolved = self.resolve_reference(reference)

            relation_views.append(
                {
                    "relation": reference.relation,
                    "target_identity": reference.target_identity,
                    "target_title": reference.target_title,
                    "human_identity": reference.human_identity,
                    "reference": reference.target_reference,
                    "resolved_path": resolved,
                    "resolved": resolved is not None,
                }
            )

        return {
            "transformation": transformation,
            "human_identity": transformation.human_identity,
            "dimensions": transformation.dimensions,
            "relations": tuple(relation_views),
            "lineage": lineage_state,
            "lineage_error": lineage_error,
            "children": self.children(identifier),
            "artifact": self._artifact_path(identifier),
        }

    def relate(
        self,
        transformation: Transformation,
        *,
        relation: str,
        target_identity: str,
        target_title: str,
        target_reference: str,
    ) -> Transformation:
        """
        Add one explicit epistemic relation without copying the target.

        The Transformation remains immutable; a matured value is persisted
        using the same stable TR identity.
        """

        persisted = self.get(transformation.identifier)

        if persisted != transformation:
            raise TransformationError(
                "Transformation does not match persisted state"
            )

        reference = EpistemicReference(
            relation=relation,
            target_identity=target_identity,
            target_title=target_title,
            target_reference=target_reference,
        )

        if reference in transformation.relations:
            return transformation

        matured = replace(
            transformation,
            relations=transformation.relations + (reference,),
        )

        self._write(matured)
        return matured

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
