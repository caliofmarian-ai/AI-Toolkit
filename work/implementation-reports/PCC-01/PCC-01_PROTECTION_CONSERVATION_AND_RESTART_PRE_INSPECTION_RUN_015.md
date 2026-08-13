# PCC-01 — PROTECTION CONSERVATION AND RESTART PRE-INSPECTION — RUN 015

**Stage:** Protection conservation + persistence/recovery/restart investigation

**Expected baseline:** `3e5f63ad101e080cf765f4a54383c3246d3866fb`

**Protection predecessor:** `work/implementation-reports/PCC-01/PCC-01_PROTECTION_IMPLEMENTATION_REPORT_RUN_014.md`

**Software construction in this run:** NONE

**Canon modification:** NONE

---

## 1. Baseline

```text
Expected:    3e5f63ad101e080cf765f4a54383c3246d3866fb
LOCAL:       3e5f63ad101e080cf765f4a54383c3246d3866fb
origin/main: 3e5f63ad101e080cf765f4a54383c3246d3866fb
PASS: baseline verified
```

## 2. Pre-Conservation Working Tree

```text
 M lib/python/experience/__init__.py
?? lib/python/experience/protection.py
?? tests/experience/test_experience_protection.py
?? work/implementation-reports/PCC-01/PCC-01_PROTECTION_CONSERVATION_AND_RESTART_PRE_INSPECTION_RUN_015.md
?? work/implementation-reports/PCC-01/PCC-01_PROTECTION_IMPLEMENTATION_REPORT_RUN_014.md
?? work/implementation-reports/PCC-01/PCC-01_PROTECTION_PRE_IMPLEMENTATION_INSPECTION_RUN_013.md

PASS: exact Protection/RUN 013/RUN 014/RUN 015 boundary
```

## 3. Prior Evidence

```text
PASS: RUN 013 inspection = PASS
PASS: RUN 014 implementation = PASS
PASS: Protection tests = 12 passed
PASS: complete Experience tests = 66 passed
```

## 4. Fresh Behavioral Verification

### Protection
```text
............                                                             [100%]
12 passed in 0.27s
```

### Complete Experience
```text
..................................................................       [100%]
66 passed in 0.41s
```

## 5. Protection Integrity

```text
lib/python/experience/__init__.py
2382c0a222a71ad0c482436b67f45732f10cf28a699e16145b56fb7e0be89345

lib/python/experience/protection.py
dfd9e1f087ef86902cdfe16bb0569e281badf95ad450f6dcad6288a603d1d3fa

tests/experience/test_experience_protection.py
0ab5cd19211022be40eeef943bea318de18615016c52f0816c07eb7ff3d53ae1

work/implementation-reports/PCC-01/PCC-01_PROTECTION_PRE_IMPLEMENTATION_INSPECTION_RUN_013.md
61ff4508a66fe60ea647b65337cb2d25d0dad6d43a3d2bf9e4c912b601b54249

work/implementation-reports/PCC-01/PCC-01_PROTECTION_IMPLEMENTATION_REPORT_RUN_014.md
1e830c921c3934f3d80ac1b9289c33fe2a02541bd0ccdad4eaedf77740dc4747
```

## 6. Staging Boundary

```text
lib/python/experience/__init__.py
lib/python/experience/protection.py
tests/experience/test_experience_protection.py
work/implementation-reports/PCC-01/PCC-01_PROTECTION_IMPLEMENTATION_REPORT_RUN_014.md
work/implementation-reports/PCC-01/PCC-01_PROTECTION_PRE_IMPLEMENTATION_INSPECTION_RUN_013.md

PASS: exactly five authorized artifacts staged
PASS: RUN 015 remains outside conservation commit
```

## 7. Staged Integrity

PASS: all staged bytes equal inspected local bytes.

## 8. Protection Conservation Interpretation

The Protection organ is eligible for conservation because:

- its pre-implementation inspection exists;
- its local implementation report is PASS;
- dedicated Protection behavior passes;
- complete Experience regression behavior passes;
- the staged boundary contains only authorized PCC-01 artifacts.

This conservation does NOT mean complete PCC-01 implementation.

This conservation does NOT demonstrate restart identity continuity.

## 9. Protection Conservation Result

```text
Protection conservation HEAD: ecf446ed0ad7fe165f54176cad0dad528e006c58
LOCAL:       ecf446ed0ad7fe165f54176cad0dad528e006c58
origin/main: ecf446ed0ad7fe165f54176cad0dad528e006c58
PASS: LOCAL == origin/main
```

## 10. Persistence / Recovery / Restart Candidate Tissue

Occurrence does not demonstrate behavioral compatibility.

```text
```

## 11. Current Experience Persistence-Facing Anatomy

### `lib/python/experience/identity.py`

```python
"""Stable identity for PCC-01 Core Experience."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


class ExperienceIdentityError(ValueError):
    """Raised when an Experience identity is malformed."""


@dataclass(frozen=True, slots=True)
class ExperienceId:
    """Immutable identity belonging to one Experience."""

    value: str

    def __post_init__(self) -> None:
        try:
            parsed = UUID(self.value)
        except (ValueError, TypeError, AttributeError) as exc:
            raise ExperienceIdentityError(
                f"Invalid Experience identity: {self.value!r}"
            ) from exc

        canonical = str(parsed)

        if self.value != canonical:
            raise ExperienceIdentityError(
                "Experience identity must use canonical UUID representation"
            )

    @classmethod
    def create(cls) -> "ExperienceId":
        """Create a new Experience identity."""
        return cls(str(uuid4()))

    @classmethod
    def from_string(cls, value: str) -> "ExperienceId":
        """Reconstruct an existing identity without regeneration."""
        return cls(value)

    def __str__(self) -> str:
        return self.value
```

### `lib/python/experience/model.py`

```python
"""Domain anatomy of one PCC-01 Core Experience."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone

from .identity import ExperienceId
from .lifecycle import ExperienceState, transition


@dataclass(frozen=True, slots=True)
class Experience:
    """One Core Experience domain entity.

    Experience remains distinct from Session, Memory, Evidence,
    raw dialogue, process, provider, storage, and authority.
    """

    experience_id: ExperienceId
    created_at: datetime
    state: ExperienceState

    def __post_init__(self) -> None:
        if self.created_at.tzinfo is None:
            raise ValueError("Experience created_at must be timezone-aware")

    @classmethod
    def create(cls) -> "Experience":
        """Create a new Experience in CREATED state."""
        return cls(
            experience_id=ExperienceId.create(),
            created_at=datetime.now(timezone.utc),
            state=ExperienceState.CREATED,
        )

    def activate(self) -> "Experience":
        """Transition CREATED -> ACTIVE while preserving identity."""
        return replace(
            self,
            state=transition(self.state, ExperienceState.ACTIVE),
        )

    def close(self) -> "Experience":
        """Transition ACTIVE -> CLOSED while preserving identity."""
        return replace(
            self,
            state=transition(self.state, ExperienceState.CLOSED),
        )
```

### `lib/python/experience/repository.py`

```python
"""Repository boundary for PCC-01 Core Experience."""

from __future__ import annotations

from abc import ABC, abstractmethod

from .identity import ExperienceId
from .model import Experience


class ExperienceRepositoryError(RuntimeError):
    """Base error for Experience repository operations."""


class ExperienceNotFoundError(ExperienceRepositoryError):
    """Raised when an Experience cannot be found by its identity."""


class ExperienceAlreadyExistsError(ExperienceRepositoryError):
    """Raised when creation would replace an existing Experience."""


class ExperienceRepository(ABC):
    """Storage-independent contract for Core Experience.

    The repository stores and retrieves Experience state.

    Storage is not Experience.
    Persistence is not authority.
    """

    @abstractmethod
    def add(self, experience: Experience) -> None:
        """Store a newly admitted Experience without replacement."""

    @abstractmethod
    def get(self, experience_id: ExperienceId) -> Experience:
        """Return one Experience by stable Experience identity."""

    @abstractmethod
    def save(self, experience: Experience) -> None:
        """Persist the current state of an already admitted Experience."""

    @abstractmethod
    def contains(self, experience_id: ExperienceId) -> bool:
        """Return whether this repository knows the Experience identity."""


class InMemoryExperienceRepository(ExperienceRepository):
    """Minimal repository implementation for Core behavioral tests.

    This implementation is intentionally process-local.

    It does NOT demonstrate persistence across real process death.
    """

    def __init__(self) -> None:
        self._experiences: dict[ExperienceId, Experience] = {}

    def add(self, experience: Experience) -> None:
        if experience.experience_id in self._experiences:
            raise ExperienceAlreadyExistsError(
                f"Experience already exists: {experience.experience_id}"
            )

        self._experiences[experience.experience_id] = experience

    def get(self, experience_id: ExperienceId) -> Experience:
        try:
            return self._experiences[experience_id]
        except KeyError as exc:
            raise ExperienceNotFoundError(
                f"Experience not found: {experience_id}"
            ) from exc

    def save(self, experience: Experience) -> None:
        if experience.experience_id not in self._experiences:
            raise ExperienceNotFoundError(
                f"Cannot save unknown Experience: {experience.experience_id}"
            )

        self._experiences[experience.experience_id] = experience

    def contains(self, experience_id: ExperienceId) -> bool:
        return experience_id in self._experiences
```

### `lib/python/experience/service.py`

```python
"""Application physiology for PCC-01 Core Experience."""

from __future__ import annotations

from .identity import ExperienceId
from .model import Experience
from .repository import ExperienceRepository


class ExperienceService:
    """Coordinates Core Experience behavior.

    The service does not own Experience identity.
    The service does not become Session, Memory, Evidence, or authority.
    """

    def __init__(self, repository: ExperienceRepository) -> None:
        self._repository = repository

    def create_experience(self) -> Experience:
        """Create and admit a new Experience."""
        experience = Experience.create()
        self._repository.add(experience)
        return experience

    def get_experience(self, experience_id: ExperienceId) -> Experience:
        """Inspect an admitted Experience by stable identity."""
        return self._repository.get(experience_id)

    def activate_experience(
        self,
        experience_id: ExperienceId,
    ) -> Experience:
        """Activate an admitted Experience while preserving identity."""
        current = self._repository.get(experience_id)
        active = current.activate()
        self._repository.save(active)
        return active

    def close_experience(
        self,
        experience_id: ExperienceId,
    ) -> Experience:
        """Close an active Experience while preserving identity."""
        current = self._repository.get(experience_id)
        closed = current.close()
        self._repository.save(closed)
        return closed
```

### `lib/python/experience/session_binding.py`

```python
"""Explicit Session-to-Experience binding for PCC-01.

This module defines relational tissue only.

It does not define Session itself and does not alter Experience.

Epistemic boundaries:

    Experience != Session
    Experience != Memory
    Experience != Evidence
    Experience != raw dialogue
    Session != process
    Session != provider
    Storage != Experience
    Interpretation != historical fact
    Persistence != authority
    Human Acceptance != Implementation
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import NewType

from .identity import ExperienceId


SessionId = NewType("SessionId", str)


class SessionBindingError(ValueError):
    """Base error for invalid Session/Experience binding operations."""


class InvalidSessionIdError(SessionBindingError):
    """Raised when a Session identity is invalid."""


class InvalidExperienceBindingError(SessionBindingError):
    """Raised when an Experience identity is invalid for binding."""


def normalize_session_id(value: str) -> SessionId:
    """Validate and normalize an external Session identity."""

    if not isinstance(value, str):
        raise InvalidSessionIdError("session_id must be a string")

    normalized = value.strip()

    if not normalized:
        raise InvalidSessionIdError("session_id must not be empty")

    return SessionId(normalized)


def validate_experience_id(value: ExperienceId) -> ExperienceId:
    """Require the established Core Experience identity type.

    Session Binding consumes ExperienceId exactly as defined by the
    Experience organ.  It does not convert Experience identity into
    Session identity or replace it with a parallel representation.
    """

    if not isinstance(value, ExperienceId):
        raise InvalidExperienceBindingError(
            "experience_id must be an ExperienceId"
        )

    return value


@dataclass(frozen=True, slots=True)
class SessionBinding:
    """Relationship between one Session identity and one Experience identity.

    The binding owns neither organ and owns neither lifecycle.
    """

    session_id: SessionId
    experience_id: ExperienceId

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        experience_id: ExperienceId,
    ) -> "SessionBinding":
        return cls(
            session_id=normalize_session_id(session_id),
            experience_id=validate_experience_id(experience_id),
        )

    def belongs_to_experience(self, experience_id: ExperienceId) -> bool:
        """Return whether this binding references the supplied Experience."""

        if not isinstance(experience_id, ExperienceId):
            return False

        return self.experience_id == experience_id

    def belongs_to_session(self, session_id: str) -> bool:
        """Return whether this binding references the supplied Session."""

        try:
            normalized = normalize_session_id(session_id)
        except InvalidSessionIdError:
            return False

        return self.session_id == normalized
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

## 12. Existing Persistence / Recovery / Restart Tests

```text
tests/epistemic/test_memory.py:19:    restored = store.recall(memory.id)
tests/epistemic/test_memory.py:21:    assert restored is not None
tests/epistemic/test_memory.py:23:    assert restored.id == memory.id
tests/epistemic/test_memory.py:25:    assert restored.content == memory.content
tests/epistemic/test_memory.py:27:    assert restored.session == "SESSION-000001"
tests/epistemic/test_memory.py:29:    assert restored.capability == "CAP-0001"
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
tests/experience/test_experience_core.py:56:        "process",
tests/experience/test_experience_protection.py:93:def test_persistence_is_not_implicitly_authorization():
tests/engineering/test_project_export_import.py:66:    data = json.loads(outfile.read_text())
```

## 13. Next Construction Questions

The next implementation must be derived from evidence in this report.

Questions requiring resolution:

1. What persistent substrate should ExperienceRepository use?
2. Does an existing repository/storage organ satisfy the accepted Experience repository contract?
3. What exact serialized fields are required to reconstruct the same Experience?
4. How is ExperienceId restored rather than regenerated?
5. What constitutes recovery rather than creation?
6. How will malformed or corrupt persisted Experience data fail explicitly?
7. How will persistence remain distinct from authority?
8. What executable process-death boundary can be used in Termux tests?
9. How will process A persist an Experience and process B recover it?
10. What evidence proves that process B is genuinely a new OS process?
11. How will the test compare ID_before_restart and ID_after_restart?
12. Which persistence behavior belongs now and which belongs to later Retention/Forgetting?
13. How will Session Binding survive without making Session equal Experience?
14. How will Protection state interact with serialization/recovery?
15. What must remain explicitly outside the next implementation?

## 14. Mandatory Restart Invariant

`ID_before_restart == ID_after_restart`

**Status after RUN 015:** NOT DEMONSTRATED

RUN 015 performs inspection only after Protection conservation.

It does not execute a real process-death/restart continuity proof.

## 15. Epistemic Boundaries

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

## 16. PCC-01 Status

**Implementation Status:** NOT DEMONSTRATED

**Canonical Status:** NOT CANON

**Production Status:** NOT PRODUCTION-READY

## 17. Final Working Tree

```text
?? work/implementation-reports/PCC-01/PCC-01_PROTECTION_CONSERVATION_AND_RESTART_PRE_INSPECTION_RUN_015.md
```

## 18. Conservation State

Protection software + tests + RUN 013 + RUN 014 are conserved at:

`ecf446ed0ad7fe165f54176cad0dad528e006c58`

RUN 015 remains local and untracked for GPT inspection.

No additional software was constructed after the Protection commit.

## 19. Final Result

**RUN 015: PASS**

**Protection:** CONSERVED

**Restart continuity:** NOT DEMONSTRATED

**NEXT REQUIRED ACTION:** GPT inspection of persistence/recovery/restart anatomy before any further software construction.

---

END OF PCC-01 PROTECTION CONSERVATION AND RESTART PRE-INSPECTION — RUN 015
