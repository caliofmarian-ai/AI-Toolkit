import pytest

from python.ai_platform.interrupted_turn import (
    recover_interrupted_human_turn,
)
from python.ai_platform.service import AIPlatformService
from python.ai_platform.sessions import AISessionEngine


def journey(journey_id="journey-e19"):
    return {
        "schema": "FUSION-02-JOURNEY-STATE-1",
        "journey_id": journey_id,
        "need_id": "need-e19",
        "status": "IN_PROGRESS",
        "step_count": 3,
        "epistemic_gain": True,
        "stopping_reason": "",
    }


def test_interruption_checkpoint_survives_restart(
    tmp_path,
):
    first = AISessionEngine(str(tmp_path))

    session = first.create(
        {
            "question": "research safely",
        }
    )

    first.bind_journey(
        session["id"],
        journey(),
    )

    first.mark_journey_interruption(
        session["id"],
        reason="provider-failure:RuntimeError",
    )

    before = first.journey_reference(
        session["id"]
    )

    second = AISessionEngine(str(tmp_path))

    after = second.journey_reference(
        session["id"]
    )

    assert after == before
    assert after["journey_id"] == "journey-e19"
    assert after["need_id"] == "need-e19"
    assert after["status"] == "INTERRUPTED"
    assert after["authority_conferred"] is False
    assert after["human_authority_preserved"] is True
    assert after["restart_recoverable"] is True


def test_interruption_without_journey_does_not_fabricate_one(
    tmp_path,
):
    engine = AISessionEngine(str(tmp_path))

    session = engine.create(
        {
            "question": "simple request",
        }
    )

    result = engine.mark_journey_interruption(
        session["id"],
        reason="process-stop",
    )

    assert result.get(
        "journey_reference",
        {},
    ) == {}


def test_new_journey_after_interruption_is_allowed(
    tmp_path,
):
    engine = AISessionEngine(str(tmp_path))

    session = engine.create(
        {
            "question": "first",
        }
    )

    engine.bind_journey(
        session["id"],
        journey("journey-first"),
    )

    engine.mark_journey_interruption(
        session["id"],
        reason="provider-failure:RuntimeError",
    )

    engine.bind_journey(
        session["id"],
        journey("journey-second"),
    )

    current = engine.journey_reference(
        session["id"]
    )

    assert current["journey_id"] == "journey-second"
    assert current["status"] == "IN_PROGRESS"


def test_real_unconfigured_provider_failure_is_persisted(
    tmp_path,
):
    repository = tmp_path / "repository"
    durable = tmp_path / "durable"

    repository.mkdir()

    service = AIPlatformService(
        repository_root=str(repository),
        workspace_root=str(tmp_path),
        state_root=str(durable),
    )

    with pytest.raises(
        ValueError,
        match="no adapter found for provider",
    ):
        service.ask_repository(
            "continue safely after failure",
            provider_id="missing-provider-e19",
            model="missing-model-e19",
        )

    sessions = service.sessions.list_sessions()

    assert len(sessions) == 1

    session = sessions[0]
    reference = session["journey_reference"]

    assert reference["status"] == "INTERRUPTED"
    assert reference["stopping_reason"] == (
        "provider-failure:ValueError"
    )
    assert reference["authority_conferred"] is False
    assert reference["human_authority_preserved"] is True
    assert reference["restart_recoverable"] is True

    assert session["conversation_history"] == []
    assert session["token_usage"] == []
    assert len(session["raw_sources"]) == 1
    assert session["raw_sources"][0]["actor"] == "HUMAN"
    assert session["raw_sources"][0]["content"] == (
        "continue safely after failure"
    )
    assert session["raw_sources"][0][
        "epistemic_status"
    ]["evidence"] is False
    assert session["raw_sources"][0][
        "epistemic_status"
    ]["automatic_authority"] is False


def test_real_failure_checkpoint_and_human_turn_survive_restart(
    tmp_path,
):
    durable = tmp_path / "durable-organism"
    deployment_a = tmp_path / "release-a"
    deployment_b = tmp_path / "release-b"

    deployment_a.mkdir()
    deployment_b.mkdir()

    first = AIPlatformService(
        repository_root=str(deployment_a),
        workspace_root=str(tmp_path),
        state_root=str(durable),
    )

    question = (
        "resume this exact human request after restart"
    )

    with pytest.raises(
        ValueError,
        match="no adapter found for provider",
    ):
        first.ask_repository(
            question,
            provider_id="missing-provider-e19",
            model="missing-model-e19",
        )

    before_session = first.sessions.list_sessions()[0]
    session_id = before_session["id"]

    before_reference = first.sessions.journey_reference(
        session_id
    )

    second = AIPlatformService(
        repository_root=str(deployment_b),
        workspace_root=str(tmp_path),
        state_root=str(durable),
    )

    recovered_session = second.sessions.get(session_id)
    after_reference = second.sessions.journey_reference(
        session_id
    )

    assert after_reference == before_reference
    assert after_reference["status"] == "INTERRUPTED"
    assert after_reference["restart_recoverable"] is True
    assert after_reference["authority_conferred"] is False
    assert after_reference[
        "human_authority_preserved"
    ] is True

    interrupted = recover_interrupted_human_turn(
        recovered_session
    )

    assert interrupted is not None
    assert interrupted.session_id == session_id
    assert interrupted.content == question
    assert interrupted.sequence == 1
    assert interrupted.expected_ai_sequence == 2
    assert interrupted.restart_recoverable is True

    context = second.conversation_context.build(
        session_id
    )

    assert context["active_session"]["session_id"] == (
        session_id
    )
    assert context["conversation"]["sources"][0][
        "content"
    ] == question
    assert context["conversation"]["sources"][0][
        "epistemic_status"
    ]["raw_source"] is True
    assert context["conversation"]["sources"][0][
        "epistemic_status"
    ]["evidence"] is False
    assert context["epistemic_boundaries"][
        "automatic_sedimentation"
    ] is False
    assert context["epistemic_boundaries"][
        "human_authority_preserved"
    ] is True


def test_real_resume_does_not_duplicate_human_source(
    tmp_path,
):
    durable = tmp_path / "durable-resume"
    deployment_a = tmp_path / "release-a"
    deployment_b = tmp_path / "release-b"

    deployment_a.mkdir()
    deployment_b.mkdir()

    first = AIPlatformService(
        repository_root=str(deployment_a),
        workspace_root=str(tmp_path),
        state_root=str(durable),
    )

    question = "preserve one human source only"

    with pytest.raises(
        ValueError,
        match="no adapter found for provider",
    ):
        first.ask_repository(
            question,
            provider_id="missing-provider-e19",
            model="missing-model-e19",
        )

    session_id = first.sessions.list_sessions()[0]["id"]

    second = AIPlatformService(
        repository_root=str(deployment_b),
        workspace_root=str(tmp_path),
        state_root=str(durable),
    )

    with pytest.raises(
        ValueError,
        match="no adapter found for provider",
    ):
        second.ask_repository(
            "this replacement question must be ignored",
            session_id=session_id,
            resume_interrupted_turn=True,
            provider_id="missing-provider-e19",
            model="missing-model-e19",
        )

    recovered = second.sessions.get(session_id)

    assert len(recovered["raw_sources"]) == 1
    assert recovered["raw_sources"][0]["actor"] == "HUMAN"
    assert recovered["raw_sources"][0]["content"] == question
    assert recovered["conversation_history"] == []
    assert recovered["token_usage"] == []

    reference = recovered["journey_reference"]

    assert reference["status"] == "INTERRUPTED"
    assert reference["authority_conferred"] is False
    assert reference["human_authority_preserved"] is True
    assert reference["restart_recoverable"] is True

def test_registered_static_provider_uses_real_pipeline_contract(
    tmp_path,
):
    repository = tmp_path / "repository"
    durable = tmp_path / "durable"

    repository.mkdir()

    service = AIPlatformService(
        repository_root=str(repository),
        workspace_root=str(tmp_path),
        state_root=str(durable),
    )

    result = service.ask_repository(
        "inspect architecture",
        provider_id="anthropic",
        model="claude-sonnet-4.5",
    )

    assert result["provider"] == "anthropic"
    assert result["model"] == "claude-sonnet-4.5"
    assert result["answer"]
    assert result["raw_source_count"] == 2
    assert result["epistemic_status"][
        "conversation_is_raw_source"
    ] is True
    assert result["epistemic_status"][
        "conversation_is_evidence"
    ] is False
    assert result["epistemic_status"][
        "conversation_is_canon"
    ] is False
    assert result["epistemic_status"][
        "human_authority_preserved"
    ] is True

    session = service.sessions.get(
        result["session_id"]
    )

    assert len(session["raw_sources"]) == 2
    assert [
        item["actor"]
        for item in session["raw_sources"]
    ] == ["HUMAN", "AI"]
    assert session["journey_reference"]["status"] != (
        "INTERRUPTED"
    )
