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
from pathlib import Path
from typing import Literal
import json


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



# ---------------------------------------------------------------------------
# PCC-03 — Verified Knowledge
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Knowledge:
    """
    A governed epistemic understanding promoted from an explicit Verification.

    Knowledge is not raw Evidence and is not merely a Verification result.
    It is an explicit epistemic promotion whose provenance remains navigable
    back through the Verification and the already-preserved provenance chain.

    This value does not represent Memory, Current State, or Living Project
    Image and does not replace any existing Knowledge Engine.
    """

    identifier: str
    title: str
    statement: str
    verification_identifier: str
    authority: str
    status: str = "ESTABLISHED"


class KnowledgePromotionError(ProvenanceError):
    """Raised when a Verification cannot responsibly become Knowledge."""


def _knowledge_identifier(number: int) -> str:
    return f"KN-{number:06d}"


def _require_knowledge_text(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise KnowledgePromotionError(
            f"{name} must contain explicit epistemic information"
        )
    return value.strip()


def promote_verified_knowledge(
    verification: Verification,
    *,
    identifier: str,
    title: str,
    statement: str,
    authority: str,
) -> Knowledge:
    """
    Explicitly promote a Verification into Knowledge.

    Promotion is never inferred merely because Evidence or Verification exists.
    The caller must supply the semantic statement and responsible authority.

    Existing provenance remains authoritative for the history leading to the
    Verification.  This function does not copy Source, Observation, Evidence,
    Claim, or Verification content into another persistence authority.
    """

    if not isinstance(verification, Verification):
        raise KnowledgePromotionError(
            "Knowledge promotion requires an explicit Verification"
        )

    identifier = _require_knowledge_text("identifier", identifier)

    if not identifier.startswith("KN-"):
        raise KnowledgePromotionError(
            "Knowledge identifier must use the KN-* identity family"
        )

    title = _require_knowledge_text("title", title)
    statement = _require_knowledge_text("statement", statement)
    authority = _require_knowledge_text("authority", authority)

    verification_identifier = getattr(
        verification,
        "identifier",
        None,
    )

    if not verification_identifier:
        raise KnowledgePromotionError(
            "Verification must have a stable epistemic identity"
        )

    return Knowledge(
        identifier=identifier,
        title=title,
        statement=statement,
        verification_identifier=verification_identifier,
        authority=authority,
    )

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
        self._knowledge: dict[str, Knowledge] = {}
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

    def promote_knowledge(
        self,
        verification: Verification,
        title: str,
        statement: str,
        *,
        authority: str,
    ) -> Knowledge:
        """
        Explicitly promote a registered Verification into persistent Knowledge.

        Promotion remains governed and non-automatic. The existing RUN 004
        promotion boundary validates epistemic content; this method gives the
        resulting Knowledge a stable identity inside this Provenance organ.
        """
        self._require_registered_verification(verification)

        identifier = self._next_identifier(
            "KN",
            self._knowledge,
        )

        knowledge = promote_verified_knowledge(
            verification,
            identifier=identifier,
            title=title,
            statement=statement,
            authority=authority,
        )

        self._knowledge[identifier] = knowledge
        return knowledge

    def knowledge_for_verification(
        self,
        verification: Verification,
    ) -> tuple[Knowledge, ...]:
        """Navigate forward from Verification to explicit Knowledge."""
        self._require_registered_verification(verification)

        return tuple(
            knowledge
            for knowledge in self._knowledge.values()
            if (
                knowledge.verification_identifier
                == verification.identifier
            )
        )

    def verification_for_knowledge(
        self,
        knowledge: Knowledge,
    ) -> Verification:
        """Navigate backward from Knowledge to its explicit Verification."""
        self._require_registered_knowledge(knowledge)

        return self._verifications[
            knowledge.verification_identifier
        ]

    def provenance_to_source_from_knowledge(
        self,
        knowledge: Knowledge,
    ) -> tuple[
        Knowledge,
        Verification,
        Claim,
        tuple[Evidence, ...],
        tuple[Observation, ...],
        tuple[Source, ...],
    ]:
        """
        Explain established Knowledge backward to explicit origin.

        No relation is inferred. The Knowledge points to its Verification and
        the inherited PCC-03 provenance anatomy supplies the remaining path.
        """
        verification = self.verification_for_knowledge(knowledge)

        (
            verification,
            claim,
            evidence,
            observations,
            sources,
        ) = self.provenance_to_source(verification)

        return (
            knowledge,
            verification,
            claim,
            evidence,
            observations,
            sources,
        )

    def source_for_observation(
        self,
        observation: Observation,
    ) -> Source:
        """Navigate backward from Observation to its explicit Source."""
        self._require_registered_observation(observation)
        return self._sources[observation.source]

    def observations_from_source(
        self,
        source: Source,
    ) -> tuple[Observation, ...]:
        """Navigate forward from Source to explicit Observations."""
        self._require_registered_source(source)

        return tuple(
            observation
            for observation in self._observations.values()
            if observation.source == source.identifier
        )

    def observation_for_evidence(
        self,
        evidence: Evidence,
    ) -> Observation:
        """Navigate backward from Evidence to its explicit Observation."""
        self._require_registered_evidence(evidence)
        return self._observations[evidence.observation]

    def evidence_from_observation(
        self,
        observation: Observation,
    ) -> tuple[Evidence, ...]:
        """Navigate forward from Observation to preserved Evidence."""
        self._require_registered_observation(observation)

        return tuple(
            evidence
            for evidence in self._evidence.values()
            if evidence.observation == observation.identifier
        )

    def claims_for_evidence(
        self,
        evidence: Evidence,
        *,
        role: EvidenceRole | None = None,
    ) -> tuple[Claim, ...]:
        """
        Navigate forward from Evidence to explicitly related Claims.

        No relation is inferred from naming, proximity, source, or timing.
        """
        self._require_registered_evidence(evidence)

        if role is not None and role not in (
            "SUPPORTS",
            "CONTRADICTS",
            "NEUTRAL",
        ):
            raise ProvenanceError(
                f"Unknown Evidence role: {role}"
            )

        return tuple(
            self._claims[relation.claim]
            for relation in self._evidence_relations
            if relation.evidence == evidence.identifier
            and (role is None or relation.role == role)
        )

    def evidence_for_claim(
        self,
        claim: Claim,
        *,
        role: EvidenceRole | None = None,
    ) -> tuple[Evidence, ...]:
        """
        Navigate backward from Claim to explicitly related Evidence.

        Supporting, contradicting, and neutral Evidence remain distinguishable.
        """
        self._require_registered_claim(claim)

        if role is not None and role not in (
            "SUPPORTS",
            "CONTRADICTS",
            "NEUTRAL",
        ):
            raise ProvenanceError(
                f"Unknown Evidence role: {role}"
            )

        return tuple(
            self._evidence[relation.evidence]
            for relation in self._evidence_relations
            if relation.claim == claim.identifier
            and (role is None or relation.role == role)
        )

    def verifications_for_claim(
        self,
        claim: Claim,
    ) -> tuple[Verification, ...]:
        """Navigate forward from Claim to its explicit Verifications."""
        self._require_registered_claim(claim)

        return tuple(
            verification
            for verification in self._verifications.values()
            if verification.claim == claim.identifier
        )

    def claim_for_verification(
        self,
        verification: Verification,
    ) -> Claim:
        """Navigate backward from Verification to its explicit Claim."""
        self._require_registered_verification(verification)
        return self._claims[verification.claim]

    def provenance_to_source(
        self,
        verification: Verification,
    ) -> tuple[
        Verification,
        Claim,
        tuple[Evidence, ...],
        tuple[Observation, ...],
        tuple[Source, ...],
    ]:
        """
        Traverse established PCC-03 anatomy backward toward origin.

        Only explicit persisted relations are followed.
        Knowledge and Current State remain outside this increment.
        """
        claim = self.claim_for_verification(verification)
        evidence = self.evidence_for_claim(claim)

        observations = tuple(
            self.observation_for_evidence(item)
            for item in evidence
        )

        sources: list[Source] = []

        for observation in observations:
            source = self.source_for_observation(observation)
            if source not in sources:
                sources.append(source)

        return (
            verification,
            claim,
            evidence,
            observations,
            tuple(sources),
        )

    def provenance_from_source(
        self,
        source: Source,
    ) -> tuple[
        Source,
        tuple[Observation, ...],
        tuple[Evidence, ...],
        tuple[Claim, ...],
        tuple[Verification, ...],
    ]:
        """
        Traverse established PCC-03 anatomy forward from origin.

        This public traversal preserves the RUN 003 contract and stops at
        Verification. Knowledge uses a distinct RUN 005 traversal so inherited
        callers are not silently changed.
        """
        self._require_registered_source(source)

        observations = self.observations_from_source(source)

        evidence: list[Evidence] = []
        for observation in observations:
            for item in self.evidence_from_observation(observation):
                if item not in evidence:
                    evidence.append(item)

        claims: list[Claim] = []
        for item in evidence:
            for claim in self.claims_for_evidence(item):
                if claim not in claims:
                    claims.append(claim)

        verifications: list[Verification] = []
        for claim in claims:
            for verification in self.verifications_for_claim(claim):
                if verification not in verifications:
                    verifications.append(verification)

        return (
            source,
            observations,
            tuple(evidence),
            tuple(claims),
            tuple(verifications),
        )

    def provenance_from_source_to_knowledge(
        self,
        source: Source,
    ) -> tuple[
        Source,
        tuple[Observation, ...],
        tuple[Evidence, ...],
        tuple[Claim, ...],
        tuple[Verification, ...],
        tuple[Knowledge, ...],
    ]:
        """
        Traverse explicit PCC-03 provenance from Source through Knowledge.

        This is a RUN 005 extension. The inherited provenance_from_source()
        contract remains unchanged.
        """
        (
            source,
            observations,
            evidence,
            claims,
            verifications,
        ) = self.provenance_from_source(source)

        knowledge: list[Knowledge] = []

        for verification in verifications:
            for item in self.knowledge_for_verification(verification):
                if item not in knowledge:
                    knowledge.append(item)

        return (
            source,
            observations,
            evidence,
            claims,
            verifications,
            tuple(knowledge),
        )

    def supporting_evidence(
        self,
        claim: Claim,
    ) -> tuple[Evidence, ...]:
        self._require_registered_claim(claim)

        return self.evidence_for_claim(
            claim,
            role="SUPPORTS",
        )

    def contradicting_evidence(
        self,
        claim: Claim,
    ) -> tuple[Evidence, ...]:
        self._require_registered_claim(claim)

        return self.evidence_for_claim(
            claim,
            role="CONTRADICTS",
        )

    def save(self, root: Path) -> Path:
        """
        Persist this Provenance anatomy as one human-inspectable Markdown
        manifestation.

        Markdown is the persisted authority for this increment. The embedded
        JSON block is serialization inside that same manifestation and is not
        a second persistence authority.
        """

        root = Path(root)
        root.mkdir(parents=True, exist_ok=True)

        path = root / "PROVENANCE.md"

        payload = {
            "sources": [
                {
                    "identifier": item.identifier,
                    "title": item.title,
                    "kind": item.kind,
                    "reference": item.reference,
                    "transformation": item.transformation,
                }
                for item in self._sources.values()
            ],
            "observations": [
                {
                    "identifier": item.identifier,
                    "title": item.title,
                    "source": item.source,
                    "observed": item.observed,
                    "interpretation": item.interpretation,
                }
                for item in self._observations.values()
            ],
            "evidence": [
                {
                    "identifier": item.identifier,
                    "title": item.title,
                    "observation": item.observation,
                    "reference": item.reference,
                    "domain": item.domain,
                }
                for item in self._evidence.values()
            ],
            "claims": [
                {
                    "identifier": item.identifier,
                    "title": item.title,
                    "statement": item.statement,
                    "transformation": item.transformation,
                }
                for item in self._claims.values()
            ],
            "verifications": [
                {
                    "identifier": item.identifier,
                    "title": item.title,
                    "claim": item.claim,
                    "state": item.state,
                    "basis": item.basis,
                }
                for item in self._verifications.values()
            ],
            "knowledge": [
                {
                    "identifier": item.identifier,
                    "title": item.title,
                    "statement": item.statement,
                    "verification_identifier": (
                        item.verification_identifier
                    ),
                    "authority": item.authority,
                    "status": item.status,
                }
                for item in self._knowledge.values()
            ],
            "evidence_relations": [
                {
                    "evidence": item.evidence,
                    "claim": item.claim,
                    "role": item.role,
                }
                for item in self._evidence_relations
            ],
        }

        lines = [
            "# Epistemic Provenance",
            "",
            "Status: PERSISTED",
            "",
            "## Human-Readable Inventory",
            "",
            "### Sources",
            "",
        ]

        if self._sources:
            lines.extend(
                f"- {item.display_identity}"
                for item in self._sources.values()
            )
        else:
            lines.append("NONE")

        lines.extend(["", "### Observations", ""])

        if self._observations:
            lines.extend(
                f"- {item.display_identity}"
                for item in self._observations.values()
            )
        else:
            lines.append("NONE")

        lines.extend(["", "### Evidence", ""])

        if self._evidence:
            lines.extend(
                f"- {item.display_identity}"
                for item in self._evidence.values()
            )
        else:
            lines.append("NONE")

        lines.extend(["", "### Claims", ""])

        if self._claims:
            lines.extend(
                f"- {item.display_identity}"
                for item in self._claims.values()
            )
        else:
            lines.append("NONE")

        lines.extend(["", "### Verifications", ""])

        if self._verifications:
            lines.extend(
                f"- {item.display_identity}"
                for item in self._verifications.values()
            )
        else:
            lines.append("NONE")

        lines.extend(["", "### Knowledge", ""])

        if self._knowledge:
            lines.extend(
                f"- {item.identifier} — {item.title}"
                for item in self._knowledge.values()
            )
        else:
            lines.append("NONE")

        lines.extend(
            [
                "",
                "## Machine-Recoverable Representation",
                "",
                "```json",
                json.dumps(
                    payload,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                ),
                "```",
                "",
            ]
        )

        path.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        return path

    @classmethod
    def load(cls, root: Path) -> "Provenance":
        """
        Recover persisted Provenance without inventing missing information.

        Malformed, incomplete, duplicate, or dangling persisted relations are
        surfaced explicitly as ProvenanceError.
        """

        path = Path(root) / "PROVENANCE.md"

        if not path.is_file():
            raise ProvenanceError(
                f"Persisted Provenance does not exist: {path}"
            )

        text = path.read_text(encoding="utf-8")

        opening = "```json\n"
        closing = "\n```"

        if opening not in text:
            raise ProvenanceError(
                "Persisted Provenance missing machine-recoverable block"
            )

        payload_text = text.split(opening, 1)[1]

        if closing not in payload_text:
            raise ProvenanceError(
                "Persisted Provenance has unterminated representation"
            )

        payload_text = payload_text.split(closing, 1)[0]

        try:
            payload = json.loads(payload_text)
        except json.JSONDecodeError as exc:
            raise ProvenanceError(
                "Persisted Provenance representation is malformed"
            ) from exc

        required = {
            "sources",
            "observations",
            "evidence",
            "claims",
            "verifications",
            "knowledge",
            "evidence_relations",
        }

        if set(payload) != required:
            raise ProvenanceError(
                "Persisted Provenance schema is incomplete or unknown"
            )

        provenance = cls()

        def register(
            collection: dict[str, object],
            item: object,
            identifier: str,
        ) -> None:
            if identifier in collection:
                raise ProvenanceError(
                    f"Duplicate persisted identity: {identifier}"
                )
            collection[identifier] = item

        try:
            for data in payload["sources"]:
                item = Source(**data)
                register(
                    provenance._sources,
                    item,
                    item.identifier,
                )

            for data in payload["observations"]:
                item = Observation(**data)

                if item.source not in provenance._sources:
                    raise ProvenanceError(
                        "Observation references missing Source: "
                        f"{item.source}"
                    )

                register(
                    provenance._observations,
                    item,
                    item.identifier,
                )

            for data in payload["evidence"]:
                item = Evidence(**data)

                if item.observation not in provenance._observations:
                    raise ProvenanceError(
                        "Evidence references missing Observation: "
                        f"{item.observation}"
                    )

                register(
                    provenance._evidence,
                    item,
                    item.identifier,
                )

            for data in payload["claims"]:
                item = Claim(**data)
                register(
                    provenance._claims,
                    item,
                    item.identifier,
                )

            for data in payload["verifications"]:
                item = Verification(**data)

                if item.claim not in provenance._claims:
                    raise ProvenanceError(
                        "Verification references missing Claim: "
                        f"{item.claim}"
                    )

                register(
                    provenance._verifications,
                    item,
                    item.identifier,
                )

            for data in payload["knowledge"]:
                item = Knowledge(**data)

                if (
                    item.verification_identifier
                    not in provenance._verifications
                ):
                    raise ProvenanceError(
                        "Knowledge references missing Verification: "
                        f"{item.verification_identifier}"
                    )

                register(
                    provenance._knowledge,
                    item,
                    item.identifier,
                )

            for data in payload["evidence_relations"]:
                relation = EvidenceRelation(**data)

                if relation.evidence not in provenance._evidence:
                    raise ProvenanceError(
                        "EvidenceRelation references missing Evidence: "
                        f"{relation.evidence}"
                    )

                if relation.claim not in provenance._claims:
                    raise ProvenanceError(
                        "EvidenceRelation references missing Claim: "
                        f"{relation.claim}"
                    )

                if relation in provenance._evidence_relations:
                    raise ProvenanceError(
                        "Duplicate persisted EvidenceRelation"
                    )

                provenance._evidence_relations.append(relation)

        except TypeError as exc:
            raise ProvenanceError(
                "Persisted Provenance entity is malformed"
            ) from exc

        return provenance

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

    def _require_registered_verification(
        self,
        verification: Verification,
    ) -> None:
        if (
            self._verifications.get(verification.identifier)
            != verification
        ):
            raise ProvenanceError(
                "Verification is not registered in this Provenance"
            )

    def _require_registered_claim(self, claim: Claim) -> None:
        if self._claims.get(claim.identifier) != claim:
            raise ProvenanceError(
                f"Unknown Claim: {claim.identifier}"
            )

    def _require_registered_knowledge(
        self,
        knowledge: Knowledge,
    ) -> None:
        if self._knowledge.get(knowledge.identifier) != knowledge:
            raise ProvenanceError(
                f"Unknown Knowledge: {knowledge.identifier}"
            )
