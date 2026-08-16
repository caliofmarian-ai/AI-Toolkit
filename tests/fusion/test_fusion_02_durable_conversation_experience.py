import json

import pytest

from python.ai_platform.service import AIPlatformService
from python.ai_platform.sessions import AISessionEngine
from python.experience.deployment import prepare_experience_repository
from python.experience.identity import ExperienceId
from python.runtime.organism import EpistemicOrganismAccess
from python.runtime.owner_access import OwnerAccessBoundary


def _fake_result(prompt, settings, provider_id="", model="", context_override=None):
    return {
        "answer": "AI durable answer",
        "provider": provider_id or "test-provider",
        "model": model or "test-model",
        "usage": {
            "provider": provider_id or "test-provider",
            "input_tokens": 3,
            "output_tokens": 4,
            "estimated_cost": 0.0,
            "latency_ms": 1,
            "success": True,
        },
        "context": context_override if context_override is not None else {},
    }


def test_owner_gate_still_fails_closed():
    boundary = OwnerAccessBoundary(token="owner-secret")

    assert boundary.authenticate({}).authenticated is False
    assert (
        boundary.authenticate(
            {"Authorization": "Bearer attacker"}
        ).authenticated
        is False
    )
    assert (
        boundary.authenticate(
            {"Authorization": "Bearer owner-secret"}
        ).authenticated
        is True
    )


def test_human_and_ai_become_durable_raw_sources(tmp_path):
    service = AIPlatformService(str(tmp_path))
    service.pipeline.run = _fake_result

    result = service.ask_repository(
        "Human durable question",
        provider_id="test-provider",
        model="test-model",
    )

    session = service.sessions.get(result["session_id"])

    assert session["experience_id"] == result["experience_id"]

    sources = session["raw_sources"]
    assert len(sources) == 2

    human, ai = sources

    assert human["actor"] == "HUMAN"
    assert human["content"] == "Human durable question"
    assert human["sequence"] == 1

    assert ai["actor"] == "AI"
    assert ai["content"] == "AI durable answer"
    assert ai["sequence"] == 2

    for source in sources:
        assert source["source_semantics"] == "RAW_SOURCE_NOT_EVIDENCE"
        assert source["epistemic_status"]["raw_source"] is True
        assert source["epistemic_status"]["evidence"] is False
        assert source["epistemic_status"]["canon"] is False
        assert source["epistemic_status"]["sedimentation"] is False
        assert source["epistemic_status"]["automatic_authority"] is False

        assert source["project"] == session["project"]
        assert source["repository"] == session["repository"]
        assert source["session_id"] == session["id"]
        assert source["experience_id"] == session["experience_id"]


def test_persistent_experience_is_real_existing_repository(tmp_path):
    service = AIPlatformService(str(tmp_path))
    service.pipeline.run = _fake_result

    result = service.ask_repository("question")

    repository = prepare_experience_repository(
        repository_root=tmp_path
    )

    experience = repository.get(
        ExperienceId(result["experience_id"])
    )

    assert str(experience.experience_id) == result["experience_id"]
    assert experience.state.value == "ACTIVE"


def test_restart_recovers_same_session_sources_and_experience(tmp_path):
    first = AIPlatformService(str(tmp_path))
    first.pipeline.run = _fake_result

    result = first.ask_repository(
        "persist me",
        provider_id="provider-a",
        model="model-a",
    )

    session_id = result["session_id"]
    experience_id = result["experience_id"]

    # Independent instances simulate process reconstruction boundaries.
    restarted_sessions = AISessionEngine(str(tmp_path))
    recovered_session = restarted_sessions.get(session_id)

    assert recovered_session["id"] == session_id
    assert recovered_session["experience_id"] == experience_id
    assert len(recovered_session["raw_sources"]) == 2

    restarted_organism = EpistemicOrganismAccess(tmp_path)
    recovered = restarted_organism.conversation_session(session_id)

    assert recovered["session_id"] == session_id
    assert recovered["experience"]["experience_id"] == experience_id
    assert recovered["experience"]["recovered"] is True
    assert len(recovered["raw_sources"]) == 2
    assert recovered["raw_sources"][0]["actor"] == "HUMAN"
    assert recovered["raw_sources"][1]["actor"] == "AI"

    json.dumps(recovered)


def test_existing_session_can_resume_without_new_experience(tmp_path):
    service = AIPlatformService(str(tmp_path))
    service.pipeline.run = _fake_result

    first = service.ask_repository("first")
    second = service.ask_repository(
        "second",
        session_id=first["session_id"],
    )

    assert second["session_id"] == first["session_id"]
    assert second["experience_id"] == first["experience_id"]

    session = service.sessions.get(first["session_id"])

    assert len(session["raw_sources"]) == 4
    assert [x["sequence"] for x in session["raw_sources"]] == [
        1, 2, 3, 4
    ]
    assert [x["actor"] for x in session["raw_sources"]] == [
        "HUMAN", "AI", "HUMAN", "AI"
    ]


def test_human_source_survives_provider_failure(tmp_path):
    service = AIPlatformService(str(tmp_path))

    def fail(*args, **kwargs):
        raise RuntimeError("provider unavailable")

    service.pipeline.run = fail

    with pytest.raises(RuntimeError, match="provider unavailable"):
        service.ask_repository("must survive failure")

    sessions = service.sessions.list_sessions()
    assert len(sessions) == 1

    session = sessions[0]

    assert session["experience_id"]
    assert len(session["raw_sources"]) == 1
    assert session["raw_sources"][0]["actor"] == "HUMAN"
    assert (
        session["raw_sources"][0]["content"]
        == "must survive failure"
    )


def test_no_automatic_epistemic_promotion(tmp_path):
    service = AIPlatformService(str(tmp_path))
    service.pipeline.run = _fake_result

    result = service.ask_repository("raw only")

    recovered = EpistemicOrganismAccess(
        tmp_path
    ).conversation_session(result["session_id"])

    boundaries = recovered["epistemic_boundaries"]

    assert boundaries["raw_source_is_evidence"] is False
    assert boundaries["raw_source_is_canon"] is False
    assert boundaries["ai_statement_is_evidence"] is False
    assert boundaries["automatic_sedimentation"] is False
    assert boundaries["human_authority_preserved"] is True
