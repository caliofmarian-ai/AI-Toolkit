from lib.python.experience.performance import (
    ExperiencePerformanceSample,
    characterize_persistent_repository,
)
from lib.python.experience.persistent_repository import (
    JsonFileExperienceRepository,
)


def test_performance_sample_is_machine_inspectable(tmp_path):
    sample = characterize_persistent_repository(
        tmp_path / "experience.json",
        experience_count=3,
    )

    payload = sample.to_dict()

    assert set(payload) == {
        "experience_count",
        "add_seconds",
        "contains_seconds",
        "get_seconds",
        "save_seconds",
        "total_seconds",
        "store_bytes",
    }

    assert payload["experience_count"] == 3
    assert payload["store_bytes"] > 0


def test_characterization_exercises_real_persistent_repository(tmp_path):
    path = tmp_path / "experience.json"

    sample = characterize_persistent_repository(
        path,
        experience_count=5,
    )

    repository = JsonFileExperienceRepository(path)

    assert sample.experience_count == 5
    assert path.exists()
    assert sample.store_bytes == path.stat().st_size

    store = repository._read_store()

    assert len(store["experiences"]) == 5


def test_characterization_preserves_experience_identity_and_state(tmp_path):
    path = tmp_path / "experience.json"

    characterize_persistent_repository(
        path,
        experience_count=4,
    )

    repository = JsonFileExperienceRepository(path)
    store = repository._read_store()

    assert len(store["experiences"]) == 4

    for identity, representation in store["experiences"].items():
        recovered = repository.get(
            __import__(
                "lib.python.experience.identity",
                fromlist=["ExperienceId"],
            ).ExperienceId.from_string(identity)
        )

        assert str(recovered.experience_id) == identity
        assert recovered.state.value == "ACTIVE"
        assert representation["state"] == "ACTIVE"


def test_characterization_reports_non_negative_durations(tmp_path):
    sample = characterize_persistent_repository(
        tmp_path / "experience.json",
        experience_count=2,
    )

    assert sample.add_seconds >= 0
    assert sample.contains_seconds >= 0
    assert sample.get_seconds >= 0
    assert sample.save_seconds >= 0
    assert sample.total_seconds >= 0


def test_characterization_rejects_invalid_workload_size(tmp_path):
    path = tmp_path / "experience.json"

    for value in (0, -1, True, 1.5, "10", None):
        try:
            characterize_persistent_repository(
                path,
                experience_count=value,
            )
        except ValueError:
            pass
        else:
            raise AssertionError(
                f"invalid experience_count accepted: {value!r}"
            )


def test_store_size_grows_with_real_persisted_population(tmp_path):
    small = characterize_persistent_repository(
        tmp_path / "small.json",
        experience_count=2,
    )

    larger = characterize_persistent_repository(
        tmp_path / "larger.json",
        experience_count=8,
    )

    assert larger.experience_count > small.experience_count
    assert larger.store_bytes > small.store_bytes


def test_performance_evidence_does_not_encode_machine_specific_threshold():
    fields = ExperiencePerformanceSample.__dataclass_fields__

    assert "max_seconds" not in fields
    assert "deadline" not in fields
    assert "production_threshold" not in fields
