from pathlib import Path

from python.ai_platform.sessions import AISessionEngine


def test_explicit_state_root_survives_repository_root_change(
    tmp_path,
):
    durable=tmp_path / "durable-state"
    deployment_a=tmp_path / "deployment-a"
    deployment_b=tmp_path / "deployment-b"

    deployment_a.mkdir()
    deployment_b.mkdir()

    first=AISessionEngine(
        str(deployment_a),
        state_root=str(durable),
    )

    session=first.create(
        {
            "id":"AI-SESSION-DURABLE-001",
            "project":"AI-Toolkit",
            "repository":"AI-Toolkit",
            "conversation_history":[
                {
                    "actor":"human",
                    "content":"remember this across deployment",
                }
            ],
            "raw_sources":[
                {
                    "actor":"human",
                    "content":"raw durable source",
                }
            ],
            "experience_id":"experience-durable-001",
            "journey_reference":{
                "journey_id":"journey-durable-001",
                "need_id":"need-durable-001",
                "status":"IN_PROGRESS",
                "step_count":3,
                "epistemic_gain":True,
                "stopping_reason":"",
            },
        }
    )

    assert session["id"] == "AI-SESSION-DURABLE-001"

    persisted=(
        durable
        / ".ai"
        / "ai_sessions"
        / "AI-SESSION-DURABLE-001.json"
    )

    assert persisted.is_file()

    # Simulate a new Railway deployment checkout/root while the
    # durable mounted state location remains the same.
    second=AISessionEngine(
        str(deployment_b),
        state_root=str(durable),
    )

    recovered=second.get("AI-SESSION-DURABLE-001")

    assert recovered["id"] == "AI-SESSION-DURABLE-001"
    assert recovered["experience_id"] == "experience-durable-001"

    assert recovered["conversation_history"] == [
        {
            "actor":"human",
            "content":"remember this across deployment",
        }
    ]

    assert recovered["raw_sources"] == [
        {
            "actor":"human",
            "content":"raw durable source",
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


def test_environment_state_root_survives_deployment_change(
    monkeypatch,
    tmp_path,
):
    durable=tmp_path / "railway-volume"
    deployment_a=tmp_path / "release-a"
    deployment_b=tmp_path / "release-b"

    deployment_a.mkdir()
    deployment_b.mkdir()

    monkeypatch.setenv(
        "AI_TOOLKIT_STATE_ROOT",
        str(durable),
    )

    first=AISessionEngine(str(deployment_a))

    first.create(
        {
            "id":"AI-SESSION-ENV-001",
            "conversation_history":[
                {
                    "actor":"human",
                    "content":"persistent conversation",
                }
            ],
        }
    )

    second=AISessionEngine(str(deployment_b))

    recovered=second.get("AI-SESSION-ENV-001")

    assert recovered["id"] == "AI-SESSION-ENV-001"
    assert recovered["conversation_history"][0]["content"] == (
        "persistent conversation"
    )

    assert second.state_root == durable.resolve()


def test_local_fallback_preserves_historical_anatomy(
    monkeypatch,
    tmp_path,
):
    monkeypatch.delenv(
        "AI_TOOLKIT_STATE_ROOT",
        raising=False,
    )

    engine=AISessionEngine(str(tmp_path))

    assert engine.state_root == tmp_path.resolve()
    assert engine.dir == (
        tmp_path.resolve()
        / ".ai"
        / "ai_sessions"
    )

    engine.create(
        {
            "id":"AI-SESSION-LOCAL-001",
        }
    )

    assert (
        tmp_path
        / ".ai"
        / "ai_sessions"
        / "AI-SESSION-LOCAL-001.json"
    ).is_file()


def test_repository_identity_is_not_replaced_by_state_root(
    tmp_path,
):
    repository=tmp_path / "repository"
    durable=tmp_path / "durable"

    repository.mkdir()

    engine=AISessionEngine(
        str(repository),
        state_root=str(durable),
    )

    created=engine.create(
        {
            "id":"AI-SESSION-IDENTITY-001",
        }
    )

    assert engine.root == repository.resolve()
    assert engine.state_root == durable.resolve()

    # Default project/repository identity continues to originate
    # from repository anatomy, not from the storage volume name.
    assert created["project"] == repository.name
    assert created["repository"] == repository.name


def test_state_root_does_not_create_session_until_requested(
    tmp_path,
):
    repository=tmp_path / "repository"
    durable=tmp_path / "durable"

    repository.mkdir()

    engine=AISessionEngine(
        str(repository),
        state_root=str(durable),
    )

    assert engine.list_sessions() == []
    assert not engine.dir.exists()

    assert engine.get("UNKNOWN-SESSION") == {}
    assert not engine.dir.exists()
