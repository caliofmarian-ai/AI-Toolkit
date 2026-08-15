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

# ---------------------------------------------------------------------------
# PCC-04 RUN 002 — durable sedimentation physiology
# ---------------------------------------------------------------------------

from pathlib import Path
import json


class SedimentationPersistenceError(RuntimeError):
    """Durable Sedimentation representation could not be preserved or read."""


class SedimentationRepository:
    """
    Durable repository for the existing Sedimentation organ.

    This repository owns only Sedimentation persistence.

    It is not a Memory Store, Knowledge Engine, Provenance organ, Current State
    organ, or Living Project Image.
    """

    _FILENAME = "sedimentation.json"

    def __init__(self) -> None:
        self._sedimentations: dict[str, Sedimentation] = {}

    def register(self, sedimentation: Sedimentation) -> None:
        if not isinstance(sedimentation, Sedimentation):
            raise TypeError(
                "sedimentation must be an explicit Sedimentation"
            )

        existing = self._sedimentations.get(sedimentation.identifier)

        if existing is not None and existing != sedimentation:
            raise ValueError(
                "Sedimentation identity collision: "
                f"{sedimentation.identifier}"
            )

        self._sedimentations[sedimentation.identifier] = sedimentation

    def get(self, identifier: str) -> Sedimentation:
        try:
            return self._sedimentations[identifier]
        except KeyError as exc:
            raise KeyError(
                f"unknown Sedimentation identity: {identifier}"
            ) from exc

    def by_provenance(
        self,
        provenance_identifier: str,
    ) -> tuple[Sedimentation, ...]:
        if (
            not isinstance(provenance_identifier, str)
            or not provenance_identifier.strip()
        ):
            raise ValueError(
                "provenance_identifier must be an explicit non-empty string"
            )

        return tuple(
            sedimentation
            for sedimentation in self._sedimentations.values()
            if sedimentation.provenance_identifier
            == provenance_identifier
        )

    def all(self) -> tuple[Sedimentation, ...]:
        return tuple(self._sedimentations.values())

    def save(self, directory: str | Path) -> Path:
        root = Path(directory)
        root.mkdir(parents=True, exist_ok=True)

        path = root / self._FILENAME

        payload = {
            "schema": "PCC-04-SEDIMENTATION-1",
            "sedimentations": [
                {
                    "identifier": item.identifier,
                    "title": item.title,
                    "provenance_identifier": item.provenance_identifier,
                    "statement": item.statement,
                    "target": item.target.value,
                    "authority": item.authority.value,
                    "uncertainty": item.uncertainty,
                }
                for item in self._sedimentations.values()
            ],
        }

        try:
            path.write_text(
                json.dumps(
                    payload,
                    indent=2,
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
        except OSError as exc:
            raise SedimentationPersistenceError(
                f"could not persist Sedimentation repository: {exc}"
            ) from exc

        return path

    @classmethod
    def load(
        cls,
        directory: str | Path,
    ) -> "SedimentationRepository":
        path = Path(directory) / cls._FILENAME

        repository = cls()

        if not path.exists():
            return repository

        try:
            payload = json.loads(
                path.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            raise SedimentationPersistenceError(
                f"could not reconstruct Sedimentation repository: {exc}"
            ) from exc

        if payload.get("schema") != "PCC-04-SEDIMENTATION-1":
            raise SedimentationPersistenceError(
                "unsupported Sedimentation persistence schema"
            )

        raw_items = payload.get("sedimentations")

        if not isinstance(raw_items, list):
            raise SedimentationPersistenceError(
                "sedimentations must be represented as a list"
            )

        try:
            for raw in raw_items:
                item = Sedimentation(
                    identifier=raw["identifier"],
                    title=raw["title"],
                    provenance_identifier=raw[
                        "provenance_identifier"
                    ],
                    statement=raw["statement"],
                    target=SedimentationTarget(raw["target"]),
                    authority=SedimentationAuthority(
                        raw["authority"]
                    ),
                    uncertainty=raw.get("uncertainty"),
                )
                repository.register(item)
        except (
            KeyError,
            TypeError,
            ValueError,
        ) as exc:
            raise SedimentationPersistenceError(
                f"invalid persisted Sedimentation anatomy: {exc}"
            ) from exc

        return repository
