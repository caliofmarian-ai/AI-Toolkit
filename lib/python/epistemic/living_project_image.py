"""
PCC-06 — Living Project Image.

RUN 002 — Minimal Anatomy of the Living Epistemic Image.

This module provides the smallest derived, read-only anatomy through which
the epistemic organism can represent what it demonstrably exists as now
without turning that representation into Canon, Evidence, Memory, Git,
Persistent Experience, CSL, Progressive Recall, Human Authority, or an
autonomous truth authority.

The Living Project Image is a derived epistemic surface.

It preserves semantic identity, bounded epistemic state, supporting
references, navigable provenance, uncertainty, and conflict.

It does not own the realities it represents.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


EpistemicState = Literal[
    "DEMONSTRATED",
    "UNKNOWN",
    "UNCERTAIN",
    "AMBIGUOUS",
    "CONFLICTING",
    "UNCONFIRMED",
    "NOT VERIFIED",
]

SupportKind = Literal[
    "CANON",
    "REPOSITORY",
    "IMPLEMENTATION",
    "TEST",
    "EVIDENCE",
    "KNOWLEDGE",
    "CURRENT_STATE",
    "MEMORY",
    "TRANSFORMATION",
    "PERSISTENT_EXPERIENCE",
    "WITNESS",
    "TRACE",
    "LINEAGE",
    "HISTORICAL",
    "OTHER",
]

_ALLOWED_STATES = {
    "DEMONSTRATED",
    "UNKNOWN",
    "UNCERTAIN",
    "AMBIGUOUS",
    "CONFLICTING",
    "UNCONFIRMED",
    "NOT VERIFIED",
}

_ALLOWED_SUPPORT_KINDS = {
    "CANON",
    "REPOSITORY",
    "IMPLEMENTATION",
    "TEST",
    "EVIDENCE",
    "KNOWLEDGE",
    "CURRENT_STATE",
    "MEMORY",
    "TRANSFORMATION",
    "PERSISTENT_EXPERIENCE",
    "WITNESS",
    "TRACE",
    "LINEAGE",
    "HISTORICAL",
    "OTHER",
}


class LivingProjectImageError(ValueError):
    """Raised when a Living Project Image would violate epistemic structure."""


def _text(name: str, value: str) -> str:
    if not isinstance(value, str):
        raise LivingProjectImageError(f"{name} must be text")

    value = value.strip()

    if not value:
        raise LivingProjectImageError(f"{name} must not be empty")

    return value


@dataclass(frozen=True)
class EpistemicReference:
    """
    Navigable reference toward supporting epistemic reality.

    A reference is not the referenced body and does not acquire its authority.
    """

    identifier: str
    title: str
    kind: SupportKind
    reference: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "identifier", _text("identifier", self.identifier))
        object.__setattr__(self, "title", _text("title", self.title))
        object.__setattr__(self, "reference", _text("reference", self.reference))

        if self.kind not in _ALLOWED_SUPPORT_KINDS:
            raise LivingProjectImageError(
                f"unsupported epistemic reference kind: {self.kind}"
            )

    @property
    def display_identity(self) -> str:
        return f"{self.identifier} — {self.title}"


@dataclass(frozen=True)
class LivingProjectStatement:
    """
    One derived statement on the organism's current epistemic surface.

    The statement remains distinct from every supporting epistemic body.
    """

    identifier: str
    title: str
    statement: str
    epistemic_state: EpistemicState
    supports: tuple[EpistemicReference, ...] = ()
    provenance_paths: tuple[str, ...] = ()
    uncertainty: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    derived: bool = True
    authoritative: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "identifier", _text("identifier", self.identifier))
        object.__setattr__(self, "title", _text("title", self.title))
        object.__setattr__(self, "statement", _text("statement", self.statement))

        if not self.identifier.startswith("LPI-STMT-"):
            raise LivingProjectImageError(
                "Living Project Statement identity must use LPI-STMT-*"
            )

        if self.epistemic_state not in _ALLOWED_STATES:
            raise LivingProjectImageError(
                f"unsupported epistemic state: {self.epistemic_state}"
            )

        if self.derived is not True:
            raise LivingProjectImageError(
                "Living Project Statements must remain explicitly derived"
            )

        if self.authoritative is not False:
            raise LivingProjectImageError(
                "Living Project Image cannot declare itself authoritative"
            )

        if self.epistemic_state == "DEMONSTRATED" and not self.supports:
            raise LivingProjectImageError(
                "DEMONSTRATED state requires explicit supporting reality"
            )

        if self.epistemic_state == "UNCERTAIN" and not self.uncertainty:
            raise LivingProjectImageError(
                "UNCERTAIN state must preserve its uncertainty"
            )

        if self.epistemic_state == "CONFLICTING" and not self.conflicts:
            raise LivingProjectImageError(
                "CONFLICTING state must preserve visible conflict"
            )

        for path in self.provenance_paths:
            _text("provenance path", path)

        for item in self.uncertainty:
            _text("uncertainty", item)

        for item in self.conflicts:
            _text("conflict", item)

    @property
    def display_identity(self) -> str:
        return f"{self.identifier} — {self.title}"


@dataclass(frozen=True)
class LivingProjectImage:
    """
    Derived read-only current epistemic image.

    Destruction of this object destroys no authoritative project reality.
    The image can be reconstructed from the same preserved inputs.
    """

    identifier: str
    title: str
    statements: tuple[LivingProjectStatement, ...]
    derived: bool = True
    authoritative: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "identifier", _text("identifier", self.identifier))
        object.__setattr__(self, "title", _text("title", self.title))

        if not self.identifier.startswith("LPI-"):
            raise LivingProjectImageError(
                "Living Project Image identity must use LPI-*"
            )

        if self.derived is not True:
            raise LivingProjectImageError(
                "Living Project Image must remain explicitly derived"
            )

        if self.authoritative is not False:
            raise LivingProjectImageError(
                "Living Project Image cannot become an authority"
            )

        identities = tuple(item.identifier for item in self.statements)

        if len(identities) != len(set(identities)):
            raise LivingProjectImageError(
                "Living Project Image cannot contain duplicate statement identities"
            )

    @property
    def display_identity(self) -> str:
        return f"{self.identifier} — {self.title}"

    def statement(self, identifier: str) -> LivingProjectStatement:
        identifier = _text("statement identifier", identifier)

        for item in self.statements:
            if item.identifier == identifier:
                return item

        raise LivingProjectImageError(
            f"Living Project Statement not present: {identifier}"
        )

    def by_state(
        self,
        epistemic_state: EpistemicState,
    ) -> tuple[LivingProjectStatement, ...]:
        if epistemic_state not in _ALLOWED_STATES:
            raise LivingProjectImageError(
                f"unsupported epistemic state: {epistemic_state}"
            )

        return tuple(
            item
            for item in self.statements
            if item.epistemic_state == epistemic_state
        )


def form_living_project_image(
    *,
    identifier: str,
    title: str,
    statements: tuple[LivingProjectStatement, ...],
) -> LivingProjectImage:
    """
    Form a deterministic derived image from explicitly supplied representations.

    No source organ is mutated.
    No retrieval is performed.
    No missing support is invented.
    No canonical admission is performed.
    """

    if not isinstance(statements, tuple):
        raise LivingProjectImageError(
            "Living Project Image statements must be an immutable tuple"
        )

    for item in statements:
        if not isinstance(item, LivingProjectStatement):
            raise LivingProjectImageError(
                "Living Project Image accepts only LivingProjectStatement bodies"
            )

    return LivingProjectImage(
        identifier=identifier,
        title=title,
        statements=statements,
    )
