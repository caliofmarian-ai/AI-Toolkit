from __future__ import annotations

from datetime import datetime, timezone

import pytest

from python.ai_platform.historical_experience_recovery import (
    HistoricalAttributeStatus,
    HistoricalOrphanExperienceEvidence,
    HistoricalRecoveryError,
    inspect_historical_orphan,
)
from python.experience.lifecycle import ExperienceState


TARGET_EXPERIENCE = "3e264780-2ce0-491d-8903-41f0af66c6cb"
TARGET_SESSION = "AI-SESSION-3BAD91C0B88C"


def historical_session() -> dict:
    return {
        "id": TARGET_SESSION,
        "experience_id": TARGET_EXPERIENCE,
        "created_at": "2026-08-20T23:54:23.712193+00:00",
        "updated_at": "2026-08-20T23:54:27.620179+00:00",
        "conversation_history": [
            {
                "question": "historical question",
                "answer": "historical answer",
                "timestamp": "2026-08-20T23:54:27.619787+00:00",
            }
        ],
        "raw_sources": [
            {
                "event_id": (
                    "RAW-AI-SESSION-3BAD91C0B88C-"
                    "000001-91FCA0C0"
                ),
                "session_id": TARGET_SESSION,
                "experience_id": TARGET_EXPERIENCE,
                "actor": "HUMAN",
                "sequence": 1,
                "timestamp": "2026-08-20T23:54:23.714696+00:00",
                "source_semantics": "RAW_SOURCE_NOT_EVIDENCE",
            },
            {
                "event_id": (
                    "RAW-AI-SESSION-3BAD91C0B88C-"
                    "000002-27322D0A"
                ),
                "session_id": TARGET_SESSION,
                "experience_id": TARGET_EXPERIENCE,
                "actor": "AI",
                "sequence": 2,
                "timestamp": "2026-08-20T23:54:27.620051+00:00",
                "source_semantics": "RAW_SOURCE_NOT_EVIDENCE",
            },
        ],
        "journey_reference": {
            "journey_id": "journey-442c7a9416e29f324437",
            "need_id": "need-ae36aef6dd693b77287d",
            "status": "IN_PROGRESS",
        },
    }


def test_real_historical_identity_is_preserved():
    evidence = inspect_historical_orphan(
        historical_session()
    )

    assert (
        str(evidence.experience_id)
        == TARGET_EXPERIENCE
    )

    assert evidence.session_id == TARGET_SESSION

    assert (
        evidence.identity_status
        is HistoricalAttributeStatus.DEMONSTRATED
    )


def test_real_historical_state_is_demonstrated_active():
    evidence = inspect_historical_orphan(
        historical_session()
    )

    assert evidence.state is ExperienceState.ACTIVE

    assert (
        evidence.state_status
        is HistoricalAttributeStatus.DEMONSTRATED
    )


def test_exact_created_at_remains_irrecoverable():
    evidence = inspect_historical_orphan(
        historical_session()
    )

    assert (
        evidence.created_at_status
        is HistoricalAttributeStatus.IRRECOVERABLE
    )

    assert not hasattr(evidence, "created_at")


def test_temporal_bounds_match_demonstrated_chronology():
    evidence = inspect_historical_orphan(
        historical_session()
    )

    assert evidence.temporal_bounds.lower_exclusive == datetime(
        2026,
        8,
        20,
        23,
        54,
        23,
        712193,
        tzinfo=timezone.utc,
    )

    assert evidence.temporal_bounds.upper_exclusive == datetime(
        2026,
        8,
        20,
        23,
        54,
        23,
        714696,
        tzinfo=timezone.utc,
    )


def test_recovery_provenance_is_explicit():
    evidence = inspect_historical_orphan(
        historical_session()
    )

    assert (
        evidence.recovery_provenance
        == "HISTORICAL_ORPHAN_RECOVERY"
    )


def test_raw_source_evidence_count_is_conserved():
    evidence = inspect_historical_orphan(
        historical_session()
    )

    assert evidence.raw_source_count == 2


def test_missing_experience_identity_is_rejected():
    session = historical_session()
    session["experience_id"] = ""

    with pytest.raises(
        HistoricalRecoveryError,
        match="does not reference an Experience",
    ):
        inspect_historical_orphan(session)


def test_missing_raw_sources_are_rejected():
    session = historical_session()
    session["raw_sources"] = []

    with pytest.raises(
        HistoricalRecoveryError,
        match="no matching raw-source evidence",
    ):
        inspect_historical_orphan(session)


def test_wrong_first_actor_is_rejected():
    session = historical_session()
    session["raw_sources"][0]["actor"] = "AI"

    with pytest.raises(
        HistoricalRecoveryError,
        match="first demonstrated raw source is not HUMAN",
    ):
        inspect_historical_orphan(session)


def test_wrong_first_sequence_is_rejected():
    session = historical_session()
    session["raw_sources"][0]["sequence"] = 2
    session["raw_sources"][1]["sequence"] = 3

    with pytest.raises(
        HistoricalRecoveryError,
        match="first demonstrated raw source is not sequence 1",
    ):
        inspect_historical_orphan(session)


def test_invalid_chronology_is_rejected():
    session = historical_session()

    session["raw_sources"][0][
        "timestamp"
    ] = session["created_at"]

    with pytest.raises(
        HistoricalRecoveryError,
        match="chronology does not bound",
    ):
        inspect_historical_orphan(session)


def test_recovery_evidence_is_not_an_experience():
    evidence = inspect_historical_orphan(
        historical_session()
    )

    assert isinstance(
        evidence,
        HistoricalOrphanExperienceEvidence,
    )

    assert evidence.__class__.__name__ != "Experience"


def test_bridge_exposes_read_only_classifier():
    from python.ai_platform.conversation_experience import (
        ConversationExperienceBridge,
    )

    assert hasattr(
        ConversationExperienceBridge,
        "classify_historical_orphan",
    )


def test_existing_experience_model_remains_strict():
    from python.experience.model import Experience

    fields = set(Experience.__dataclass_fields__)

    assert fields == {
        "experience_id",
        "created_at",
        "state",
    }


def test_existing_persistence_contract_remains_strict():
    from pathlib import Path

    source = Path(
        "lib/python/experience/persistence.py"
    ).read_text(encoding="utf-8")

    assert "Interpretation != historical fact" in source

    assert (
        "Recovery must reconstruct the persisted Experience identity."
        in source
    )

    assert (
        "It must never generate a replacement identity."
        in source
    )
