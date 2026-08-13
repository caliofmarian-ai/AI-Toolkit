from lib.python.experience.lifecycle import ExperienceState
from lib.python.experience.repository import InMemoryExperienceRepository
from lib.python.experience.service import ExperienceService


def test_complete_core_lifecycle_preserves_one_experience_identity():
    repository = InMemoryExperienceRepository()
    service = ExperienceService(repository)

    created = service.create_experience()
    identity = created.experience_id

    active = service.activate_experience(identity)
    inspected_active = service.get_experience(identity)
    closed = service.close_experience(identity)
    inspected_closed = service.get_experience(identity)

    assert created.state is ExperienceState.CREATED
    assert active.state is ExperienceState.ACTIVE
    assert inspected_active.state is ExperienceState.ACTIVE
    assert closed.state is ExperienceState.CLOSED
    assert inspected_closed.state is ExperienceState.CLOSED

    assert active.experience_id == identity
    assert inspected_active.experience_id == identity
    assert closed.experience_id == identity
    assert inspected_closed.experience_id == identity


def test_repository_is_storage_boundary_not_experience_identity():
    repository = InMemoryExperienceRepository()
    service = ExperienceService(repository)

    experience = service.create_experience()

    assert experience is not repository
    assert not hasattr(experience, "_experiences")


def test_core_experience_contains_no_session_memory_evidence_or_dialogue():
    repository = InMemoryExperienceRepository()
    service = ExperienceService(repository)

    experience = service.create_experience()

    forbidden = (
        "session",
        "session_id",
        "memory",
        "memory_id",
        "evidence",
        "evidence_id",
        "dialogue",
        "raw_dialogue",
        "provider",
        "process",
        "authority",
    )

    for attribute in forbidden:
        assert not hasattr(experience, attribute)
