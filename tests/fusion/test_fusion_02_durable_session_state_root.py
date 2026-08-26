from pathlib import Path

from python.ai_platform.service import AIPlatformService
from python.ai_platform.sessions import AISessionEngine


def test_explicit_state_root_survives_repository_root_change(
    tmp_path,
):
    durable = tmp_path / "durable-state"
    deployment_a = tmp_path / "deployment-a"
    deployment_b = tmp_path / "deployment-b"

    deployment_a.mkdir()
    deployment_b.mkdir()

    first = AISessionEngine(
        str(deployment_a),
        state_root=str(durable),
    )

    session = first.create(
        {
            "id": "AI-SESSION-DURABLE-001",
            "project": "AI-Toolkit",
            "repository": "AI-Toolkit",
            "conversation_history": [
                {
                    "actor": "human",
                    "content": "remember this across deployment",
                }
            ],
            "raw_sources": [
                {
                    "actor": "human",
                    "content": "raw durable source",
                }
            ],
            "experience_id": "experience-durable-001",
            "journey_reference": {
                "journey_id": "journey-durable-001",
                "need_id": "need-durable-001",
                "status": "IN_PROGRESS",
                "step_count": 3,
                "epistemic_gain": True,
                "stopping_reason": "",
            },
        }
    )

    assert session["id"] == "AI-SESSION-DURABLE-001"

    persisted = (
        durable
        / ".ai"
        / "ai_sessions"
        / "AI-SESSION-DURABLE-001.json"
    )

    assert persisted.is_file()

    second = AISessionEngine(
        str(deployment_b),
        state_root=str(durable),
    )

    recovered = second.get("AI-SESSION-DURABLE-001")

    assert recovered["id"] == "AI-SESSION-DURABLE-001"
    assert recovered["experience_id"] == (
        "experience-durable-001"
    )
    assert recovered["conversation_history"] == [
        {
            "actor": "human",
            "content": "remember this across deployment",
        }
    ]
    assert recovered["raw_sources"] == [
        {
            "actor": "human",
            "content": "raw durable source",
        }
    ]
    assert recovered["journey_reference"]["journey_id"] == (
        "journey-durable-001"
    )
    assert recovered["journey_reference"]["need_id"] == (
        "need-durable-001"
    )
    assert first.root != second.root
    assert first.state_root == second.state_root
    assert first.dir == second.dir


def test_service_recovers_session_experience_and_context_after_restart(
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

    session = first.sessions.create(
        {
            "id": "AI-SESSION-REAL-RESTART-001",
            "project": "AI-Toolkit",
            "repository": "AI-Toolkit",
            "selected_provider": "provider-alpha",
            "selected_model": "model-alpha",
        }
    )

    experience, binding = (
        first.conversation_experience.ensure_experience(
            session
        )
    )

    session = first.sessions.bind_experience(
        session["id"],
        str(experience.experience_id),
    )

    assert binding.session_id == session["id"]

    human_source = (
        first.conversation_experience.raw_source(
            session=session,
            experience=experience,
            actor="HUMAN",
            content=(
                "continue AI-Toolkit after a real deployment "
                "restart"
            ),
            sequence=1,
        )
    )

    session = first.sessions.append_raw_source(
        session["id"],
        human_source,
    )

    first.sessions.bind_journey(
        session["id"],
        {
            "journey_id": "JOURNEY-REAL-RESTART-001",
            "need_id": "NEED-REAL-RESTART-001",
            "status": "PARTIAL",
            "step_count": 4,
            "epistemic_gain": True,
            "stopping_reason": "DEPLOYMENT_RESTART",
        },
    )

    assert (
        durable
        / ".ai"
        / "ai_sessions"
        / "AI-SESSION-REAL-RESTART-001.json"
    ).is_file()

    assert (
        durable
        / ".ai"
        / "runtime"
        / "state"
        / "experience.json"
    ).is_file()

    second = AIPlatformService(
        repository_root=str(deployment_b),
        workspace_root=str(tmp_path),
        state_root=str(durable),
    )

    recovered_session = second.sessions.get(
        "AI-SESSION-REAL-RESTART-001"
    )

    assert recovered_session["id"] == (
        "AI-SESSION-REAL-RESTART-001"
    )
    assert recovered_session["experience_id"] == str(
        experience.experience_id
    )
    assert recovered_session["journey_reference"][
        "journey_id"
    ] == "JOURNEY-REAL-RESTART-001"

    recovered_experience = (
        second.conversation_experience.recover_experience(
            recovered_session["experience_id"]
        )
    )

    assert str(recovered_experience.experience_id) == (
        recovered_session["experience_id"]
    )

    context = second.conversation_context.build(
        recovered_session["id"],
        partner_identity={
            "provider": "provider-alpha",
            "model": "model-alpha",
        },
    )

    assert context["active_session"]["session_id"] == (
        recovered_session["id"]
    )
    assert context["active_session"]["experience_id"] == (
        recovered_session["experience_id"]
    )
    assert context["persistent_experience"]["recovered"] is True
    assert context["conversation"]["sources"][0][
        "content"
    ] == (
        "continue AI-Toolkit after a real deployment restart"
    )
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

    assert first.sessions.root != second.sessions.root
    assert (
        first.sessions.state_root
        == second.sessions.state_root
        == durable.resolve()
    )


def test_explicit_state_root_does_not_replace_repository_identity(
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

    created = service.sessions.create(
        {
            "id": "AI-SESSION-IDENTITY-001",
        }
    )

    assert service.sessions.root == repository.resolve()
    assert service.sessions.state_root == durable.resolve()
    assert created["project"] == repository.name
    assert created["repository"] == repository.name


def test_state_root_remains_lazy_until_session_is_requested(
    tmp_path,
):
    repository = tmp_path / "repository"
    durable = tmp_path / "durable"

    repository.mkdir()

    engine = AISessionEngine(
        str(repository),
        state_root=str(durable),
    )

    assert engine.list_sessions() == []
    assert not engine.dir.exists()
    assert engine.get("UNKNOWN-SESSION") == {}
    assert not engine.dir.exists()


def test_local_fallback_preserves_historical_anatomy(
    tmp_path,
):
    engine = AISessionEngine(str(tmp_path))

    assert engine.state_root == tmp_path.resolve()
    assert engine.dir == (
        tmp_path.resolve()
        / ".ai"
        / "ai_sessions"
    )

    engine.create(
        {
            "id": "AI-SESSION-LOCAL-001",
        }
    )

    assert (
        tmp_path
        / ".ai"
        / "ai_sessions"
        / "AI-SESSION-LOCAL-001.json"
    ).is_file()
