# PCC-01 — SESSION BINDING CORRECTION REPORT — RUN 011

**Purpose:** Correct RUN 010 ExperienceId compatibility without modifying conserved Core Experience tissue.

**Expected baseline:** `5c82eb85b42e0cc686cd95e8b2ee053c36a62b82`

**Prior result:** RUN 010 failed because SessionBinding treated ExperienceId as str.

**Git conservation:** NOT PERFORMED

---

## 1. Baseline

```text
Expected:    5c82eb85b42e0cc686cd95e8b2ee053c36a62b82
LOCAL:       5c82eb85b42e0cc686cd95e8b2ee053c36a62b82
origin/main: 5c82eb85b42e0cc686cd95e8b2ee053c36a62b82
PASS: baseline unchanged
```

## 2. Authoritative Experience Identity Inspection

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
ExperienceId class: <class 'lib.python.experience.identity.ExperienceId'>
Runtime identity type: <class 'lib.python.experience.identity.ExperienceId'>
Runtime identity repr: ExperienceId(value='5c68c15f-1fbc-460a-b6e4-346e64ef3486')
PASS: Experience.create() returns ExperienceId
PASS: RUN 010 assumption reproduced
ExperienceId is not str
Therefore isinstance(experience_id, str) was incompatible with Core Experience identity anatomy

## 3. Corrected Session Binding Dedicated Tests

```text
....................                                                     [100%]
20 passed in 0.49s
PASS: corrected Session Binding suite
```

## 4. Complete Core Experience Regression

```text
......................................................                   [100%]
54 passed in 0.66s
PASS: complete Core Experience suite
```

## 5. Conservation Boundary

```text
PASS: conserved Core Experience tissue unchanged
PASS: only new Session Binding tissue is under construction
```

## 6. Corrected Anatomy

```text
Session identity -> SessionId
Experience identity -> existing ExperienceId
Relationship -> SessionBinding

SessionBinding does not redefine ExperienceId.
SessionBinding does not convert ExperienceId to str.
SessionBinding does not make Experience equal Session.
```

## 7. Implemented Source

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

## 8. Test Source

```python
import pytest

from lib.python.experience import Experience
from lib.python.experience.identity import ExperienceId
from lib.python.experience.session_binding import (
    InvalidExperienceBindingError,
    InvalidSessionIdError,
    SessionBinding,
    normalize_session_id,
    validate_experience_id,
)


def test_experience_create_returns_established_experience_identity():
    experience = Experience.create()

    assert isinstance(experience.experience_id, ExperienceId)


def test_session_binding_connects_distinct_identities():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert binding.session_id == "session-alpha"
    assert binding.experience_id == experience.experience_id


def test_session_identity_is_not_experience_identity():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert binding.session_id != binding.experience_id
    assert isinstance(binding.experience_id, ExperienceId)


def test_binding_does_not_replace_experience():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert isinstance(experience, Experience)
    assert not isinstance(binding, Experience)


def test_binding_preserves_exact_experience_identity():
    experience = Experience.create()
    original_identity = experience.experience_id

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=original_identity,
    )

    assert binding.experience_id is original_identity
    assert experience.experience_id is original_identity


def test_session_id_is_normalized():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="  session-alpha  ",
        experience_id=experience.experience_id,
    )

    assert binding.session_id == "session-alpha"


@pytest.mark.parametrize("session_id", ["", " ", "\n", "\t"])
def test_empty_session_identity_is_rejected(session_id):
    experience = Experience.create()

    with pytest.raises(InvalidSessionIdError):
        SessionBinding.create(
            session_id=session_id,
            experience_id=experience.experience_id,
        )


def test_non_string_session_identity_is_rejected():
    with pytest.raises(InvalidSessionIdError):
        normalize_session_id(123)  # type: ignore[arg-type]


def test_raw_string_cannot_replace_experience_identity():
    with pytest.raises(InvalidExperienceBindingError):
        SessionBinding.create(
            session_id="session-alpha",
            experience_id="not-an-experience-id",  # type: ignore[arg-type]
        )


def test_none_cannot_replace_experience_identity():
    with pytest.raises(InvalidExperienceBindingError):
        SessionBinding.create(
            session_id="session-alpha",
            experience_id=None,  # type: ignore[arg-type]
        )


def test_validate_experience_id_preserves_identity_object():
    experience = Experience.create()

    validated = validate_experience_id(experience.experience_id)

    assert validated is experience.experience_id


def test_binding_can_confirm_experience_membership():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert binding.belongs_to_experience(experience.experience_id)


def test_binding_rejects_other_experience_membership():
    first = Experience.create()
    second = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=first.experience_id,
    )

    assert not binding.belongs_to_experience(second.experience_id)


def test_binding_rejects_raw_string_experience_membership():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert not binding.belongs_to_experience(
        experience.experience_id.value  # type: ignore[arg-type]
    )


def test_binding_can_confirm_session_membership():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert binding.belongs_to_session("session-alpha")
    assert binding.belongs_to_session(" session-alpha ")


def test_binding_rejects_other_session_membership():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert not binding.belongs_to_session("session-beta")


def test_binding_rejects_invalid_session_membership_query():
    experience = Experience.create()

    binding = SessionBinding.create(
        session_id="session-alpha",
        experience_id=experience.experience_id,
    )

    assert not binding.belongs_to_session("")
```

## 9. Integrity

```text
a7872978d32c5fbe7b2ecd9c60bf2fe1e6390c3bf1babf40d85a7775f50ceb18  lib/python/experience/session_binding.py
48f6d35bbf3bcad8fc7c1c98658085faab9bb0b0fc0582d70047791f8bba7907  tests/experience/test_experience_session_binding.py
```

## 10. Final Git State

```text
?? lib/python/experience/session_binding.py
?? tests/experience/test_experience_session_binding.py
?? work/implementation-reports/PCC-01/PCC-01_SESSION_BINDING_CORRECTION_REPORT_RUN_011.md
?? work/implementation-reports/PCC-01/PCC-01_SESSION_BINDING_IMPLEMENTATION_REPORT_RUN_010.md
```

## 11. Epistemic Boundaries

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

## 12. Restart Invariant

**ID_before_restart == ID_after_restart**

RUN 011 does NOT demonstrate this invariant.

No process death or restart was performed.

## 13. PCC-01 Status

**Implementation Status:** NOT DEMONSTRATED

**Canonical Status:** NOT CANON

**Production Status:** NOT PRODUCTION-READY

## 14. Conservation

No `git add` performed.

No commit performed.

No push performed.

## 15. Final Result

**RUN 011: PASS**

**RUN 010 root cause:** CORRECTED

**Session Binding:** BUILT LOCALLY AND TESTED

**NEXT REQUIRED ACTION:** GPT inspection before conservation.

---

END OF PCC-01 SESSION BINDING CORRECTION REPORT — RUN 011
