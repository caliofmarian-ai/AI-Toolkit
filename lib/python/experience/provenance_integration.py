"""Experience Provenance Integration for PCC-01.

This organ connects Persistent Experience with provenance semantics already
present in AI-Toolkit.

It does not replace Knowledge Graph provenance.
It does not merge Experience with Evidence.
It does not merge Experience with Session.
It does not grant authority.
It does not modify Core Experience serialization.

Inherited provenance vocabulary:
    provenance
    derived_from
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from .identity import ExperienceId


class ExperienceProvenanceError(ValueError):
    """Raised when Experience provenance violates its physiology."""


def _required_text(name: str, value: str) -> str:
    if not isinstance(value, str):
        raise ExperienceProvenanceError(
            f"{name} must be text"
        )

    normalized = value.strip()

    if not normalized:
        raise ExperienceProvenanceError(
            f"{name} must not be empty"
        )

    return normalized


@dataclass(frozen=True, slots=True)
class ExperienceProvenance:
    """Traceable origin context associated with one Experience."""

    experience_id: ExperienceId
    provenance: str
    mechanism: str
    observed_at: datetime
    session_context: str | None = None
    derived_from: tuple[str, ...] = ()
    historical_fact: str | None = None
    interpretation: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(
            self.experience_id,
            ExperienceId,
        ):
            raise ExperienceProvenanceError(
                "experience_id must be ExperienceId"
            )

        object.__setattr__(
            self,
            "provenance",
            _required_text(
                "provenance",
                self.provenance,
            ),
        )

        object.__setattr__(
            self,
            "mechanism",
            _required_text(
                "mechanism",
                self.mechanism,
            ),
        )

        if not isinstance(
            self.observed_at,
            datetime,
        ):
            raise ExperienceProvenanceError(
                "observed_at must be datetime"
            )

        if self.observed_at.tzinfo is None:
            raise ExperienceProvenanceError(
                "observed_at must be timezone-aware"
            )

        if self.session_context is not None:
            object.__setattr__(
                self,
                "session_context",
                _required_text(
                    "session_context",
                    self.session_context,
                ),
            )

        if not isinstance(
            self.derived_from,
            tuple,
        ):
            raise ExperienceProvenanceError(
                "derived_from must be tuple"
            )

        normalized_derivations = tuple(
            _required_text(
                "derived_from entry",
                item,
            )
            for item in self.derived_from
        )

        object.__setattr__(
            self,
            "derived_from",
            normalized_derivations,
        )

        if self.historical_fact is not None:
            object.__setattr__(
                self,
                "historical_fact",
                _required_text(
                    "historical_fact",
                    self.historical_fact,
                ),
            )

        if self.interpretation is not None:
            object.__setattr__(
                self,
                "interpretation",
                _required_text(
                    "interpretation",
                    self.interpretation,
                ),
            )

    @classmethod
    def observe(
        cls,
        *,
        experience_id: ExperienceId,
        provenance: str,
        mechanism: str,
        session_context: str | None = None,
        derived_from: tuple[str, ...] = (),
        historical_fact: str | None = None,
        interpretation: str | None = None,
    ) -> "ExperienceProvenance":
        """Observe provenance without mutating Core Experience."""

        return cls(
            experience_id=experience_id,
            provenance=provenance,
            mechanism=mechanism,
            observed_at=datetime.now(
                timezone.utc
            ),
            session_context=session_context,
            derived_from=derived_from,
            historical_fact=historical_fact,
            interpretation=interpretation,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize only this integration organ."""

        return {
            "experience_id": str(
                self.experience_id
            ),
            "provenance": self.provenance,
            "mechanism": self.mechanism,
            "observed_at": (
                self.observed_at.isoformat()
            ),
            "session_context": (
                self.session_context
            ),
            "derived_from": list(
                self.derived_from
            ),
            "historical_fact": (
                self.historical_fact
            ),
            "interpretation": (
                self.interpretation
            ),
        }

    @classmethod
    def from_dict(
        cls,
        payload: dict[str, Any],
    ) -> "ExperienceProvenance":
        """Restore provenance while preserving Experience identity."""

        if not isinstance(payload, dict):
            raise ExperienceProvenanceError(
                "payload must be mapping"
            )

        try:
            experience_id = (
                ExperienceId.from_string(
                    payload["experience_id"]
                )
            )

            observed_at = (
                datetime.fromisoformat(
                    payload["observed_at"]
                )
            )

            derived_from = tuple(
                payload.get(
                    "derived_from",
                    (),
                )
            )

            return cls(
                experience_id=experience_id,
                provenance=payload[
                    "provenance"
                ],
                mechanism=payload[
                    "mechanism"
                ],
                observed_at=observed_at,
                session_context=payload.get(
                    "session_context"
                ),
                derived_from=derived_from,
                historical_fact=payload.get(
                    "historical_fact"
                ),
                interpretation=payload.get(
                    "interpretation"
                ),
            )

        except ExperienceProvenanceError:
            raise

        except (
            KeyError,
            TypeError,
            ValueError,
        ) as exc:
            raise ExperienceProvenanceError(
                "invalid provenance payload"
            ) from exc
