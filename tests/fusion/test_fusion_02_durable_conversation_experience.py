import json

import pytest

from python.ai_platform.service import AIPlatformService
from python.ai_platform.sessions import AISessionEngine
from python.experience.deployment import prepare_experience_repository
from python.experience.identity import ExperienceId
from python.runtime.organism import EpistemicOrganismAccess
from python.runtime.owner_access import OwnerAccessBoundary


REAL_PROVIDER = "anthropic"
REAL_MODEL = "claude-sonnet-4.5"
MISSING_PROVIDER = "missing-provider-durable-experience"
MISSING_MODEL = "missing-model-durable-experience"


def ask_through_registered_pipeline(
    service,
    question,
    *,
    session_id=None,
):
    return service.ask_repository(
        question,
        session_id=session_id,
        provider_id=REAL_PROVIDER,
        model=REAL_MODEL,
    )


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


def test_human_and_ai_become_durable_raw_sources(
    tmp_path,
):
    service = AIPlatformService(str(tmp_path))

    result = ask_through_registered_pipeline(
        service,
        "Human durable question",
    )

    assert result["provider"] == REAL_PROVIDER
    assert result["model"] == REAL_MODEL
    assert result["answer"]

    session = service.sessions.get(
        result["session_id"]
    )

    assert (
        session["experience_id"]
        == result["experience_id"]
    )

    sources = session["raw_sources"]

    assert len(sources) == 2

    human, ai = sources

    assert human["actor"] == "HUMAN"
    assert (
        human["content"]
        == "Human durable question"
    )
    assert human["sequence"] == 1

    assert ai["actor"] == "AI"
    assert ai["content"] == result["answer"]
    assert ai["content"]
    assert ai["sequence"] == 2

    for raw_source in sources:
        assert (
            raw_source["source_semantics"]
            == "RAW_SOURCE_NOT_EVIDENCE"
        )
        assert (
            raw_source["epistemic_status"]["raw_source"]
            is True
        )
        assert (
            raw_source["epistemic_status"]["evidence"]
            is False
        )
        assert (
            raw_source["epistemic_status"]["canon"]
            is False
        )
        assert (
            raw_source["epistemic_status"]["sedimentation"]
            is False
        )
        assert (
            raw_source["epistemic_status"][
                "automatic_authority"
            ]
            is False
        )

        assert (
            raw_source["project"]
            == session["project"]
        )
        assert (
            raw_source["repository"]
            == session["repository"]
        )
        assert (
            raw_source["session_id"]
            == session["id"]
        )
        assert (
            raw_source["experience_id"]
            == session["experience_id"]
        )


def test_persistent_experience_is_real_existing_repository(
    tmp_path,
):
    service = AIPlatformService(str(tmp_path))

    result = ask_through_registered_pipeline(
        service,
        "create persistent experience",
    )

    repository = prepare_experience_repository(
        repository_root=tmp_path
    )

    experience = repository.get(
        ExperienceId(result["experience_id"])
    )

    assert (
        str(experience.experience_id)
        == result["experience_id"]
    )
    assert experience.state.value == "ACTIVE"


def test_restart_recovers_same_session_sources_and_experience(
    tmp_path,
):
    first = AIPlatformService(str(tmp_path))

    result = ask_through_registered_pipeline(
        first,
        "persist me",
    )

    session_id = result["session_id"]
    experience_id = result["experience_id"]

    restarted_sessions = AISessionEngine(
        str(tmp_path)
    )

    recovered_session = restarted_sessions.get(
        session_id
    )

    assert recovered_session["id"] == session_id
    assert (
        recovered_session["experience_id"]
        == experience_id
    )
    assert (
        len(recovered_session["raw_sources"])
        == 2
    )

    restarted_organism = EpistemicOrganismAccess(
        tmp_path
    )

    recovered = restarted_organism.conversation_session(
        session_id
    )

    assert recovered["session_id"] == session_id
    assert (
        recovered["experience"]["experience_id"]
        == experience_id
    )
    assert (
        recovered["experience"]["recovered"]
        is True
    )
    assert len(recovered["raw_sources"]) == 2
    assert (
        recovered["raw_sources"][0]["actor"]
        == "HUMAN"
    )
    assert (
        recovered["raw_sources"][1]["actor"]
        == "AI"
    )

    json.dumps(recovered)


def test_existing_session_can_resume_without_new_experience(
    tmp_path,
):
    service = AIPlatformService(str(tmp_path))

    first = ask_through_registered_pipeline(
        service,
        "first",
    )

    second = ask_through_registered_pipeline(
        service,
        "second",
        session_id=first["session_id"],
    )

    assert (
        second["session_id"]
        == first["session_id"]
    )
    assert (
        second["experience_id"]
        == first["experience_id"]
    )

    session = service.sessions.get(
        first["session_id"]
    )

    assert len(session["raw_sources"]) == 4

    assert [
        item["sequence"]
        for item in session["raw_sources"]
    ] == [1, 2, 3, 4]

    assert [
        item["actor"]
        for item in session["raw_sources"]
    ] == [
        "HUMAN",
        "AI",
        "HUMAN",
        "AI",
    ]

    assert (
        session["raw_sources"][1]["content"]
        == first["answer"]
    )
    assert (
        session["raw_sources"][3]["content"]
        == second["answer"]
    )


def test_human_source_survives_real_provider_failure(
    tmp_path,
):
    service = AIPlatformService(str(tmp_path))

    with pytest.raises(
        ValueError,
        match="no adapter found for provider",
    ):
        service.ask_repository(
            "must survive failure",
            provider_id=MISSING_PROVIDER,
            model=MISSING_MODEL,
        )

    sessions = service.sessions.list_sessions()

    assert len(sessions) == 1

    session = sessions[0]

    assert session["experience_id"]
    assert len(session["raw_sources"]) == 1
    assert (
        session["raw_sources"][0]["actor"]
        == "HUMAN"
    )
    assert (
        session["raw_sources"][0]["content"]
        == "must survive failure"
    )
    assert (
        session["journey_reference"]["status"]
        == "INTERRUPTED"
    )


def test_no_automatic_epistemic_promotion(
    tmp_path,
):
    service = AIPlatformService(str(tmp_path))

    result = ask_through_registered_pipeline(
        service,
        "raw only",
    )

    recovered = EpistemicOrganismAccess(
        tmp_path
    ).conversation_session(
        result["session_id"]
    )

    boundaries = recovered[
        "epistemic_boundaries"
    ]

    assert (
        boundaries["raw_source_is_evidence"]
        is False
    )
    assert (
        boundaries["raw_source_is_canon"]
        is False
    )
    assert (
        boundaries["ai_statement_is_evidence"]
        is False
    )
    assert (
        boundaries["automatic_sedimentation"]
        is False
    )
    assert (
        boundaries["human_authority_preserved"]
        is True
    )
