"""
FUSION-02 — historical orphan Experience recovery evidence.

This module does not manufacture an Experience.

It represents demonstrated recovery evidence when a durable AI
session still references an Experience whose original persisted
representation was lost before Experience storage became durable.

Epistemic boundaries:

recovery evidence != original persisted Experience
temporal bound != exact historical created_at
inference != historical fact
session != Experience
Journey != Experience
persistence != authority

An original Experience identity may be demonstrated even when one
or more historical attributes are no longer exactly recoverable.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Mapping, Sequence

from python.experience.identity import ExperienceId
from python.experience.lifecycle import ExperienceState


class HistoricalRecoveryError(RuntimeError):
    """Historical orphan recovery evidence is invalid or insufficient."""


class HistoricalAttributeStatus(str, Enum):
    """Epistemic status of one historical Experience attribute."""

    DEMONSTRATED = "DEMONSTRATED"
    BOUNDED = "BOUNDED"
    IRRECOVERABLE = "IRRECOVERABLE"


@dataclass(frozen=True, slots=True)
class HistoricalTemporalBounds:
    """
    Demonstrated temporal bounds around lost Experience creation.

    These values are evidence boundaries only.

    They must never be serialized as the exact original
    Experience.created_at.
    """

    lower_exclusive: datetime
    upper_exclusive: datetime

    def __post_init__(self) -> None:
        if self.lower_exclusive.tzinfo is None:
            raise HistoricalRecoveryError(
                "lower temporal bound must be timezone-aware"
            )

        if self.upper_exclusive.tzinfo is None:
            raise HistoricalRecoveryError(
                "upper temporal bound must be timezone-aware"
            )

        if self.lower_exclusive >= self.upper_exclusive:
            raise HistoricalRecoveryError(
                "historical temporal bounds must be ordered"
            )


@dataclass(frozen=True, slots=True)
class HistoricalOrphanExperienceEvidence:
    """
    Evidence describing one historically orphaned Experience.

    This is deliberately not an Experience domain entity.

    It cannot silently enter PersistentExperienceRepository because
    the exact original created_at is unavailable.
    """

    experience_id: ExperienceId
    state: ExperienceState
    temporal_bounds: HistoricalTemporalBounds
    identity_status: HistoricalAttributeStatus
    state_status: HistoricalAttributeStatus
    created_at_status: HistoricalAttributeStatus
    recovery_provenance: str
    session_id: str
    raw_source_count: int

    def __post_init__(self) -> None:
        if self.identity_status is not HistoricalAttributeStatus.DEMONSTRATED:
            raise HistoricalRecoveryError(
                "historical Experience identity must be demonstrated"
            )

        if self.state_status is not HistoricalAttributeStatus.DEMONSTRATED:
            raise HistoricalRecoveryError(
                "historical Experience state must be demonstrated"
            )

        if self.created_at_status is not HistoricalAttributeStatus.IRRECOVERABLE:
            raise HistoricalRecoveryError(
                "exact original created_at must remain explicitly irrecoverable"
            )

        if self.recovery_provenance != "HISTORICAL_ORPHAN_RECOVERY":
            raise HistoricalRecoveryError(
                "invalid historical recovery provenance"
            )

        if not self.session_id.strip():
            raise HistoricalRecoveryError(
                "historical recovery requires session identity"
            )

        if self.raw_source_count < 1:
            raise HistoricalRecoveryError(
                "historical recovery requires raw-source evidence"
            )


def inspect_historical_orphan(
    session: Mapping[str, Any],
) -> HistoricalOrphanExperienceEvidence:
    """
    Classify demonstrated evidence for a historically orphaned Experience.

    This function is read-only.

    It does not:
    - create an Experience;
    - add anything to the Experience repository;
    - modify the AI session;
    - fabricate created_at;
    - replace Experience identity.

    The ACTIVE state is accepted only when the durable session anatomy
    demonstrates the FUSION-02 conversation physiology produced by the
    existing ConversationExperienceBridge:

        Experience.create().activate()
        -> bind Experience to session
        -> first HUMAN raw source

    The temporal interval is:

        session.created_at
        <
        original Experience.created_at
        <
        first matching raw-source timestamp

    The interval is evidence. It is not an exact timestamp.
    """

    if not isinstance(session, Mapping):
        raise HistoricalRecoveryError(
            "historical recovery requires a session mapping"
        )

    session_id = str(session.get("id", "")).strip()
    experience_raw = str(session.get("experience_id", "")).strip()
    session_created_raw = str(session.get("created_at", "")).strip()

    if not session_id:
        raise HistoricalRecoveryError(
            "historical recovery requires stable session identity"
        )

    if not experience_raw:
        raise HistoricalRecoveryError(
            "session does not reference an Experience"
        )

    if not session_created_raw:
        raise HistoricalRecoveryError(
            "session creation timestamp is unavailable"
        )

    try:
        experience_id = ExperienceId.from_string(experience_raw)
    except Exception as exc:
        raise HistoricalRecoveryError(
            "session Experience identity is invalid"
        ) from exc

    try:
        session_created = datetime.fromisoformat(session_created_raw)
    except ValueError as exc:
        raise HistoricalRecoveryError(
            "session creation timestamp is invalid"
        ) from exc

    if session_created.tzinfo is None:
        raise HistoricalRecoveryError(
            "session creation timestamp must be timezone-aware"
        )

    raw_sources = session.get("raw_sources", [])

    if not isinstance(raw_sources, Sequence) or isinstance(
        raw_sources,
        (str, bytes),
    ):
        raise HistoricalRecoveryError(
            "session raw_sources must be a sequence"
        )

    matching_sources: list[tuple[int, datetime, Mapping[str, Any]]] = []

    for item in raw_sources:
        if not isinstance(item, Mapping):
            continue

        if str(item.get("experience_id", "")).strip() != experience_raw:
            continue

        if str(item.get("session_id", "")).strip() != session_id:
            continue

        sequence_raw = item.get("sequence")
        timestamp_raw = str(item.get("timestamp", "")).strip()

        if (
            isinstance(sequence_raw, bool)
            or not isinstance(sequence_raw, int)
            or sequence_raw < 1
            or not timestamp_raw
        ):
            continue

        try:
            timestamp = datetime.fromisoformat(timestamp_raw)
        except ValueError:
            continue

        if timestamp.tzinfo is None:
            continue

        matching_sources.append(
            (sequence_raw, timestamp, item)
        )

    if not matching_sources:
        raise HistoricalRecoveryError(
            "no matching raw-source evidence exists"
        )

    matching_sources.sort(
        key=lambda row: (row[0], row[1])
    )

    first_sequence, first_timestamp, first_source = matching_sources[0]

    if first_sequence != 1:
        raise HistoricalRecoveryError(
            "first demonstrated raw source is not sequence 1"
        )

    actor = str(first_source.get("actor", "")).strip().upper()

    if actor != "HUMAN":
        raise HistoricalRecoveryError(
            "first demonstrated raw source is not HUMAN"
        )

    if first_timestamp <= session_created:
        raise HistoricalRecoveryError(
            "raw-source chronology does not bound Experience creation"
        )

    source_semantics = str(
        first_source.get("source_semantics", "")
    ).strip()

    if source_semantics and source_semantics != "RAW_SOURCE_NOT_EVIDENCE":
        raise HistoricalRecoveryError(
            "unexpected raw-source semantics"
        )

    return HistoricalOrphanExperienceEvidence(
        experience_id=experience_id,
        state=ExperienceState.ACTIVE,
        temporal_bounds=HistoricalTemporalBounds(
            lower_exclusive=session_created,
            upper_exclusive=first_timestamp,
        ),
        identity_status=HistoricalAttributeStatus.DEMONSTRATED,
        state_status=HistoricalAttributeStatus.DEMONSTRATED,
        created_at_status=HistoricalAttributeStatus.IRRECOVERABLE,
        recovery_provenance="HISTORICAL_ORPHAN_RECOVERY",
        session_id=session_id,
        raw_source_count=len(matching_sources),
    )

@dataclass(frozen=True, slots=True)
class HistoricalExperienceContinuity:
    """
    Runtime continuity handle for a demonstrated historical orphan.

    This is NOT an Experience domain entity.
    This is NOT persisted as an Experience.
    This does NOT invent Experience.created_at.

    It carries only the stable Experience identity required for
    continued raw-conversation physiology, together with explicit
    historical recovery evidence.

    HistoricalExperienceContinuity != Experience
    continuity != reconstruction
    continuity != fabricated history
    """

    experience_id: ExperienceId
    evidence: HistoricalOrphanExperienceEvidence

    def __post_init__(self) -> None:
        if self.experience_id != self.evidence.experience_id:
            raise HistoricalRecoveryError(
                "continuity identity must equal demonstrated historical identity"
            )

    @property
    def recovery_provenance(self) -> str:
        return self.evidence.recovery_provenance

    @property
    def historical_state(self) -> ExperienceState:
        return self.evidence.state

    @property
    def exact_created_at_recoverable(self) -> bool:
        return False


def historical_continuity(
    session: Mapping[str, Any],
) -> HistoricalExperienceContinuity:
    """
    Create a non-persistent continuity handle from demonstrated evidence.

    No Experience is inserted into a repository.
    No timestamp is synthesized.
    No identity is replaced.
    """
    evidence = inspect_historical_orphan(session)

    return HistoricalExperienceContinuity(
        experience_id=evidence.experience_id,
        evidence=evidence,
    )
