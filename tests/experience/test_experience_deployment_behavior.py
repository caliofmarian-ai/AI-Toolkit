from lib.python.experience.deployment import (
    DEFAULT_EXPERIENCE_STORE,
    EXPERIENCE_STORE_ENV,
    ExperienceDeploymentConfigurationError,
    experience_store_path,
    prepare_experience_repository,
)
from lib.python.experience.model import Experience
from lib.python.experience.persistent_repository import (
    JsonFileExperienceRepository,
)


def test_default_deployment_store_uses_runtime_state_boundary(tmp_path):
    path = experience_store_path(
        environment={},
        repository_root=tmp_path,
    )

    assert path == tmp_path / DEFAULT_EXPERIENCE_STORE
    assert path == tmp_path / ".ai/runtime/state/experience.json"


def test_deployment_store_can_be_bound_to_external_durable_location(
    tmp_path,
):
    durable = tmp_path / "mounted-volume" / "pcc01.json"

    path = experience_store_path(
        environment={
            EXPERIENCE_STORE_ENV: str(durable),
        },
        repository_root=tmp_path / "repository",
    )

    assert path == durable


def test_relative_deployment_store_uses_repository_root_environment(
    tmp_path,
):
    root = tmp_path / "repository"

    path = experience_store_path(
        environment={
            "AI_TOOLKIT_REPOSITORY_ROOT": str(root),
            EXPERIENCE_STORE_ENV: "durable/experience.json",
        }
    )

    assert path == root / "durable/experience.json"


def test_prepare_creates_required_parent_anatomy(tmp_path):
    root = tmp_path / "repository"

    repository = prepare_experience_repository(
        environment={},
        repository_root=root,
    )

    assert isinstance(
        repository,
        JsonFileExperienceRepository,
    )
    assert (root / ".ai/runtime/state").is_dir()


def test_experience_survives_repository_reconstruction(tmp_path):
    durable = tmp_path / "volume" / "experience.json"

    environment = {
        EXPERIENCE_STORE_ENV: str(durable),
    }

    first_process = prepare_experience_repository(
        environment=environment,
    )

    experience = Experience.create()
    first_process.add(experience)

    original_identity = experience.experience_id

    del first_process

    second_process = prepare_experience_repository(
        environment=environment,
    )

    recovered = second_process.get(original_identity)

    assert recovered.experience_id == original_identity
    assert second_process.contains(original_identity)


def test_active_state_survives_repository_reconstruction(tmp_path):
    durable = tmp_path / "volume" / "experience.json"
    environment = {
        EXPERIENCE_STORE_ENV: str(durable),
    }

    process_a = prepare_experience_repository(
        environment=environment,
    )

    experience = Experience.create().activate()
    process_a.add(experience)

    identity = experience.experience_id

    del process_a

    process_b = prepare_experience_repository(
        environment=environment,
    )

    recovered = process_b.get(identity)

    assert recovered.experience_id == identity
    assert recovered.state.value == "ACTIVE"


def test_repeated_deployment_preparation_is_idempotent(tmp_path):
    environment = {
        EXPERIENCE_STORE_ENV: str(
            tmp_path / "volume" / "experience.json"
        )
    }

    first = prepare_experience_repository(
        environment=environment,
    )
    second = prepare_experience_repository(
        environment=environment,
    )

    assert isinstance(first, JsonFileExperienceRepository)
    assert isinstance(second, JsonFileExperienceRepository)


def test_empty_store_configuration_is_rejected(tmp_path):
    try:
        experience_store_path(
            environment={
                EXPERIENCE_STORE_ENV: "   ",
            },
            repository_root=tmp_path,
        )
    except ExperienceDeploymentConfigurationError:
        pass
    else:
        raise AssertionError(
            "empty deployment store configuration accepted"
        )


def test_directory_cannot_be_used_as_experience_store(tmp_path):
    store = tmp_path / "volume"
    store.mkdir()

    try:
        prepare_experience_repository(
            environment={
                EXPERIENCE_STORE_ENV: str(store),
            }
        )
    except ExperienceDeploymentConfigurationError:
        pass
    else:
        raise AssertionError(
            "directory accepted as Experience persistence file"
        )


def test_deployment_configuration_does_not_redefine_experience(tmp_path):
    environment = {
        EXPERIENCE_STORE_ENV: str(
            tmp_path / "volume-a" / "experience.json"
        )
    }

    repository = prepare_experience_repository(
        environment=environment,
    )

    experience = Experience.create()
    identity = experience.experience_id

    repository.add(experience)

    assert repository.get(identity).experience_id == identity
    assert experience.experience_id == identity
