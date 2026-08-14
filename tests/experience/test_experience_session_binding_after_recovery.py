"""PCC-01 Session Binding after Experience recovery.

Evidence-derived physiology:

Experience.create
    -> serialize_experience
    -> recover_experience
    -> SessionBinding.create

Contract boundaries:
Experience != Session
Storage != Experience
Persistence != authority

This test does not invent a repository implementation.
"""

from lib.python.experience.model import Experience
from lib.python.experience.persistence import (
    recover_experience,
    serialize_experience,
)
from lib.python.experience.session_binding import SessionBinding


def _recover(experience):
    payload = serialize_experience(experience)
    recovered = recover_experience(payload)

    assert recovered is not experience

    return payload, recovered


def test_identity_survives_recovery_before_session_binding():
    original = Experience.create()
    before = original.experience_id

    _, recovered = _recover(original)

    after = recovered.experience_id

    assert before == after


def test_recovered_experience_can_bind_to_session():
    original = Experience.create()
    before = original.experience_id

    _, recovered = _recover(original)

    binding = SessionBinding.create(
        session_id="SESSION-AFTER-RECOVERY",
        experience_id=recovered.experience_id,
    )

    assert binding.experience_id == before
    assert binding.belongs_to_experience(before)
    assert binding.belongs_to_session(
        "SESSION-AFTER-RECOVERY"
    )


def test_session_binding_does_not_change_experience_identity():
    original = Experience.create()
    before = original.experience_id

    _, recovered = _recover(original)

    SessionBinding.create(
        session_id="SESSION-ONE",
        experience_id=recovered.experience_id,
    )

    assert recovered.experience_id == before


def test_rebinding_does_not_redefine_experience_identity():
    original = Experience.create()
    before = original.experience_id

    _, recovered = _recover(original)

    first = SessionBinding.create(
        session_id="SESSION-ONE",
        experience_id=recovered.experience_id,
    )

    second = SessionBinding.create(
        session_id="SESSION-TWO",
        experience_id=recovered.experience_id,
    )

    assert first.session_id != second.session_id
    assert first.experience_id == before
    assert second.experience_id == before
    assert recovered.experience_id == before


def test_session_identity_remains_distinct_from_experience_identity():
    original = Experience.create()

    _, recovered = _recover(original)

    binding = SessionBinding.create(
        session_id="SESSION-DISTINCT",
        experience_id=recovered.experience_id,
    )

    assert str(binding.session_id) != str(
        recovered.experience_id
    )


def test_recovery_does_not_require_session_identity():
    original = Experience.create()

    payload, recovered = _recover(original)

    assert "session_id" not in payload
    assert (
        recovered.experience_id
        == original.experience_id
    )


def test_binding_does_not_mutate_persistent_experience_body():
    original = Experience.create()

    _, recovered = _recover(original)

    before = serialize_experience(recovered)

    SessionBinding.create(
        session_id="SESSION-RELATIONAL",
        experience_id=recovered.experience_id,
    )

    after = serialize_experience(recovered)

    assert after == before
