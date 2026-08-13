"""Repository physiology for persistent Experience Protection.

The repository stores Protection state independently from Core
Experience state while using the same ExperienceId relationship.

Storage != Experience.
Persistence != authority.
Persisted protection != authorization.
"""

from __future__ import annotations

import json
import os
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from .identity import ExperienceId
from .protection import ExperienceProtection
from .protection_persistence import (
    ProtectionPersistenceError,
    recover_protection,
    serialize_protection,
)


class ProtectionRepositoryError(RuntimeError):
    """Base error for Protection repository operations."""


class ProtectionNotFoundError(ProtectionRepositoryError):
    """Raised when no Protection record exists for an Experience."""


class ProtectionAlreadyExistsError(ProtectionRepositoryError):
    """Raised when add would replace an existing Protection record."""


class ProtectionStoreCorruptionError(ProtectionRepositoryError):
    """Raised when persisted Protection state cannot be trusted."""


class ProtectionRepository(ABC):
    """Storage-independent contract for Experience Protection."""

    @abstractmethod
    def add(self, protection: ExperienceProtection) -> None:
        """Persist a new Protection record without replacement."""

    @abstractmethod
    def get(
        self,
        experience_id: ExperienceId,
    ) -> ExperienceProtection:
        """Recover Protection associated with one Experience identity."""

    @abstractmethod
    def save(self, protection: ExperienceProtection) -> None:
        """Persist replacement state for an existing Protection record."""

    @abstractmethod
    def contains(self, experience_id: ExperienceId) -> bool:
        """Return whether Protection exists for the Experience identity."""


class JsonFileProtectionRepository(ProtectionRepository):
    """JSON-backed persistent repository for Protection state."""

    _FORMAT_VERSION = 1

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

        if self._path.exists() and self._path.is_dir():
            raise ProtectionRepositoryError(
                f"Protection store path is a directory: {self._path}"
            )

    @property
    def path(self) -> Path:
        return self._path

    def add(self, protection: ExperienceProtection) -> None:
        _require_protection(protection)

        store = self._read_store()
        key = str(protection.experience_id)

        if key in store["protections"]:
            raise ProtectionAlreadyExistsError(
                f"Protection already exists: {protection.experience_id}"
            )

        store["protections"][key] = serialize_protection(protection)
        self._write_store(store)

    def get(
        self,
        experience_id: ExperienceId,
    ) -> ExperienceProtection:
        _require_experience_id(experience_id)

        store = self._read_store()
        key = str(experience_id)

        try:
            representation = store["protections"][key]
        except KeyError as exc:
            raise ProtectionNotFoundError(
                f"Protection not found: {experience_id}"
            ) from exc

        try:
            recovered = recover_protection(representation)
        except ProtectionPersistenceError as exc:
            raise ProtectionStoreCorruptionError(
                f"Persisted Protection is corrupt: {experience_id}"
            ) from exc

        if recovered.experience_id != experience_id:
            raise ProtectionStoreCorruptionError(
                "persisted Protection identity does not match repository key"
            )

        return recovered

    def save(self, protection: ExperienceProtection) -> None:
        _require_protection(protection)

        store = self._read_store()
        key = str(protection.experience_id)

        if key not in store["protections"]:
            raise ProtectionNotFoundError(
                f"Cannot save unknown Protection: {protection.experience_id}"
            )

        store["protections"][key] = serialize_protection(protection)
        self._write_store(store)

    def contains(self, experience_id: ExperienceId) -> bool:
        _require_experience_id(experience_id)

        return str(experience_id) in self._read_store()["protections"]

    def _empty_store(self) -> dict[str, Any]:
        return {
            "format_version": self._FORMAT_VERSION,
            "protections": {},
        }

    def _read_store(self) -> dict[str, Any]:
        if not self._path.exists():
            return self._empty_store()

        try:
            raw = self._path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ProtectionRepositoryError(
                f"cannot read Protection store: {self._path}"
            ) from exc

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ProtectionStoreCorruptionError(
                "Protection store contains invalid JSON"
            ) from exc

        if not isinstance(data, dict):
            raise ProtectionStoreCorruptionError(
                "Protection store root must be an object"
            )

        if set(data.keys()) != {"format_version", "protections"}:
            raise ProtectionStoreCorruptionError(
                "Protection store has invalid top-level fields"
            )

        if data["format_version"] != self._FORMAT_VERSION:
            raise ProtectionStoreCorruptionError(
                "Protection store format version is unsupported"
            )

        protections = data["protections"]

        if not isinstance(protections, dict):
            raise ProtectionStoreCorruptionError(
                "Protection store protections field must be an object"
            )

        for key, representation in protections.items():
            if not isinstance(key, str):
                raise ProtectionStoreCorruptionError(
                    "Protection store identity key must be a string"
                )

            try:
                recovered = recover_protection(representation)
            except ProtectionPersistenceError as exc:
                raise ProtectionStoreCorruptionError(
                    f"invalid persisted Protection entry: {key}"
                ) from exc

            if str(recovered.experience_id) != key:
                raise ProtectionStoreCorruptionError(
                    "Protection store key and embedded identity disagree"
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
            raise ProtectionRepositoryError(
                f"cannot write Protection store: {self._path}"
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


def _require_protection(
    value: ExperienceProtection,
) -> ExperienceProtection:
    if not isinstance(value, ExperienceProtection):
        raise TypeError(
            "protection must be ExperienceProtection"
        )

    return value
