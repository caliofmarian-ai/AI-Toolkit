from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
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
    human_question: str
    constraints: Mapping[str, bool]
    source_identity_kind: str
    source_paths: tuple[str, ...]
    evidence: tuple[Mapping[str, Any], ...]
    provenance: tuple[Mapping[str, Any], ...]
    epistemic_results: tuple[Mapping[str, Any], ...]
    semantic_identities: tuple[str, ...]
    epistemic_classes: tuple[str, ...]
    uncertainties: tuple[str, ...]
    relationships: tuple[Mapping[str, Any], ...]
    journey_summary: Mapping[str, Any]
    authority_conferred: bool
    human_authority_preserved: bool
    unknown_is_valid: bool
    bounded: bool

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["constraints"] = dict(self.constraints)
        result["source_paths"] = list(self.source_paths)
        result["evidence"] = [dict(item) for item in self.evidence]
        result["provenance"] = [dict(item) for item in self.provenance]
        result["epistemic_results"] = [
            dict(item) for item in self.epistemic_results
        ]
        result["semantic_identities"] = list(self.semantic_identities)
        result["epistemic_classes"] = list(self.epistemic_classes)
        result["uncertainties"] = list(self.uncertainties)
        result["relationships"] = [
            dict(item) for item in self.relationships
        ]
        result["journey_summary"] = dict(self.journey_summary)
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

    def execute_read_navigation(
        self,
        source_path: str,
        *,
        read,
        repository_root=None,
    ) -> Dict[str, Any]:
        """Read one bounded repository source without conferring authority."""
        normalized_path = str(source_path or "").strip()

        if not normalized_path:
            return {
                "schema": "FUSION-02-READ-ONLY-SOURCE-1",
                "capability": "read",
                "status": "UNKNOWN",
                "read_only": True,
                "bounded": True,
                "authority_conferred": False,
                "human_authority_preserved": True,
                "unknown_is_valid": True,
                "source_identity_kind": "repository-relative-path",
                "source_path": "",
                "content": "",
                "epistemic_gain": False,
            }

        candidate = Path(normalized_path)

        if candidate.is_absolute() or ".." in candidate.parts:
            return {
                "schema": "FUSION-02-READ-ONLY-SOURCE-1",
                "capability": "read",
                "status": "UNKNOWN",
                "read_only": True,
                "bounded": True,
                "authority_conferred": False,
                "human_authority_preserved": True,
                "unknown_is_valid": True,
                "source_identity_kind": "repository-relative-path",
                "source_path": normalized_path,
                "content": "",
                "epistemic_gain": False,
            }

        if repository_root is None:
            return {
                "schema": "FUSION-02-READ-ONLY-SOURCE-1",
                "capability": "read",
                "status": "UNKNOWN",
                "read_only": True,
                "bounded": True,
                "authority_conferred": False,
                "human_authority_preserved": True,
                "unknown_is_valid": True,
                "source_identity_kind": "repository-relative-path",
                "source_path": normalized_path,
                "content": "",
                "epistemic_gain": False,
            }

        root = Path(repository_root)

        try:
            content = read(root, normalized_path)
        except (OSError, UnicodeError):
            return {
                "schema": "FUSION-02-READ-ONLY-SOURCE-1",
                "capability": "read",
                "status": "UNKNOWN",
                "read_only": True,
                "bounded": True,
                "authority_conferred": False,
                "human_authority_preserved": True,
                "unknown_is_valid": True,
                "source_identity_kind": "repository-relative-path",
                "source_path": normalized_path,
                "content": "",
                "epistemic_gain": False,
            }

        if not isinstance(content, str):
            content = ""

        return {
            "schema": "FUSION-02-READ-ONLY-SOURCE-1",
            "capability": "read",
            "status": (
                "RETRIEVED"
                if content
                else "UNKNOWN"
            ),
            "read_only": True,
            "bounded": True,
            "authority_conferred": False,
            "human_authority_preserved": True,
            "unknown_is_valid": True,
            "source_identity_kind": "repository-relative-path",
            "source_path": normalized_path,
            "content": content,
            "epistemic_gain": bool(content),
        }

    def attach_read_evidence(
        self,
        *,
        retrieval: Mapping[str, Any],
        read_navigation: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Attach one bounded read observation to candidate retrieval."""
        if not isinstance(retrieval, Mapping):
            raise TypeError("retrieval must be a mapping")

        if not isinstance(read_navigation, Mapping):
            raise TypeError("read_navigation must be a mapping")

        if retrieval.get("authority_conferred") is not False:
            raise ValueError(
                "Retrieval must not confer epistemic authority"
            )

        if read_navigation.get("authority_conferred") is not False:
            raise ValueError(
                "Read observation must not confer epistemic authority"
            )

        if read_navigation.get("read_only") is not True:
            raise ValueError(
                "Research read observation must remain read-only"
            )

        if read_navigation.get("bounded") is not True:
            raise ValueError(
                "Research read observation must remain bounded"
            )

        source_path = str(
            read_navigation.get("source_path", "")
        ).strip()

        source_paths = tuple(
            value
            for value in retrieval.get("source_paths", ())
            if isinstance(value, str)
        )

        if source_path and source_path not in source_paths:
            raise ValueError(
                "Read observation source must originate from retrieval"
            )

        result = dict(retrieval)

        observations = []

        existing = result.get("read_observations", ())

        if isinstance(existing, (list, tuple)):
            observations.extend(
                dict(item)
                for item in existing
                if isinstance(item, Mapping)
            )

        if source_path:
            observations.append(
                {
                    "source_path": source_path,
                    "source_identity_kind": read_navigation.get(
                        "source_identity_kind",
                        "repository-relative-path",
                    ),
                    "status": read_navigation.get(
                        "status",
                        "UNKNOWN",
                    ),
                    "content": read_navigation.get(
                        "content",
                        "",
                    ),
                    "epistemic_gain": bool(
                        read_navigation.get(
                            "epistemic_gain",
                            False,
                        )
                    ),
                    "authority_conferred": False,
                    "human_authority_preserved": True,
                    "read_only": True,
                    "bounded": True,
                }
            )

        result["read_observations"] = observations
        result["authority_conferred"] = False
        result["working_context_materialized"] = False

        return result

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
                human_question=need.question,
                constraints=dict(need.constraints),
                source_identity_kind="repository-relative-path",
                source_paths=(),
                evidence=(),
                provenance=(),
                epistemic_results=(),
                semantic_identities=(),
                epistemic_classes=(),
                uncertainties=("retrieval-unavailable",),
                relationships=(),
                journey_summary={
                    "status": journey.status,
                    "step_count": journey.step_count,
                    "epistemic_gain": journey.epistemic_gain,
                    "stopping_reason": journey.stopping_reason,
                },
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

            read_observation = None

            raw_read_observations = retrieval.get(
                "read_observations",
                (),
            )

            if isinstance(
                raw_read_observations,
                (list, tuple),
            ):
                for observation in raw_read_observations:
                    if not isinstance(observation, Mapping):
                        continue

                    if (
                        observation.get("source_path")
                        == path
                    ):
                        read_observation = observation
                        break

            item = {
                "source_path": path,
                "source_identity_kind": source_identity_kind,
                "families": families,
            }

            if read_observation is not None:
                item["read_status"] = (
                    read_observation.get(
                        "status",
                        "UNKNOWN",
                    )
                )
                item["content"] = (
                    read_observation.get(
                        "content",
                        "",
                    )
                )
                item["read_only"] = True
                item["bounded"] = True
                item["authority_conferred"] = False

                for metadata_key in (
                    "repository_identity",
                    "requested_branch",
                    "requested_commit",
                    "resolved_commit",
                    "branch_head_commit",
                    "blob_sha",
                    "byte_count",
                    "content_complete",
                    "uncertainty",
                ):
                    if metadata_key in read_observation:
                        item[metadata_key] = (
                            read_observation[metadata_key]
                        )

            evidence.append(item)

        provenance = tuple(
            {
                "source_path": item["source_path"],
                "source_identity_kind": item["source_identity_kind"],
                "retrieval_capability": retrieval.get("capability", ""),
                "read_observed": "read_status" in item,
                "authority_conferred": False,
                **(
                    {
                        "repository_identity": item.get(
                            "repository_identity",
                            "",
                        ),
                        "requested_branch": item.get(
                            "requested_branch",
                            "",
                        ),
                        "requested_commit": item.get(
                            "requested_commit",
                            "",
                        ),
                        "resolved_commit": item.get(
                            "resolved_commit",
                            "",
                        ),
                        "blob_sha": item.get(
                            "blob_sha",
                            "",
                        ),
                        "byte_count": item.get(
                            "byte_count",
                            0,
                        ),
                        "content_complete": item.get(
                            "content_complete",
                            False,
                        ),
                    }
                    if item.get("repository_identity")
                    else {}
                ),
            }
            for item in evidence
        )

        semantic = result.get("semantic", {})
        semantic_identities: list[str] = []

        if isinstance(semantic, Mapping):
            for path in selected_paths:
                value = semantic.get(path)

                if not isinstance(value, Mapping):
                    continue

                identity = value.get("identity", "")

                if not isinstance(identity, str):
                    continue

                identity = identity.strip()

                if identity and identity not in semantic_identities:
                    semantic_identities.append(identity)

        raw_class = retrieval.get("epistemic_class", "")
        epistemic_classes = (
            (raw_class.strip(),)
            if isinstance(raw_class, str) and raw_class.strip()
            else ()
        )

        raw_uncertainties = retrieval.get("uncertainties", ())
        uncertainties = (
            tuple(
                dict.fromkeys(
                    value.strip()
                    for value in raw_uncertainties
                    if isinstance(value, str) and value.strip()
                )
            )
            if isinstance(raw_uncertainties, (list, tuple))
            else ()
        )

        raw_relationships = retrieval.get("relationships", ())
        relationships = (
            tuple(
                dict(value)
                for value in raw_relationships
                if isinstance(value, Mapping)
            )
            if isinstance(raw_relationships, (list, tuple))
            else ()
        )

        epistemic_results = tuple(
            {
                "identity": (
                    semantic_identities[index]
                    if index < len(semantic_identities)
                    else item["source_path"]
                ),
                "source_path": item["source_path"],
                "epistemic_class": (
                    epistemic_classes[0]
                    if epistemic_classes
                    else "UNKNOWN"
                ),
                "authority": "TECHNICAL_OBSERVATION",
            }
            for index, item in enumerate(evidence)
        )

        journey_summary = {
            "status": journey.status,
            "step_count": journey.step_count,
            "epistemic_gain": journey.epistemic_gain,
            "stopping_reason": journey.stopping_reason,
        }

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
            human_question=need.question,
            constraints=dict(need.constraints),
            source_identity_kind=source_identity_kind,
            source_paths=tuple(selected_paths),
            evidence=tuple(evidence),
            provenance=provenance,
            epistemic_results=epistemic_results,
            semantic_identities=tuple(semantic_identities),
            epistemic_classes=epistemic_classes,
            uncertainties=uncertainties,
            relationships=relationships,
            journey_summary=journey_summary,
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

    def conserve_journey_boundary(
        self,
        *,
        journey: JourneyState,
        boundary: str,
        provider_failed: bool = False,
        stopping_reason: str = "",
    ) -> JourneyState:
        """Conserve Journey state across a terminal execution boundary."""
        normalized_boundary = str(
            boundary or ""
        ).strip().upper()

        normalized_reason = str(
            stopping_reason or ""
        ).strip().upper()

        allowed_boundaries = {
            "PARTIAL",
            "BLOCKED",
            "HUMAN_REQUIRED",
            "FORBIDDEN",
            "PROVIDER_FAILURE",
        }

        if provider_failed:
            normalized_boundary = "PROVIDER_FAILURE"

        if normalized_boundary not in allowed_boundaries:
            raise ValueError(
                "unsupported journey conservation boundary: "
                + normalized_boundary
            )

        reason = (
            normalized_reason
            or normalized_boundary
        )

        return JourneyState(
            schema=journey.schema,
            journey_id=journey.journey_id,
            need_id=journey.need_id,
            status=normalized_boundary,
            step_count=journey.step_count,
            epistemic_gain=journey.epistemic_gain,
            visited=tuple(journey.visited),
            stopping_reason=reason,
        )

    def evaluate_cognitive_loop_guard(
        self,
        *,
        journey: JourneyState,
        need_id: str = "",
        result_identity: str = "",
        observation_identity: str = "",
        capability: str = "",
        unavailable_organ: bool = False,
        ambiguous: bool = False,
        authority_stop: bool = False,
        epistemic_gain: bool = True,
    ) -> Dict[str, Any]:
        """Evaluate one bounded set of cognitive-loop stopping guards."""
        normalized_need = str(need_id or "").strip()
        normalized_result = str(
            result_identity or ""
        ).strip()
        normalized_observation = str(
            observation_identity or ""
        ).strip()
        normalized_capability = str(
            capability or ""
        ).strip()

        visited = tuple(
            str(value).strip()
            for value in journey.visited
            if str(value).strip()
        )

        repeated_need = bool(
            normalized_need
            and normalized_need == journey.need_id
            and journey.step_count > 0
        )

        result_token = (
            f"result:{normalized_result}"
            if normalized_result
            else ""
        )

        repeated_result = bool(
            result_token
            and result_token in visited
        )

        identity_capability_token = (
            "observation:"
            + normalized_observation
            + "|capability:"
            + normalized_capability
            if normalized_observation
            and normalized_capability
            else ""
        )

        repeated_identity_capability = bool(
            identity_capability_token
            and identity_capability_token in visited
        )

        traversal_cycle = bool(
            normalized_observation
            and normalized_observation in visited
        )

        no_epistemic_gain = not bool(
            epistemic_gain
        )

        stopping_reason = ""

        if authority_stop:
            stopping_reason = "AUTHORITY_STOP"
        elif unavailable_organ:
            stopping_reason = "UNAVAILABLE_ORGAN"
        elif ambiguous:
            stopping_reason = "AMBIGUITY"
        elif repeated_identity_capability:
            stopping_reason = (
                "REPEATED_IDENTITY_CAPABILITY"
            )
        elif repeated_result:
            stopping_reason = "REPEATED_RESULT"
        elif traversal_cycle:
            stopping_reason = "TRAVERSAL_CYCLE"
        elif repeated_need:
            stopping_reason = "REPEATED_NEED"
        elif no_epistemic_gain:
            stopping_reason = "NO_EPISTEMIC_GAIN"

        return {
            "schema": (
                "FUSION-02-COGNITIVE-LOOP-GUARD-1"
            ),
            "continue_navigation": not bool(
                stopping_reason
            ),
            "stopping_reason": stopping_reason,
            "repeated_need": repeated_need,
            "repeated_result": repeated_result,
            "repeated_identity_capability": (
                repeated_identity_capability
            ),
            "traversal_cycle": traversal_cycle,
            "unavailable_organ": bool(
                unavailable_organ
            ),
            "ambiguous": bool(ambiguous),
            "authority_stop": bool(
                authority_stop
            ),
            "no_epistemic_gain": (
                no_epistemic_gain
            ),
            "authority_conferred": False,
            "human_authority_preserved": True,
            "unknown_is_valid": True,
            "bounded": True,
        }

    def evaluate_cognitive_step(
        self,
        *,
        journey: JourneyState,
        outcome: str,
        observation_identity: str = "",
        epistemic_gain: bool,
    ) -> Dict[str, Any]:
        """Evaluate one bounded cognitive step and transition its journey."""
        allowed_outcomes = {
            "SATISFIED",
            "PARTIAL",
            "UNKNOWN",
            "BLOCKED",
            "HUMAN_REQUIRED",
            "FORBIDDEN",
            "NO_EPISTEMIC_GAIN",
        }

        normalized_outcome = str(outcome or "").strip().upper()

        if normalized_outcome not in allowed_outcomes:
            raise ValueError(
                "unsupported cognitive outcome: "
                + normalized_outcome
            )

        gain = bool(epistemic_gain)

        effective_outcome = normalized_outcome

        if (
            normalized_outcome in {"PARTIAL", "UNKNOWN"}
            and not gain
        ):
            effective_outcome = "NO_EPISTEMIC_GAIN"

        continue_navigation = (
            effective_outcome in {"PARTIAL", "UNKNOWN"}
            and gain
        )

        if continue_navigation:
            next_status = "IN_PROGRESS"
            stopping_reason = ""
        else:
            next_status = effective_outcome
            stopping_reason = effective_outcome

        visited = list(journey.visited)

        normalized_identity = str(
            observation_identity or ""
        ).strip()

        if (
            normalized_identity
            and normalized_identity not in visited
        ):
            visited.append(normalized_identity)

        transitioned_journey = JourneyState(
            schema=journey.schema,
            journey_id=journey.journey_id,
            need_id=journey.need_id,
            status=next_status,
            step_count=journey.step_count + 1,
            epistemic_gain=gain,
            visited=tuple(visited),
            stopping_reason=stopping_reason,
        )

        return {
            "schema": "FUSION-02-COGNITIVE-STEP-1",
            "outcome": effective_outcome,
            "continue_navigation": continue_navigation,
            "authority_conferred": False,
            "human_authority_preserved": True,
            "unknown_is_valid": True,
            "journey": transitioned_journey.to_dict(),
        }


@dataclass(frozen=True)
class ContextBudget:
    """Provider-safe budget for temporary Working Context consciousness."""

    provider_capacity: int
    reserved_orientation: int
    reserved_question: int
    reserved_instructions: int
    reserved_answer: int
    available_context: int

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass(frozen=True)
class GovernedWorkingContext:
    """Whole-object Working Context selected under a provider budget."""

    budget: ContextBudget
    context: Mapping[str, Any]
    estimated_context_units: int
    compacted: bool
    rejected: bool
    rejection_reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "budget": self.budget.to_dict(),
            "context": dict(self.context),
            "estimated_context_units": self.estimated_context_units,
            "compacted": self.compacted,
            "rejected": self.rejected,
            "rejection_reason": self.rejection_reason,
        }


class ContextBudgetGovernor:
    """Govern provider-facing context without mutating organism knowledge."""

    def calculate_budget(
        self,
        *,
        provider_capacity: int | None,
        reserved_orientation: int,
        reserved_question: int,
        reserved_instructions: int,
        reserved_answer: int,
    ) -> ContextBudget:
        if provider_capacity is None or provider_capacity <= 0:
            raise ValueError(
                "provider capacity must be known and positive"
            )

        reservations = (
            reserved_orientation,
            reserved_question,
            reserved_instructions,
            reserved_answer,
        )

        if any(value < 0 for value in reservations):
            raise ValueError("budget reservations cannot be negative")

        reserved_total = sum(reservations)

        if reserved_total >= provider_capacity:
            raise ValueError(
                "provider capacity exhausted by required reservations"
            )

        return ContextBudget(
            provider_capacity=provider_capacity,
            reserved_orientation=reserved_orientation,
            reserved_question=reserved_question,
            reserved_instructions=reserved_instructions,
            reserved_answer=reserved_answer,
            available_context=provider_capacity-reserved_total,
        )

    @staticmethod
    def estimate_units(value: Any) -> int:
        import json

        serialized=json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )

        return max(1, (len(serialized.encode("utf-8"))+3)//4)

    def govern(
        self,
        *,
        working_context: WorkingContext,
        budget: ContextBudget,
    ) -> GovernedWorkingContext:
        original=working_context.to_dict()

        if self.estimate_units(original) <= budget.available_context:
            return GovernedWorkingContext(
                budget=budget,
                context=original,
                estimated_context_units=self.estimate_units(original),
                compacted=False,
                rejected=False,
                rejection_reason="",
            )

        base=dict(original)
        evidence=list(base.pop("evidence", []))
        provenance=list(base.pop("provenance", []))
        epistemic_results=list(base.pop("epistemic_results", []))
        relationships=list(base.pop("relationships", []))

        if self.estimate_units(base) > budget.available_context:
            return GovernedWorkingContext(
                budget=budget,
                context={},
                estimated_context_units=0,
                compacted=True,
                rejected=True,
                rejection_reason="HARD_CONTEXT_OVERFLOW",
            )

        selected_evidence=[]
        selected_provenance=[]
        selected_results=[]

        provenance_by_path={
            item.get("source_path"): item
            for item in provenance
            if isinstance(item, Mapping)
        }

        result_by_path={
            item.get("source_path"): item
            for item in epistemic_results
            if isinstance(item, Mapping)
        }

        for item in evidence:
            if not isinstance(item, Mapping):
                continue

            path=item.get("source_path")
            candidate=dict(base)
            candidate["evidence"]=selected_evidence+[dict(item)]

            candidate_provenance=list(selected_provenance)
            if path in provenance_by_path:
                candidate_provenance.append(
                    dict(provenance_by_path[path])
                )

            candidate_results=list(selected_results)
            if path in result_by_path:
                candidate_results.append(
                    dict(result_by_path[path])
                )

            candidate["provenance"]=candidate_provenance
            candidate["epistemic_results"]=candidate_results
            candidate["relationships"]=relationships

            if (
                self.estimate_units(candidate)
                > budget.available_context
            ):
                break

            selected_evidence.append(dict(item))
            selected_provenance=candidate_provenance
            selected_results=candidate_results

        compacted=dict(base)
        compacted["evidence"]=selected_evidence
        compacted["provenance"]=selected_provenance
        compacted["epistemic_results"]=selected_results
        compacted["relationships"]=relationships

        while (
            relationships
            and self.estimate_units(compacted)
            > budget.available_context
        ):
            relationships=relationships[:-1]
            compacted["relationships"]=relationships

        estimated=self.estimate_units(compacted)

        if estimated > budget.available_context:
            return GovernedWorkingContext(
                budget=budget,
                context={},
                estimated_context_units=0,
                compacted=True,
                rejected=True,
                rejection_reason="HARD_CONTEXT_OVERFLOW",
            )

        return GovernedWorkingContext(
            budget=budget,
            context=compacted,
            estimated_context_units=estimated,
            compacted=True,
            rejected=False,
            rejection_reason="",
        )
