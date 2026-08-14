from datetime import datetime, timezone

from lib.python.experience.model import Experience
from lib.python.experience.retention import (
    ExperienceRetention,
    RetentionState,
)
from lib.python.experience.retention_persistence import (
    ExperienceRetentionRepository,
)


def test_retention_survives_repository_reconstruction(tmp_path):
    experience = Experience.create()
    experience_id = experience.experience_id

    retained_at = datetime(
        2026,
        8,
        14,
        12,
        30,
        tzinfo=timezone.utc,
    )

    before = ExperienceRetention.unretained(
        experience_id
    ).retain(
        reason="restart-surviving retention",
        retained_at=retained_at,
    )

    repository_a = ExperienceRetentionRepository(
        tmp_path
    )
    repository_a.save(before)

    del repository_a

    repository_b = ExperienceRetentionRepository(
        tmp_path
    )
    after = repository_b.load(experience_id)

    assert after.experience_id == experience_id
    assert after.state is RetentionState.RETAINED
    assert after.reason == before.reason
    assert after.retained_at == retained_at
    assert repository_b.contains(experience_id)


def test_unretained_state_is_durably_distinguishable_from_loss(
    tmp_path,
):
    experience = Experience.create()

    before = ExperienceRetention.unretained(
        experience.experience_id
    )

    repository_a = ExperienceRetentionRepository(
        tmp_path
    )
    repository_a.save(before)

    repository_b = ExperienceRetentionRepository(
        tmp_path
    )
    after = repository_b.load(
        experience.experience_id
    )

    assert after.state is RetentionState.UNRETAINED
    assert after.is_retained is False
    assert repository_b.contains(
        experience.experience_id
    )


def test_retention_persistence_does_not_change_identity(
    tmp_path,
):
    experience = Experience.create()
    before_id = experience.experience_id

    retention = ExperienceRetention.unretained(
        before_id
    ).retain(
        reason="identity conservation"
    )

    repository = ExperienceRetentionRepository(
        tmp_path
    )
    repository.save(retention)

    recovered = repository.load(before_id)

    assert recovered.experience_id == before_id
    assert experience.experience_id == before_id
