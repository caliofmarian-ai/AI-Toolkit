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
