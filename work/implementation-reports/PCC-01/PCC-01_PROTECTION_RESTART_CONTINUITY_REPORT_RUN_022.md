# PCC-01 — PROTECTION CONTINUITY ACROSS REAL PROCESS RESTART — RUN 022

**Purpose:** Demonstrate whether Experience protection state survives persistence, real process death, new process startup, and recovery without converting persistence into authority.

**Expected baseline:** `058e12c3ebd753eb43d47e40714a4ce21011c5d5`

**Git conservation:** NONE

---

## 1. Baseline

```text
Expected:    058e12c3ebd753eb43d47e40714a4ce21011c5d5
LOCAL:       058e12c3ebd753eb43d47e40714a4ce21011c5d5
origin/main: 058e12c3ebd753eb43d47e40714a4ce21011c5d5
PASS: baseline
```

## 2. Existing Anatomy

```text
lib/python/experience/protection.py
lib/python/experience/persistence.py
lib/python/experience/persistent_repository.py
lib/python/experience/model.py
```

## 3. Existing Protection API

```python
"""Protection physiology for Persistent Experience.

Protection is an explicit domain organ.

It does not make persistence authoritative.
It does not replace lifecycle.
It does not replace retention or forgetting.
It does not derive authority from storage.

Its responsibility is to make the protection condition of an
Experience explicit and to reject operations that violate that
condition.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .identity import ExperienceId


class ExperienceProtectionError(Exception):
    """Base error for Experience protection violations."""


class InvalidProtectionIdentityError(ExperienceProtectionError):
    """Raised when protection is requested for an invalid Experience identity."""


class ProtectedExperienceMutationError(ExperienceProtectionError):
    """Raised when a protected Experience is subjected to prohibited mutation."""


class UnauthorizedExperienceOperationError(ExperienceProtectionError):
    """Raised when an operation lacks explicit authorization."""


class ProtectionState(str, Enum):
    """Observable protection condition of an Experience."""

    UNPROTECTED = "unprotected"
    PROTECTED = "protected"


@dataclass(frozen=True, slots=True)
class ExperienceProtection:
    """Protection state associated with exactly one Experience identity.

    The protector references the Experience identity but does not own
    or replace that identity.

    Protection is deliberately distinct from persistence and authority.
    """

    experience_id: ExperienceId
    state: ProtectionState

    @classmethod
    def unprotected(
        cls,
        experience_id: ExperienceId,
    ) -> "ExperienceProtection":
        return cls(
            experience_id=_require_experience_id(experience_id),
            state=ProtectionState.UNPROTECTED,
        )

    @classmethod
    def protected(
        cls,
        experience_id: ExperienceId,
    ) -> "ExperienceProtection":
        return cls(
            experience_id=_require_experience_id(experience_id),
            state=ProtectionState.PROTECTED,
        )

    @property
    def is_protected(self) -> bool:
        return self.state is ProtectionState.PROTECTED

    def protect(self) -> "ExperienceProtection":
        """Return the protected condition without changing identity."""

        if self.is_protected:
            return self

        return ExperienceProtection(
            experience_id=self.experience_id,
            state=ProtectionState.PROTECTED,
        )

    def require_mutation_allowed(self) -> None:
        """Reject ordinary mutation while the Experience is protected."""

        if self.is_protected:
            raise ProtectedExperienceMutationError(
                "protected Experience cannot be mutated by an ordinary operation"
            )

    def require_authorized(self, *, authorized: bool) -> None:
        """Require explicit authorization for a protected operation.

        Persistence itself never supplies this authorization.
        """

        if not isinstance(authorized, bool):
            raise TypeError("authorized must be bool")

        if self.is_protected and not authorized:
            raise UnauthorizedExperienceOperationError(
                "operation on protected Experience requires explicit authorization"
            )


def _require_experience_id(value: ExperienceId) -> ExperienceId:
    """Validate the identity consumed by the Protection organ."""

    if not isinstance(value, ExperienceId):
        raise InvalidProtectionIdentityError(
            "experience_id must be an ExperienceId"
        )

    return value
```

## 4. Existing Persistence API

```python
"""Serialization boundary for PCC-01 Persistent Experience.

Serialization is a transport/storage representation of Experience.

Storage != Experience.
Persistence != authority.
Interpretation != historical fact.

Recovery must reconstruct the persisted Experience identity.
It must never generate a replacement identity.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping

from .identity import ExperienceId, ExperienceIdentityError
from .lifecycle import ExperienceState
from .model import Experience


class ExperiencePersistenceError(RuntimeError):
    """Base error for Experience persistence representation failures."""


class ExperienceSerializationError(ExperiencePersistenceError):
    """Raised when an Experience cannot be serialized safely."""


class ExperienceRecoveryError(ExperiencePersistenceError):
    """Raised when persisted Experience data cannot be recovered safely."""


_REQUIRED_FIELDS = frozenset(
    {
        "experience_id",
        "created_at",
        "state",
    }
)


def serialize_experience(experience: Experience) -> dict[str, str]:
    """Serialize exactly the minimum Core Experience state."""

    if not isinstance(experience, Experience):
        raise ExperienceSerializationError(
            "serialize_experience requires an Experience"
        )

    return {
        "experience_id": str(experience.experience_id),
        "created_at": experience.created_at.isoformat(),
        "state": experience.state.value,
    }


def recover_experience(data: Mapping[str, Any]) -> Experience:
    """Recover one existing Experience without regenerating identity."""

    if not isinstance(data, Mapping):
        raise ExperienceRecoveryError(
            "persisted Experience representation must be a mapping"
        )

    fields = frozenset(data.keys())

    if fields != _REQUIRED_FIELDS:
        missing = sorted(_REQUIRED_FIELDS - fields)
        unexpected = sorted(fields - _REQUIRED_FIELDS)

        raise ExperienceRecoveryError(
            "invalid persisted Experience fields; "
            f"missing={missing}, unexpected={unexpected}"
        )

    experience_id_raw = data["experience_id"]
    created_at_raw = data["created_at"]
    state_raw = data["state"]

    if not isinstance(experience_id_raw, str):
        raise ExperienceRecoveryError(
            "persisted experience_id must be a string"
        )

    if not isinstance(created_at_raw, str):
        raise ExperienceRecoveryError(
            "persisted created_at must be a string"
        )

    if not isinstance(state_raw, str):
        raise ExperienceRecoveryError(
            "persisted state must be a string"
        )

    try:
        experience_id = ExperienceId.from_string(experience_id_raw)
    except ExperienceIdentityError as exc:
        raise ExperienceRecoveryError(
            "persisted Experience identity is invalid"
        ) from exc

    try:
        created_at = datetime.fromisoformat(created_at_raw)
    except ValueError as exc:
        raise ExperienceRecoveryError(
            "persisted created_at is invalid"
        ) from exc

    if created_at.tzinfo is None:
        raise ExperienceRecoveryError(
            "persisted created_at must be timezone-aware"
        )

    try:
        state = ExperienceState(state_raw)
    except ValueError as exc:
        raise ExperienceRecoveryError(
            "persisted Experience state is invalid"
        ) from exc

    return Experience(
        experience_id=experience_id,
        created_at=created_at,
        state=state,
    )
```

## 5. Existing Persistent Repository API

```python
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
```

## 6. Public Structural Index

```text
[Protection]
ExperienceProtectionError
InvalidProtectionIdentityError
ProtectedExperienceMutationError
UnauthorizedExperienceOperationError
ProtectionState
ExperienceProtection
_require_experience_id

[lib/python/experience/persistence.py]
ExperiencePersistenceError
ExperienceSerializationError
ExperienceRecoveryError
serialize_experience
recover_experience
[lib/python/experience/persistent_repository.py]
PersistentExperienceRepositoryError
ExperienceStoreCorruptionError
JsonFileExperienceRepository
_require_experience_id
```

## 7. Protection/Persistence Behavioral References

```text
lib/python/experience/__init__.py:34:from .protection import (
lib/python/experience/__init__.py:35:    ExperienceProtection,
lib/python/experience/__init__.py:36:    ExperienceProtectionError,
lib/python/experience/__init__.py:37:    InvalidProtectionIdentityError,
lib/python/experience/__init__.py:38:    ProtectedExperienceMutationError,
lib/python/experience/__init__.py:39:    ProtectionState,
lib/python/experience/__init__.py:45:    ExperienceRecoveryError,
lib/python/experience/__init__.py:46:    ExperienceSerializationError,
lib/python/experience/__init__.py:47:    recover_experience,
lib/python/experience/__init__.py:48:    serialize_experience,
lib/python/experience/__init__.py:53:    JsonFileExperienceRepository,
lib/python/experience/repository.py:41:    def save(self, experience: Experience) -> None:
lib/python/experience/repository.py:76:    def save(self, experience: Experience) -> None:
lib/python/experience/repository.py:79:                f"Cannot save unknown Experience: {experience.experience_id}"
lib/python/experience/service.py:37:        self._repository.save(active)
lib/python/experience/service.py:47:        self._repository.save(closed)
lib/python/experience/protection.py:1:"""Protection physiology for Persistent Experience.
lib/python/experience/protection.py:3:Protection is an explicit domain organ.
lib/python/experience/protection.py:10:Its responsibility is to make the protection condition of an
lib/python/experience/protection.py:23:class ExperienceProtectionError(Exception):
lib/python/experience/protection.py:24:    """Base error for Experience protection violations."""
lib/python/experience/protection.py:27:class InvalidProtectionIdentityError(ExperienceProtectionError):
lib/python/experience/protection.py:28:    """Raised when protection is requested for an invalid Experience identity."""
lib/python/experience/protection.py:31:class ProtectedExperienceMutationError(ExperienceProtectionError):
lib/python/experience/protection.py:32:    """Raised when a protected Experience is subjected to prohibited mutation."""
lib/python/experience/protection.py:35:class UnauthorizedExperienceOperationError(ExperienceProtectionError):
lib/python/experience/protection.py:39:class ProtectionState(str, Enum):
lib/python/experience/protection.py:40:    """Observable protection condition of an Experience."""
lib/python/experience/protection.py:42:    UNPROTECTED = "unprotected"
lib/python/experience/protection.py:43:    PROTECTED = "protected"
lib/python/experience/protection.py:47:class ExperienceProtection:
lib/python/experience/protection.py:48:    """Protection state associated with exactly one Experience identity.
lib/python/experience/protection.py:50:    The protector references the Experience identity but does not own
lib/python/experience/protection.py:53:    Protection is deliberately distinct from persistence and authority.
lib/python/experience/protection.py:57:    state: ProtectionState
lib/python/experience/protection.py:60:    def unprotected(
lib/python/experience/protection.py:63:    ) -> "ExperienceProtection":
lib/python/experience/protection.py:66:            state=ProtectionState.UNPROTECTED,
lib/python/experience/protection.py:70:    def protected(
lib/python/experience/protection.py:73:    ) -> "ExperienceProtection":
lib/python/experience/protection.py:76:            state=ProtectionState.PROTECTED,
lib/python/experience/protection.py:80:    def is_protected(self) -> bool:
lib/python/experience/protection.py:81:        return self.state is ProtectionState.PROTECTED
lib/python/experience/protection.py:83:    def protect(self) -> "ExperienceProtection":
lib/python/experience/protection.py:84:        """Return the protected condition without changing identity."""
lib/python/experience/protection.py:86:        if self.is_protected:
lib/python/experience/protection.py:89:        return ExperienceProtection(
lib/python/experience/protection.py:91:            state=ProtectionState.PROTECTED,
lib/python/experience/protection.py:95:        """Reject ordinary mutation while the Experience is protected."""
lib/python/experience/protection.py:97:        if self.is_protected:
lib/python/experience/protection.py:98:            raise ProtectedExperienceMutationError(
lib/python/experience/protection.py:99:                "protected Experience cannot be mutated by an ordinary operation"
lib/python/experience/protection.py:103:        """Require explicit authorization for a protected operation.
lib/python/experience/protection.py:111:        if self.is_protected and not authorized:
lib/python/experience/protection.py:113:                "operation on protected Experience requires explicit authorization"
lib/python/experience/protection.py:118:    """Validate the identity consumed by the Protection organ."""
lib/python/experience/protection.py:121:        raise InvalidProtectionIdentityError(
lib/python/experience/persistence.py:1:"""Serialization boundary for PCC-01 Persistent Experience.
lib/python/experience/persistence.py:3:Serialization is a transport/storage representation of Experience.
lib/python/experience/persistence.py:9:Recovery must reconstruct the persisted Experience identity.
lib/python/experience/persistence.py:27:class ExperienceSerializationError(ExperiencePersistenceError):
lib/python/experience/persistence.py:28:    """Raised when an Experience cannot be serialized safely."""
lib/python/experience/persistence.py:31:class ExperienceRecoveryError(ExperiencePersistenceError):
lib/python/experience/persistence.py:32:    """Raised when persisted Experience data cannot be recovered safely."""
lib/python/experience/persistence.py:44:def serialize_experience(experience: Experience) -> dict[str, str]:
lib/python/experience/persistence.py:45:    """Serialize exactly the minimum Core Experience state."""
lib/python/experience/persistence.py:48:        raise ExperienceSerializationError(
lib/python/experience/persistence.py:49:            "serialize_experience requires an Experience"
lib/python/experience/persistence.py:59:def recover_experience(data: Mapping[str, Any]) -> Experience:
lib/python/experience/persistence.py:60:    """Recover one existing Experience without regenerating identity."""
lib/python/experience/persistence.py:63:        raise ExperienceRecoveryError(
lib/python/experience/persistence.py:73:        raise ExperienceRecoveryError(
lib/python/experience/persistence.py:83:        raise ExperienceRecoveryError(
lib/python/experience/persistence.py:88:        raise ExperienceRecoveryError(
lib/python/experience/persistence.py:93:        raise ExperienceRecoveryError(
lib/python/experience/persistence.py:100:        raise ExperienceRecoveryError(
lib/python/experience/persistence.py:107:        raise ExperienceRecoveryError(
lib/python/experience/persistence.py:112:        raise ExperienceRecoveryError(
lib/python/experience/persistence.py:119:        raise ExperienceRecoveryError(
lib/python/experience/persistent_repository.py:4:contract using a JSON file as a persistence substrate.
lib/python/experience/persistent_repository.py:6:The JSON file is storage.
lib/python/experience/persistent_repository.py:13:import json
lib/python/experience/persistent_repository.py:23:    ExperienceRecoveryError,
lib/python/experience/persistent_repository.py:24:    recover_experience,
lib/python/experience/persistent_repository.py:25:    serialize_experience,
lib/python/experience/persistent_repository.py:40:    """Raised when the persisted store cannot be trusted or recovered."""
lib/python/experience/persistent_repository.py:43:class JsonFileExperienceRepository(ExperienceRepository):
lib/python/experience/persistent_repository.py:44:    """JSON-backed Experience repository.
lib/python/experience/persistent_repository.py:48:    RUN 016 verifies recovery using independent repository instances.
lib/python/experience/persistent_repository.py:76:        store["experiences"][key] = serialize_experience(experience)
lib/python/experience/persistent_repository.py:93:            recovered = recover_experience(representation)
lib/python/experience/persistent_repository.py:99:        if recovered.experience_id != experience_id:
lib/python/experience/persistent_repository.py:104:        return recovered
lib/python/experience/persistent_repository.py:106:    def save(self, experience: Experience) -> None:
lib/python/experience/persistent_repository.py:113:                f"Cannot save unknown Experience: {experience.experience_id}"
lib/python/experience/persistent_repository.py:116:        store["experiences"][key] = serialize_experience(experience)
lib/python/experience/persistent_repository.py:144:            data = json.loads(raw)
lib/python/experience/persistent_repository.py:145:        except json.JSONDecodeError as exc:
lib/python/experience/persistent_repository.py:147:                "Experience store contains invalid JSON"
lib/python/experience/persistent_repository.py:179:                recovered = recover_experience(representation)
lib/python/experience/persistent_repository.py:180:            except ExperienceRecoveryError as exc:
lib/python/experience/persistent_repository.py:185:            if str(recovered.experience_id) != key:
lib/python/experience/persistent_repository.py:195:        payload = json.dumps(
lib/python/experience/persistent_repository.py:217:                handle.write(payload)
tests/experience/test_experience_repository.py:18:    loaded = repository.get(experience.experience_id)
tests/experience/test_experience_repository.py:20:    assert loaded == experience
tests/experience/test_experience_repository.py:21:    assert loaded.experience_id == experience.experience_id
tests/experience/test_experience_repository.py:52:def test_repository_saves_new_state_without_changing_identity():
tests/experience/test_experience_repository.py:58:    repository.save(active)
tests/experience/test_experience_repository.py:60:    loaded = repository.get(created.experience_id)
tests/experience/test_experience_repository.py:62:    assert loaded.state == active.state
tests/experience/test_experience_repository.py:63:    assert loaded.experience_id == created.experience_id
tests/experience/test_experience_repository.py:66:def test_repository_rejects_save_for_unknown_experience():
tests/experience/test_experience_repository.py:71:        repository.save(experience)
tests/experience/test_experience_protection.py:4:from lib.python.experience.protection import (
tests/experience/test_experience_protection.py:5:    ExperienceProtection,
tests/experience/test_experience_protection.py:6:    InvalidProtectionIdentityError,
tests/experience/test_experience_protection.py:7:    ProtectedExperienceMutationError,
tests/experience/test_experience_protection.py:8:    ProtectionState,
tests/experience/test_experience_protection.py:17:def test_unprotected_state_is_explicit():
tests/experience/test_experience_protection.py:20:    protection = ExperienceProtection.unprotected(identity)
tests/experience/test_experience_protection.py:22:    assert protection.experience_id == identity
tests/experience/test_experience_protection.py:23:    assert protection.state is ProtectionState.UNPROTECTED
tests/experience/test_experience_protection.py:24:    assert protection.is_protected is False
tests/experience/test_experience_protection.py:27:def test_protected_state_is_explicit():
tests/experience/test_experience_protection.py:30:    protection = ExperienceProtection.protected(identity)
tests/experience/test_experience_protection.py:32:    assert protection.experience_id == identity
tests/experience/test_experience_protection.py:33:    assert protection.state is ProtectionState.PROTECTED
tests/experience/test_experience_protection.py:34:    assert protection.is_protected is True
tests/experience/test_experience_protection.py:37:def test_protect_preserves_experience_identity():
tests/experience/test_experience_protection.py:40:    before = ExperienceProtection.unprotected(identity)
tests/experience/test_experience_protection.py:41:    after = before.protect()
tests/experience/test_experience_protection.py:44:    assert after.state is ProtectionState.PROTECTED
tests/experience/test_experience_protection.py:47:def test_protection_does_not_generate_replacement_identity():
tests/experience/test_experience_protection.py:50:    protection = ExperienceProtection.protected(identity)
tests/experience/test_experience_protection.py:52:    assert protection.experience_id is identity
tests/experience/test_experience_protection.py:55:def test_protection_is_immutable():
tests/experience/test_experience_protection.py:56:    protection = ExperienceProtection.protected(new_identity())
tests/experience/test_experience_protection.py:59:        protection.state = ProtectionState.UNPROTECTED
tests/experience/test_experience_protection.py:63:    with pytest.raises(InvalidProtectionIdentityError):
tests/experience/test_experience_protection.py:64:        ExperienceProtection.protected("not-an-experience-id")
tests/experience/test_experience_protection.py:67:def test_unprotected_experience_allows_ordinary_mutation_gate():
tests/experience/test_experience_protection.py:68:    protection = ExperienceProtection.unprotected(new_identity())
tests/experience/test_experience_protection.py:70:    protection.require_mutation_allowed()
tests/experience/test_experience_protection.py:73:def test_protected_experience_rejects_ordinary_mutation():
tests/experience/test_experience_protection.py:74:    protection = ExperienceProtection.protected(new_identity())
tests/experience/test_experience_protection.py:76:    with pytest.raises(ProtectedExperienceMutationError):
tests/experience/test_experience_protection.py:77:        protection.require_mutation_allowed()
tests/experience/test_experience_protection.py:80:def test_protected_operation_requires_explicit_authorization():
tests/experience/test_experience_protection.py:81:    protection = ExperienceProtection.protected(new_identity())
tests/experience/test_experience_protection.py:84:        protection.require_authorized(authorized=False)
tests/experience/test_experience_protection.py:87:def test_explicit_authorization_allows_protected_operation_gate():
tests/experience/test_experience_protection.py:88:    protection = ExperienceProtection.protected(new_identity())
tests/experience/test_experience_protection.py:90:    protection.require_authorized(authorized=True)
tests/experience/test_experience_protection.py:94:    protection = ExperienceProtection.protected(new_identity())
tests/experience/test_experience_protection.py:97:        protection.require_authorized(authorized=False)
tests/experience/test_experience_protection.py:101:    protection = ExperienceProtection.protected(new_identity())
tests/experience/test_experience_protection.py:104:        protection.require_authorized(authorized="yes")
tests/experience/test_experience_persistence.py:9:    ExperienceRecoveryError,
tests/experience/test_experience_persistence.py:10:    ExperienceSerializationError,
tests/experience/test_experience_persistence.py:11:    recover_experience,
tests/experience/test_experience_persistence.py:12:    serialize_experience,
tests/experience/test_experience_persistence.py:16:def test_experience_serialization_contains_only_core_fields():
tests/experience/test_experience_persistence.py:19:    data = serialize_experience(experience)
tests/experience/test_experience_persistence.py:28:def test_serialization_preserves_identity_value():
tests/experience/test_experience_persistence.py:31:    data = serialize_experience(experience)
tests/experience/test_experience_persistence.py:36:def test_recovery_reconstructs_same_identity_value():
tests/experience/test_experience_persistence.py:39:    data = serialize_experience(before)
tests/experience/test_experience_persistence.py:40:    after = recover_experience(data)
tests/experience/test_experience_persistence.py:46:def test_recovery_reconstructs_identity_object_without_using_create(monkeypatch):
tests/experience/test_experience_persistence.py:48:    data = serialize_experience(before)
tests/experience/test_experience_persistence.py:52:            "ExperienceId.create() must not run during recovery"
tests/experience/test_experience_persistence.py:61:    after = recover_experience(data)
tests/experience/test_experience_persistence.py:66:def test_recovery_preserves_created_at():
tests/experience/test_experience_persistence.py:69:    after = recover_experience(
tests/experience/test_experience_persistence.py:70:        serialize_experience(before)
tests/experience/test_experience_persistence.py:76:def test_recovery_preserves_lifecycle_state():
tests/experience/test_experience_persistence.py:79:    after = recover_experience(
tests/experience/test_experience_persistence.py:80:        serialize_experience(before)
tests/experience/test_experience_persistence.py:86:def test_serialization_rejects_non_experience():
tests/experience/test_experience_persistence.py:87:    with pytest.raises(ExperienceSerializationError):
tests/experience/test_experience_persistence.py:88:        serialize_experience(object())
tests/experience/test_experience_persistence.py:107:def test_recovery_rejects_invalid_field_sets(data):
tests/experience/test_experience_persistence.py:108:    with pytest.raises(ExperienceRecoveryError):
tests/experience/test_experience_persistence.py:109:        recover_experience(data)
tests/experience/test_experience_persistence.py:112:def test_recovery_rejects_invalid_identity():
tests/experience/test_experience_persistence.py:114:    data = serialize_experience(experience)
tests/experience/test_experience_persistence.py:117:    with pytest.raises(ExperienceRecoveryError):
tests/experience/test_experience_persistence.py:118:        recover_experience(data)
tests/experience/test_experience_persistence.py:121:def test_recovery_rejects_naive_created_at():
tests/experience/test_experience_persistence.py:123:    data = serialize_experience(experience)
tests/experience/test_experience_persistence.py:126:    with pytest.raises(ExperienceRecoveryError):
tests/experience/test_experience_persistence.py:127:        recover_experience(data)
tests/experience/test_experience_persistence.py:130:def test_recovery_rejects_invalid_lifecycle_state():
tests/experience/test_experience_persistence.py:132:    data = serialize_experience(experience)
tests/experience/test_experience_persistence.py:135:    with pytest.raises(ExperienceRecoveryError):
tests/experience/test_experience_persistence.py:136:        recover_experience(data)
tests/experience/test_experience_persistence.py:139:def test_recovery_does_not_mutate_serialized_representation():
tests/experience/test_experience_persistence.py:141:    data = serialize_experience(before)
tests/experience/test_experience_persistence.py:144:    recover_experience(data)
tests/experience/test_experience_recovery.py:1:import json
tests/experience/test_experience_recovery.py:8:    JsonFileExperienceRepository,
tests/experience/test_experience_recovery.py:17:    store = tmp_path / "experience-store.json"
tests/experience/test_experience_recovery.py:18:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:26:def test_new_repository_instance_recovers_existing_experience(tmp_path):
tests/experience/test_experience_recovery.py:27:    store = tmp_path / "experience-store.json"
tests/experience/test_experience_recovery.py:29:    writer = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:33:    reader = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:40:def test_save_survives_repository_instance_replacement(tmp_path):
tests/experience/test_experience_recovery.py:41:    store = tmp_path / "experience-store.json"
tests/experience/test_experience_recovery.py:43:    first = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:49:    first.save(active)
tests/experience/test_experience_recovery.py:51:    second = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:52:    recovered = second.get(created.experience_id)
tests/experience/test_experience_recovery.py:54:    assert recovered.state == active.state
tests/experience/test_experience_recovery.py:55:    assert recovered.experience_id == created.experience_id
tests/experience/test_experience_recovery.py:59:    store = tmp_path / "experience-store.json"
tests/experience/test_experience_recovery.py:60:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:69:def test_repository_rejects_unknown_save(tmp_path):
tests/experience/test_experience_recovery.py:70:    store = tmp_path / "experience-store.json"
tests/experience/test_experience_recovery.py:71:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:74:        repository.save(Experience.create())
tests/experience/test_experience_recovery.py:78:    store = tmp_path / "experience-store.json"
tests/experience/test_experience_recovery.py:79:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:84:    replacement_repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:91:def test_invalid_json_is_explicit_corruption(tmp_path):
tests/experience/test_experience_recovery.py:92:    store = tmp_path / "experience-store.json"
tests/experience/test_experience_recovery.py:93:    store.write_text("{not-json", encoding="utf-8")
tests/experience/test_experience_recovery.py:95:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:102:    store = tmp_path / "experience-store.json"
tests/experience/test_experience_recovery.py:104:        json.dumps({"wrong": "shape"}),
tests/experience/test_experience_recovery.py:108:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:115:    store = tmp_path / "experience-store.json"
tests/experience/test_experience_recovery.py:117:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:121:    data = json.loads(store.read_text(encoding="utf-8"))
tests/experience/test_experience_recovery.py:131:        json.dumps(data),
tests/experience/test_experience_recovery.py:135:    replacement = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:142:    store = tmp_path / "missing.json"
tests/experience/test_experience_recovery.py:143:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:154:    store = tmp_path / "experience-store.json"
tests/experience/test_experience_recovery.py:156:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:160:    recovered = JsonFileExperienceRepository(store).get(
tests/experience/test_experience_recovery.py:164:    assert not hasattr(recovered, "authority")
tests/experience/harness/pcc01_restart_writer.py:6:A later independent Python interpreter must recover that Experience.
tests/experience/harness/pcc01_restart_writer.py:11:import json
tests/experience/harness/pcc01_restart_writer.py:18:    JsonFileExperienceRepository,
tests/experience/harness/pcc01_restart_writer.py:31:    repository = JsonFileExperienceRepository(store_path)
tests/experience/harness/pcc01_restart_writer.py:45:        json.dumps(
tests/experience/harness/pcc01_restart_writer.py:53:    print(json.dumps(evidence, sort_keys=True))
tests/experience/harness/pcc01_restart_reader.py:5:ExperienceId, recovers the Experience from storage, and records the
tests/experience/harness/pcc01_restart_reader.py:11:import json
tests/experience/harness/pcc01_restart_reader.py:18:    JsonFileExperienceRepository,
tests/experience/harness/pcc01_restart_reader.py:33:    before = json.loads(
tests/experience/harness/pcc01_restart_reader.py:41:    repository = JsonFileExperienceRepository(store_path)
tests/experience/harness/pcc01_restart_reader.py:42:    recovered = repository.get(before_id)
tests/experience/harness/pcc01_restart_reader.py:49:        "experience_id_after": str(recovered.experience_id),
tests/experience/harness/pcc01_restart_reader.py:52:            == str(recovered.experience_id)
tests/experience/harness/pcc01_restart_reader.py:54:        "state_after": recovered.state.value,
tests/experience/harness/pcc01_restart_reader.py:59:        json.dumps(
tests/experience/harness/pcc01_restart_reader.py:67:    print(json.dumps(evidence, sort_keys=True))
tests/experience/test_experience_real_process_restart.py:3:import json
tests/experience/test_experience_real_process_restart.py:47:def test_identity_survives_real_process_death_and_new_process_recovery(
tests/experience/test_experience_real_process_restart.py:50:    store = tmp_path / "experience-store.json"
tests/experience/test_experience_real_process_restart.py:51:    before_evidence = tmp_path / "before.json"
tests/experience/test_experience_real_process_restart.py:52:    after_evidence = tmp_path / "after.json"
tests/experience/test_experience_real_process_restart.py:76:    before = json.loads(
tests/experience/test_experience_real_process_restart.py:103:    after = json.loads(
```

## 8. Dedicated Protection Restart Test

```text
F
=================================== FAILURES ===================================
__________ test_protected_experience_can_be_recovered_by_new_process ___________

tmp_path = PosixPath('/data/data/com.termux/files/usr/tmp/pytest-of-u0_a268/pytest-103/test_protected_experience_can_0')

    def test_protected_experience_can_be_recovered_by_new_process(tmp_path):
        storage = tmp_path / "experience-storage"
        storage.mkdir()
    
        writer_result = tmp_path / "writer.json"
        reader_result = tmp_path / "reader.json"
    
        process_a = run_process(WRITER, storage, writer_result)
    
>       assert process_a.returncode == 0, (
            "Process A failed.\n"
            f"STDOUT:\n{process_a.stdout}\n"
            f"STDERR:\n{process_a.stderr}"
        )
E       AssertionError: Process A failed.
E         STDOUT:
E         
E         STDERR:
E         Traceback (most recent call last):
E           File "/storage/emulated/0/AI-Projects/AI-Toolkit/tests/experience/harness/pcc01_protection_restart_writer.py", line 143, in <module>
E             main()
E           File "/storage/emulated/0/AI-Projects/AI-Toolkit/tests/experience/harness/pcc01_protection_restart_writer.py", line 127, in main
E             repository = find_repository()
E                          ^^^^^^^^^^^^^^^^^
E           File "/storage/emulated/0/AI-Projects/AI-Toolkit/tests/experience/harness/pcc01_protection_restart_writer.py", line 41, in find_repository
E             raise RuntimeError("Unable to construct existing persistent repository")
E         RuntimeError: Unable to construct existing persistent repository
E         
E       assert 1 == 0
E        +  where 1 = CompletedProcess(args=['/data/data/com.termux/files/usr/bin/python', '/storage/emulated/0/AI-Projects/AI-Toolkit/tests...ble to construct existing persistent repository")\nRuntimeError: Unable to construct existing persistent repository\n').returncode

tests/experience/test_experience_protection_restart.py:55: AssertionError
=========================== short test summary info ============================
FAILED tests/experience/test_experience_protection_restart.py::test_protected_experience_can_be_recovered_by_new_process
1 failed in 0.77s
```

Exit code: 1

## 9. Complete Experience Regression

```text
................................................F....................... [ 77%]
.....................                                                    [100%]
=================================== FAILURES ===================================
__________ test_protected_experience_can_be_recovered_by_new_process ___________

tmp_path = PosixPath('/data/data/com.termux/files/usr/tmp/pytest-of-u0_a268/pytest-104/test_protected_experience_can_0')

    def test_protected_experience_can_be_recovered_by_new_process(tmp_path):
        storage = tmp_path / "experience-storage"
        storage.mkdir()
    
        writer_result = tmp_path / "writer.json"
        reader_result = tmp_path / "reader.json"
    
        process_a = run_process(WRITER, storage, writer_result)
    
>       assert process_a.returncode == 0, (
            "Process A failed.\n"
            f"STDOUT:\n{process_a.stdout}\n"
            f"STDERR:\n{process_a.stderr}"
        )
E       AssertionError: Process A failed.
E         STDOUT:
E         
E         STDERR:
E         Traceback (most recent call last):
E           File "/storage/emulated/0/AI-Projects/AI-Toolkit/tests/experience/harness/pcc01_protection_restart_writer.py", line 143, in <module>
E             main()
E           File "/storage/emulated/0/AI-Projects/AI-Toolkit/tests/experience/harness/pcc01_protection_restart_writer.py", line 127, in main
E             repository = find_repository()
E                          ^^^^^^^^^^^^^^^^^
E           File "/storage/emulated/0/AI-Projects/AI-Toolkit/tests/experience/harness/pcc01_protection_restart_writer.py", line 41, in find_repository
E             raise RuntimeError("Unable to construct existing persistent repository")
E         RuntimeError: Unable to construct existing persistent repository
E         
E       assert 1 == 0
E        +  where 1 = CompletedProcess(args=['/data/data/com.termux/files/usr/bin/python', '/storage/emulated/0/AI-Projects/AI-Toolkit/tests...ble to construct existing persistent repository")\nRuntimeError: Unable to construct existing persistent repository\n').returncode

tests/experience/test_experience_protection_restart.py:55: AssertionError
=========================== short test summary info ============================
FAILED tests/experience/test_experience_protection_restart.py::test_protected_experience_can_be_recovered_by_new_process
1 failed, 92 passed in 1.97s
```

Exit code: 1

## 10. Evidence Interpretation

**Protection continuity across real process restart:** NOT DEMONSTRATED

The experiment did not produce sufficient behavioral evidence of protection state after recovery.

This is not automatically a defect in Protection itself. The report must be inspected to determine whether the cause is:

- Protection state is not serialized;
- Protection state is not restored;
- Protection is intentionally derived rather than persisted;
- the existing Protection API requires a different integration path;
- or the adaptive harness could not exercise the existing contract without architectural guessing.

**Complete Experience regression:** FAIL

## 11. Final Working Tree

```text
tests/experience/harness/pcc01_protection_restart_reader.py
tests/experience/harness/pcc01_protection_restart_writer.py
tests/experience/test_experience_protection_restart.py
work/implementation-reports/PCC-01/PCC-01_PROTECTION_RESTART_CONTINUITY_REPORT_RUN_022.md
work/implementation-reports/PCC-01/PCC-01_RUN020_EVIDENCE_CONSERVATION_REPORT_RUN_021.md

PASS: only authorized RUN 021/RUN 022 evidence and Protection restart test tissue exist locally
```

## 12. Protection Continuity Status

**NOT DEMONSTRATED**

## 13. Central Identity Invariant

`ID_before_restart == ID_after_restart`

**Status:** DEMONSTRATED LOCALLY by the already-conserved real process restart harness.

RUN 022 does not revoke or broaden that earlier evidence.

## 14. Epistemic Boundaries

- Experience != Session
- Experience != Memory
- Experience != Evidence
- Experience != raw dialogue
- Session != process
- Session != provider
- Storage != Experience
- Interpretation != historical fact
- Persistence != authority
- Human Acceptance != Implementation

Protection surviving persistence, if demonstrated, does not make persisted data authoritative.

Authority remains external to persistence and remains Human Authority where the accepted PCC-01 contract requires it.

## 15. PCC-01 Status

**Implementation Status:** NOT DEMONSTRATED

**Canonical Status:** NOT CANON

**Production Status:** NOT PRODUCTION-READY

## 16. Conservation State

No `git add` performed.

No commit performed.

No push performed.

## 17. Final Result

**RUN 022: INVESTIGATION REQUIRED**

**Protection continuity:** NOT DEMONSTRATED

**Overall PCC-01:** NOT DEMONSTRATED

**NEXT REQUIRED ACTION:** GPT inspection of RUN 022 before any correction, conservation, or further PCC-01 construction.

---

END OF PCC-01 PROTECTION CONTINUITY ACROSS REAL PROCESS RESTART — RUN 022
