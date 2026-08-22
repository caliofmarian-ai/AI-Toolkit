from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class InterruptedHumanTurn:
    """
    Non-authoritative continuity description for one HUMAN raw source
    that was durably recorded but never received its corresponding AI
    raw source.

    This object does not create Evidence, Knowledge, or Canon.
    It does not mutate the session.
    """

    event_id: str
    sequence: int
    content: str
    experience_id: str
    session_id: str
    journey_id: str
    restart_recoverable: bool

    @property
    def expected_ai_sequence(self) -> int:
        return self.sequence + 1


def recover_interrupted_human_turn(
    session: Mapping[str, Any],
) -> InterruptedHumanTurn | None:
    """
    Detect a durable HUMAN turn that has no following AI raw source.

    Recovery is deliberately conservative.

    Modern sessions use explicit interruption physiology:

    - Journey status is INTERRUPTED;
    - restart_recoverable is explicitly True.

    Historical sessions may predate those fields. They are recoverable
    only when the durable raw-source anatomy itself demonstrates an
    unmatched final HUMAN turn:

    - the final raw source is HUMAN;
    - it belongs to this exact session;
    - its sequence is the final contiguous raw-source sequence;
    - it has non-empty content;
    - the Journey remains IN_PROGRESS;
    - restart_recoverable is absent, rather than explicitly False.

    An explicit restart_recoverable=False is always authoritative and
    prevents recovery.

    No durable mutation is performed by this detector.

    Returning None means normal conversation physiology should continue.
    """

    session_id = str(
        session.get("id", "")
    ).strip()

    if not session_id:
        return None

    raw_sources = session.get("raw_sources", [])

    if not isinstance(raw_sources, list) or not raw_sources:
        return None

    final_source = raw_sources[-1]

    if not isinstance(final_source, Mapping):
        return None

    actor = str(
        final_source.get("actor", "")
    ).strip().upper()

    if actor != "HUMAN":
        return None

    if str(
        final_source.get("session_id", "")
    ).strip() != session_id:
        return None

    sequence = final_source.get("sequence")

    if not isinstance(sequence, int):
        return None

    if sequence != len(raw_sources):
        return None

    journey = session.get("journey_reference", {})

    if not isinstance(journey, Mapping):
        return None

    status = str(
        journey.get("status", "")
    ).strip().upper()

    restart_marker_present = "restart_recoverable" in journey
    restart_recoverable = journey.get("restart_recoverable")

    explicit_interruption = (
        status == "INTERRUPTED"
        and restart_recoverable is True
    )

    historical_interruption = (
        status == "IN_PROGRESS"
        and not restart_marker_present
    )

    if not (
        explicit_interruption
        or historical_interruption
    ):
        return None

    content = str(
        final_source.get(
            "content",
            final_source.get(
                "question",
                final_source.get("text", ""),
            ),
        )
    )

    if not content.strip():
        return None

    return InterruptedHumanTurn(
        event_id=str(
            final_source.get("event_id", "")
        ).strip(),
        sequence=sequence,
        content=content,
        experience_id=str(
            final_source.get("experience_id", "")
        ).strip(),
        session_id=session_id,
        journey_id=str(
            journey.get("journey_id", "")
        ).strip(),
        restart_recoverable=(
            explicit_interruption
            or historical_interruption
        ),
    )
