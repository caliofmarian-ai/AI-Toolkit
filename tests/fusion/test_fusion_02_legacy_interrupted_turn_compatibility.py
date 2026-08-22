from python.ai_platform.interrupted_turn import (
    recover_interrupted_human_turn,
)


SESSION_ID = "AI-SESSION-3BAD91C0B88C"
EXPERIENCE_ID = "3e264780-2ce0-491d-8903-41f0af66c6cb"


def _human_source(
    sequence: int = 3,
    *,
    content: str = "Continue preserved conversation",
):
    return {
        "actor": "HUMAN",
        "content": content,
        "event_id": f"RAW-{SESSION_ID}-{sequence:06d}",
        "experience_id": EXPERIENCE_ID,
        "sequence": sequence,
        "session_id": SESSION_ID,
    }


def _ai_source(sequence: int):
    return {
        "actor": "AI",
        "content": "AI response",
        "event_id": f"RAW-{SESSION_ID}-{sequence:06d}",
        "experience_id": EXPERIENCE_ID,
        "sequence": sequence,
        "session_id": SESSION_ID,
    }


def _base_sources():
    return [
        {
            "actor": "HUMAN",
            "content": "first human",
            "event_id": f"RAW-{SESSION_ID}-000001",
            "experience_id": EXPERIENCE_ID,
            "sequence": 1,
            "session_id": SESSION_ID,
        },
        _ai_source(2),
    ]


def _session(journey, final=None):
    sources = _base_sources()

    if final is not None:
        sources.append(final)

    return {
        "id": SESSION_ID,
        "experience_id": EXPERIENCE_ID,
        "raw_sources": sources,
        "journey_reference": journey,
    }


def test_historical_in_progress_session_recovers_final_human():
    session = _session(
        {
            "journey_id": "journey-historical",
            "status": "IN_PROGRESS",
        },
        _human_source(),
    )

    recovered = recover_interrupted_human_turn(session)

    assert recovered is not None
    assert recovered.sequence == 3
    assert recovered.expected_ai_sequence == 4
    assert recovered.session_id == SESSION_ID
    assert recovered.experience_id == EXPERIENCE_ID
    assert recovered.content == "Continue preserved conversation"
    assert recovered.restart_recoverable is True


def test_modern_explicit_interruption_still_recovers():
    session = _session(
        {
            "journey_id": "journey-modern",
            "status": "INTERRUPTED",
            "restart_recoverable": True,
        },
        _human_source(),
    )

    recovered = recover_interrupted_human_turn(session)

    assert recovered is not None
    assert recovered.sequence == 3
    assert recovered.expected_ai_sequence == 4


def test_explicit_false_restart_marker_blocks_recovery():
    session = _session(
        {
            "journey_id": "journey-blocked",
            "status": "IN_PROGRESS",
            "restart_recoverable": False,
        },
        _human_source(),
    )

    assert recover_interrupted_human_turn(session) is None


def test_interrupted_without_explicit_restart_permission_is_not_recovered():
    session = _session(
        {
            "journey_id": "journey-ambiguous",
            "status": "INTERRUPTED",
        },
        _human_source(),
    )

    assert recover_interrupted_human_turn(session) is None


def test_completed_journey_is_not_recovered():
    session = _session(
        {
            "journey_id": "journey-complete",
            "status": "COMPLETED",
        },
        _human_source(),
    )

    assert recover_interrupted_human_turn(session) is None


def test_final_ai_source_is_not_interrupted_human_turn():
    session = {
        "id": SESSION_ID,
        "experience_id": EXPERIENCE_ID,
        "raw_sources": _base_sources(),
        "journey_reference": {
            "journey_id": "journey-normal",
            "status": "IN_PROGRESS",
        },
    }

    assert recover_interrupted_human_turn(session) is None


def test_wrong_session_source_is_rejected():
    final = _human_source()
    final["session_id"] = "AI-SESSION-OTHER"

    session = _session(
        {
            "journey_id": "journey-historical",
            "status": "IN_PROGRESS",
        },
        final,
    )

    assert recover_interrupted_human_turn(session) is None


def test_non_contiguous_final_sequence_is_rejected():
    session = _session(
        {
            "journey_id": "journey-historical",
            "status": "IN_PROGRESS",
        },
        _human_source(sequence=4),
    )

    assert recover_interrupted_human_turn(session) is None


def test_empty_human_content_is_rejected():
    session = _session(
        {
            "journey_id": "journey-historical",
            "status": "IN_PROGRESS",
        },
        _human_source(content="   "),
    )

    assert recover_interrupted_human_turn(session) is None


def test_detector_is_read_only():
    session = _session(
        {
            "journey_id": "journey-historical",
            "status": "IN_PROGRESS",
        },
        _human_source(),
    )

    import copy

    before = copy.deepcopy(session)

    recovered = recover_interrupted_human_turn(session)

    assert recovered is not None
    assert session == before


def test_real_historical_shape_from_railway_is_recoverable():
    session = {
        "id": SESSION_ID,
        "experience_id": EXPERIENCE_ID,
        "raw_sources": [
            {
                "actor": "HUMAN",
                "content": "original question",
                "event_id": (
                    "RAW-AI-SESSION-3BAD91C0B88C-"
                    "000001-91FCA0C0"
                ),
                "experience_id": EXPERIENCE_ID,
                "sequence": 1,
                "session_id": SESSION_ID,
            },
            {
                "actor": "AI",
                "content": "original response",
                "event_id": (
                    "RAW-AI-SESSION-3BAD91C0B88C-"
                    "000002-27322D0A"
                ),
                "experience_id": EXPERIENCE_ID,
                "sequence": 2,
                "session_id": SESSION_ID,
            },
            {
                "actor": "HUMAN",
                "content": (
                    "Continue this existing conversation using its "
                    "preserved session history and historical continuity. "
                    "Briefly confirm what repository you are operating on, "
                    "what you understand the current engineering objective "
                    "to be, and identify the next safest engineering action. "
                    "Do not modify the repository or execute any write "
                    "operation."
                ),
                "event_id": (
                    "RAW-AI-SESSION-3BAD91C0B88C-"
                    "000003-0F552580"
                ),
                "experience_id": EXPERIENCE_ID,
                "sequence": 3,
                "session_id": SESSION_ID,
            },
        ],
        "journey_reference": {
            "epistemic_gain": True,
            "journey_id": "journey-8113ed477839fda431a5",
            "need_id": "need-6a77ff41ac06e69c37cb",
            "status": "IN_PROGRESS",
            "step_count": 1,
            "stopping_reason": "",
        },
    }

    recovered = recover_interrupted_human_turn(session)

    assert recovered is not None
    assert recovered.event_id == (
        "RAW-AI-SESSION-3BAD91C0B88C-000003-0F552580"
    )
    assert recovered.sequence == 3
    assert recovered.expected_ai_sequence == 4
    assert recovered.journey_id == (
        "journey-8113ed477839fda431a5"
    )
