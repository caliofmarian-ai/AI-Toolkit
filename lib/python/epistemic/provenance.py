"""
PCC-03 — Provenance + Lineage.

This module implements the first executable anatomy of epistemic provenance.

Canonical direction:

    Source
        ↓
    Observation
        ↓
    Evidence
        ↓
    Claim
        ↓
    Verification

Knowledge and Current State remain later integration boundaries.

Transformation lineage is NOT reimplemented here. Temporal and causal
Transformation genealogy remains owned by the existing PCC-02
Transformation organ.

The implementation preserves explicit epistemic boundaries:

* a Source is not automatically Evidence;
* an Observation is not an Interpretation;
* Evidence does not automatically establish a Claim;
* a Claim is not true merely because it exists;
* Verification must remain explicit;
* absence of knowledge must not be invented;
* human authority evidence and technical evidence are not interchangeable;
* AI statements are not automatically Evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


UNKNOWN = "UNKNOWN"
NOT_VERIFIED = "NOT VERIFIED"


class ProvenanceError(ValueError):
    """Raised when an invalid provenance relationship is requested."""


SourceKind = Literal[
    "HUMAN",
    "AI",
    "CANON",
    "REPOSITORY",
    "EXECUTION",
    "RUNTIME",
    "TEST",
    "EXTERNAL",
    "RESEARCH",
    "HISTORICAL",
    "OTHER",
]

EvidenceRole = Literal[
    "SUPPORTS",
    "CONTRADICTS",
    "NEUTRAL",
]

EvidenceDomain = Literal[
    "AUTHORITY",
    "TECHNICAL",
    "OBSERVATIONAL",
    "DOCUMENTARY",
    "OTHER",
]


def _require_text(field: str, value: str) -> str:
    if not isinstance(value, str):
        raise ProvenanceError(f"{field} must be text")

    value = value.strip()

    if not value:
        raise ProvenanceError(f"{field} must not be empty")

    return value


@dataclass(frozen=True)
class Source:
    """
    Origin from which epistemically relevant information was obtained.

    Source records origin. It does not automatically prove a conclusion.
    """

    identifier: str
    title: str
    kind: SourceKind
    reference: str
    transformation: str | None = None

    @property
    def display_identity(self) -> str:
        return f"{self.identifier} — {self.title}"


@dataclass(frozen=True)
class Observation:
    """
    What was actually observed from a Source.

    Observation remains distinct from interpretation.
    """

    identifier: str
    title: str
    source: str
    observed: str
    interpretation: str = UNKNOWN

    @property
    def display_identity(self) -> str:
        return f"{self.identifier} — {self.title}"


@dataclass(frozen=True)
class Evidence:
    """
    Preserved material capable of supporting or contradicting a Claim.
    """

    identifier: str
    title: str
    observation: str
    reference: str
    domain: EvidenceDomain = "OTHER"

    @property
    def display_identity(self) -> str:
        return f"{self.identifier} — {self.title}"


@dataclass(frozen=True)
class EvidenceRelation:
    """
    Explicit relation between Evidence and a Claim.

    Evidence proximity, filename similarity, timing, or AI inference does not
    establish this relation.
    """

    evidence: str
    claim: str
    role: EvidenceRole


@dataclass(frozen=True)
class Claim:
    """
    Explicit statement about reality.

    A Claim does not become true merely because it exists.
    """

    identifier: str
    title: str
    statement: str
    transformation: str | None = None

    @property
    def display_identity(self) -> str:
        return f"{self.identifier} — {self.title}"


@dataclass(frozen=True)
class Verification:
    """
    Explicit evaluation of a Claim relative to available Evidence.
    """

    identifier: str
    title: str
    claim: str
    state: str
    basis: str = UNKNOWN

    @property
    def display_identity(self) -> str:
        return f"{self.identifier} — {self.title}"


class Provenance:
    """
    In-memory executable provenance anatomy.

    Persistence, bidirectional graph traversal, temporal truth integration,
    Knowledge promotion, and Living Project Image integration are intentionally
    outside Increment 001.

    PCC-02 remains authoritative for Transformation lineage.
    """

    def __init__(self) -> None:
        self._sources: dict[str, Source] = {}
        self._observations: dict[str, Observation] = {}
        self._evidence: dict[str, Evidence] = {}
        self._claims: dict[str, Claim] = {}
        self._verifications: dict[str, Verification] = {}
        self._evidence_relations: list[EvidenceRelation] = []

    @staticmethod
    def _next_identifier(prefix: str, collection: dict[str, object]) -> str:
        return f"{prefix}-{len(collection) + 1:06d}"

    def add_source(
        self,
        title: str,
        *,
        kind: SourceKind,
        reference: str,
        transformation: str | None = None,
    ) -> Source:
        title = _require_text("title", title)
        reference = _require_text("reference", reference)

        identifier = self._next_identifier("SRC", self._sources)

        source = Source(
            identifier=identifier,
            title=title,
            kind=kind,
            reference=reference,
            transformation=transformation,
        )

        self._sources[identifier] = source
        return source

    def observe(
        self,
        source: Source,
        title: str,
        observed: str,
        *,
        interpretation: str = UNKNOWN,
    ) -> Observation:
        self._require_registered_source(source)

        title = _require_text("title", title)
        observed = _require_text("observed", observed)

        if interpretation != UNKNOWN:
            interpretation = _require_text(
                "interpretation",
                interpretation,
            )

        identifier = self._next_identifier(
            "OBS",
            self._observations,
        )

        observation = Observation(
            identifier=identifier,
            title=title,
            source=source.identifier,
            observed=observed,
            interpretation=interpretation,
        )

        self._observations[identifier] = observation
        return observation

    def preserve_evidence(
        self,
        observation: Observation,
        title: str,
        reference: str,
        *,
        domain: EvidenceDomain = "OTHER",
    ) -> Evidence:
        self._require_registered_observation(observation)

        title = _require_text("title", title)
        reference = _require_text("reference", reference)

        identifier = self._next_identifier(
            "EV",
            self._evidence,
        )

        evidence = Evidence(
            identifier=identifier,
            title=title,
            observation=observation.identifier,
            reference=reference,
            domain=domain,
        )

        self._evidence[identifier] = evidence
        return evidence

    def make_claim(
        self,
        title: str,
        statement: str,
        *,
        transformation: str | None = None,
    ) -> Claim:
        title = _require_text("title", title)
        statement = _require_text("statement", statement)

        identifier = self._next_identifier(
            "CLM",
            self._claims,
        )

        claim = Claim(
            identifier=identifier,
            title=title,
            statement=statement,
            transformation=transformation,
        )

        self._claims[identifier] = claim
        return claim

    def relate_evidence(
        self,
        evidence: Evidence,
        claim: Claim,
        role: EvidenceRole,
    ) -> EvidenceRelation:
        self._require_registered_evidence(evidence)
        self._require_registered_claim(claim)

        relation = EvidenceRelation(
            evidence=evidence.identifier,
            claim=claim.identifier,
            role=role,
        )

        if relation not in self._evidence_relations:
            self._evidence_relations.append(relation)

        return relation

    def verify(
        self,
        claim: Claim,
        title: str,
        *,
        state: str = NOT_VERIFIED,
        basis: str = UNKNOWN,
    ) -> Verification:
        self._require_registered_claim(claim)

        title = _require_text("title", title)
        state = _require_text("state", state)

        if basis != UNKNOWN:
            basis = _require_text("basis", basis)

        identifier = self._next_identifier(
            "VER",
            self._verifications,
        )

        verification = Verification(
            identifier=identifier,
            title=title,
            claim=claim.identifier,
            state=state,
            basis=basis,
        )

        self._verifications[identifier] = verification
        return verification

    def supporting_evidence(
        self,
        claim: Claim,
    ) -> tuple[Evidence, ...]:
        self._require_registered_claim(claim)

        return tuple(
            self._evidence[relation.evidence]
            for relation in self._evidence_relations
            if relation.claim == claim.identifier
            and relation.role == "SUPPORTS"
        )

    def contradicting_evidence(
        self,
        claim: Claim,
    ) -> tuple[Evidence, ...]:
        self._require_registered_claim(claim)

        return tuple(
            self._evidence[relation.evidence]
            for relation in self._evidence_relations
            if relation.claim == claim.identifier
            and relation.role == "CONTRADICTS"
        )

    def _require_registered_source(self, source: Source) -> None:
        if self._sources.get(source.identifier) != source:
            raise ProvenanceError(
                f"Unknown Source: {source.identifier}"
            )

    def _require_registered_observation(
        self,
        observation: Observation,
    ) -> None:
        if self._observations.get(observation.identifier) != observation:
            raise ProvenanceError(
                f"Unknown Observation: {observation.identifier}"
            )

    def _require_registered_evidence(
        self,
        evidence: Evidence,
    ) -> None:
        if self._evidence.get(evidence.identifier) != evidence:
            raise ProvenanceError(
                f"Unknown Evidence: {evidence.identifier}"
            )

    def _require_registered_claim(self, claim: Claim) -> None:
        if self._claims.get(claim.identifier) != claim:
            raise ProvenanceError(
                f"Unknown Claim: {claim.identifier}"
            )
