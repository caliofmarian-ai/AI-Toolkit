import pytest

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


def test_interruption_checkpoint_survives_restart(tmp_path):
    first=AISessionEngine(str(tmp_path))

    session=first.create({
        "question":"research safely",
    })

    first.bind_journey(
        session["id"],
        journey(),
    )

    first.mark_journey_interruption(
        session["id"],
        reason="provider-failure:RuntimeError",
    )

    before=first.journey_reference(
        session["id"]
    )

    second=AISessionEngine(str(tmp_path))

    after=second.journey_reference(
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
    engine=AISessionEngine(str(tmp_path))

    session=engine.create({
        "question":"simple request",
    })

    result=engine.mark_journey_interruption(
        session["id"],
        reason="process-stop",
    )

    assert result.get(
        "journey_reference",
        {},
    ) == {}


def test_new_journey_after_interruption_is_allowed(tmp_path):
    engine=AISessionEngine(str(tmp_path))

    session=engine.create({
        "question":"first",
    })

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

    current=engine.journey_reference(
        session["id"]
    )

    assert current["journey_id"] == "journey-second"
    assert current["status"] == "IN_PROGRESS"


def test_service_provider_failure_persists_interruption(
    monkeypatch,
    tmp_path,
):
    service=AIPlatformService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    def fail_provider(*args, **kwargs):
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr(
        service.pipeline,
        "run",
        fail_provider,
    )

    with pytest.raises(
        RuntimeError,
        match="provider unavailable",
    ):
        service.ask_repository("hi")

    sessions=service.sessions.list_sessions()

    assert len(sessions) == 1

    session=sessions[0]
    reference=session["journey_reference"]

    assert reference["status"] == "INTERRUPTED"
    assert (
        reference["stopping_reason"]
        == "provider-failure:RuntimeError"
    )
    assert reference["authority_conferred"] is False
    assert reference["human_authority_preserved"] is True
    assert reference["restart_recoverable"] is True

    # Provider failed: no answer may be fabricated.
    assert session["conversation_history"] == []
    assert session["token_usage"] == []


def test_service_failure_checkpoint_survives_new_service(
    monkeypatch,
    tmp_path,
):
    first=AIPlatformService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    def fail_provider(*args, **kwargs):
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr(
        first.pipeline,
        "run",
        fail_provider,
    )

    with pytest.raises(RuntimeError):
        first.ask_repository("hi")

    session_id=first.sessions.list_sessions()[0]["id"]

    before=first.sessions.journey_reference(
        session_id
    )

    second=AIPlatformService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    after=second.sessions.journey_reference(
        session_id
    )

    assert after == before
    assert after["status"] == "INTERRUPTED"
    assert after["authority_conferred"] is False
    assert after["human_authority_preserved"] is True


def test_synthetic_session_boundary_does_not_create_persistence(
    monkeypatch,
    tmp_path,
):
    service=AIPlatformService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    synthetic={
        "id":"synthetic-e19-session",
        "raw_sources":[],
        "conversation_history":[],
        "token_usage":[],
        "selected_provider":"provider-a",
        "selected_model":"model-a",
    }

    monkeypatch.setattr(
        service.sessions,
        "create",
        lambda payload: dict(synthetic),
    )

    monkeypatch.setattr(
        service.sessions,
        "get",
        lambda session_id: {},
    )

    monkeypatch.setattr(
        service.sessions,
        "bind_experience",
        lambda session_id, experience_id: dict(synthetic),
    )

    monkeypatch.setattr(
        service.sessions,
        "append_raw_source",
        lambda session_id, source: dict(synthetic),
    )

    monkeypatch.setattr(
        service.conversation_context,
        "build",
        lambda session_id, partner_identity=None: {
            "schema": "SYNTHETIC-E19-CONTEXT-1",
            "session_id": session_id,
            "conversation": {
                "synthetic": True,
                "persistent": False,
            },
            "partner_identity": dict(
                partner_identity or {}
            ),
        },
    )

    def fail_provider(*args, **kwargs):
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr(
        service.pipeline,
        "run",
        fail_provider,
    )

    with pytest.raises(RuntimeError):
        service.ask_repository("hi")

    # Synthetic/test-double service boundary remains non-persistent.
    assert (
        service.sessions.get(
            "synthetic-e19-session"
        )
        == {}
    )
