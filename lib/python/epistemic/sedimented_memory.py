"""Canonical semantic Memory physiology for PCC-04.

This module does not preserve raw Experience.

Persistent Experience remains responsible for lived project experience.

Sedimented Memory preserves meaning that has passed through the
Sedimentation physiology and is explicitly accepted for downstream
retention.

Memory remains distinct from Knowledge.  The same accepted
Sedimentation may target Memory, Knowledge, or both, but connection
does not imply identity.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable
from uuid import uuid4

from .sedimentation import (
    GovernedSedimentation,
    SedimentationAuthority,
    SedimentationTarget,
)


class SedimentedMemoryError(RuntimeError):
    """Base failure for canonical Sedimented Memory physiology."""


class MemoryIdentityError(SedimentedMemoryError):
    """Raised when semantic Memory identity is invalid."""


class MemoryPromotionError(SedimentedMemoryError):
    """Raised when Sedimentation is not permitted to become Memory."""


class DownstreamKnowledgeError(SedimentedMemoryError):
    """Raised when Knowledge delivery is requested without a receptor."""


@dataclass(frozen=True)
class SedimentedMemoryId:
    """Stable identity of one semantic Memory."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not self.value.strip():
            raise MemoryIdentityError(
                "Sedimented Memory identity must be a non-empty string."
            )

    @classmethod
    def create(cls) -> "SedimentedMemoryId":
        return cls(f"MEM-{uuid4().hex}")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class SedimentedMemory:
    """Meaning retained from one accepted Sedimentation.

    This is not the original Experience and does not claim to be it.
    """

    memory_id: SedimentedMemoryId
    sedimentation_identifier: str
    meaning: str
    provenance_identifier: str
    uncertainty: str | None = None

    def __post_init__(self) -> None:
        for field_name in (
            "sedimentation_identifier",
            "meaning",
            "provenance_identifier",
        ):
            value = getattr(self, field_name)

            if not isinstance(value, str) or not value.strip():
                raise MemoryIdentityError(
                    f"{field_name} must be a non-empty string."
                )

        if self.uncertainty is not None:
            if (
                not isinstance(self.uncertainty, str)
                or not self.uncertainty.strip()
            ):
                raise MemoryIdentityError(
                    "uncertainty must be None or a non-empty string."
                )


class SedimentationDelivery(Enum):
    """What downstream physiology actually occurred."""

    MEMORY = "MEMORY"
    KNOWLEDGE = "KNOWLEDGE"
    MEMORY_AND_KNOWLEDGE = "MEMORY_AND_KNOWLEDGE"


@dataclass(frozen=True)
class SedimentationDeliveryResult:
    """Explicit result of downstream Sedimentation physiology."""

    sedimentation_identifier: str
    delivery: SedimentationDelivery
    memory: SedimentedMemory | None
    knowledge: object | None

    def __post_init__(self) -> None:
        if (
            not isinstance(self.sedimentation_identifier, str)
            or not self.sedimentation_identifier.strip()
        ):
            raise MemoryIdentityError(
                "sedimentation_identifier must be non-empty."
            )

        if self.delivery is SedimentationDelivery.MEMORY:
            if self.memory is None or self.knowledge is not None:
                raise MemoryPromotionError(
                    "MEMORY delivery must contain only Memory."
                )

        elif self.delivery is SedimentationDelivery.KNOWLEDGE:
            if self.memory is not None or self.knowledge is None:
                raise MemoryPromotionError(
                    "KNOWLEDGE delivery must contain only Knowledge."
                )

        elif self.delivery is SedimentationDelivery.MEMORY_AND_KNOWLEDGE:
            if self.memory is None or self.knowledge is None:
                raise MemoryPromotionError(
                    "MEMORY_AND_KNOWLEDGE delivery requires both."
                )


KnowledgeReceptor = Callable[[GovernedSedimentation], object]


class SedimentedMemoryPhysiology:
    """Controlled delivery from accepted Sedimentation.

    The physiology owns neither Persistent Experience nor Knowledge.

    A Knowledge receptor is injected explicitly so PCC-04 cannot create
    a competing Knowledge organ.
    """

    def __init__(
        self,
        knowledge_receptor: KnowledgeReceptor | None = None,
    ) -> None:
        self._knowledge_receptor = knowledge_receptor

    @staticmethod
    def _sedimentation_identifier(
        governed: GovernedSedimentation,
    ) -> str:
        sedimentation = governed.sedimentation

        for attribute in (
            "sedimentation_id",
            "identifier",
            "id",
        ):
            if hasattr(sedimentation, attribute):
                value = getattr(sedimentation, attribute)

                if value is not None:
                    rendered = str(value)

                    if rendered.strip():
                        return rendered

        raise MemoryPromotionError(
            "Accepted Sedimentation has no stable identity."
        )

    @staticmethod
    def _meaning(
        governed: GovernedSedimentation,
    ) -> str:
        sedimentation = governed.sedimentation

        for attribute in (
            "meaning",
            "learning",
            "content",
            "summary",
        ):
            if not hasattr(sedimentation, attribute):
                continue

            value = getattr(sedimentation, attribute)

            if hasattr(value, "meaning"):
                value = getattr(value, "meaning")

            if value is not None:
                rendered = str(value)

                if rendered.strip():
                    return rendered

        raise MemoryPromotionError(
            "Sedimentation exposes no semantic meaning for Memory."
        )

    @staticmethod
    def _provenance_identifier(
        governed: GovernedSedimentation,
    ) -> str:
        value = getattr(
            governed.sedimentation,
            "provenance_identifier",
            None,
        )

        if value is None or not str(value).strip():
            raise MemoryPromotionError(
                "Sedimentation must preserve provenance before Memory."
            )

        return str(value)

    @staticmethod
    def _uncertainty(
        governed: GovernedSedimentation,
    ) -> str | None:
        value = getattr(
            governed.sedimentation,
            "uncertainty",
            None,
        )

        if value is None:
            return None

        rendered = str(value)

        return rendered if rendered.strip() else None

    @staticmethod
    def _require_accepted(
        governed: GovernedSedimentation,
    ) -> None:
        authority = governed.authority

        if authority is not SedimentationAuthority.ACCEPTED:
            raise MemoryPromotionError(
                "Only explicitly accepted Sedimentation may be delivered "
                "into Memory or Knowledge."
            )

    def _to_memory(
        self,
        governed: GovernedSedimentation,
    ) -> SedimentedMemory:
        return SedimentedMemory(
            memory_id=SedimentedMemoryId.create(),
            sedimentation_identifier=self._sedimentation_identifier(
                governed
            ),
            meaning=self._meaning(governed),
            provenance_identifier=self._provenance_identifier(
                governed
            ),
            uncertainty=self._uncertainty(governed),
        )

    def _to_knowledge(
        self,
        governed: GovernedSedimentation,
    ) -> object:
        if self._knowledge_receptor is None:
            raise DownstreamKnowledgeError(
                "Knowledge delivery requires the existing Knowledge "
                "physiology to be supplied explicitly."
            )

        return self._knowledge_receptor(governed)

    def deliver(
        self,
        governed: GovernedSedimentation,
    ) -> SedimentationDeliveryResult:
        self._require_accepted(governed)

        target = governed.sedimentation.target

        identifier = self._sedimentation_identifier(
            governed
        )

        if target is SedimentationTarget.MEMORY:
            memory = self._to_memory(governed)

            return SedimentationDeliveryResult(
                sedimentation_identifier=identifier,
                delivery=SedimentationDelivery.MEMORY,
                memory=memory,
                knowledge=None,
            )

        if target is SedimentationTarget.KNOWLEDGE:
            knowledge = self._to_knowledge(governed)

            return SedimentationDeliveryResult(
                sedimentation_identifier=identifier,
                delivery=SedimentationDelivery.KNOWLEDGE,
                memory=None,
                knowledge=knowledge,
            )

        if target is SedimentationTarget.MEMORY_AND_KNOWLEDGE:
            memory = self._to_memory(governed)
            knowledge = self._to_knowledge(governed)

            return SedimentationDeliveryResult(
                sedimentation_identifier=identifier,
                delivery=SedimentationDelivery.MEMORY_AND_KNOWLEDGE,
                memory=memory,
                knowledge=knowledge,
            )

        raise MemoryPromotionError(
            f"Unsupported Sedimentation target: {target!r}"
        )
