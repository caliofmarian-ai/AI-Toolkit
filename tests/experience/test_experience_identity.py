import dataclasses

import pytest

from lib.python.experience.identity import (
    ExperienceId,
    ExperienceIdentityError,
)


def test_independent_experience_identities_are_unique():
    first = ExperienceId.create()
    second = ExperienceId.create()

    assert first != second


def test_existing_identity_can_be_reconstructed_without_regeneration():
    original = ExperienceId.create()
    reconstructed = ExperienceId.from_string(str(original))

    assert reconstructed == original


def test_experience_identity_is_immutable():
    identity = ExperienceId.create()

    with pytest.raises(dataclasses.FrozenInstanceError):
        identity.value = str(ExperienceId.create())


def test_malformed_identity_is_rejected():
    with pytest.raises(ExperienceIdentityError):
        ExperienceId.from_string("not-an-experience-id")
