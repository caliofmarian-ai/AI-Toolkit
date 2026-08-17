from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any, Callable, Mapping


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
class NeedEvaluation:
    schema: str
    need_id: str
    research_required: bool
    requested_capabilities: tuple[str, ...]
    reason: str
    confidence: str

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["requested_capabilities"] = list(self.requested_capabilities)
        return result


@dataclass(frozen=True)
class NavigationPlan:
    schema: str
    need_id: str
    required: bool
    capabilities: tuple[str, ...]
    read_only: bool
    authority_preserved: bool
    working_context_materialized: bool
    retrieval_executed: bool
    stopping_conditions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["capabilities"] = list(self.capabilities)
        result["stopping_conditions"] = list(self.stopping_conditions)
        return result


@dataclass(frozen=True)
class WorkingContext:
    schema: str
    need_id: str
    journey_id: str
    status: str
    source_identity_kind: str
    source_paths: tuple[str, ...]
    evidence: tuple[Mapping[str, Any], ...]
    authority_conferred: bool
    human_authority_preserved: bool
    unknown_is_valid: bool
    bounded: bool

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["source_paths"] = list(self.source_paths)
        result["evidence"] = [
            dict(item)
            for item in self.evidence
        ]
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
    NEED_EVALUATION_SCHEMA = "FUSION-02-NEED-EVALUATION-1"
    NAVIGATION_PLAN_SCHEMA = "FUSION-02-NAVIGATION-PLAN-1"
    WORKING_CONTEXT_SCHEMA = "FUSION-02-WORKING-CONTEXT-1"

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

    def evaluate_need(self, need: InformationNeed) -> NeedEvaluation:
        question = need.question.casefold()

        repository_signals = (
            "repository",
            "repo",
            "git",
            "github",
            "commit",
            "branch",
            "pull request",
            "issue",
            "code",
            "file",
            "implementation",
            "test",
            "audit",
            "evidence",
            "source",
            "trace",
            "dependency",
            "architecture",
        )

        trivial_messages = {
            "hi",
            "hello",
            "hey",
            "thanks",
            "thank you",
            "ok",
            "okay",
        }

        if question in trivial_messages:
            return NeedEvaluation(
                schema=self.NEED_EVALUATION_SCHEMA,
                need_id=need.need_id,
                research_required=False,
                requested_capabilities=(),
                reason="NO_EPISTEMIC_NAVIGATION_REQUIRED",
                confidence="HIGH",
            )

        if any(signal in question for signal in repository_signals):
            return NeedEvaluation(
                schema=self.NEED_EVALUATION_SCHEMA,
                need_id=need.need_id,
                research_required=True,
                requested_capabilities=(
                    "search",
                    "resolve",
                    "read",
                    "inspect",
                ),
                reason="REPOSITORY_EVIDENCE_REQUIRED",
                confidence="BOUNDED_HEURISTIC",
            )

        return NeedEvaluation(
            schema=self.NEED_EVALUATION_SCHEMA,
            need_id=need.need_id,
            research_required=False,
            requested_capabilities=(),
            reason="RESEARCH_REQUIREMENT_UNDEMONSTRATED",
            confidence="UNKNOWN",
        )

    def plan_navigation(
        self,
        need: InformationNeed,
        evaluation: NeedEvaluation,
    ) -> NavigationPlan:
        required = evaluation.research_required

        return NavigationPlan(
            schema=self.NAVIGATION_PLAN_SCHEMA,
            need_id=need.need_id,
            required=required,
            capabilities=(
                evaluation.requested_capabilities
                if required
                else ()
            ),
            read_only=True,
            authority_preserved=True,
            working_context_materialized=False,
            retrieval_executed=False,
            stopping_conditions=(
                "NEED_SATISFIED",
                "NO_EPISTEMIC_GAIN",
                "UNKNOWN",
                "HUMAN_REQUIRED",
                "FORBIDDEN",
            ) if required else (),
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

    def execute_search_navigation(
        self,
        *,
        plan: NavigationPlan,
        journey: JourneyState,
        keyword: str,
        search: Callable[[str], Mapping[str, Any]],
    ) -> dict[str, Any]:
        """Execute one bounded read-only search navigation step."""
        if not plan.required:
            return {
                "navigation_plan": plan.to_dict(),
                "journey": journey.to_dict(),
                "retrieval": None,
            }

        if "search" not in plan.capabilities:
            return {
                "navigation_plan": plan.to_dict(),
                "journey": journey.to_dict(),
                "retrieval": None,
            }

        if not plan.read_only:
            raise ValueError("Navigation plan must remain read-only")

        if not plan.authority_preserved:
            raise ValueError("Navigation plan must preserve Human authority")

        if plan.working_context_materialized:
            raise ValueError(
                "Search navigation cannot begin from materialized Working Context"
            )

        normalized_keyword = " ".join(str(keyword).split())

        if not normalized_keyword:
            raise ValueError("Search keyword must not be empty")

        raw_result = search(normalized_keyword)

        if not isinstance(raw_result, Mapping):
            raise TypeError("Search result must be a mapping")

        result = dict(raw_result)

        evidence_paths: list[str] = []

        for family in ("python", "shell", "tests", "docs"):
            values = result.get(family, ())

            if isinstance(values, (list, tuple)):
                for value in values:
                    if isinstance(value, str) and value:
                        evidence_paths.append(value)

        semantic = result.get("semantic", {})

        if isinstance(semantic, Mapping):
            for value in semantic:
                if isinstance(value, str) and value:
                    evidence_paths.append(value)

        source_paths = tuple(dict.fromkeys(evidence_paths))
        epistemic_gain = bool(source_paths)

        updated_plan = NavigationPlan(
            schema=plan.schema,
            need_id=plan.need_id,
            required=plan.required,
            capabilities=plan.capabilities,
            read_only=plan.read_only,
            authority_preserved=plan.authority_preserved,
            working_context_materialized=False,
            retrieval_executed=True,
            stopping_conditions=plan.stopping_conditions,
        )

        updated_journey = JourneyState(
            schema=journey.schema,
            journey_id=journey.journey_id,
            need_id=journey.need_id,
            status=(
                "IN_PROGRESS"
                if epistemic_gain
                else "NO_EPISTEMIC_GAIN"
            ),
            step_count=journey.step_count + 1,
            epistemic_gain=epistemic_gain,
            visited=journey.visited + ("evidence:search",),
            stopping_reason=(
                ""
                if epistemic_gain
                else "NO_EPISTEMIC_GAIN"
            ),
        )

        return {
            "navigation_plan": updated_plan.to_dict(),
            "journey": updated_journey.to_dict(),
            "retrieval": {
                "schema": "FUSION-02-READ-ONLY-SEARCH-1",
                "capability": "search",
                "keyword": normalized_keyword,
                "read_only": True,
                "authority_conferred": False,
                "working_context_materialized": False,
                "source_identity_kind": "repository-relative-path",
                "source_paths": list(source_paths),
                "result": result,
            },
        }

    def materialize_working_context(
        self,
        *,
        need: InformationNeed,
        journey: JourneyState,
        retrieval: Mapping[str, Any] | None,
        max_sources: int = 8,
    ) -> WorkingContext:
        """Materialize bounded active evidence from one retrieval result."""
        if max_sources < 1:
            raise ValueError("max_sources must be at least 1")

        if retrieval is None:
            return WorkingContext(
                schema=self.WORKING_CONTEXT_SCHEMA,
                need_id=need.need_id,
                journey_id=journey.journey_id,
                status="UNKNOWN",
                source_identity_kind="repository-relative-path",
                source_paths=(),
                evidence=(),
                authority_conferred=False,
                human_authority_preserved=True,
                unknown_is_valid=True,
                bounded=True,
            )

        if not isinstance(retrieval, Mapping):
            raise TypeError("retrieval must be a mapping or None")

        if retrieval.get("authority_conferred") is not False:
            raise ValueError(
                "Retrieval must not confer epistemic authority"
            )

        if retrieval.get("working_context_materialized") is not False:
            raise ValueError(
                "Working Context must be materialized exactly once "
                "from candidate retrieval"
            )

        source_identity_kind = retrieval.get(
            "source_identity_kind",
            "",
        )

        if source_identity_kind != "repository-relative-path":
            raise ValueError(
                "Working Context requires repository-relative source identity"
            )

        raw_paths = retrieval.get("source_paths", ())

        if not isinstance(raw_paths, (list, tuple)):
            raise TypeError("retrieval source_paths must be a sequence")

        selected_paths: list[str] = []

        for value in raw_paths:
            if not isinstance(value, str):
                continue

            normalized = value.strip()

            if not normalized:
                continue

            if normalized in selected_paths:
                continue

            selected_paths.append(normalized)

            if len(selected_paths) >= max_sources:
                break

        result = retrieval.get("result", {})

        if not isinstance(result, Mapping):
            raise TypeError("retrieval result must be a mapping")

        evidence: list[Mapping[str, Any]] = []

        for path in selected_paths:
            families: list[str] = []

            for family in ("python", "shell", "tests", "docs"):
                values = result.get(family, ())

                if (
                    isinstance(values, (list, tuple))
                    and path in values
                ):
                    families.append(family)

            semantic = result.get("semantic", {})

            if isinstance(semantic, Mapping) and path in semantic:
                families.append("semantic")

            evidence.append(
                {
                    "source_path": path,
                    "source_identity_kind": source_identity_kind,
                    "families": families,
                }
            )

        status = (
            "MATERIALIZED"
            if selected_paths
            else "UNKNOWN"
        )

        return WorkingContext(
            schema=self.WORKING_CONTEXT_SCHEMA,
            need_id=need.need_id,
            journey_id=journey.journey_id,
            status=status,
            source_identity_kind=source_identity_kind,
            source_paths=tuple(selected_paths),
            evidence=tuple(evidence),
            authority_conferred=False,
            human_authority_preserved=True,
            unknown_is_valid=True,
            bounded=True,
        )

    def initialize(
        self,
        question: str,
        *,
        session_id: str = "",
    ) -> dict[str, Any]:
        need = self.formulate_need(question)
        evaluation = self.evaluate_need(need)

        evaluated_need = InformationNeed(
            schema=need.schema,
            need_id=need.need_id,
            question=need.question,
            objective=need.objective,
            epistemic_status=need.epistemic_status,
            research_required=evaluation.research_required,
            requested_capabilities=evaluation.requested_capabilities,
            constraints=need.constraints,
        )

        navigation_plan = self.plan_navigation(
            evaluated_need,
            evaluation,
        )

        journey = self.begin_journey(
            evaluated_need,
            session_id=session_id,
        )

        return {
            "information_need": evaluated_need.to_dict(),
            "need_evaluation": evaluation.to_dict(),
            "navigation_plan": navigation_plan.to_dict(),
            "journey": journey.to_dict(),
        }
