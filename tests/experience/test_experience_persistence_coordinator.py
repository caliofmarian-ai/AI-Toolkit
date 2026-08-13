from datetime import datetime, timezone

import pytest

from lib.python.experience.identity import ExperienceId
from lib.python.experience.lifecycle import ExperienceState
from lib.python.experience.model import Experience
from lib.python.experience.persistence_coordinator import (
    CoordinationStage,
    ExperiencePersistenceCoordinator,
    PersistenceCoordinationIdentityError,
    PersistenceCoordinationStateError,
)
from lib.python.experience.persistent_repository import (
    JsonFileExperienceRepository,
)
from lib.python.experience.protection import (
    ExperienceProtection,
    ProtectionState,
)
from lib.python.experience.protection_repository import (
    JsonFileProtectionRepository,
)


def make_experience(experience_id=None):
    return Experience(
        experience_id=experience_id or Experience.create().experience_id,
        created_at=datetime.now(timezone.utc),
        state=ExperienceState.ACTIVE,
    )


def make_coordinator(tmp_path):
    experience_repository = JsonFileExperienceRepository(
        tmp_path / "experiences.json"
    )
    protection_repository = JsonFileProtectionRepository(
        tmp_path / "protections.json"
    )

    coordinator = ExperiencePersistenceCoordinator(
        experience_repository,
        protection_repository,
    )

    return (
        coordinator,
        experience_repository,
        protection_repository,
    )


def test_coordinator_persists_distinct_organs(tmp_path):
    coordinator, experience_repository, protection_repository = (
        make_coordinator(tmp_path)
    )

    experience = make_experience()
    protection = ExperienceProtection.protected(
        experience.experience_id
    )

    result = coordinator.persist(experience, protection)

    assert experience_repository.contains(
        experience.experience_id
    )
    assert protection_repository.contains(
        experience.experience_id
    )

    assert result.experience.experience_id == experience.experience_id
    assert result.protection.experience_id == experience.experience_id
    assert result.protection.state is ProtectionState.PROTECTED


def test_coordination_exposes_ordered_physiological_stages(tmp_path):
    coordinator, _, _ = make_coordinator(tmp_path)

    experience = make_experience()
    protection = ExperienceProtection.protected(
        experience.experience_id
    )

    observed = []

    coordinator.persist(
        experience,
        protection,
        observe_stage=observed.append,
    )

    assert [state.stage for state in observed] == [
        CoordinationStage.PREPARING,
        CoordinationStage.PROTECTION_WRITTEN,
        CoordinationStage.EXPERIENCE_WRITTEN,
        CoordinationStage.COMPLETE,
    ]

    assert all(
        state.experience_id == experience.experience_id
        for state in observed
    )


def test_coordinator_rejects_identity_disagreement(tmp_path):
    coordinator, _, _ = make_coordinator(tmp_path)

    experience = make_experience()

    protection = ExperienceProtection.protected(
        Experience.create().experience_id
    )

    with pytest.raises(PersistenceCoordinationIdentityError):
        coordinator.persist(experience, protection)


def test_recovery_rejects_missing_pair(tmp_path):
    coordinator, _, _ = make_coordinator(tmp_path)

    with pytest.raises(
        PersistenceCoordinationStateError,
        match="no durable",
    ):
        coordinator.recover(Experience.create().experience_id)


def test_recovery_rejects_experience_without_protection(tmp_path):
    coordinator, experience_repository, _ = make_coordinator(tmp_path)

    experience = make_experience()

    experience_repository.add(experience)

    with pytest.raises(
        PersistenceCoordinationStateError,
        match="Protection is missing",
    ):
        coordinator.recover(experience.experience_id)


def test_recovery_rejects_orphan_protection(tmp_path):
    coordinator, _, protection_repository = make_coordinator(tmp_path)

    experience_id = Experience.create().experience_id

    protection_repository.add(
        ExperienceProtection.protected(experience_id)
    )

    with pytest.raises(
        PersistenceCoordinationStateError,
        match="orphan Protection",
    ):
        coordinator.recover(experience_id)


def test_recovery_preserves_identity_and_protection(tmp_path):
    coordinator, _, _ = make_coordinator(tmp_path)

    experience = make_experience()
    protection = ExperienceProtection.protected(
        experience.experience_id
    )

    coordinator.persist(experience, protection)

    recovered = coordinator.recover(
        experience.experience_id
    )

    assert (
        recovered.experience.experience_id
        == experience.experience_id
    )
    assert (
        recovered.protection.experience_id
        == experience.experience_id
    )
    assert recovered.protection.is_protected


def test_persistence_does_not_supply_authorization(tmp_path):
    coordinator, _, _ = make_coordinator(tmp_path)

    experience = make_experience()
    protection = ExperienceProtection.protected(
        experience.experience_id
    )

    coordinator.persist(experience, protection)

    recovered = coordinator.recover(
        experience.experience_id
    )

    with pytest.raises(Exception):
        recovered.protection.require_authorized(
            authorized=False
        )
