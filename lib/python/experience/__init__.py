"""PCC-01 Core Experience domain organ.

This package establishes the first executable Core Experience tissue.

It does not make PCC-01 canonical, production-ready, or fully demonstrated.
"""

from .identity import ExperienceId, ExperienceIdentityError
from .lifecycle import ExperienceLifecycleError, ExperienceState
from .model import Experience
from .repository import (
    ExperienceAlreadyExistsError,
    ExperienceNotFoundError,
    ExperienceRepository,
    ExperienceRepositoryError,
    InMemoryExperienceRepository,
)
from .service import ExperienceService

__all__ = [
    "Experience",
    "ExperienceId",
    "ExperienceIdentityError",
    "ExperienceLifecycleError",
    "ExperienceState",
    "ExperienceRepository",
    "ExperienceRepositoryError",
    "ExperienceNotFoundError",
    "ExperienceAlreadyExistsError",
    "InMemoryExperienceRepository",
    "ExperienceService",
]

from .protection import (
    ExperienceProtection,
    ExperienceProtectionError,
    InvalidProtectionIdentityError,
    ProtectedExperienceMutationError,
    ProtectionState,
    UnauthorizedExperienceOperationError,
)

from .persistence import (
    ExperiencePersistenceError,
    ExperienceRecoveryError,
    ExperienceSerializationError,
    recover_experience,
    serialize_experience,
)

from .persistent_repository import (
    ExperienceStoreCorruptionError,
    JsonFileExperienceRepository,
    PersistentExperienceRepositoryError,
)
