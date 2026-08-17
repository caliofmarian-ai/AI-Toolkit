from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any, Mapping


@dataclass(frozen=True)
class InformationNeed:
    schema: str
    need_id: str
    question: str
    objective: str
    epistemic_status: str
    research_required: bool
    requested_capabilities: tuple[str, ...]
    constraints: Mapping[str, bool]

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["requested_capabilities"] = list(self.requested_capabilities)
        result["constraints"] = dict(self.constraints)
        return result


@dataclass(frozen=True)
class JourneyState:
    schema: str
    journey_id: str
    need_id: str
    status: str
    step_count: int
    epistemic_gain: bool
    visited: tuple[str, ...]
    stopping_reason: str

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["visited"] = list(self.visited)
        return result


class EpistemicCognitiveCoordinator:
    INFORMATION_NEED_SCHEMA = "FUSION-02-INFORMATION-NEED-1"
    JOURNEY_SCHEMA = "FUSION-02-JOURNEY-STATE-1"

    TERMINAL_STATUSES = (
        "SATISFIED",
        "PARTIAL",
        "UNKNOWN",
        "BLOCKED",
        "HUMAN_REQUIRED",
        "FORBIDDEN",
        "NO_EPISTEMIC_GAIN",
    )

    def formulate_need(self, question: str) -> InformationNeed:
        normalized = " ".join(str(question).split())

        if not normalized:
            raise ValueError("Human question must not be empty")

        digest = sha256(normalized.encode("utf-8")).hexdigest()[:20]

        return InformationNeed(
            schema=self.INFORMATION_NEED_SCHEMA,
            need_id=f"need-{digest}",
            question=normalized,
            objective="ANSWER_HUMAN_REQUEST",
            epistemic_status="UNRESOLVED",
            research_required=False,
            requested_capabilities=(),
            constraints={
                "retrieval_confers_authority": False,
                "navigation_read_only": True,
                "unknown_is_valid": True,
                "human_authority_preserved": True,
                "knowledge_availability_is_not_working_context": True,
                "full_repository_profile_default_payload": False,
            },
        )

    def begin_journey(
        self,
        need: InformationNeed,
        *,
        session_id: str = "",
    ) -> JourneyState:
        seed = f"{session_id}:{need.need_id}"
        digest = sha256(seed.encode("utf-8")).hexdigest()[:20]

        return JourneyState(
            schema=self.JOURNEY_SCHEMA,
            journey_id=f"journey-{digest}",
            need_id=need.need_id,
            status="UNRESOLVED",
            step_count=0,
            epistemic_gain=False,
            visited=(),
            stopping_reason="",
        )

    def initialize(
        self,
        question: str,
        *,
        session_id: str = "",
    ) -> dict[str, Any]:
        need = self.formulate_need(question)
        journey = self.begin_journey(
            need,
            session_id=session_id,
        )

        return {
            "information_need": need.to_dict(),
            "journey": journey.to_dict(),
        }
