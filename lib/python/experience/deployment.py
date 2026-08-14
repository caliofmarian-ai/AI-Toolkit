"""Deployment boundary for PCC-01 Persistent Experience.

This organ translates deployment configuration into a durable Experience
repository location.

Deployment != Experience.
Deployment != Memory.
Deployment != authority.

The persistent location is explicit so a production runtime may bind PCC-01
to durable storage supplied by its deployment environment.
"""

from __future__ import annotations

import os
from pathlib import Path

from .persistent_repository import JsonFileExperienceRepository


DEFAULT_EXPERIENCE_STORE = ".ai/runtime/state/experience.json"
EXPERIENCE_STORE_ENV = "PCC01_EXPERIENCE_STORE"


class ExperienceDeploymentConfigurationError(RuntimeError):
    """Raised when PCC-01 deployment storage cannot be prepared."""


def experience_store_path(
    *,
    environment: dict[str, str] | None = None,
    repository_root: str | Path | None = None,
) -> Path:
    """Resolve the durable Experience store for this deployment.

    PCC01_EXPERIENCE_STORE may be absolute or relative.

    Relative paths are anchored to AI_TOOLKIT_REPOSITORY_ROOT when supplied,
    matching the existing runtime deployment boundary.
    """

    env = os.environ if environment is None else environment

    configured = env.get(
        EXPERIENCE_STORE_ENV,
        DEFAULT_EXPERIENCE_STORE,
    ).strip()

    if not configured:
        raise ExperienceDeploymentConfigurationError(
            "PCC-01 Experience store path cannot be empty"
        )

    path = Path(configured).expanduser()

    if path.is_absolute():
        return path

    if repository_root is None:
        root_value = env.get(
            "AI_TOOLKIT_REPOSITORY_ROOT",
            os.getcwd(),
        )
        root = Path(root_value)
    else:
        root = Path(repository_root)

    return root / path


def prepare_experience_repository(
    *,
    environment: dict[str, str] | None = None,
    repository_root: str | Path | None = None,
) -> JsonFileExperienceRepository:
    """Prepare the persistent Experience repository for deployment."""

    path = experience_store_path(
        environment=environment,
        repository_root=repository_root,
    )

    try:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
    except OSError as exc:
        raise ExperienceDeploymentConfigurationError(
            f"cannot prepare PCC-01 persistence directory: {path.parent}"
        ) from exc

    if path.exists() and path.is_dir():
        raise ExperienceDeploymentConfigurationError(
            f"PCC-01 Experience store must be a file path: {path}"
        )

    return JsonFileExperienceRepository(path)
