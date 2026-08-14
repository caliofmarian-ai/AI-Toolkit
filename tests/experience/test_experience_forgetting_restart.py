from datetime import datetime, timezone

import pytest

from lib.python.experience.forgetting import (
    ExperienceForgetting,
    ForgettingState,
)
from lib.python.experience.forgetting_persistence import (
    ExperienceForgettingNotFoundError,
    ExperienceForgettingRepository,
)
from lib.python.experience.model import Experience


def test_explicit_forgetting_survives_repository_reconstruction(
    tmp_path,
):
    experience = Experience.create()
    experience_id = experience.experience_id

    moment = datetime(
        2026,
        8,
        14,
        13,
        30,
        tzinfo=timezone.utc,
    )

    before = ExperienceForgetting.present(
        experience_id
    ).forget(
        reason="restart-surviving forgetting",
        authorized=True,
        forgotten_at=moment,
    )

    repository_a = ExperienceForgettingRepository(
        tmp_path
    )
    repository_a.save(before)

    del repository_a

    repository_b = ExperienceForgettingRepository(
        tmp_path
    )
    after = repository_b.load(experience_id)

    assert after.experience_id == experience_id
    assert after.state is ForgettingState.FORGOTTEN
    assert after.reason == before.reason
    assert after.forgotten_at == moment
    assert repository_b.contains(experience_id)


def test_missing_record_is_not_fabricated_as_forgetting(
    tmp_path,
):
    experience = Experience.create()

    repository = ExperienceForgettingRepository(
        tmp_path
    )

    assert repository.contains(
        experience.experience_id
    ) is False

    with pytest.raises(
        ExperienceForgettingNotFoundError
    ):
        repository.load(
            experience.experience_id
        )


def test_present_state_is_distinct_from_missing_record(
    tmp_path,
):
    experience = Experience.create()

    present = ExperienceForgetting.present(
        experience.experience_id
    )

    repository = ExperienceForgettingRepository(
        tmp_path
    )
    repository.save(present)

    recovered = repository.load(
        experience.experience_id
    )

    assert recovered.state is ForgettingState.PRESENT
    assert recovered.is_forgotten is False
    assert repository.contains(
        experience.experience_id
    ) is True


def test_forgetting_recovery_preserves_identity(
    tmp_path,
):
    experience = Experience.create()
    before_id = experience.experience_id

    forgotten = ExperienceForgetting.present(
        before_id
    ).forget(
        reason="identity conservation",
        authorized=True,
    )

    repository = ExperienceForgettingRepository(
        tmp_path
    )
    repository.save(forgotten)

    recovered = repository.load(before_id)

    assert recovered.experience_id == before_id
    assert experience.experience_id == before_id
