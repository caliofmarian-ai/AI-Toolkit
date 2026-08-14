from datetime import datetime, timezone

import pytest

from lib.python.experience.forgetting import (
    ExperienceForgetting,
    ExperienceForgettingError,
    ForgettingState,
    InvalidForgettingReasonError,
    UnauthorizedForgettingError,
)
from lib.python.experience.model import Experience
from lib.python.experience.retention import ExperienceRetention


def test_new_forgetting_state_is_explicitly_present():
    experience = Experience.create()

    forgetting = ExperienceForgetting.present(
        experience.experience_id
    )

    assert forgetting.experience_id == experience.experience_id
    assert forgetting.state is ForgettingState.PRESENT
    assert forgetting.is_forgotten is False
    assert forgetting.reason is None
    assert forgetting.forgotten_at is None


def test_forgetting_requires_explicit_authorization():
    experience = Experience.create()

    forgetting = ExperienceForgetting.present(
        experience.experience_id
    )

    with pytest.raises(UnauthorizedForgettingError):
        forgetting.forget(
            reason="authorized forgetting required",
            authorized=False,
        )


def test_forgetting_requires_explicit_reason():
    experience = Experience.create()

    forgetting = ExperienceForgetting.present(
        experience.experience_id
    )

    with pytest.raises(InvalidForgettingReasonError):
        forgetting.forget(
            reason="",
            authorized=True,
        )


def test_forgetting_preserves_experience_identity():
    experience = Experience.create()
    before = experience.experience_id

    forgetting = ExperienceForgetting.present(
        before
    ).forget(
        reason="explicit owner-authorized forgetting",
        authorized=True,
    )

    assert forgetting.experience_id == before
    assert experience.experience_id == before
    assert forgetting.is_forgotten is True


def test_forgetting_time_is_explicit_and_timezone_aware():
    experience = Experience.create()

    moment = datetime(
        2026,
        8,
        14,
        13,
        0,
        tzinfo=timezone.utc,
    )

    forgetting = ExperienceForgetting.present(
        experience.experience_id
    ).forget(
        reason="controlled forgetting examination",
        authorized=True,
        forgotten_at=moment,
    )

    assert forgetting.forgotten_at == moment
    assert forgetting.forgotten_at.tzinfo is not None


def test_same_forgetting_operation_is_idempotent():
    experience = Experience.create()

    forgotten = ExperienceForgetting.present(
        experience.experience_id
    ).forget(
        reason="same forgetting rule",
        authorized=True,
    )

    repeated = forgotten.forget(
        reason="same forgetting rule",
        authorized=True,
    )

    assert repeated is forgotten


def test_forgetting_reason_cannot_be_silently_rewritten():
    experience = Experience.create()

    forgotten = ExperienceForgetting.present(
        experience.experience_id
    ).forget(
        reason="original reason",
        authorized=True,
    )

    with pytest.raises(ExperienceForgettingError):
        forgotten.forget(
            reason="replacement reason",
            authorized=True,
        )


def test_retention_and_forgetting_are_distinct_organs():
    experience = Experience.create()

    retention = ExperienceRetention.unretained(
        experience.experience_id
    ).retain(
        reason="retention examination"
    )

    forgetting = ExperienceForgetting.present(
        experience.experience_id
    )

    assert retention.experience_id == forgetting.experience_id
    assert retention.is_retained is True
    assert forgetting.is_forgotten is False
    assert type(retention) is not type(forgetting)


def test_forgetting_does_not_mutate_experience_body():
    experience = Experience.create()

    before = (
        experience.experience_id,
        experience.created_at,
        experience.state,
    )

    ExperienceForgetting.present(
        experience.experience_id
    ).forget(
        reason="external forgetting physiology",
        authorized=True,
    )

    after = (
        experience.experience_id,
        experience.created_at,
        experience.state,
    )

    assert after == before
