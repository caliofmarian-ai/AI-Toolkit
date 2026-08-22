from __future__ import annotations

from python.ai_platform.interrupted_turn import (
    InterruptedHumanTurn,
    recover_interrupted_human_turn,
)


def _session() -> dict:
    return {
        "id": "AI-SESSION-RECOVERY",
        "experience_id": "experience-original",
        "raw_sources": [
            {
                "event_id": "RAW-1",
                "sequence": 1,
                "actor": "HUMAN",
                "session_id": "AI-SESSION-RECOVERY",
                "experience_id": "experience-original",
                "content": "first question",
            },
            {
                "event_id": "RAW-2",
                "sequence": 2,
                "actor": "AI",
                "session_id": "AI-SESSION-RECOVERY",
                "experience_id": "experience-original",
                "content": "first answer",
            },
            {
                "event_id": "RAW-3",
                "sequence": 3,
                "actor": "HUMAN",
                "session_id": "AI-SESSION-RECOVERY",
                "experience_id": "experience-original",
                "content": "continue this exact interrupted request",
            },
        ],
        "journey_reference": {
            "journey_id": "journey-recovery",
            "need_id": "need-recovery",
            "status": "INTERRUPTED",
            "stopping_reason": "provider-failure",
            "restart_recoverable": True,
            "human_authority_preserved": True,
            "authority_conferred": False,
        },
    }


def test_detects_exact_interrupted_human_turn():
    recovered = recover_interrupted_human_turn(_session())

    assert isinstance(recovered, InterruptedHumanTurn)
    assert recovered.sequence == 3
    assert recovered.expected_ai_sequence == 4
    assert recovered.event_id == "RAW-3"
    assert recovered.session_id == "AI-SESSION-RECOVERY"
    assert recovered.experience_id == "experience-original"
    assert recovered.journey_id == "journey-recovery"
    assert recovered.content == (
        "continue this exact interrupted request"
    )
    assert recovered.restart_recoverable is True


def test_does_not_recover_completed_ai_turn():
    session = _session()

    session["raw_sources"].append(
        {
            "event_id": "RAW-4",
            "sequence": 4,
            "actor": "AI",
            "session_id": "AI-SESSION-RECOVERY",
            "experience_id": "experience-original",
            "content": "answer",
        }
    )

    assert recover_interrupted_human_turn(session) is None


def test_does_not_recover_non_interrupted_journey():
    session = _session()
    session["journey_reference"]["status"] = "IN_PROGRESS"

    assert recover_interrupted_human_turn(session) is None


def test_does_not_recover_without_restart_authority():
    session = _session()
    session["journey_reference"]["restart_recoverable"] = False

    assert recover_interrupted_human_turn(session) is None


def test_does_not_recover_wrong_session_identity():
    session = _session()
    session["raw_sources"][-1]["session_id"] = "OTHER"

    assert recover_interrupted_human_turn(session) is None


def test_does_not_recover_broken_temporal_sequence():
    session = _session()
    session["raw_sources"][-1]["sequence"] = 7

    assert recover_interrupted_human_turn(session) is None


def test_recovery_is_read_only():
    session = _session()

    before = repr(session)

    recovered = recover_interrupted_human_turn(session)

    assert recovered is not None
    assert repr(session) == before


def test_service_contains_non_duplication_guard():
    from pathlib import Path

    source = Path(
        "lib/python/ai_platform/service.py"
    ).read_text(encoding="utf-8")

    assert (
        "recover_interrupted_human_turn(session)"
        in source
    )

    assert "if interrupted_turn is None:" in source

    assert "effective_question" in source


def test_recovery_does_not_change_session_engine_sequence_contract():
    from pathlib import Path

    source = Path(
        "lib/python/ai_platform/sessions.py"
    ).read_text(encoding="utf-8")

    assert (
        "expected_sequence = len(sources) + 1"
        in source
    )

    assert (
        "raw source temporal sequence does not continue session order"
        in source
    )
