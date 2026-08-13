# PCC-01 — EXPERIENCE + PROTECTION PERSISTENCE COORDINATION INSPECTION — RUN 027

**Purpose:** Investigate the physiology required to coordinate independently persisted Experience and Protection state without collapsing their epistemic boundaries.

**Expected baseline:** `058e12c3ebd753eb43d47e40714a4ce21011c5d5`

**Predecessor:** RUN 026

**Mode:** INSPECTION ONLY

**Software modification:** NONE

---

## 1. Authoritative Baseline

```text
Expected:    058e12c3ebd753eb43d47e40714a4ce21011c5d5
LOCAL:       058e12c3ebd753eb43d47e40714a4ce21011c5d5
origin/main: 058e12c3ebd753eb43d47e40714a4ce21011c5d5
PASS
```

## 2. Predecessor Evidence

RUN 026 demonstrates locally:

- real Process A -> Process B boundary;
- Experience identity continuity;
- Protection continuity;
- Persistence != authority.

RUN 026 explicitly does NOT demonstrate atomic Experience + Protection persistence.

## 3. Current Experience Behavioral Baseline

```text
........................................................................ [ 63%]
.........................................                                [100%]
113 passed in 2.66s
```

Exit code: 0

## 4. Current Persistence Anatomy


### `lib/python/experience/persistence.py`

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

### `lib/python/experience/persistent_repository.py`

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

### `lib/python/experience/protection.py`

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

### `lib/python/experience/protection_persistence.py`

```python
"""Persistence representation for the Experience Protection organ.

Protection remains distinct from Experience.

Experience != Protection.
Storage != Experience.
Persistence != authority.

A persisted PROTECTED condition records state.
It does not grant authorization.
"""

from __future__ import annotations

from typing import Any, Mapping

from .identity import ExperienceId, ExperienceIdentityError
from .protection import ExperienceProtection, ProtectionState


class ProtectionPersistenceError(RuntimeError):
    """Base error for Protection persistence failures."""


class ProtectionSerializationError(ProtectionPersistenceError):
    """Raised when Protection cannot be serialized safely."""


class ProtectionRecoveryError(ProtectionPersistenceError):
    """Raised when persisted Protection cannot be recovered safely."""


_REQUIRED_FIELDS = frozenset(
    {
        "experience_id",
        "state",
    }
)


def serialize_protection(
    protection: ExperienceProtection,
) -> dict[str, str]:
    """Serialize exactly the persistent state owned by Protection."""

    if not isinstance(protection, ExperienceProtection):
        raise ProtectionSerializationError(
            "serialize_protection requires ExperienceProtection"
        )

    return {
        "experience_id": str(protection.experience_id),
        "state": protection.state.value,
    }


def recover_protection(
    data: Mapping[str, Any],
) -> ExperienceProtection:
    """Recover Protection without generating a new Experience identity."""

    if not isinstance(data, Mapping):
        raise ProtectionRecoveryError(
            "persisted Protection representation must be a mapping"
        )

    fields = frozenset(data.keys())

    if fields != _REQUIRED_FIELDS:
        missing = sorted(_REQUIRED_FIELDS - fields)
        unexpected = sorted(fields - _REQUIRED_FIELDS)

        raise ProtectionRecoveryError(
            "invalid persisted Protection fields; "
            f"missing={missing}, unexpected={unexpected}"
        )

    experience_id_raw = data["experience_id"]
    state_raw = data["state"]

    if not isinstance(experience_id_raw, str):
        raise ProtectionRecoveryError(
            "persisted Protection experience_id must be a string"
        )

    if not isinstance(state_raw, str):
        raise ProtectionRecoveryError(
            "persisted Protection state must be a string"
        )

    try:
        experience_id = ExperienceId.from_string(experience_id_raw)
    except ExperienceIdentityError as exc:
        raise ProtectionRecoveryError(
            "persisted Protection identity is invalid"
        ) from exc

    try:
        state = ProtectionState(state_raw)
    except ValueError as exc:
        raise ProtectionRecoveryError(
            "persisted Protection state is invalid"
        ) from exc

    return ExperienceProtection(
        experience_id=experience_id,
        state=state,
    )
```

### `lib/python/experience/protection_repository.py`

```python
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
```

## 5. Structural Relationship Index

```text
========================================================================
lib/python/experience/persistence.py
========================================================================
CLASS ExperiencePersistenceError
CLASS ExperienceSerializationError
CLASS ExperienceRecoveryError
FUNCTION serialize_experience
FUNCTION recover_experience

========================================================================
lib/python/experience/persistent_repository.py
========================================================================
CLASS PersistentExperienceRepositoryError
CLASS ExperienceStoreCorruptionError
CLASS JsonFileExperienceRepository
  METHOD __init__
  METHOD path
  METHOD add
  METHOD get
  METHOD save
  METHOD contains
  METHOD _empty_store
  METHOD _read_store
  METHOD _write_store
FUNCTION _require_experience_id

========================================================================
lib/python/experience/protection.py
========================================================================
CLASS ExperienceProtectionError
CLASS InvalidProtectionIdentityError
CLASS ProtectedExperienceMutationError
CLASS UnauthorizedExperienceOperationError
CLASS ProtectionState
CLASS ExperienceProtection
  METHOD unprotected
  METHOD protected
  METHOD is_protected
  METHOD protect
  METHOD require_mutation_allowed
  METHOD require_authorized
FUNCTION _require_experience_id

========================================================================
lib/python/experience/protection_persistence.py
========================================================================
CLASS ProtectionPersistenceError
CLASS ProtectionSerializationError
CLASS ProtectionRecoveryError
FUNCTION serialize_protection
FUNCTION recover_protection

========================================================================
lib/python/experience/protection_repository.py
========================================================================
CLASS ProtectionRepositoryError
CLASS ProtectionNotFoundError
CLASS ProtectionAlreadyExistsError
CLASS ProtectionStoreCorruptionError
CLASS ProtectionRepository
  METHOD add
  METHOD get
  METHOD save
  METHOD contains
CLASS JsonFileProtectionRepository
  METHOD __init__
  METHOD path
  METHOD add
  METHOD get
  METHOD save
  METHOD contains
  METHOD _empty_store
  METHOD _read_store
  METHOD _write_store
FUNCTION _require_experience_id
FUNCTION _require_protection

```

## 6. Existing Coordination Tissue Search

The following search is anatomical evidence only.

Term occurrence does not demonstrate behavioral compatibility.

```text
lib/python/planning_engine/__init__.py:4:Coordinates Repository, Knowledge,
lib/python/cli/main.py:716:        print(f"  Commit:         {live.get('current_commit', '')}")
lib/python/agents/development_agent.py:29:from python.execution_coordinator.engine import ExecutionCoordinator
lib/python/agents/development_agent.py:152:            ExecutionCoordinator().coordinate(
lib/python/session_runtime/runtime.py:27:    def checkpoint(self, session, step):
lib/python/execution_coordinator/__init__.py:2:Execution Coordinator
lib/python/execution_coordinator/engine.py:5:class ExecutionCoordinator:
lib/python/execution_coordinator/engine.py:9:    def coordinate(self, roadmap):
lib/python/workspace_orchestrator/__init__.py:6:The permanent top-level coordinator of the entire AI CTO architecture.
lib/python/workspace_orchestrator/__init__.py:9:Coordinates every existing CORE engine:
lib/python/workspace_orchestrator/engine.py:5:WorkspaceOrchestrator: the permanent top-level coordinator of the entire
lib/python/workspace_orchestrator/engine.py:9:Coordinates (but does NOT duplicate) every existing engine:
lib/python/workspace_orchestrator/persistence.py:18:All writes are atomic (write to temp, then rename) and deterministic
lib/python/workspace_orchestrator/persistence.py:59:    # Atomic write helpers
lib/python/workspace_orchestrator/persistence.py:66:        """Write *data* atomically to base_dir/filename.  Returns the path."""
lib/python/workspace_orchestrator/state_manager.py:9:atomically before the next operation begins.
lib/python/workspace_orchestrator/state_manager.py:28:    - Flush state atomically after each mutation
lib/python/coverage_engine/engine.py:38:        metrics.append(self._keyword_metric("Runtime", index, ["runtime", "execution", "coordinator"]))
lib/python/drift_engine/engine.py:61:                    "orphan-documentation-%s" % doc.id.lower(),
lib/python/drift_engine/engine.py:62:                    "Orphan Documentation",
lib/python/drift_engine/engine.py:103:        findings.extend(self._orphan_implementation_findings(index, matches, timestamp))
lib/python/drift_engine/engine.py:163:    def _orphan_implementation_findings(self, index, matches, timestamp):
lib/python/drift_engine/engine.py:173:            if not any(keyword in lowered for keyword in ["engine", "graph", "planner", "runtime", "coordinator", "audit", "validator"]):
lib/python/drift_engine/engine.py:179:                    id="orphan-implementation-%s" % wf.name.replace(".", "-").lower(),
lib/python/drift_engine/engine.py:180:                    category="Orphan Implementation",
lib/python/knowledge_graph/graph.py:43:    def orphan_nodes(self):
lib/python/ai_cto_scanner/detectors.py:395:            r"checkpoint\b",
lib/python/ai_cto_scanner/report.py:506:            "| Orphan modules | %d |" % len(ig.get("orphan_modules", [])),
lib/python/semantic_repository_intelligence/import_graph.py:7:(highly-imported) and orphan (never-imported) modules.
lib/python/semantic_repository_intelligence/import_graph.py:134:        # Orphan modules: Python files that no other Python file imports
lib/python/semantic_repository_intelligence/import_graph.py:136:        orphan = sorted(p for p in python_paths if p not in imported_targets)
lib/python/semantic_repository_intelligence/import_graph.py:143:            orphan_modules=orphan,
lib/python/semantic_repository_intelligence/models.py:150:    orphan_modules: List[str]  # modules never imported by anyone
lib/python/semantic_repository_intelligence/models.py:160:            "orphan_modules": self.orphan_modules,
lib/python/semantic_repository_intelligence/persistence.py:110:                "orphan_modules": import_graph.get("orphan_modules", [])[:10],
lib/python/semantic_repository_intelligence/recommendation_engine.py:50:        recs.extend(self._orphan_module_recs(import_graph))
lib/python/semantic_repository_intelligence/recommendation_engine.py:99:    def _orphan_module_recs(
lib/python/semantic_repository_intelligence/recommendation_engine.py:102:        orphans = import_graph.orphan_modules
lib/python/semantic_repository_intelligence/recommendation_engine.py:103:        if len(orphans) <= 2:
lib/python/semantic_repository_intelligence/recommendation_engine.py:105:        sample = sorted(orphans)[:5]
lib/python/semantic_repository_intelligence/recommendation_engine.py:108:            title="Investigate %d orphan modules" % len(orphans),
lib/python/semantic_repository_intelligence/recommendation_engine.py:113:                % len(orphans)
lib/python/semantic_repository_intelligence/recommendation_engine.py:117:            confidence=self._confidence.score(0.75, sample, cross_reference_count=len(orphans), evidence_tier="ast"),
lib/python/semantic_repository_intelligence/recommendation_engine.py:118:            evidence=["Orphan modules: %s" % ", ".join(sample)],
lib/python/development_state_engine/models.py:105:    head_commit: str
lib/python/development_state_engine/models.py:122:        _require_non_empty_string("head_commit", self.head_commit)
lib/python/development_state_engine/models.py:133:            "head_commit": self.head_commit,
lib/python/development_state_engine/models.py:148:            head_commit=data["head_commit"],
lib/python/development_state_engine/repository.py:46:        """Persist current state using atomic deterministic writes."""
lib/python/development_state_engine/repository.py:53:        self._atomic_write_text(self.current_state_path, serialized)
lib/python/development_state_engine/repository.py:75:        self._atomic_write_text(snapshot_path, self._serialize(payload))
lib/python/development_state_engine/repository.py:110:        self._atomic_write_text(export_path, self._serialize(state.to_dict()))
lib/python/development_state_engine/repository.py:156:    def _atomic_write_text(self, path: Path, content: str):
lib/python/development_state_engine/repository.py:186:        self._atomic_write_text(self.integrity_path, self._serialize(integrity_payload))
lib/python/development_state_engine/runtime.py:131:        self._atomic_write_json(self.events_path, document)
lib/python/development_state_engine/runtime.py:190:    def _atomic_write_json(self, path: Path, payload: Mapping[str, Any]):
lib/python/development_state_engine/runtime.py:209:    """Coordinates state persistence, runtime events, and executive snapshots."""
lib/python/development_state_engine/runtime.py:294:        self._atomic_write_json(self.executive_snapshot_path, snapshot.to_dict())
lib/python/development_state_engine/runtime.py:598:    def _atomic_write_json(self, path: Path, payload: Mapping[str, Any]):
lib/python/development_state_engine/runtime.py:912:        head_commit: Optional[str] = None,
lib/python/development_state_engine/runtime.py:921:                head_commit=head_commit or self._git_value("rev-parse", "HEAD") or state.repository_state.head_commit,
lib/python/development_state_engine/runtime.py:1036:        head_commit = self._git_value("rev-parse", "HEAD") or "UNKNOWN"
lib/python/development_state_engine/runtime.py:1038:        identifier_seed = f"{self.repository_root}-{branch}-{head_commit}"
lib/python/development_state_engine/runtime.py:1058:                head_commit=head_commit,
lib/python/executive_briefing_engine/persistence.py:26:    All writes are atomic (write to temp then rename) and deterministic
lib/python/executive_briefing_engine/persistence.py:101:        self._atomic_write(path, payload)
lib/python/executive_briefing_engine/persistence.py:104:    def _atomic_write(self, path: Path, payload: Mapping[str, Any]):
lib/python/executive_briefing_engine/priority_engine.py:161:                rationale="The current batch is the active unit of work.",
lib/python/context_synchronization_engine/__init__.py:13:    SynchronizationCoordinator,
lib/python/context_synchronization_engine/__init__.py:40:    "SynchronizationCoordinator",
lib/python/context_synchronization_engine/engine.py:26:    "current_commit",
lib/python/context_synchronization_engine/engine.py:101:        commit = self._git("rev-parse", "HEAD")
lib/python/context_synchronization_engine/engine.py:115:            "current_commit": commit,
lib/python/context_synchronization_engine/engine.py:459:            "current_commit": self._first_set(git_context.get("current_commit", ""), previous.get("current_commit", "")),
lib/python/context_synchronization_engine/engine.py:551:            if field in {"current_branch", "current_commit", "current_tag"} and _clean_scalar(git_context.get(field, "")) == value:
lib/python/context_synchronization_engine/engine.py:732:class SynchronizationCoordinator:
lib/python/context_synchronization_engine/engine.py:858:            head_commit=str(live_context.get("current_commit", "") or state.repository_state.head_commit),
lib/python/context_synchronization_engine/engine.py:938:                "current_commit": live_context.get("sources", {}).get("current_commit", ""),
lib/python/context_synchronization_engine/engine.py:955:                "current_commit": git_context.get("current_commit", ""),
lib/python/context_synchronization_engine/engine.py:1576:        self.coordinator = SynchronizationCoordinator(self.repository, self.workspace_root)
lib/python/context_synchronization_engine/engine.py:1579:        return self.coordinator.synchronize(refresh=refresh)
lib/python/context_synchronization_engine/persistence.py:15:        self._atomic_write(path, self._serialize(payload))
lib/python/context_synchronization_engine/persistence.py:20:        self._atomic_write(path, content if content.endswith("\n") else content + "\n")
lib/python/context_synchronization_engine/persistence.py:38:    def _atomic_write(self, path: Path, content: str) -> None:
lib/python/autonomous_planning_engine/persistence.py:5:Writes all planning artifacts to .ai/planning/ atomically.
lib/python/autonomous_planning_engine/persistence.py:30:    All writes are atomic (write to temp file, then rename) and
lib/python/autonomous_planning_engine/persistence.py:100:        self._atomic_write(path, content)
lib/python/autonomous_planning_engine/persistence.py:103:    def _atomic_write(self, path: Path, content: str) -> None:
lib/python/autonomous_execution_engine/__init__.py:20:    ExecutionCoordinator,
lib/python/autonomous_execution_engine/__init__.py:75:from .rollback import ExecutionRollbackPlanner
lib/python/autonomous_execution_engine/__init__.py:82:    "ExecutionCoordinator",
lib/python/autonomous_execution_engine/__init__.py:95:    "ExecutionRollbackPlanner",
lib/python/autonomous_execution_engine/engine.py:76:from .rollback import ExecutionRollbackPlanner
lib/python/autonomous_execution_engine/engine.py:152:class ExecutionCoordinator:
lib/python/autonomous_execution_engine/engine.py:154:    CORE-015 — Execution Coordinator.
lib/python/autonomous_execution_engine/engine.py:156:    Coordinates the full execution pipeline by delegating each stage
lib/python/autonomous_execution_engine/engine.py:166:    def coordinate(
lib/python/autonomous_execution_engine/engine.py:177:        """Run all pipeline stages and return the coordination result."""
lib/python/autonomous_execution_engine/engine.py:253:        self._rollback_planner = ExecutionRollbackPlanner()
lib/python/autonomous_execution_engine/engine.py:639:            commit=context_data.get("current_commit", ""),
lib/python/autonomous_execution_engine/engine.py:745:        """Internal coordination hook for ExecutionCoordinator."""
lib/python/autonomous_execution_engine/models.py:117:    commit: str
lib/python/autonomous_execution_engine/models.py:142:            "commit": self.commit,
lib/python/autonomous_execution_engine/persistence.py:5:Writes all execution artifacts to .ai/execution/ atomically.
lib/python/autonomous_execution_engine/persistence.py:32:    All writes are atomic (write to temp file, then rename) and
lib/python/autonomous_execution_engine/persistence.py:119:            self._atomic_write_text(md_path, md_content)
lib/python/autonomous_execution_engine/persistence.py:169:        self._atomic_write_text(path, content)
lib/python/autonomous_execution_engine/persistence.py:172:    def _atomic_write_text(self, path: Path, content: str) -> None:
lib/python/autonomous_execution_engine/rollback.py:2:Autonomous Execution Engine — Rollback Planner
lib/python/autonomous_execution_engine/rollback.py:5:Produces a deterministic rollback plan for every execution step
lib/python/autonomous_execution_engine/rollback.py:12:class ExecutionRollbackPlanner:
lib/python/autonomous_execution_engine/rollback.py:14:    CORE-015F — Execution Rollback Planner.
lib/python/autonomous_execution_engine/rollback.py:16:    Analyses the execution context and produces a rollback plan.
lib/python/autonomous_execution_engine/rollback.py:17:    The planner NEVER executes rollback — it only describes how.
lib/python/autonomous_execution_engine/rollback.py:18:    Owner approval is always required before any rollback is attempted.
lib/python/autonomous_execution_engine/rollback.py:28:        Produce a rollback plan for the given execution.
lib/python/autonomous_execution_engine/rollback.py:30:        Returns a deterministic dict describing rollback steps
lib/python/autonomous_execution_engine/rollback.py:35:        # Walk stages in reverse — only stages that completed need rollback
lib/python/autonomous_execution_engine/rollback.py:40:            step = self._rollback_step(stage, context)
lib/python/autonomous_execution_engine/rollback.py:46:            "rollback_required": bool(steps),
lib/python/autonomous_execution_engine/rollback.py:51:                "Rollback must be approved by the Owner before execution. "
lib/python/autonomous_execution_engine/rollback.py:52:                "The AI CTO will NEVER perform rollback autonomously."
lib/python/autonomous_execution_engine/rollback.py:58:    def _rollback_step(
lib/python/autonomous_execution_engine/rollback.py:63:        """Produce a single rollback step description."""
lib/python/autonomous_execution_engine/rollback.py:66:        commit = context.get("commit", "")
lib/python/autonomous_execution_engine/rollback.py:75:                    f"branch={branch!r}, commit={commit!r}"
lib/python/autonomous_execution_engine/rollback.py:86:        # Other stages are read-only — no rollback needed
lib/python/self_evaluation_engine/__init__.py:17:from .engine import EvaluationCoordinator, SelfEvaluationEngine
lib/python/self_evaluation_engine/__init__.py:60:    "EvaluationCoordinator",
lib/python/self_evaluation_engine/engine.py:77:class EvaluationCoordinator:
lib/python/self_evaluation_engine/engine.py:79:    CORE-016 — Evaluation Coordinator.
lib/python/self_evaluation_engine/engine.py:87:    def coordinate(
lib/python/self_evaluation_engine/engine.py:175:        self._coordinator = EvaluationCoordinator(repository=str(self.root))
lib/python/self_evaluation_engine/engine.py:212:            self._coordinator.coordinate(
lib/python/self_evaluation_engine/persistence.py:5:Writes all evaluation artifacts to .ai/self_evaluation/ atomically.
lib/python/self_evaluation_engine/persistence.py:32:    All writes are atomic and deterministic.
lib/python/self_evaluation_engine/persistence.py:161:            self._atomic_write_text(md_path, md_content)
lib/python/self_evaluation_engine/persistence.py:198:        self._atomic_write_text(path, content)
lib/python/self_evaluation_engine/persistence.py:201:    def _atomic_write_text(self, path: Path, content: str) -> None:
lib/python/self_improvement_engine/__init__.py:19:    ImprovementCoordinator,
lib/python/self_improvement_engine/__init__.py:54:    "ImprovementCoordinator",
lib/python/self_improvement_engine/engine.py:70:    Coordinates all analyzers and generators into an OptimizationPlan.
lib/python/self_improvement_engine/engine.py:104:    Coordinates the full improvement lifecycle by consuming all CORE
lib/python/self_improvement_engine/engine.py:151:class ImprovementCoordinator:
lib/python/self_improvement_engine/engine.py:153:    CORE-017 — Improvement Coordinator.
lib/python/self_improvement_engine/engine.py:163:    def coordinate(self, evaluation_data: Dict[str, Any]) -> Dict[str, Any]:
lib/python/self_improvement_engine/engine.py:217:        self._coordinator = ImprovementCoordinator(repository=str(self.root))
lib/python/self_improvement_engine/engine.py:233:        # Coordinate all improvement analysis
lib/python/self_improvement_engine/engine.py:234:        components = self._coordinator.coordinate(evaluation_data)
lib/python/self_improvement_engine/persistence.py:5:Writes all improvement artifacts to .ai/self_improvement/ atomically.
lib/python/self_improvement_engine/persistence.py:33:    All writes are atomic and deterministic.
lib/python/self_improvement_engine/persistence.py:161:            self._atomic_write_text(md_path, md_content)
lib/python/self_improvement_engine/persistence.py:200:        self._atomic_write_text(path, content)
lib/python/self_improvement_engine/persistence.py:203:    def _atomic_write_text(self, path: Path, content: str) -> None:
lib/python/runtime/config.py:45:    checkpoints_dir: str = ".ai/runtime/checkpoints"
lib/python/runtime/config.py:68:            checkpoints_dir=os.environ.get("RUNTIME_CHECKPOINTS_DIR", ".ai/runtime/checkpoints"),
lib/python/runtime/identity.py:22:    git_commit: str
lib/python/runtime/identity.py:39:            git_commit=os.environ.get("RAILWAY_GIT_COMMIT_SHA", "unknown"),
lib/python/runtime/identity.py:52:            "git_commit": self.git_commit,
lib/python/runtime/job_queue.py:22:    """A unit of work submitted to the Job Queue."""
lib/python/runtime/railway.py:30:    git_commit_sha: str
lib/python/runtime/railway.py:42:            "git_commit_sha": self.git_commit_sha,
lib/python/runtime/railway.py:57:        git_commit_sha=os.environ.get("RAILWAY_GIT_COMMIT_SHA", "unknown"),
lib/python/runtime/railway.py:68:        "Railway deployment: project=%s service=%s deployment=%s env=%s commit=%s",
lib/python/runtime/railway.py:73:        metadata.git_commit_sha[:8] if metadata.git_commit_sha != "unknown" else "unknown",
lib/python/engineering_engine/github_transaction_log.py:9:class TransactionRecord:
lib/python/engineering_engine/github_transaction_log.py:16:class TransactionLog:
lib/python/engineering_engine/github_transaction_log.py:17:    records: list[TransactionRecord] = field(default_factory=list)
lib/python/engineering_engine/github_transaction_log.py:20:class GitHubTransactionLogger:
lib/python/engineering_engine/github_transaction_log.py:25:    ) -> TransactionLog:
lib/python/engineering_engine/github_transaction_log.py:28:            return TransactionLog()
lib/python/engineering_engine/github_transaction_log.py:34:        return TransactionLog(
lib/python/engineering_engine/github_transaction_log.py:36:                TransactionRecord(**item)
lib/python/engineering_engine/github_transaction_log.py:43:        log: TransactionLog,
lib/python/engineering_engine/github_transaction_log.py:63:        log: TransactionLog,
lib/python/engineering_engine/github_transaction_log.py:70:            TransactionRecord(
lib/python/engineering_engine/github_resume_engine.py:9:from lib.python.engineering_engine.github_transaction_log import (
lib/python/engineering_engine/github_resume_engine.py:10:    TransactionLog,
lib/python/engineering_engine/github_resume_engine.py:24:        log: TransactionLog,
lib/python/engineering_engine/github_transaction_executor.py:11:from lib.python.engineering_engine.github_transaction_log import (
lib/python/engineering_engine/github_transaction_executor.py:12:    GitHubTransactionLogger,
lib/python/engineering_engine/github_transaction_executor.py:16:class GitHubTransactionalExecutor:
lib/python/engineering_engine/github_transaction_executor.py:26:        logger = GitHubTransactionLogger()
lib/python/dashboard/service.py:77:        purpose="Coordinate multiple repositories from one workspace view.",
lib/python/dashboard/service.py:114:        known_limitations="The MVP reflects local persisted state and does not yet coordinate active remote agents.",
lib/python/engineering_workspace/capabilities.py:36:    GIT_COMMIT = "git.commit"
lib/python/ai_control_center/kernel.py:9:It coordinates them.
lib/python/experience/service.py:11:    """Coordinates Core Experience behavior.
tests/test_execution_coordinator.sh:23:print("Coordinator:", state["status"])
tests/test_execution_coordinator.sh:34:print("Execution Coordinator PASS")
tests/experience/harness/pcc01_protection_restart_writer.py:55:    # This does NOT yet claim atomic coordination between the two
tests/test_runtime_layout.sh:60:assert_dir "$RUNTIME_ROOT/checkpoints"
tests/test_runtime_layout.sh:75:assert_gitignore_line ".ai/runtime/checkpoints/*"
tests/test_runtime_layout.sh:90:assert_no_repo_regex "\\.ai/batches/.*(execution_state|checkpoint|profil|session|cache|log|temporary|temp)"
tests/test_session_runtime.sh:15:runtime.checkpoint(session,"inspect")
tests/test_session_runtime.sh:16:runtime.checkpoint(session,"validation")
tests/test_session_runtime.sh:17:runtime.checkpoint(session,"planning")
tests/test_workspace_orchestrator.sh:451:    def test_atomic_write(self):
tests/test_semantic_repository_intelligence.sh:83:assert isinstance(ig.orphan_modules, list), 'orphan_modules must be list'
tests/test_development_state_engine_models.sh:46:            head_commit="abcdef1",
tests/test_development_state_engine_models.sh:48:            latest_merge="merge-commit",
tests/test_development_state_persistence.sh:58:                head_commit="abc1234",
tests/test_development_state_runtime.sh:156:        self.engine.RecordMerge("MERGE-9", branch="main", head_commit="abc1234", timestamp="2026-08-03T02:40:00Z")
tests/test_development_state_runtime_integration.sh:33:        subprocess.run(["git", "commit", "-m", "init"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
tests/test_development_state_runtime_integration.sh:36:                "import_graph": {"node_count": 1, "edge_count": 0, "critical_modules": [], "orphan_modules": []},
tests/test_development_state_runtime_integration.sh:90:        subprocess.run(["git", "commit", "-m", "init"], cwd=other_root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
tests/test_executive_briefing_engine.sh:180:                        "risks": ["Circular dependency in core", "Orphan module detected"],
tests/test_context_synchronization_engine.sh:29:    SynchronizationCoordinator,
tests/test_context_synchronization_engine.sh:103:            "import_graph": {"node_count": 1, "edge_count": 0, "circular_dependency_count": 0, "critical_modules": [], "orphan_modules": []},
tests/test_context_synchronization_engine.sh:121:        "GIT_COMMITTER_DATE": "2026-08-03T00:00:00+00:00",
tests/test_context_synchronization_engine.sh:123:    run(["git", "commit", "-m", "init"], cwd=repo, env=env)
tests/test_context_synchronization_engine.sh:301:            SynchronizationCoordinator,
tests/test_autonomous_planning_engine.sh:381:# 12. PlanningPersistence — atomic writes
tests/test_autonomous_execution_engine.sh:19:    ExecutionCoordinator,
tests/test_autonomous_execution_engine.sh:32:    ExecutionRollbackPlanner,
tests/test_autonomous_execution_engine.sh:217:# 10. ExecutionRollbackPlanner
tests/test_autonomous_execution_engine.sh:220:planner = ExecutionRollbackPlanner()
tests/test_autonomous_execution_engine.sh:223:    context={"branch": "main", "commit": "abc123", "batch": "BATCH-001"},
tests/test_autonomous_execution_engine.sh:233:print("10. ExecutionRollbackPlanner OK")
tests/test_autonomous_execution_engine.sh:248:    commit="abc",
tests/test_autonomous_execution_engine.sh:302:# 12. ExecutionPersistence — atomic writes
tests/test_self_evaluation_engine.sh:19:    EvaluationCoordinator,
tests/test_self_improvement_engine.sh:19:    ImprovementCoordinator,
tests/test_runtime_regression.sh:47:    ".ai/runtime/checkpoints",
tests/test_runtime_webhooks.sh:22:payload = json.dumps({"ref": "refs/heads/main", "commits": []}).encode()
```

## 7. Accepted PCC-01 Requirements Relevant To Coordination


### Source: `work/specifications/PCC-01_CORE_EXPERIENCE_IMPLEMENTATION_SPECIFICATION.md`

```text
3:**Capability:** PCC-01 — Persistent Experience  
7:**Human Authority:** Owner  
17:This document specifies the first executable organ of PCC-01 — Persistent Experience.
27:It does not claim that Persistent Experience has been demonstrated.
31:It defines the software contract that must be accepted by the Human Authority before implementation begins.
53:Persistence is not authority.
68:- Experience Identity represents its persistent identity;
70:- Experience Repository represents controlled conservation and retrieval;
82:2. Experience Identity;
84:4. Experience Repository;
90:It does not yet establish the complete physiology of Persistent Experience.
104:7. Storage != Experience
106:9. Persistence != authority
113:## 6. Central Identity Invariant
117:**ID_before_restart == ID_after_restart**
119:Core Experience MUST be designed so that this invariant can later be demonstrated across real process death and process restart.
123:Core unit tests MUST NOT be presented as proof of real restart continuity.
137:- a storage path;
153:| Experience Identity | CONSTRUIM NOU |
155:| Experience Repository | CONSTRUIM NOU |
182:`lib/python/experience/identity.py`
186:`lib/python/experience/repository.py`
192:No Session, Memory, Evidence, retention, forgetting or protection implementation belongs inside these modules merely for convenience.
204:`tests/experience/test_experience_identity.py`
208:`tests/experience/test_experience_repository.py`
227:- possess exactly one Experience identity;
230:- remain independent from Session identity;
231:- remain independent from Memory identity;
232:- remain independent from Evidence identity;
235:The model MUST NOT perform repository I/O.
239:The model MUST NOT declare authority.
253:Additional fields MUST NOT silently introduce Session, Memory, Evidence, Provenance, authority, retention or protection semantics before their respective phases.
266:- survive repository save/load;
267:- remain identical after reconstruction from persisted representation;
271:- be independent from storage filenames.
279:## 14. Identity Creation
281:A new Experience receives a new identity only during explicit creation.
283:Loading an existing Experience MUST NOT generate a replacement identity.
285:Recovery of an existing Experience MUST NOT generate a replacement identity.
287:Deserialization MUST preserve the stored Experience identity.
291:## 15. Identity Uniqueness
299:unless both objects are explicitly representations of the same persisted Experience.
303:## 16. Identity Stability
309:must hold at the repository boundary.
313:`ID_before_restart == ID_after_restart`
319:## 17. Identity Immutability
323:An Experience whose identity changes becomes a different Experience and MUST NOT be silently treated as continuity of the original.
349:Future phases MAY extend lifecycle semantics for retention, archival, forgetting, conflict or protection.
359:the Experience has been admitted into the Core Experience domain and possesses a valid identity but has not yet entered active operation.
363:- persistence;
366:- authority;
384:- canonical authority.
460:- whether a storage file exists;
467:## 27. Experience Repository Responsibility
469:Experience Repository defines the conservation boundary for Core Experience.
473:Repository is not Experience.
475:Storage is not Experience.
479:## 28. Repository Contract
481:The Core Experience Repository MUST provide behavior equivalent to:
487:The exact Python method names may follow repository conventions discovered in the existing codebase, provided these semantics remain unchanged.
491:## 29. Repository Save Semantics
500:Saving MUST NOT silently create a new Experience identity.
504:## 30. Repository Load Semantics
508:1. reconstruct the corresponding Experience with the same identity and state; or
515:## 31. Repository Identity Invariant
519:`E.experience_id == repository.load(E.experience_id).experience_id`
523:This proves repository identity preservation.
525:It does NOT yet prove real process restart continuity.
529:## 32. Repository Serialization Boundary
535:The repository MAY serialize the model into a deterministic structured representation.
537:The representation MUST preserve enough information to reconstruct the Core Experience without generating a new identity.
556:## 34. Storage Boundary
558:The physical storage mechanism is an implementation detail behind Experience Repository.
560:A filename is not an Experience identity.
564:A serialized record is not authority.
566:The repository abstraction MUST prevent higher-level services from depending unnecessarily on storage layout.
570:## 35. Repository Implementation Strategy
572:The first Core Experience repository SHOULD use the simplest deterministic storage strategy compatible with the repository's existing architecture.
574:Before implementation, existing repository/storage infrastructure MUST be reused where behaviorally compatible.
580:If existing infrastructure cannot satisfy the Experience Repository contract without collapsing epistemic boundaries, a dedicated repository implementation MUST be used.
603:Exact method names may follow repository conventions if semantics remain explicit.
611:1. generate exactly one new Experience identity;
616:Whether creation immediately persists the Experience MUST be explicit in implementation and tests.
629:4. preserve Experience identity;
630:5. persist the resulting state when repository-backed operation is used;
642:4. preserve Experience identity;
643:5. persist the resulting state when repository-backed operation is used;
650:Retrieval MUST load an existing Experience through the repository boundary.
664:`Experience Repository`
666:`serialization/storage`
678:`Experience Identity`
682:Infrastructure MUST depend on domain contracts rather than forcing storage semantics into the domain model where practical.
706:Experience MUST NOT inherit Memory identity.
708:Experience MUST NOT become a Memory record merely because it can persist.
730:Core Experience MUST be designed so provenance can later be associated without rewriting Experience identity semantics.
758:## 49. Authority Boundary
760:Persistence does not grant authority.
770:Authority remains governed separately.
772:Human Authority remains with the Owner where Human Acceptance is required.
778:Experience identity MUST NOT be derived from process identity.
782:The Experience identity must remain capable of surviving that death through later persistence/recovery phases.
788:Experience identity MUST NOT be derived from an AI provider.
796:## 52. Protection Against Concept Collapse
800:- Experience subclasses Session merely to reuse identity;
805:- storage location is treated as Experience identity;
806:- persisted data is treated as authoritative because it persisted;
819:`ExperienceIdentityError`
825:`ExperienceRepositoryError`
831:- malformed identity;
832:- persistence/repository failure.
842:a failed load MUST NOT create a new Experience with a new UUID and return it as if recovery succeeded.
844:That would destroy identity continuity.
857:6. Session identity is not required;
858:7. Memory identity is not required;
859:8. Evidence identity is not required.
863:## 56. Identity Invariants
865:Identity MUST maintain:
867:1. creation generates a valid identity;
869:3. load does not regenerate identity;
870:4. lifecycle transitions do not modify identity;
871:5. serialization round-trip preserves identity;
872:6. repository round-trip preserves identity.
885:6. lifecycle does not imply authority.
889:## 58. Repository Invariants
891:Repository MUST maintain:
893:1. save/load identity preservation;
896:4. no identity regeneration on load;
897:5. no silent replacement of an existing Experience with another identity;
898:6. storage representation remains behind repository boundary.
906:1. one creation request produces one new Experience identity;
907:2. activation preserves identity;
908:3. closure preserves identity;
909:4. retrieval preserves identity;
931:If persisted Core Experience records require a schema marker, that marker MUST be explicit.
939:## 62. Creation Versus Recovery
941:Creation and recovery are distinct operations.
947:Recovery:
949:`persisted existing Experience -> reconstructed same Experience + same Experience ID`
951:Recovery MUST NEVER silently execute creation semantics.
955:## 63. Loading Versus Recovery
957:Core Repository load is a prerequisite for later recovery behavior.
959:A successful load proves that a persisted representation can reconstruct the domain object.
961:It does not alone prove recovery across real process death.
963:Real restart recovery belongs to a subsequent PCC-01 phase.
967:## 64. Core Persistence Boundary
969:The Repository milestone introduces enough persistence behavior to test deterministic save/load.
971:This is not yet the complete PCC-01 persistence/recovery demonstration.
973:The later restart harness MUST start a genuinely new process and recover the Experience from durable state.
977:## 65. Future Restart Harness Requirement
983:3. persists it;
986:6. loads/recover the Experience;
987:7. obtains the recovered Experience ID;
992:`ID_before_restart == ID_after_restart`
1010:## 67. Core Test — Identity Uniqueness
1020:## 68. Core Test — Identity Immutability
1022:Attempt prohibited identity mutation through the supported public API.
1076:This test MUST NOT be described as process-restart Evidence.
1080:## 73. Core Test — Repository Save/Load
1096:## 74. Core Test — Repository Not Found
1113:- it has a valid identity;
1115:- retrieval semantics behave according to the selected persistence contract.
1125:Assert identity preservation and ACTIVE state.
1135:Assert identity preservation and CLOSED state.
1147:This protects the first three epistemic boundaries structurally and behaviorally.
1151:## 79. Core Test — Storage Is Not Identity
1153:Where a file-backed repository is used, test behavior MUST demonstrate that Experience identity is read from domain data and is not inferred solely from an arbitrary runtime object identity.
1155:Storage naming may use Experience ID for deterministic addressing.
1157:That naming convention does not redefine identity semantics.
1167:- explicit failure/not-found;
1169:- no persisted substitute record.
1178:- Identity;
1180:- Repository;
1192:- identity uniqueness;
1193:- identity stability through Core operations;
1196:- repository save/load;
1203:## 83. Core Acceptance Criterion — Identity
1207:`ID_at_creation == ID_after_repository_round_trip`
1213:`ID_before_restart == ID_after_restart`
1227:- storage.
1235:Before reusing existing repository/storage components, implementation review MUST establish behavioral compatibility.
1261:## 88. Explicitly Out of Scope — Protection
1263:Experience Protection is NOT implemented in this milestone.
1265:Protection belongs after the Core organ exists and before the complete persistence/recovery acceptance loop.
1328:Any future canonization requires an explicit Human Authority gate.
1348:3. Experience Identity;
1350:5. Experience Repository;
1363:1. restart harness;
1364:2. recovery test;
1367:5. protection;
1383:Where the repository exposes a genuine unresolved compatibility question, implementation MUST stop at that boundary and inspect behavior.
1385:It MUST NOT silently invent architectural authority.
1396:4. adapt through a boundary if partially compatible;
1405:Existing organs remain valid unless explicitly superseded through accepted architectural authority.
1435:If existing repository behavior is ambiguous:
1448:## 104. Human Authority Rule
1450:The Human Authority for this gate is:
1454:Only the Human Authority may accept or reject this implementation specification.
1483:2. verify its structural integrity;
1513:No later artifact may retroactively convert an earlier research artifact into Canon without explicit authority.
1521:- stable identity;
1527:This success does NOT yet mean PCC-01 Persistent Experience is fully implemented.
1541:Persistent Experience ultimately requires the organism to preserve an identifiable Experience across genuine process death and process restart without confusing it with Session, Memory or Evidence.
1545:**ID_before_restart == ID_after_restart**
1561:These statuses may change only through their respective future evidence and authority gates.
1573:**Experience Identity**
1577:**Experience Repository**
1591:Storage into Experience.
1593:Persistence into authority.
1599:**ID_before_restart == ID_after_restart**
```

### Source: `work/contracts/PCC-01_IMPLEMENTATION_CONTRACT_2026-08-13.md`

```text
1:# PCC-01 — Persistent Experience Implementation Contract
4:Capability: Persistent Experience
6:Human Authority: Owner
19:Acest document transformă anatomia reconciliată și acceptată a PCC-01 — Persistent Experience într-un contract executabil pentru construcția software.
43:**Ce trebuie să existe efectiv în software pentru ca organismul epistemic să poată trăi, identifica, lega, proteja, păstra, recupera și uita controlat Experience fără să falsifice trecutul și fără să confunde Experience cu Session, Memory, Evidence, raw dialogue sau Storage?**
51:Persistent Experience nu este un fișier.
69:Persistent Experience este o **funcție a organismului epistemic**.
91:**Storage != Experience**
95:**Persistence != authority**
113:5. protectorul experienței;
114:6. corpul persistent;
144:- interacțiuni cu repository-ul;
167:Persistarea conversației nu demonstrează Persistent Experience.
207:Fiecare Experience persistentă trebuie să primească o identitate stabilă.
211:- să supraviețuiască restartului;
225:Aceeași Experience recuperată după restart trebuie să poată fi recunoscută drept aceeași Experience.
227:Restartul nu poate produce o identitate nouă doar pentru că procesul software este nou.
263:O Experience persistentă trebuie să aibă un corp reprezentabil.
295:# 16. Persistența
297:O Experience declarată persistentă trebuie să supraviețuiască terminării procesului.
299:Dacă organismul moare operațional și repornește, Experience persistentă trebuie să poată fi recuperată.
303:# 17. Criteriul minim de restart
310:4. Experience este persistată;
313:7. registrul persistent este reconstituit;
325:# 18. Persistența nu este memorie RAM
335:Persistența trebuie demonstrată peste o frontieră reală de restart.
339:# 19. Integritatea corpului persistent
341:Corpul persistent trebuie să poată detecta cel puțin situațiile în care datele necesare sunt:
404:Persistent Experience trebuie să respecte principiul:
451:- dispariție prin restart.
526:# 32. Session și restart
528:Dacă o Session trebuie să continue logic după restart, identitatea și starea minimă necesară continuității trebuie să poată fi recuperate.
530:Restartul procesului nu trebuie confundat automat cu nașterea unei Session complet noi.
650:Recuperarea este funcția prin care organismul regăsește Experience persistentă.
660:# 44. Recuperarea după restart
662:După restart real, organismul trebuie să poată recupera aceeași Experience fără să se bazeze pe obiecte rămase în memorie.
678:Proveniența necesară trebuie să supraviețuiască aceleiași frontiere de restart ca Experience.
688:Restartul nu poate transforma o Experience protejată într-una neprotejată.
755:- persisted;
789:- candidate -> persisted fără criteriul de acceptare atunci când acesta este obligatoriu;
790:- protected -> exported fără autorizație.
807:- invalid identity;
811:- corrupted persistent body;
816:- persistence failure.
822:Nicio eroare de persistență nu poate fi raportată ca succes.
830:# 59. Atomicitatea minimă
834:În special, implementarea trebuie să analizeze atomicitatea pentru:
836:- persistarea Experience;
849:În special, aceeași comandă de persistare nu trebuie să creeze automat mai multe Experience identice dacă intenția este aceeași operație.
870:- timpul persistării;
884:Ordinea accidentală a citirii din storage nu trebuie tratată drept adevăr istoric.
890:Corpul persistent trebuie să aibă o strategie de versiune.
900:Dacă schema persistentă evoluează, migrarea trebuie să fie:
929:- storage;
930:- persistence;
931:- repository state;
951:5. nu face storage-ul autoritatea semantică;
980:# 72. Un singur adevăr pentru Session identity
982:Trebuie stabilită o fiziologie unică pentru Session identity.
990:# 73. Storage adapter
992:Backend-ul persistent trebuie accesat printr-o frontieră care nu obligă restul organismului să considere backend-ul drept model semantic.
999:- adapterul de persistență.
1013:**Experience -> serialized body -> persistent storage -> load -> Experience**
1029:Implementarea trebuie să poată verifica integritatea minimă a corpului persistent.
1045:# 78. Consistența
1050:- dar corpul persistent lipsește;
1080:# 80. Recovery
1082:Dacă la boot este detectată o stare recuperabilă, mecanismul de recovery trebuie să fie explicit.
1084:Recovery nu trebuie să ascundă pierderea de date.
1092:Închiderea normală trebuie să lase corpul persistent într-o stare coerentă.
1096:Testele trebuie să includă cel puțin o formă de restart în care noul proces nu reutilizează memoria vechiului proces.
1108:- persist Experience;
1178:Logurile nu sunt storage-ul Experience.
1191:- persist;
1196:- recovery semnificativ;
1203:Human Authority rămâne distinctă de mecanismele automate.
1252:Dacă un corp persistent este corupt, organismul trebuie să poată raporta corupția.
1276:# 97. Conflict persistent
1278:Conflictul trebuie să supraviețuiască restartului dacă nu a fost rezolvat înainte de restart.
1280:Restartul nu este mecanism de rezolvare a conflictului.
1284:# 98. Retention după restart
1286:Politica de retenție trebuie să supraviețuiască restartului.
1292:# 99. Forgetting după restart
1294:Dacă o operație de forgetting este în curs sau necesită stare persistentă, restartul nu trebuie să producă o stare imposibil de explicat.
1300:# 100. Protecția după restart
1306:# 101. Binding după restart
1308:Binding-ul Experience <-> Session trebuie să poată fi recuperat după restart fără a fi recalculat arbitrar din indicii incomplete.
1312:# 102. Proveniența după restart
1314:Proveniența trebuie să fie recuperabilă după restart.
1316:Dacă organismul își amintește conținutul, dar nu mai știe de unde provine, Persistent Experience este incompletă.
1353:Înainte sau în timpul persistării trebuie aplicată politica de protecție necesară.
1355:Nu trebuie să existe o fereastră în care materialul protejat este persistat neprotejat și ulterior „reparat” fără justificare.
1359:# 107. Bucla de viață — persistență
1361:Experience este serializată și persistată prin corpul fizic ales.
1363:Succesul este declarat numai după satisfacerea criteriului de persistență stabilit de adapter.
1409:**candidate -> Experience -> identity -> protection -> persistence -> Session binding -> process death -> process restart -> recovery -> inspection -> retention/forgetting behavior**
1429:- persistence;
1432:- protection;
1438:# 117. Testul de restart real
1440:Cel puțin un test trebuie să creeze o frontieră reală între procesul care persistă și procesul care recuperează.
1454:**Experience ID înainte de restart == Experience ID după restart**
1456:pentru aceeași Experience persistentă.
1462:Testul trebuie să demonstreze că binding-ul corect poate fi recuperat după restart.
1476:După restart, proveniența trebuie să fie echivalentă semantic cu cea persistată înainte de restart.
1488:Trebuie demonstrat că politica de retenție produce tranziția așteptată și supraviețuiește restartului unde este relevant.
1512:Trebuie introdusă cel puțin o stare persistentă coruptă sau incompatibilă controlat.
1559:- testul de restart real;
1561:- dovada binding-ului persistent;
1568:- starea repository-ului;
1623:# 138. Condiția 2 — persistența
1625:Experience trebuie să supraviețuiască restartului real.
1637:Experience <-> Session binding trebuie să fie explicit, persistent, inspectabil și sigur în fața ambiguității/conflictului.
1643:Protecția obligatorie trebuie să funcționeze și să supraviețuiască restartului.
1659:# 144. Condiția 8 — recovery
1661:Restartul, reîncărcarea și stările recuperabile trebuie tratate fără falsificarea succesului.
1685:Dacă procesul de guvernanță PCC-01 cere acceptare umană finală, numai Human Authority poate acorda acea acceptare.
1718:- backup/recovery;
1760:7. adapterul persistent;
1767:14. recovery;
1770:17. testul end-to-end de restart.
1801:# 156. Faza III — corpul persistent
1803:După stabilizarea modelului logic, corpul persistent trebuie conectat prin adapter.
1807:Schema storage nu trebuie să dicteze anatomia Experience.
1827:Protection, retention, archive și forgetting trebuie integrate în ciclul de viață.
1833:# 159. Faza VI — recovery
1837:Această fază transformă persistența din presupunere în comportament demonstrabil.
1877:- o pot recupera după restart;
1888:- inventează identități după restart;
1893:- tratează storage-ul drept adevăr semantic;
1924:Persistent Experience trebuie să rămână independentă semantic de furnizorul AI.
1930:# 167. Repository independence
1932:PCC-01 poate fi folosit de AI-Toolkit pentru experiențe legate de repository.
1934:Dar modelul Experience nu trebuie să fie limitat semantic la GitHub sau la un repository specific.
1987:- storage-ul;
2018:Implementarea poate descoperi fapte noi despre repository.
2040:Duplicarea identității, Session management-ului sau persistence-ului trebuie evitată.
2054:Persistența trebuie să funcționeze în mediile suportate de AI-Toolkit fără să depindă de o particularitate accidentală a telefonului de dezvoltare.
2110:Persistența nu conferă autoritate.
2130:Un test de persistence nu demonstrează automat privacy.
2142:- identity;
2143:- persistence;
2144:- restart;
2145:- Session identity;
2150:- protection;
2154:- recovery;
2209:- demonstrația restart;
2211:- demonstrația protection;
2332:- apariția unui al doilea storage incompatibil;
2358:- storage complete;
2360:- restart test complete.
2374:3. identități persistente;
2377:6. protection metadata;
2378:7. persistence;
2381:10. recovery;
2395:Persistent Experience include și capacitatea sănătoasă de a nu păstra ceea ce nu mai trebuie păstrat.
2427:Trebuie alterat controlat un corp persistent de test.
2437:Trebuie demonstrat că după restart organismul poate explica originea Experience și relația ei cu Session.
2445:Aceasta este frontiera minimă prin care se demonstrează că experiența aparține organismului persistent și nu memoriei volatile a procesului anterior.
2467:Dacă există rebinding sau alte tranziții istorice în scenariul de acceptare, istoricul relevant trebuie să fie recuperabil după restart.
2495:- persistence;
2498:- protection;
2501:- recovery;
2511:Storage nu trebuie să controleze semantic Experience.
2513:Dashboard nu trebuie să controleze storage.
2533:**Identity**
2535:**Protection**
2537:**Persistence**
2541:**Recovery**
2557:**raw dialogue -> database -> "Persistent Experience implemented"**
2569:**provider conversation id -> Session identity -> permanent truth**
2611:O arhitectură frumoasă fără persistență reală nu satisface PCC-01.
2631:- pierdere la restart;
2654:- bucla reală de restart trece;
2770:6. persista Experience;
2776:12. recupera după restart;
2798:7. confunda Storage cu Experience;
2799:8. confunda persistence cu authority;
2823:**Identity**
2826:**Protection**
2829:**Persistent Body**
2850:**Recovery**
2851:readuce Experience după restart.
2871:Identity este continuitatea prin care organismul știe că vorbește despre aceeași experiență.
2873:Protection seamănă cu barierele și mecanismele de protecție.
2875:Persistent Body este țesutul în care experiența poate supraviețui stării operaționale de moment.
2889:Recovery este reamintirea după o întrerupere.
2927:Persistent Experience există pentru a oferi continuitate epistemică.
2937:Persistența trebuie să conserve istoria, nu să o reinventeze.
2981:Persistent Experience nu trebuie să devină o justificare pentru retenție nelimitată.
2989:Persistența fără protecție nu este o funcție sănătoasă.
3019:Anatomia acceptată a PCC-01 poate fi transformată într-o implementare software coerentă numai dacă Persistent Experience este construită ca o fiziologie de continuitate și nu ca o simplă funcție de stocare.
3031:- Experience identity;
3032:- Session identity;
3035:- persistent storage boundary;
3038:- protection;
3044:- restart recovery;
3094:- storage;
3098:- privacy/protection;
3211:**Storage**
3212:= suport fizic pentru persistență.
3226:**Human Authority**
3247:**Storage != Experience**
3251:**Persistence != authority**
3259:Pentru o Experience persistentă sănătoasă:
3261:**ID_before_restart == ID_after_restart**
3271:**provenance_before_restart ≈ provenance_after_restart**
3281:**binding_before_restart == binding_after_restart**
3289:Restartul nu poate reduce implicit protecția.
3301:Un conflict nerezolvat înainte de restart rămâne conflict după restart dacă faptele nu s-au schimbat.
3313:Persistarea unei afirmații nu îi crește automat autoritatea epistemică.
3333:Necesită decizia Human Authority.
3337:# 286. Întrebarea pentru Human Authority
3399:- Storage;
3400:- Human Authority.
3402:Contractul cere persistență reală peste restart.
3426:Persistent Experience trebuie construită ca o funcție vie a organismului epistemic.
3456:Acesta este contractul candidat pentru construirea primei implementări reale PCC-01 — Persistent Experience.
3468:END OF PCC-01 — PERSISTENT EXPERIENCE IMPLEMENTATION CONTRACT
```

### Source: `work/planning/PCC-01_IMPLEMENTATION_INVENTORY_AND_BUILD_PLAN.md`

```text
1:# PCC-01 — Persistent Experience Implementation Inventory and Build Plan
4:Capability: Persistent Experience  
6:Human Authority: Owner  
20:Acest document transformă PCC-01 Implementation Contract acceptat de om într-un inventar concret al corpului software existent și într-un plan de construcție pentru funcția Persistent Experience.
54:- modelele pot reprezenta structuri anatomice;
55:- storage-ul poate reprezenta țesut de conservare;
115:- o înregistrare accidentală într-un storage.
133:Session trebuie să poată dispărea fără ca Experience persistentă să dispară.
169:# 10. Frontiera Storage
171:Storage este infrastructură de conservare.
173:Storage nu este obiectul conservat.
177:**Storage != Experience**
179:Schimbarea backend-ului de storage nu trebuie să schimbe identitatea semantică a Experience.
193:# 12. Frontiera Authority
195:Persistența unei informații nu îi conferă autoritate.
199:**Persistence != authority**
219:Auditul anterior nu a demonstrat existența unui organ Python PCC-01 care să implementeze complet identitatea și ciclul Persistent Experience.
231:`work/persistent-experience/active/`
239:Nu le tratăm automat ca storage.
255:- identity;
259:- protection state;
260:- persistence state;
292:**ID_before_restart == ID_after_restart**
294:Dacă obiectul recuperat după restart reprezintă aceeași Experience, identitatea sa trebuie păstrată.
306:candidate -> Experience -> identified -> protected -> persisted -> bound -> recoverable
310:recoverable -> retained
312:recoverable -> archived
314:recoverable -> forgotten
316:recoverable -> conflicted
318:recoverable -> ambiguous
326:Trebuie să existe o frontieră între materialul candidat și Experience persistentă.
344:Înainte de persistență trebuie validate invariantele minime.
352:# 23. Experience protection
354:Contractul cere protejarea Experience înainte ca aceasta să intre în persistența durabilă.
358:Protection trebuie să fie o stare observabilă, nu doar o presupunere.
362:# 24. Experience persistence
364:Persistența Experience trebuie implementată explicit.
372:# 25. Semantic persistence existent
374:Repository-ul conține infrastructură de persistență în alte subsisteme, inclusiv semantic repository intelligence.
384:# 26. Experience repository
386:PCC-01 are nevoie de o frontieră de repository/storage dedicată Experience.
393:- load by identity;
399:- restart recovery.
403:# 27. Persistența atomică
405:Nu trebuie să existe stări în care Experience pare persistentă runtime-ului, dar nu este conservată durabil.
411:# 28. Recovery
413:Recovery după restart este funcție obligatorie.
417:Recovery nu înseamnă reconstruirea unei Experience noi din text.
419:Trebuie recuperată aceeași identitate persistentă.
423:# 29. Restart boundary
433:Repository-ul conține un subsistem `session_runtime`.
439:- storage.
477:Experience identity
481:Session identity.
493:# 35. Binding persistence
495:Binding-ul relevant trebuie să supraviețuiască restartului dacă contractul cere recuperarea relației.
501:# 36. Binding recovery
503:După restart trebuie să putem demonstra:
508:- relația persistentă poate fi inspectată.
524:Aceasta este una dintre diferențele fundamentale dintre runtime state și Persistent Experience.
530:Repository-ul conține mai multe componente asociate Memory.
552:Storage-ul Memory poate oferi precedent tehnic.
574:Repository-ul conține mecanisme Evidence.
613:- identity;
614:- persistence;
615:- restart;
616:- recovery;
620:- protection;
624:- failure behavior.
630:Evidence poate conține referința la Experience identity.
638:Repository-ul conține mecanisme de provenance în zona knowledge/CDM.
650:Fiecare Experience persistentă trebuie să poată indica originea sa.
696:Repository-ul conține Execution Engine.
714:Persistent Experience nu trebuie cuplată exclusiv la execuția autonomă.
720:Repository-ul conține Review Agent.
782:Retention trebuie separată de storage existence.
818:# 65. Protection policy
835:Persistența fără control de acces nu satisface contractul.
848:- persistence;
849:- recovery;
858:# 68. Failure model
870:Un obiect invalid trebuie refuzat înainte de a deveni Experience persistentă validă.
874:# 70. Duplicate identity
876:Dacă aceeași identity este revendicată incompatibil de două corpuri, operația trebuie refuzată sau conflictul reprezentat explicit.
882:Load pentru identity inexistentă trebuie să producă rezultat explicit.
888:# 72. Corrupted persistence
890:Dacă storage-ul persistent este corupt, recovery nu trebuie să pretindă succes.
892:Trebuie produs failure observabil și Evidence.
910:# 75. Forgetting failure
916:# 76. Restart failure
918:Dacă recovery după restart eșuează, PCC-01 nu poate trece poarta IMPLEMENTED.
924:Persistent Experience trebuie să fie inspectabilă prin interfețe controlate.
946:Dashboard-ul poate deveni suprafață de observare pentru Persistent Experience.
974:Experience persistentă nu trebuie să depindă de existența procesului care a creat-o.
996:Serializare -> persistență -> reload nu trebuie să schimbe identitatea semantică.
1008:Persistența trebuie să poată identifica versiunea structurii Experience.
1021:- persisted_at;
1022:- recovered_at, când este Evidence/runtime metadata;
1046:Acesta nu trebuie să fie doar un wrapper peste storage.
1055:- identity;
1057:- protection;
1058:- persistence;
1069:# 93. Experience Service nu este Storage
1073:Repository-ul păstrează corpul persistent.
1079:# 94. Experience Repository
1081:Repository-ul este organul de conservare.
1089:Modelul este anatomia obiectului persistent.
1095:# 96. Experience Identity
1097:Identity este mecanism transversal.
1149:Nu este necesară pentru primul test minim de restart dacă nu este cerută de calea executabilă.
1191:# 107. Build Phase 2 — Identity
1193:Construim mecanismul de identity.
1207:# 109. Build Phase 4 — Repository
1209:Construim persistența Experience.
1215:# 110. Build Phase 5 — Recovery
1217:Construim recovery după restart.
1237:# 113. Build Phase 8 — Protection
1283:UI nu poate compensa lipsa persistence.
1285:Evidence nu poate compensa lipsa recovery.
1303:# 123. Test — identity uniqueness
1305:Două Experience distincte nu trebuie să primească accidental aceeași identity.
1309:# 124. Test — identity stability
1311:Serializarea și reload-ul nu trebuie să schimbe identity.
1315:# 125. Test — persistence
1317:Experience trebuie să existe în storage după operația de persistence confirmată.
1327:# 127. Test — process restart
1333:# 128. Test — recovery
1335:Procesul nou trebuie să recupereze Experience persistentă.
1339:# 129. Test — restart invariant
1343:**ID_before_restart == ID_after_restart**
1357:Experience identity != Session identity.
1363:Trebuie demonstrat că dispariția runtime-ului Session nu șterge automat Experience persistentă.
1373:# 134. Test — protection
1421:# 142. Test — duplicate identity
1423:Conflictul de identity trebuie detectat.
1427:# 143. Test — missing identity
1435:Experience -> serialization -> persistence -> load -> Experience
1443:Schimbarea providerului nu trebuie să schimbe identitatea Experience deja persistente.
1469:**candidate -> Experience -> identity -> protection -> persistence -> Session binding -> process death -> process restart -> recovery -> inspection -> retention/forgetting behavior**
1481:- identity înainte de restart;
1482:- persistence confirmată;
1485:- process restart;
1486:- identity după restart;
1487:- recovered state;
1490:- failures relevante.
1508:# 153. Evidence integrity
1526:- restart real este demonstrat;
1527:- identity este stabilă;
1565:- recovery;
1571:- failure recovery;
1593:**Experience Identity**
1599:**Experience Repository**
1605:**Experience Protection**
1701:# 169. Interdicția storage-as-Experience
1705:**Storage != Experience**
1709:# 170. Interdicția persistence-as-authority
1711:O Experience persistentă nu devine automat adevăr.
1713:**Persistence != authority**
1727:Persistent Experience trebuie să supraviețuiască morții procesului fără pierderea identității.
1731:# 173. Invariantul de restart
1733:**ID_before_restart == ID_after_restart**
1746:- Storage;
1754:Recovery nu trebuie să producă o Experience fără trasabilitate atunci când proveniența este obligatorie.
1758:# 176. Invariantul de failure
1770:# 178. Invariantul de protection
1791:- identity;
1794:- repository.
1800:**PCC-01 PERSISTENCE AND RESTART**
1804:- durable persistence;
1806:- process restart;
1807:- recovery;
1808:- identity invariant.
1819:- persistent binding;
1820:- recovery of relationship;
1827:**PCC-01 PROVENANCE AND PROTECTION**
1862:- identity;
1870:# 189. Poarta restart
1872:După Persistence and Restart trebuie demonstrat:
1874:**ID_before_restart == ID_after_restart**
1949:- identity;
1950:- restart;
1953:- protection;
1998:- persistence infrastructure.
2000:Dar auditul nu a demonstrat existența organului fiziologic complet Persistent Experience.
2032:Identity  
2036:Protection  
2038:Persistence  
2044:Process Restart  
2046:Recovery  
2060:Persistent Experience există cu adevărat numai dacă organismul poate trece printr-o întrerupere reală a procesului și poate reveni cu aceeași Experience identificabilă și inspectabilă.
2068:**same persistent Experience identity across real process restart**
2096:Cel mai mare risc nu este lipsa storage-ului.
2138:# 213. Principiul de restart
2140:Persistența nu este demonstrată până când procesul nu moare cu adevărat și un proces nou recuperează corpul persistent.
2146:Nicio stare persistentă nu înlocuiește autoritatea umană asupra Canonului.
2157:4. Experience Identity;
2159:6. Experience Repository;
2162:9. restart harness;
2163:10. recovery test;
2166:13. protection;
2185:Numele exact al package-ului trebuie confirmat împotriva convențiilor repository-ului înainte de creare.
2189:**persistent experience**
2195:# 218. Compatibilitatea repository-ului
2205:- persistence patterns.
2211:Acest plan nu autorizează crearea arbitrară a unei structuri de directoare fără verificarea repository-ului real.
2225:Dacă schema persistentă evoluează, migrarea trebuie tratată explicit înainte de production-ready.
2241:Persistența doar în RAM este insuficientă.
2267:# 227. Forgetting authority
2285:# 230. Recovery semantics
2287:Recovery trebuie să restabilească o reprezentare validă, nu doar bytes.
2293:După recovery, organismul trebuie să poată inspecta Experience într-o formă controlată.
2311:# 234. Direct storage mutation
2313:Modificarea directă a storage-ului în afara contractului trebuie considerată neautorizată sau unsupported.
2331:# 237. Recovery from archive
2375:# 244. Restart test isolation
2377:Restart test trebuie să folosească procese separate, nu resetarea unui singleton în același proces.
2393:# 247. Failure Evidence
2502:# 259. Starea Experience persistence
2508:# 260. Starea Experience recovery
2550:| Experience Identity | CONSTRUIM NOU | identitate persistentă |
2553:| Experience Repository | CONSTRUIM NOU | conservare |
2580:| Storage / Experience | Storage != Experience |
2582:| Persistence / authority | Persistence != authority |
2592:| Core Built | model + identity + lifecycle + service + repository |
2593:| Persistence Demonstrated | durable save/load |
2594:| Restart Demonstrated | proces nou recuperează aceeași identity |
2609:- identity există;
2611:- repository există;
2614:- save/load păstrează identity.
2618:# 270. Definition of Restart Done
2620:Restart este complet numai dacă:
2622:- Experience este persistată;
2626:- identity este aceeași;
2741:+ Persistence  
2743:+ Protection  
2760:persista,  
2786:Repository-ul conține organe reutilizabile importante.
2788:Persistent Experience nu trebuie construit ca un organism paralel.
2842:Înainte de prima modificare trebuie verificată încă o dată structura exactă actuală a repository-ului și trebuie stabilite căile concrete ale package-ului și testelor.
2858:El nu confundă persistența cu autoritatea.
2868:END OF PCC-01 — PERSISTENT EXPERIENCE IMPLEMENTATION INVENTORY AND BUILD PLAN
```

## 8. Current Write Physiology

```text
lib/python/experience/persistent_repository.py
  line 221: replace
  line 234: unlink

lib/python/experience/protection_repository.py
  line 243: replace
  line 256: unlink

```

## 9. Failure Windows

Given two independently persisted organs keyed by the same ExperienceId, coordination must reason about at least these states:

| Experience record | Protection record | Interpretation |
|---|---|---|
| absent | absent | no durable pair exists |
| present | absent | partial pair; Protection missing |
| absent | present | orphan Protection |
| present | present | candidate coordinated pair |

The final row is not automatically valid merely because both records exist.

Identity agreement and record validity must still be checked.

The current organism therefore has a physiological gap between:

`independent durable organs`

and

`coordinated durable organism state`.

## 10. Candidate Coordination Physiologies

This section classifies possibilities. It does not authorize implementation.

### A. Collapse Protection into Experience serialization

**Classification:** REJECT

Reason:

- violates the accepted anatomical separation;
- turns independent Protection physiology into embedded Experience state;
- conflicts with the demonstrated independent Protection persistence design.

### B. Write Experience first, then Protection

**Classification:** INSUFFICIENT

A death between writes can leave Experience without its required Protection state.

### C. Write Protection first, then Experience

**Classification:** CURRENT EXPERIMENTAL ORDER / INSUFFICIENT**

RUN 026 deliberately uses this order.

A death between writes can leave orphan Protection.

### D. Compensating rollback across two repositories

**Classification:** CANDIDATE, BUT NOT CRASH-SAFE BY ITSELF

Rollback can address ordinary exceptions while the process remains alive.

It cannot guarantee repair if the process dies before compensation executes.

### E. Durable coordination record / journal

**Classification:** STRONG CANDIDATE

A separate durable coordination record can represent an incomplete physiological transition without collapsing Experience and Protection.

Recovery can inspect the durable coordination state after restart.

### F. Single transactional storage mechanism underneath separate repositories

**Classification:** POSSIBLE FUTURE ADAPTER

This may provide stronger atomicity while retaining logical separation, but must not be assumed available from the current file repositories.

### G. Ignore partial pairs

**Classification:** REJECT

Ignoring partial durable state would hide uncertainty instead of representing it.

## 11. Required Coordination Invariants

Any later implementation must preserve all of the following:

1. Experience and Protection remain distinct organs.
2. Both are related by the same ExperienceId.
3. Protection is not embedded into the Experience serialization merely to obtain atomicity.
4. Persistence does not become authority.
5. A partial durable pair must be detectable.
6. A partial durable pair must not be silently interpreted as a complete historical fact.
7. Recovery after process death must have an explicit rule for incomplete coordination.
8. Recovery must not fabricate missing Protection.
9. Recovery must not fabricate missing Experience.
10. An orphan Protection record must be representable as an abnormal durable condition.
11. An Experience record missing required Protection must be representable as an abnormal durable condition.
12. Reconciliation behavior must be deterministic.
13. Reconciliation must preserve ExperienceId.
14. The existing central invariant remains:

`ID_before_restart == ID_after_restart`

15. Protection continuity already demonstrated by RUN 026 must not regress.
16. Existing Experience serialization must remain independent.
17. Human Acceptance remains distinct from implementation.
18. No coordination mechanism may implicitly modify Canon.

## 12. Recommended Physiology

**Recommendation:** introduce a small independent Persistence Coordination organ rather than collapsing the existing organs.

Proposed anatomy:

`ExperiencePersistenceCoordinator`

with a durable coordination record keyed by:

`ExperienceId`

The coordination record should describe the state of the persistence operation, not become Experience, Protection, Evidence, Session, or authority.

Candidate coordination lifecycle:

`PREPARING -> PROTECTION_WRITTEN -> EXPERIENCE_WRITTEN -> COMPLETE`

with an explicit abnormal/recovery condition for interrupted transitions.

The exact lifecycle names are a proposal from this inspection, not Canon.

### Why this anatomy is preferred

- reuse before duplication;
- integrate; do not collapse;
- Experience remains Experience;
- Protection remains Protection;
- partial writes become observable rather than hidden;
- restart recovery can inspect a durable physiological transition;
- the mechanism can later be replaced by a transactional storage adapter without changing the epistemic model.

### Required recovery question

The next implementation stage must define behavior for each durable interruption point:

1. coordinator exists, neither organ written;
2. Protection written, Experience absent;
3. Experience written, Protection absent;
4. both written but coordinator not marked complete;
5. both written and coordinator complete.

No case may be resolved by fabricating historical facts.

## 13. Inspection Boundary

```text
lib/python/experience/protection_persistence.py
lib/python/experience/protection_repository.py
tests/experience/harness/pcc01_protection_restart_reader.py
tests/experience/harness/pcc01_protection_restart_writer.py
tests/experience/test_experience_protection_persistence.py
tests/experience/test_experience_protection_repository.py
tests/experience/test_experience_protection_restart.py
work/implementation-reports/PCC-01/PCC-01_EXPERIENCE_PROTECTION_PERSISTENCE_COORDINATION_INSPECTION_RUN_027.md
work/implementation-reports/PCC-01/PCC-01_PROTECTION_PERSISTENCE_PHYSIOLOGY_DESIGN_INSPECTION_RUN_024.md
work/implementation-reports/PCC-01/PCC-01_PROTECTION_PERSISTENCE_REPOSITORY_IMPLEMENTATION_REPORT_RUN_025.md
work/implementation-reports/PCC-01/PCC-01_PROTECTION_REAL_PROCESS_RESTART_CONTINUITY_REPORT_RUN_026.md
work/implementation-reports/PCC-01/PCC-01_PROTECTION_RESTART_CAUSAL_INSPECTION_RUN_023.md
work/implementation-reports/PCC-01/PCC-01_PROTECTION_RESTART_CONTINUITY_REPORT_RUN_022.md
work/implementation-reports/PCC-01/PCC-01_RUN020_EVIDENCE_CONSERVATION_REPORT_RUN_021.md
```

PASS: RUN 027 modified no software or tests.

## 14. Required Behavioral Evidence For The Next Stage

A later implementation must test at minimum:

- successful coordinated persistence;
- same ExperienceId across both organs;
- process death before either organ write;
- process death after Protection write;
- process death after Experience write or an equivalent deliberately constructed abnormal state;
- process death after both writes but before coordination completion;
- recovery of a completed pair;
- deterministic detection/reconciliation of incomplete pairs;
- no fabricated missing Experience;
- no fabricated missing Protection;
- Persistence != authority after recovery;
- complete Experience regression.

The failure injection must use real process boundaries where the claim concerns crash recovery.

## 15. Epistemic Interpretation

RUN 027 is an investigation.

It does not implement Persistence Coordination.

It does not prove atomic Experience + Protection persistence.

It does not alter the already demonstrated RUN 026 Protection continuity result.

The proposed coordinator is an implementation hypothesis derived from the inspected anatomy and must not be treated as Canon.

## 16. PCC-01 Status

**Core Experience identity continuity:** DEMONSTRATED LOCALLY

**Protection continuity across real process restart:** DEMONSTRATED LOCALLY

**Experience + Protection persistence coordination:** NOT DEMONSTRATED

**PCC-01 Implementation Status:** NOT DEMONSTRATED

**Canonical Status:** NOT CANON

**Production Status:** NOT PRODUCTION-READY

## 17. Conservation

No `git add` performed.

No commit performed.

No push performed.

## 18. Final Result

**RUN 027: PASS — INSPECTION COMPLETE**

**Recommended next organ:** Experience Persistence Coordinator with durable coordination state.

**NEXT REQUIRED ACTION:** GPT/Human inspection of RUN 027 before any coordination software is built.

---

END OF PCC-01 EXPERIENCE + PROTECTION PERSISTENCE COORDINATION INSPECTION — RUN 027
