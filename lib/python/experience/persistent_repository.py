"""File-backed repository for PCC-01 Persistent Experience.

This repository implements the established ExperienceRepository
contract using a JSON file as a persistence substrate.

The JSON file is storage.
It is not Experience.
Its existence does not create authority.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .identity import ExperienceId
from .model import Experience
from .persistence import (
    ExperiencePersistenceError,
    ExperienceRecoveryError,
    recover_experience,
    serialize_experience,
)
from .repository import (
    ExperienceAlreadyExistsError,
    ExperienceNotFoundError,
    ExperienceRepository,
    ExperienceRepositoryError,
)


class PersistentExperienceRepositoryError(ExperienceRepositoryError):
    """Base error for persistent Experience repository failures."""


class ExperienceStoreCorruptionError(PersistentExperienceRepositoryError):
    """Raised when the persisted store cannot be trusted or recovered."""


class JsonFileExperienceRepository(ExperienceRepository):
    """JSON-backed Experience repository.

    The repository persists Experience state beyond object lifetime.

    RUN 016 verifies recovery using independent repository instances.
    It does NOT claim real process-death continuity.
    """

    _FORMAT_VERSION = 1

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

        if self._path.exists() and self._path.is_dir():
            raise PersistentExperienceRepositoryError(
                f"Experience store path is a directory: {self._path}"
            )

    @property
    def path(self) -> Path:
        return self._path

    def add(self, experience: Experience) -> None:
        store = self._read_store()

        key = str(experience.experience_id)

        if key in store["experiences"]:
            raise ExperienceAlreadyExistsError(
                f"Experience already exists: {experience.experience_id}"
            )

        store["experiences"][key] = serialize_experience(experience)
        self._write_store(store)

    def get(self, experience_id: ExperienceId) -> Experience:
        _require_experience_id(experience_id)

        store = self._read_store()
        key = str(experience_id)

        try:
            representation = store["experiences"][key]
        except KeyError as exc:
            raise ExperienceNotFoundError(
                f"Experience not found: {experience_id}"
            ) from exc

        try:
            recovered = recover_experience(representation)
        except ExperiencePersistenceError as exc:
            raise ExperienceStoreCorruptionError(
                f"Persisted Experience is corrupt: {experience_id}"
            ) from exc

        if recovered.experience_id != experience_id:
            raise ExperienceStoreCorruptionError(
                "persisted Experience identity does not match repository key"
            )

        return recovered

    def save(self, experience: Experience) -> None:
        store = self._read_store()

        key = str(experience.experience_id)

        if key not in store["experiences"]:
            raise ExperienceNotFoundError(
                f"Cannot save unknown Experience: {experience.experience_id}"
            )

        store["experiences"][key] = serialize_experience(experience)
        self._write_store(store)

    def contains(self, experience_id: ExperienceId) -> bool:
        _require_experience_id(experience_id)

        store = self._read_store()

        return str(experience_id) in store["experiences"]

    def _empty_store(self) -> dict[str, Any]:
        return {
            "format_version": self._FORMAT_VERSION,
            "experiences": {},
        }

    def _read_store(self) -> dict[str, Any]:
        if not self._path.exists():
            return self._empty_store()

        try:
            raw = self._path.read_text(encoding="utf-8")
        except OSError as exc:
            raise PersistentExperienceRepositoryError(
                f"cannot read Experience store: {self._path}"
            ) from exc

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ExperienceStoreCorruptionError(
                "Experience store contains invalid JSON"
            ) from exc

        if not isinstance(data, dict):
            raise ExperienceStoreCorruptionError(
                "Experience store root must be an object"
            )

        if set(data.keys()) != {"format_version", "experiences"}:
            raise ExperienceStoreCorruptionError(
                "Experience store has invalid top-level fields"
            )

        if data["format_version"] != self._FORMAT_VERSION:
            raise ExperienceStoreCorruptionError(
                "Experience store format version is unsupported"
            )

        experiences = data["experiences"]

        if not isinstance(experiences, dict):
            raise ExperienceStoreCorruptionError(
                "Experience store experiences field must be an object"
            )

        for key, representation in experiences.items():
            if not isinstance(key, str):
                raise ExperienceStoreCorruptionError(
                    "Experience store identity key must be a string"
                )

            try:
                recovered = recover_experience(representation)
            except ExperienceRecoveryError as exc:
                raise ExperienceStoreCorruptionError(
                    f"invalid persisted Experience entry: {key}"
                ) from exc

            if str(recovered.experience_id) != key:
                raise ExperienceStoreCorruptionError(
                    "Experience store key and embedded identity disagree"
                )

        return data

    def _write_store(self, store: dict[str, Any]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)

        payload = json.dumps(
            store,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        ) + "\n"

        fd: int | None = None
        temporary_path: Path | None = None

        try:
            fd, temporary_name = tempfile.mkstemp(
                prefix=f".{self._path.name}.",
                suffix=".tmp",
                dir=str(self._path.parent),
                text=True,
            )

            temporary_path = Path(temporary_name)

            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                fd = None
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())

            os.replace(temporary_path, self._path)

        except OSError as exc:
            raise PersistentExperienceRepositoryError(
                f"cannot write Experience store: {self._path}"
            ) from exc

        finally:
            if fd is not None:
                os.close(fd)

            if temporary_path is not None and temporary_path.exists():
                try:
                    temporary_path.unlink()
                except OSError:
                    pass


def _require_experience_id(value: ExperienceId) -> ExperienceId:
    if not isinstance(value, ExperienceId):
        raise TypeError("experience_id must be an ExperienceId")

    return value
