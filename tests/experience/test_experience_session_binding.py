import pytest

from lib.python.experience import Experience
from lib.python.experience.identity import ExperienceId
from lib.python.experience.session_binding import (
    InvalidExperienceBindingError,
    InvalidSessionIdError,
    SessionBinding,
    normalize_session_id,
    validate_experience_id,
)


def test_experience_create_returns_established_experience_identity():
    experience = Experience.create()

    assert isinstance(experience.experience_id, ExperienceId)


def test_session_binding_connects_distinct_identities():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert binding.session_id == "session-alpha"
    assert binding.experience_id == experience.experience_id


def test_session_identity_is_not_experience_identity():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert binding.session_id != binding.experience_id
    assert isinstance(binding.experience_id, ExperienceId)


def test_binding_does_not_replace_experience():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert isinstance(experience, Experience)
    assert not isinstance(binding, Experience)


def test_binding_preserves_exact_experience_identity():
    experience = Experience.create()
    original_identity = experience.experience_id

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=original_identity,
    )

    assert binding.experience_id is original_identity
    assert experience.experience_id is original_identity


def test_session_id_is_normalized():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="  session-alpha  ",
        experience_id=experience.experience_id,
    )

    assert binding.session_id == "session-alpha"


@pytest.mark.parametrize("session_id", ["", " ", "\n", "\t"])
def test_empty_session_identity_is_rejected(session_id):
    experience = Experience.create()

    with pytest.raises(InvalidSessionIdError):
        SessionBinding.create(
            session_id=session_id,
            experience_id=experience.experience_id,
        )


def test_non_string_session_identity_is_rejected():
    with pytest.raises(InvalidSessionIdError):
        normalize_session_id(123)  # type: ignore[arg-type]


def test_raw_string_cannot_replace_experience_identity():
    with pytest.raises(InvalidExperienceBindingError):
        SessionBinding.create(
            session_id="session-alpha",
            experience_id="not-an-experience-id",  # type: ignore[arg-type]
        )


def test_none_cannot_replace_experience_identity():
    with pytest.raises(InvalidExperienceBindingError):
        SessionBinding.create(
            session_id="session-alpha",
            experience_id=None,  # type: ignore[arg-type]
        )


def test_validate_experience_id_preserves_identity_object():
    experience = Experience.create()

    validated = validate_experience_id(experience.experience_id)

    assert validated is experience.experience_id


def test_binding_can_confirm_experience_membership():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert binding.belongs_to_experience(experience.experience_id)


def test_binding_rejects_other_experience_membership():
    first = Experience.create()
    second = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=first.experience_id,
    )

    assert not binding.belongs_to_experience(second.experience_id)


def test_binding_rejects_raw_string_experience_membership():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert not binding.belongs_to_experience(
        experience.experience_id.value  # type: ignore[arg-type]
    )


def test_binding_can_confirm_session_membership():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert binding.belongs_to_session("session-alpha")
    assert binding.belongs_to_session(" session-alpha ")


def test_binding_rejects_other_session_membership():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert not binding.belongs_to_session("session-beta")


def test_binding_rejects_invalid_session_membership_query():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert not binding.belongs_to_session("")
