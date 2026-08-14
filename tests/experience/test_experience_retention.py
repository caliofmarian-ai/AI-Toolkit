from datetime import datetime, timezone

import pytest

from lib.python.experience.model import Experience
from lib.python.experience.retention import (
    ExperienceRetention,
    ExperienceRetentionError,
    InvalidRetentionReasonError,
    RetentionState,
)


def test_new_retention_state_is_explicitly_unretained():
    experience = Experience.create()

    retention = ExperienceRetention.unretained(
        experience.experience_id
    )

    assert retention.experience_id == experience.experience_id
    assert retention.state is RetentionState.UNRETAINED
    assert retention.is_retained is False
    assert retention.reason is None
    assert retention.retained_at is None


def test_retention_preserves_experience_identity():
    experience = Experience.create()
    before = experience.experience_id

    retention = ExperienceRetention.unretained(
        before
    ).retain(
        reason="preserve accepted historical experience"
    )

    assert retention.experience_id == before
    assert experience.experience_id == before
    assert retention.is_retained is True


def test_retention_requires_explicit_reason():
    experience = Experience.create()

    retention = ExperienceRetention.unretained(
        experience.experience_id
    )

    with pytest.raises(InvalidRetentionReasonError):
        retention.retain(reason="")

    with pytest.raises(InvalidRetentionReasonError):
        retention.retain(reason="   ")


def test_retention_time_is_observable_and_timezone_aware():
    experience = Experience.create()

    retained_at = datetime(
        2026,
        8,
        14,
        12,
        0,
        tzinfo=timezone.utc,
    )

    retention = ExperienceRetention.unretained(
        experience.experience_id
    ).retain(
        reason="explicit retention examination",
        retained_at=retained_at,
    )

    assert retention.retained_at == retained_at
    assert retention.retained_at.tzinfo is not None


def test_retention_is_idempotent_for_same_explicit_rule():
    experience = Experience.create()

    retained = ExperienceRetention.unretained(
        experience.experience_id
    ).retain(
        reason="same retention rule"
    )

    repeated = retained.retain(
        reason="same retention rule"
    )

    assert repeated is retained


def test_retention_reason_cannot_be_silently_rewritten():
    experience = Experience.create()

    retained = ExperienceRetention.unretained(
        experience.experience_id
    ).retain(
        reason="original retention reason"
    )

    with pytest.raises(ExperienceRetentionError):
        retained.retain(
            reason="replacement reason"
        )


def test_retention_does_not_mutate_experience_body():
    experience = Experience.create()

    before = (
        experience.experience_id,
        experience.created_at,
        experience.state,
    )

    ExperienceRetention.unretained(
        experience.experience_id
    ).retain(
        reason="external retention physiology"
    )

    after = (
        experience.experience_id,
        experience.created_at,
        experience.state,
    )

    assert after == before
