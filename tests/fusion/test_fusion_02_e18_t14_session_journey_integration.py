import json

from python.ai_platform.sessions import AISessionEngine


def journey(
    journey_id="journey-18",
    status="IN_PROGRESS",
    step_count=2,
):
    return {
        "schema": "FUSION-02-JOURNEY-STATE-1",
        "journey_id": journey_id,
        "need_id": "need-18",
        "status": status,
        "step_count": step_count,
        "epistemic_gain": True,
        "visited": (
            "search:repository",
            "read:service.py",
        ),
        "stopping_reason": "",
    }


def test_session_persists_compact_journey_reference(tmp_path):
    engine=AISessionEngine(str(tmp_path))

    session=engine.create({
        "id": "AI-SESSION-E18",
        "project": "AI-Toolkit",
    })

    updated=engine.bind_journey(
        session["id"],
        journey(),
    )

    assert updated["journey_reference"] == {
        "journey_id": "journey-18",
        "need_id": "need-18",
        "status": "IN_PROGRESS",
        "step_count": 2,
        "epistemic_gain": True,
        "stopping_reason": "",
    }

    assert "visited" not in updated["journey_reference"]
    assert "schema" not in updated["journey_reference"]


def test_conversation_and_journey_remain_distinct(tmp_path):
    engine=AISessionEngine(str(tmp_path))

    session=engine.create({
        "id": "AI-SESSION-SEPARATION",
    })

    engine.append_interaction(
        session["id"],
        "question",
        "answer",
        {"input_tokens": 1},
    )

    engine.bind_journey(
        session["id"],
        journey(),
    )

    loaded=engine.get(session["id"])

    assert len(loaded["conversation_history"]) == 1
    assert loaded["conversation_history"][0]["question"] == "question"
    assert loaded["conversation_history"][0]["answer"] == "answer"

    assert (
        loaded["journey_reference"]["journey_id"]
        == "journey-18"
    )

    assert (
        "journey_id"
        not in loaded["conversation_history"][0]
    )


def test_working_context_is_not_session_journey_reference(tmp_path):
    engine=AISessionEngine(str(tmp_path))

    session=engine.create({
        "id": "AI-SESSION-NO-WORKING-CONTEXT",
    })

    engine.bind_journey(
        session["id"],
        journey(),
    )

    loaded=engine.get(session["id"])
    ref=loaded["journey_reference"]

    assert "working_context" not in ref
    assert "evidence" not in ref
    assert "epistemic_results" not in ref
    assert "semantic_identities" not in ref
    assert "relationships" not in ref


def test_old_session_without_journey_reference_is_readable(tmp_path):
    engine=AISessionEngine(str(tmp_path))
    engine.dir.mkdir(parents=True,exist_ok=True)

    legacy={
        "id": "AI-SESSION-LEGACY",
        "project": "AI-Toolkit",
        "conversation_history": [],
        "prompt_history": [],
        "token_usage": [],
        "repository_profile": {
            "legacy": True,
        },
        "engineering_context": {
            "legacy": True,
        },
    }

    path=engine.dir / "AI-SESSION-LEGACY.json"
    path.write_text(
        json.dumps(legacy),
        encoding="utf-8",
    )

    loaded=engine.get("AI-SESSION-LEGACY")

    assert loaded["id"] == "AI-SESSION-LEGACY"
    assert loaded["repository_profile"]["legacy"] is True
    assert engine.journey_reference(
        "AI-SESSION-LEGACY"
    ) == {}


def test_journey_reference_survives_restart(tmp_path):
    first=AISessionEngine(str(tmp_path))

    session=first.create({
        "id": "AI-SESSION-RESTART",
    })

    first.bind_journey(
        session["id"],
        journey(
            status="PARTIAL",
            step_count=4,
        ),
    )

    second=AISessionEngine(str(tmp_path))

    ref=second.journey_reference(
        "AI-SESSION-RESTART"
    )

    assert ref["journey_id"] == "journey-18"
    assert ref["need_id"] == "need-18"
    assert ref["status"] == "PARTIAL"
    assert ref["step_count"] == 4


def test_same_journey_checkpoint_can_evolve(tmp_path):
    engine=AISessionEngine(str(tmp_path))

    session=engine.create({
        "id": "AI-SESSION-CHECKPOINT",
    })

    engine.bind_journey(
        session["id"],
        journey(
            status="IN_PROGRESS",
            step_count=1,
        ),
    )

    engine.bind_journey(
        session["id"],
        journey(
            status="PARTIAL",
            step_count=5,
        ),
    )

    ref=engine.journey_reference(
        session["id"]
    )

    assert ref["journey_id"] == "journey-18"
    assert ref["status"] == "PARTIAL"
    assert ref["step_count"] == 5


def test_same_conversation_can_advance_to_new_journey(
    tmp_path,
):
    engine=AISessionEngine(str(tmp_path))

    session=engine.create({
        "id": "AI-SESSION-IDENTITY",
    })

    engine.bind_journey(
        session["id"],
        journey(),
    )

    updated=engine.bind_journey(
        session["id"],
        journey(
            journey_id="journey-other",
            status="IN_PROGRESS",
            step_count=1,
        ),
    )

    assert (
        updated["journey_reference"]["journey_id"]
        == "journey-other"
    )

    assert (
        updated["journey_reference"]["need_id"]
        == "need-18"
    )

    assert updated["conversation_history"] == []


def test_journey_binding_does_not_create_experience(tmp_path):
    engine=AISessionEngine(str(tmp_path))

    session=engine.create({
        "id": "AI-SESSION-NO-EXPERIENCE",
    })

    updated=engine.bind_journey(
        session["id"],
        journey(),
    )

    assert updated["experience_id"] == ""


def test_journey_reference_is_not_memory(tmp_path):
    engine=AISessionEngine(str(tmp_path))

    session=engine.create({
        "id": "AI-SESSION-NO-MEMORY",
    })

    engine.bind_journey(
        session["id"],
        journey(),
    )

    ref=engine.journey_reference(
        session["id"]
    )

    assert set(ref) == {
        "journey_id",
        "need_id",
        "status",
        "step_count",
        "epistemic_gain",
        "stopping_reason",
    }

    assert "memory" not in ref
    assert "knowledge" not in ref
    assert "evidence" not in ref
    assert "visited" not in ref
