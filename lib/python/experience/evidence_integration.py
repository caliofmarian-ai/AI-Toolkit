"""PCC-01 Experience integration with the inherited Evidence Engine.

This module is connective tissue.

It does not create another Evidence Engine.
It does not redefine Experience.
It does not redefine ExperienceId.
It does not make Evidence become Experience.

The relationship is referential:

    Experience identity -> Evidence query -> Evidence result

Evidence may inform an Experience while remaining evidence.
Experience may refer to evidence while remaining Experience.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from lib.python.evidence_engine.engine import EvidenceEngine

from .identity import ExperienceId


class ExperienceEvidenceIntegrationError(Exception):
    """Base error for PCC-01 Evidence integration."""


class InvalidEvidenceKeywordError(ExperienceEvidenceIntegrationError):
    """Raised when an Evidence query keyword is invalid."""


@dataclass(frozen=True, slots=True)
class ExperienceEvidenceReference:
    """Evidence discovered for one conserved Experience identity."""

    experience_id: ExperienceId
    keyword: str
    evidence: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.experience_id, ExperienceId):
            raise TypeError("experience_id must be an ExperienceId")

        if not isinstance(self.keyword, str) or not self.keyword.strip():
            raise InvalidEvidenceKeywordError(
                "evidence keyword must be a non-empty string"
            )

        if not isinstance(self.evidence, Mapping):
            raise TypeError("evidence must be a mapping")

    @property
    def has_evidence(self) -> bool:
        """Return whether the inherited Evidence Engine found evidence."""

        for key, value in self.evidence.items():
            if key == "semantic":
                if isinstance(value, Mapping) and value:
                    return True
                continue

            if isinstance(value, (list, tuple, set)) and value:
                return True

            if isinstance(value, Mapping) and value:
                return True

        return False


class ExperienceEvidenceIntegrator:
    """Bridge Experience identity to the inherited Evidence Engine."""

    def __init__(self, evidence_engine: EvidenceEngine) -> None:
        if not isinstance(evidence_engine, EvidenceEngine):
            raise TypeError(
                "evidence_engine must be the inherited EvidenceEngine"
            )

        self._evidence_engine = evidence_engine

    def find_for_experience(
        self,
        *,
        experience_id: ExperienceId,
        keyword: str,
    ) -> ExperienceEvidenceReference:
        """Find evidence without changing Experience identity."""

        if not isinstance(experience_id, ExperienceId):
            raise TypeError("experience_id must be an ExperienceId")

        if not isinstance(keyword, str) or not keyword.strip():
            raise InvalidEvidenceKeywordError(
                "evidence keyword must be a non-empty string"
            )

        evidence = self._evidence_engine.find(keyword.strip())

        return ExperienceEvidenceReference(
            experience_id=experience_id,
            keyword=keyword.strip(),
            evidence=evidence,
        )
