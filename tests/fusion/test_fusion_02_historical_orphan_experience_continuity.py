from __future__ import annotations

from pathlib import Path

import pytest

from python.ai_platform.conversation_experience import (
    ConversationExperienceBridge,
)
from python.ai_platform.historical_experience_recovery import (
    HistoricalAttributeStatus,
    HistoricalExperienceContinuity,
    historical_continuity,
)
from python.experience.lifecycle import ExperienceState
from python.experience.model import Experience


TARGET_SESSION = "AI-SESSION-3BAD91C0B88C"
TARGET_EXPERIENCE = "3e264780-2ce0-491d-8903-41f0af66c6cb"


def orphan_session() -> dict:
    return {
        "id": TARGET_SESSION,
        "experience_id": TARGET_EXPERIENCE,
        "project": "AI-Toolkit",
        "repository": "AI-Toolkit",
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


def test_continuity_preserves_original_identity():
    continuity = historical_continuity(orphan_session())

    assert isinstance(
        continuity,
        HistoricalExperienceContinuity,
    )

    assert str(continuity.experience_id) == TARGET_EXPERIENCE


def test_continuity_is_not_experience():
    continuity = historical_continuity(orphan_session())

    assert not isinstance(continuity, Experience)


def test_continuity_does_not_claim_exact_created_at():
    continuity = historical_continuity(orphan_session())

    assert continuity.exact_created_at_recoverable is False
    assert not hasattr(continuity, "created_at")


def test_continuity_preserves_demonstrated_active_state():
    continuity = historical_continuity(orphan_session())

    assert continuity.historical_state is ExperienceState.ACTIVE
    assert (
        continuity.evidence.state_status
        is HistoricalAttributeStatus.DEMONSTRATED
    )


def test_continuity_has_explicit_provenance():
    continuity = historical_continuity(orphan_session())

    assert (
        continuity.recovery_provenance
        == "HISTORICAL_ORPHAN_RECOVERY"
    )


def test_raw_source_can_continue_same_experience_identity():
    bridge = object.__new__(ConversationExperienceBridge)

    continuity = historical_continuity(orphan_session())

    raw = bridge.raw_source(
        session=orphan_session(),
        experience=continuity,
        actor="HUMAN",
        content="Continue the same historical conversation.",
        sequence=3,
    )

    assert raw["session_id"] == TARGET_SESSION
    assert raw["experience_id"] == TARGET_EXPERIENCE
    assert raw["sequence"] == 3
    assert raw["actor"] == "HUMAN"


def test_raw_source_continuity_does_not_become_evidence():
    bridge = object.__new__(ConversationExperienceBridge)

    continuity = historical_continuity(orphan_session())

    raw = bridge.raw_source(
        session=orphan_session(),
        experience=continuity,
        actor="AI",
        content="Continuation response.",
        sequence=4,
    )

    assert raw["source_semantics"] == "RAW_SOURCE_NOT_EVIDENCE"
    assert raw["epistemic_status"]["raw_source"] is True
    assert raw["epistemic_status"]["evidence"] is False
    assert raw["epistemic_status"]["canon"] is False
    assert raw["epistemic_status"]["automatic_authority"] is False


def test_existing_experience_model_remains_unchanged():
    assert set(Experience.__dataclass_fields__) == {
        "experience_id",
        "created_at",
        "state",
    }


def test_bridge_contains_narrow_not_found_recovery():
    source = Path(
        "lib/python/ai_platform/conversation_experience.py"
    ).read_text(encoding="utf-8")

    assert "ExperienceNotFoundError" in source
    assert "historical_continuity(session)" in source
    assert "if not isinstance(exc, ExperienceNotFoundError)" in source


def test_bridge_does_not_insert_continuity_into_repository():
    source = Path(
        "lib/python/ai_platform/conversation_experience.py"
    ).read_text(encoding="utf-8")

    recovery_index = source.index(
        "experience = historical_continuity(session)"
    )

    new_experience_index = source.index(
        "        else:\n"
        "            experience = Experience.create().activate()",
        recovery_index,
    )

    historical_orphan_branch = source[
        recovery_index:new_experience_index
    ]

    assert (
        "self.experiences.add(experience)"
        not in historical_orphan_branch
    )

    new_experience_branch = source[
        new_experience_index:
        source.index(
            "        binding = SessionBinding.create(",
            new_experience_index,
        )
    ]

    assert (
        "self.experiences.add(experience)"
        in new_experience_branch
    )


def test_new_experience_creation_path_is_conserved():
    source = Path(
        "lib/python/ai_platform/conversation_experience.py"
    ).read_text(encoding="utf-8")

    assert "Experience.create().activate()" in source
    assert "self.experiences.add(experience)" in source


def test_continuity_does_not_change_persistence_contract():
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
