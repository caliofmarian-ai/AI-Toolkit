import pytest

from lib.python.experience.identity import ExperienceId
from lib.python.experience.protection import (
    ExperienceProtection,
    InvalidProtectionIdentityError,
    ProtectedExperienceMutationError,
    ProtectionState,
    UnauthorizedExperienceOperationError,
)


def new_identity() -> ExperienceId:
    return ExperienceId.create()


def test_unprotected_state_is_explicit():
    identity = new_identity()

    protection = ExperienceProtection.unprotected(identity)

    assert protection.experience_id == identity
    assert protection.state is ProtectionState.UNPROTECTED
    assert protection.is_protected is False


def test_protected_state_is_explicit():
    identity = new_identity()

    protection = ExperienceProtection.protected(identity)

    assert protection.experience_id == identity
    assert protection.state is ProtectionState.PROTECTED
    assert protection.is_protected is True


def test_protect_preserves_experience_identity():
    identity = new_identity()

    before = ExperienceProtection.unprotected(identity)
    after = before.protect()

    assert after.experience_id == before.experience_id
    assert after.state is ProtectionState.PROTECTED


def test_protection_does_not_generate_replacement_identity():
    identity = new_identity()

    protection = ExperienceProtection.protected(identity)

    assert protection.experience_id is identity


def test_protection_is_immutable():
    protection = ExperienceProtection.protected(new_identity())

    with pytest.raises((AttributeError, TypeError)):
        protection.state = ProtectionState.UNPROTECTED


def test_invalid_identity_is_rejected():
    with pytest.raises(InvalidProtectionIdentityError):
        ExperienceProtection.protected("not-an-experience-id")


def test_unprotected_experience_allows_ordinary_mutation_gate():
    protection = ExperienceProtection.unprotected(new_identity())

    protection.require_mutation_allowed()


def test_protected_experience_rejects_ordinary_mutation():
    protection = ExperienceProtection.protected(new_identity())

    with pytest.raises(ProtectedExperienceMutationError):
        protection.require_mutation_allowed()


def test_protected_operation_requires_explicit_authorization():
    protection = ExperienceProtection.protected(new_identity())

    with pytest.raises(UnauthorizedExperienceOperationError):
        protection.require_authorized(authorized=False)


def test_explicit_authorization_allows_protected_operation_gate():
    protection = ExperienceProtection.protected(new_identity())

    protection.require_authorized(authorized=True)


def test_persistence_is_not_implicitly_authorization():
    protection = ExperienceProtection.protected(new_identity())

    with pytest.raises(UnauthorizedExperienceOperationError):
        protection.require_authorized(authorized=False)


def test_authorization_argument_must_be_boolean():
    protection = ExperienceProtection.protected(new_identity())

    with pytest.raises(TypeError):
        protection.require_authorized(authorized="yes")
