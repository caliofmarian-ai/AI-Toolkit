"""
PCC-04 — Sedimentation.

Sedimentation represents a governed proposal that preserved epistemic
experience has acquired meaning worthy of durable preservation.

This organ does not own Experience, Transformation, Provenance, Memory,
Knowledge, Current State, or the Living Project Image.

RUN 001 establishes only the Sedimentation anatomy and its Human Authority
boundary.

A Sedimentation proposal never becomes authoritative merely because software
or AI created it.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum


class SedimentationTarget(str, Enum):
    """The durable epistemic destination proposed for sedimentation."""

    MEMORY = "MEMORY"
    KNOWLEDGE = "KNOWLEDGE"
    MEMORY_AND_KNOWLEDGE = "MEMORY_AND_KNOWLEDGE"


class SedimentationAuthority(str, Enum):
    """Explicit authority state of a sedimentation proposal."""

    PROPOSED = "PROPOSED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class Sedimentation:
    """
    Immutable semantic sedimentation proposal.

    provenance_identifier preserves the explicit path back toward the
    epistemic reality from which the proposed meaning arose.

    statement is an interpretation. It does not replace or mutate the
    originating experience.

    uncertainty remains explicit when reality is not sufficiently established.
    """

    identifier: str
    title: str
    provenance_identifier: str
    statement: str
    target: SedimentationTarget
    authority: SedimentationAuthority = SedimentationAuthority.PROPOSED
    uncertainty: str | None = None

    def __post_init__(self) -> None:
        for name in (
            "identifier",
            "title",
            "provenance_identifier",
            "statement",
        ):
            value = getattr(self, name)

            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{name} must be an explicit non-empty string"
                )

        if not isinstance(self.target, SedimentationTarget):
            raise TypeError(
                "target must be an explicit SedimentationTarget"
            )

        if not isinstance(
            self.authority,
            SedimentationAuthority,
        ):
            raise TypeError(
                "authority must be an explicit SedimentationAuthority"
            )

        if self.uncertainty is not None:
            if not isinstance(self.uncertainty, str):
                raise TypeError(
                    "uncertainty must be a string or None"
                )

            if not self.uncertainty.strip():
                raise ValueError(
                    "uncertainty must be meaningful when supplied"
                )

    @property
    def human_readable_identity(self) -> str:
        return f"{self.identifier} — {self.title}"

    @property
    def requires_human_authority(self) -> bool:
        return self.authority is SedimentationAuthority.PROPOSED

    @property
    def is_accepted(self) -> bool:
        return self.authority is SedimentationAuthority.ACCEPTED

    @property
    def is_rejected(self) -> bool:
        return self.authority is SedimentationAuthority.REJECTED

    def accept_by_human_authority(self) -> "Sedimentation":
        """
        Explicitly accept a proposal through Human Authority.

        The original immutable proposal remains preserved.
        """

        if self.authority is not SedimentationAuthority.PROPOSED:
            raise ValueError(
                "only a PROPOSED sedimentation may be accepted"
            )

        return replace(
            self,
            authority=SedimentationAuthority.ACCEPTED,
        )

    def reject_by_human_authority(self) -> "Sedimentation":
        """
        Explicitly reject a proposal through Human Authority.

        Rejection preserves the proposal and its provenance rather than
        erasing the organism's epistemic history.
        """

        if self.authority is not SedimentationAuthority.PROPOSED:
            raise ValueError(
                "only a PROPOSED sedimentation may be rejected"
            )

        return replace(
            self,
            authority=SedimentationAuthority.REJECTED,
        )
