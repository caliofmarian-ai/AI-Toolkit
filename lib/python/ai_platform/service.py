from __future__ import annotations
import hashlib
import logging
import re

from collections import defaultdict
from typing import Any, Dict, Mapping, Optional

from .adapters import builtin_adapters
from .context_builder import AIContextBuilder
from .conversation_experience import ConversationExperienceBridge
from .conversation_context import ConversationContextReconstructor
from .interrupted_turn import recover_interrupted_human_turn
from .cognitive_coordination import (
    EpistemicCognitiveCoordinator,
    InformationNeed,
    JourneyState,
    NavigationPlan,
)
from python.evidence_engine.engine import EvidenceEngine
from python.runtime.railway import load_railway_metadata
from .model_manager import ModelManager
from .pipeline import AIRequestPipeline
from .prompt_library import PromptLibrary
from .registry import ProviderRegistry
from .sessions import AISessionEngine
from .settings import AISettingsStore, masked_provider_settings

logger = logging.getLogger(__name__)



def _fusion02_context_anatomy(context):
    """Return structural size metadata, never context values."""
    import json

    def serialized_bytes(value):
        return len(
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                default=str,
            ).encode("utf-8")
        )

    total = serialized_bytes(context)
    branches = {}

    if isinstance(context, dict):
        for key, value in context.items():
            branch_bytes = serialized_bytes(value)

            branches[str(key)] = {
                "bytes": branch_bytes,
                "percent": round(
                    (
                        branch_bytes
                        / total
                        * 100.0
                    )
                    if total
                    else 0.0,
                    2,
                ),
                "kind": (
                    "object"
                    if isinstance(value, dict)
                    else "array"
                    if isinstance(value, list)
                    else "string"
                    if isinstance(value, str)
                    else type(value).__name__
                ),
                "children": (
                    len(value)
                    if isinstance(
                        value,
                        (dict, list),
                    )
                    else 0
                ),
            }

    return {
        "total_serialized_bytes": total,
        "estimated_tokens_at_4_bytes": (
            (total + 3) // 4
        ),
        "branch_count": len(branches),
        "branches": branches,
    }


def _fusion02_log_context_anatomy(context):
    """Log structural measurements only."""
    anatomy = _fusion02_context_anatomy(
        context
    )

    ordered = sorted(
        anatomy["branches"].items(),
        key=lambda item: (
            item[1]["bytes"]
        ),
        reverse=True,
    )

    branch_summary = ",".join(
        (
            f"{name}="
            f"{data['bytes']}"
            f"({data['percent']}%)"
        )
        for name, data in ordered
    )

    logger.info(
        "FUSION-02 reconstructed context anatomy: "
        "total_serialized_bytes=%s, "
        "estimated_tokens_at_4_bytes=%s, "
        "branch_count=%s, "
        "branches=%s",
        anatomy[
            "total_serialized_bytes"
        ],
        anatomy[
            "estimated_tokens_at_4_bytes"
        ],
        anatomy[
            "branch_count"
        ],
        branch_summary,
        extra={
            "fusion02_context_anatomy":
                anatomy,
        },
    )

    return anatomy


class AIPlatformService:
    def __init__(
        self,
        repository_root: str = ".",
        workspace_root: Optional[str] = None,
        *,
        state_root: Optional[str] = None,
    ) -> None:
        self.settings = AISettingsStore(repository_root)
        self.registry = ProviderRegistry()
        self.model_manager = ModelManager()
        self.context_builder = AIContextBuilder(repository_root, workspace_root)
        self.sessions = AISessionEngine(
            repository_root,
            state_root=state_root,
        )
        self.conversation_experience = ConversationExperienceBridge(
            repository_root,
            state_root=state_root,
        )
        self.conversation_context = ConversationContextReconstructor(
            repository_root,
            workspace_root,
            state_root=state_root,
        )
        self.cognitive_coordinator = EpistemicCognitiveCoordinator()
        self.evidence_engine = EvidenceEngine(repository_root)
        self.prompt_library = PromptLibrary()
        self.pipeline = AIRequestPipeline(
            registry=self.registry,
            model_manager=self.model_manager,
            context_builder=self.context_builder,
        )
        for adapter in builtin_adapters():
            self.registry.register(adapter)

    @staticmethod
    def runtime_deployment_identity() -> Dict[str, Any]:
        """Expose active deployment identity without provider narration."""
        metadata = load_railway_metadata()
        git_commit = metadata.git_commit_sha.strip().lower()
        git_branch = metadata.git_branch.strip()
        complete = (
            metadata.is_railway
            and metadata.project_id not in {"", "local"}
            and metadata.service_id not in {"", "local"}
            and metadata.deployment_id not in {"", "local"}
            and bool(git_branch)
            and git_branch != "unknown"
            and re.fullmatch(r"[0-9a-f]{40}", git_commit)
            is not None
        )

        return {
            "schema": "FUSION-02-ACTIVE-RUNTIME-IDENTITY-1",
            "source": "SERVER_ENVIRONMENT_NOT_PROVIDER_TEXT",
            "platform": "RAILWAY" if metadata.is_railway else "LOCAL",
            "project_id": metadata.project_id,
            "service_id": metadata.service_id,
            "environment": metadata.environment,
            "environment_id": metadata.environment_id,
            "deployment_id": metadata.deployment_id,
            "repository": metadata.git_repository,
            "git_branch": git_branch,
            "git_commit": git_commit,
            "status": (
                "DEMONSTRATED"
                if complete
                else "NOT_DEMONSTRATED"
            ),
            "identity_complete": complete,
            "authority_conferred": False,
            "human_authority_preserved": True,
        }

    @staticmethod
    def checkpoint_integrity_issues(
        retrieval: Mapping[str, Any],
    ) -> list[str]:
        """Return deterministic reasons an exact checkpoint is incomplete."""
        checkpoint = retrieval.get("checkpoint_identity")

        if not isinstance(checkpoint, Mapping):
            return ["checkpoint-identity-missing"]

        issues = []
        requested_count = int(
            checkpoint.get("requested_path_count", 0)
            or 0
        )
        retrieved_count = int(
            checkpoint.get("retrieved_path_count", 0)
            or 0
        )
        observations = retrieval.get("read_observations", ())

        if checkpoint.get("status") != "RETRIEVED":
            issues.append("checkpoint-status-not-retrieved")

        if checkpoint.get("complete_files") is not True:
            issues.append("checkpoint-files-not-complete")

        if requested_count < 1:
            issues.append("checkpoint-request-empty")

        if retrieved_count != requested_count:
            issues.append("checkpoint-path-count-mismatch")

        if not isinstance(observations, (list, tuple)):
            return issues + ["checkpoint-observations-invalid"]

        if len(observations) != requested_count:
            issues.append("checkpoint-observation-count-mismatch")

        for index, observation in enumerate(observations, start=1):
            prefix = f"checkpoint-observation-{index}"

            if not isinstance(observation, Mapping):
                issues.append(prefix + "-invalid")
                continue

            content = observation.get("content")
            content_sha256 = str(
                observation.get("content_sha256", "")
            ).lower()
            blob_sha = str(
                observation.get("blob_sha", "")
            ).lower()

            if observation.get("status") != "RETRIEVED":
                issues.append(prefix + "-not-retrieved")

            if observation.get("complete_file") is not True:
                issues.append(prefix + "-file-incomplete")

            if observation.get("content_complete") is not True:
                issues.append(prefix + "-content-incomplete")

            if observation.get("blob_sha_verified") is not True:
                issues.append(prefix + "-blob-unverified")

            if re.fullmatch(r"[0-9a-f]{40}", blob_sha) is None:
                issues.append(prefix + "-blob-identity-invalid")

            if not isinstance(content, str):
                issues.append(prefix + "-content-invalid")
                continue

            encoded = content.encode("utf-8")

            if observation.get("byte_count") != len(encoded):
                issues.append(prefix + "-byte-count-mismatch")

            if observation.get("character_count") != len(content):
                issues.append(prefix + "-character-count-mismatch")

            if (
                re.fullmatch(r"[0-9a-f]{64}", content_sha256)
                is None
                or hashlib.sha256(encoded).hexdigest()
                != content_sha256
            ):
                issues.append(prefix + "-content-hash-mismatch")

        return sorted(set(issues))

    @classmethod
    def access_attestation(
        cls,
        *,
        retrieval: Mapping[str, Any],
        working_context: Mapping[str, Any],
        pipeline_result: Mapping[str, Any],
    ) -> Dict[str, Any]:
        """Build a content-free system attestation for one AI raw source."""
        runtime_identity = cls.runtime_deployment_identity()
        checkpoint = dict(
            retrieval.get("checkpoint_identity", {})
        )
        provider_execution = dict(
            pipeline_result.get("provider_execution", {})
        )
        full_file_reading = dict(
            pipeline_result.get("full_file_reading", {})
        )
        evidence = working_context.get("evidence", ())
        manifests = []

        if isinstance(evidence, (list, tuple)):
            for item in evidence:
                if not isinstance(item, Mapping):
                    continue

                manifests.append(
                    {
                        "source_path": str(
                            item.get("source_path", "")
                        ),
                        "blob_sha": str(
                            item.get("blob_sha", "")
                        ),
                        "byte_count": int(
                            item.get("byte_count", 0) or 0
                        ),
                        "character_count": int(
                            item.get("character_count", 0) or 0
                        ),
                        "content_sha256": str(
                            item.get("content_sha256", "")
                        ),
                        "blob_sha_verified": (
                            item.get("blob_sha_verified") is True
                        ),
                        "content_complete": (
                            item.get("content_complete") is True
                        ),
                    }
                )

        checkpoint_issues = cls.checkpoint_integrity_issues(
            retrieval
        )
        checkpoint_complete = not checkpoint_issues
        manifests_verified = (
            bool(manifests)
            and len(manifests)
            == int(checkpoint.get("requested_path_count", 0) or 0)
            and all(
                item["blob_sha_verified"]
                and item["content_complete"]
                and re.fullmatch(
                    r"[0-9a-f]{40}",
                    item["blob_sha"],
                )
                is not None
                and re.fullmatch(
                    r"[0-9a-f]{64}",
                    item["content_sha256"],
                )
                is not None
                for item in manifests
            )
        )
        delivered_file_count = int(
            full_file_reading.get(
                "files_delivered",
                len(
                    full_file_reading.get(
                        "delivered_by_path",
                        {},
                    )
                ),
            )
            or 0
        )
        delivery_complete = (
            full_file_reading.get("all_segments_delivered") is True
            and full_file_reading.get("raw_content_truncated") is False
            and delivered_file_count == len(manifests)
        )
        runtime_matches_checkpoint = (
            runtime_identity["identity_complete"] is True
            and runtime_identity["git_commit"]
            == checkpoint.get("resolved_commit")
            and runtime_identity["git_branch"]
            == checkpoint.get("requested_branch")
        )
        access_demonstrated = (
            checkpoint_complete
            and manifests_verified
            and delivery_complete
            and runtime_matches_checkpoint
        )
        semantic_execution = bool(
            provider_execution.get("semantic_model_execution")
        )

        return {
            "schema": "FUSION-02-GROUNDED-ACCESS-ATTESTATION-1",
            "generated_by": "AIPlatformService",
            "status": (
                "DEMONSTRATED"
                if access_demonstrated
                else "PARTIAL"
            ),
            "runtime_identity": runtime_identity,
            "repository_checkpoint": checkpoint,
            "file_manifests": manifests,
            "full_file_reading": full_file_reading,
            "provider_execution": provider_execution,
            "verification": {
                "checkpoint_complete": checkpoint_complete,
                "checkpoint_integrity_issues": checkpoint_issues,
                "file_manifests_verified": manifests_verified,
                "provider_delivery_complete": delivery_complete,
                "runtime_matches_checkpoint": runtime_matches_checkpoint,
                "external_semantic_execution": semantic_execution,
            },
            "provider_narrative": {
                "epistemic_status": "RAW_SOURCE_NOT_EVIDENCE",
                "factual_grounding": "NOT_DEMONSTRATED",
                "self_report_is_attestation": False,
            },
            "authority_conferred": False,
            "human_authority_preserved": True,
        }

    def configure_provider(self, provider_id: str, **kwargs: Any) -> Dict[str, Any]:
        settings = self.settings.configure_provider(provider_id, **kwargs)
        return masked_provider_settings(settings)

    def configure_models(self, roles: Mapping[str, str]) -> Dict[str, Any]:
        settings = self.settings.configure_models(roles)
        return masked_provider_settings(settings)

    def configure_routing(self, default_provider: str = "", fallback_provider: str = "") -> Dict[str, Any]:
        settings = self.settings.configure_routing(
            default_provider=default_provider or None,
            fallback_provider=fallback_provider or None,
        )
        return masked_provider_settings(settings)

    def test_connection(self, provider_id: str) -> Dict[str, Any]:
        settings = self.settings.load()
        provider_settings = dict(settings.get("providers", {})).get(provider_id, {})
        return self.registry.test_connection(provider_id, provider_settings)

    def connect(self, provider_id: str) -> Dict[str, Any]:
        result = self.test_connection(provider_id)
        result["action"] = "connect"
        return result

    def disconnect(self, provider_id: str) -> Dict[str, Any]:
        result = {
            "provider": provider_id,
            "status": "disconnected",
            "connection": False,
            "action": "disconnect",
        }
        return result

    def create_session(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self.sessions.create(payload)

    def activate_productive_bounded_journey(
        self,
        *,
        retrieval,
        journey_state,
        search_navigation=None,
    ):
        """Activate real bounded repository physiology before provider use."""
        read_navigation = None
        read_navigations = []
        cognitive_loop_guards = []
        cognitive_step_evaluations = []

        if isinstance(retrieval, dict):
            source_paths = retrieval.get(
                "source_paths",
                (),
            )

            if source_paths:
                # FUSION-02 productive bounded cognitive journey.
                # Compose the existing read, evaluator, JourneyState, and
                # loop-guard organs over a finite candidate-source set.
                # The journey remains read-only and confers no authority.
                max_cognitive_steps = 8
                journey_source_paths = tuple(
                    source_paths[:max_cognitive_steps]
                )

                def _bounded_repository_read(
                    repository_root,
                    relative_path,
                ):
                    target = (
                        repository_root / relative_path
                    ).resolve()

                    target.relative_to(
                        repository_root.resolve()
                    )

                    return target.read_text(
                        encoding="utf-8",
                    )

                for selected_source_path in journey_source_paths:
                    observation_identity = (
                        "read:" + selected_source_path
                    )

                    loop_guard = (
                        self.cognitive_coordinator
                        .evaluate_cognitive_loop_guard(
                            journey=journey_state,
                            observation_identity=(
                                observation_identity
                            ),
                            capability="read",
                            epistemic_gain=True,
                        )
                    )

                    cognitive_loop_guards.append(
                        loop_guard
                    )

                    if not loop_guard[
                        "continue_navigation"
                    ]:
                        journey_state = (
                            self.cognitive_coordinator
                            .conserve_journey_boundary(
                                journey=journey_state,
                                boundary="PARTIAL",
                                stopping_reason=(
                                    loop_guard[
                                        "stopping_reason"
                                    ]
                                    or "LOOP_GUARD_STOP"
                                ),
                            )
                        )
                        break

                    current_read_navigation = (
                        self.cognitive_coordinator
                        .execute_read_navigation(
                            selected_source_path,
                            read=_bounded_repository_read,
                            repository_root=(
                                self.sessions.root
                            ),
                        )
                    )

                    read_navigations.append(
                        current_read_navigation
                    )

                    retrieval = (
                        self.cognitive_coordinator
                        .attach_read_evidence(
                            retrieval=retrieval,
                            read_navigation=(
                                current_read_navigation
                            ),
                        )
                    )

                    epistemic_gain = bool(
                        current_read_navigation.get(
                            "epistemic_gain",
                            False,
                        )
                    )

                    step_evaluation = (
                        self.cognitive_coordinator
                        .evaluate_cognitive_step(
                            journey=journey_state,
                            outcome=(
                                "PARTIAL"
                                if epistemic_gain
                                else "UNKNOWN"
                            ),
                            observation_identity=(
                                observation_identity
                            ),
                            epistemic_gain=(
                                epistemic_gain
                            ),
                        )
                    )

                    cognitive_step_evaluations.append(
                        step_evaluation
                    )

                    step_journey = (
                        step_evaluation["journey"]
                    )

                    journey_state = JourneyState(
                        schema=step_journey["schema"],
                        journey_id=(
                            step_journey["journey_id"]
                        ),
                        need_id=step_journey["need_id"],
                        status=step_journey["status"],
                        step_count=(
                            step_journey["step_count"]
                        ),
                        epistemic_gain=(
                            step_journey[
                                "epistemic_gain"
                            ]
                        ),
                        visited=tuple(
                            step_journey["visited"]
                        ),
                        stopping_reason=(
                            step_journey[
                                "stopping_reason"
                            ]
                        ),
                    )

                    if not step_evaluation[
                        "continue_navigation"
                    ]:
                        break

                if read_navigations:
                    # Preserve the existing singular response contract while
                    # exposing the complete bounded journey separately.
                    read_navigation = (
                        read_navigations[0]
                    )

                    search_navigation = dict(
                        search_navigation
                    )
                    search_navigation["retrieval"] = (
                        retrieval
                    )

                if journey_state.status == "IN_PROGRESS":
                    stopping_reason = (
                        "COGNITIVE_STEP_BOUND_REACHED"
                        if len(source_paths)
                        > len(journey_source_paths)
                        else "CANDIDATE_SOURCES_EXHAUSTED"
                    )

                    journey_state = (
                        self.cognitive_coordinator
                        .conserve_journey_boundary(
                            journey=journey_state,
                            boundary="PARTIAL",
                            stopping_reason=(
                                stopping_reason
                            ),
                        )
                    )

        return {
            "retrieval": retrieval,
            "journey_state": journey_state,
            "search_navigation": search_navigation,
            "read_navigation": read_navigation,
            "read_navigations": list(read_navigations),
            "cognitive_loop_guards": list(
                cognitive_loop_guards
            ),
            "cognitive_step_evaluations": list(
                cognitive_step_evaluations
            ),
        }

    def ask_repository(
        self,
        question: str,
        *,
        session_id: str = "",
        resume_interrupted_turn: bool = False,
        provider_id: str = "",
        model: str = "",
        prompt_name: str = "",
    ) -> Dict[str, Any]:
        settings = self.settings.load()
        prompt = self.prompt_library.resolve(
            prompt_name,
            fallback=question,
        )
        effective_question = question.strip() or prompt

        if session_id:
            session = self.sessions.get(session_id)
            if not session:
                raise ValueError(f"unknown session {session_id}")
        else:
            session = self.sessions.create(
                {
                    "project": self.sessions.root.name,
                    "repository": self.sessions.root.name,
                    "selected_provider": provider_id,
                    "selected_model": model,
                }
            )

        experience, binding = (
            self.conversation_experience.ensure_experience(session)
        )

        session = self.sessions.bind_experience(
            session["id"],
            str(experience.experience_id),
        )

        interrupted_turn = recover_interrupted_human_turn(session)

        if resume_interrupted_turn:
            if interrupted_turn is None:
                raise ValueError(
                    "No interrupted human turn is available for continuation"
                )
            effective_question = interrupted_turn.content
        else:
            effective_question = question.strip() or prompt

            human_sequence = len(
                session.get("raw_sources", [])
            ) + 1

            human_source = self.conversation_experience.raw_source(
                session=session,
                experience=experience,
                actor="HUMAN",
                content=effective_question,
                sequence=human_sequence,
            )

            session = self.sessions.append_raw_source(
                session["id"],
                human_source,
            )

        cognitive_coordination = self.cognitive_coordinator.initialize(
            effective_question,
            session_id=session["id"],
        )

        need_data = cognitive_coordination["information_need"]
        journey_data = cognitive_coordination["journey"]
        navigation_plan_data = cognitive_coordination.get(
            "navigation_plan"
        )

        information_need = InformationNeed(
            schema=need_data["schema"],
            need_id=need_data["need_id"],
            question=need_data["question"],
            objective=need_data["objective"],
            epistemic_status=need_data["epistemic_status"],
            research_required=need_data["research_required"],
            requested_capabilities=tuple(
                need_data["requested_capabilities"]
            ),
            constraints=dict(need_data["constraints"]),
        )

        journey_state = JourneyState(
            schema=journey_data["schema"],
            journey_id=journey_data["journey_id"],
            need_id=journey_data["need_id"],
            status=journey_data["status"],
            step_count=journey_data["step_count"],
            epistemic_gain=journey_data["epistemic_gain"],
            visited=tuple(journey_data["visited"]),
            stopping_reason=journey_data["stopping_reason"],
        )

        search_navigation = None
        retrieval = None

        checkpoint_retrieval = (
            self.evidence_engine
            .find_github_checkpoint(
                effective_question
            )
        )

        if checkpoint_retrieval is not None:
            retrieval = checkpoint_retrieval
            checkpoint_gain = bool(
                retrieval.get("source_paths", ())
            )

            journey_state = JourneyState(
                schema=journey_state.schema,
                journey_id=journey_state.journey_id,
                need_id=journey_state.need_id,
                status=(
                    "PARTIAL"
                    if checkpoint_gain
                    else "UNKNOWN"
                ),
                step_count=journey_state.step_count + 1,
                epistemic_gain=checkpoint_gain,
                visited=(
                    journey_state.visited
                    + ("evidence:github-checkpoint",)
                ),
                stopping_reason=(
                    "CHECKPOINT_EVIDENCE_MATERIALIZED"
                    if checkpoint_gain
                    else "CHECKPOINT_EVIDENCE_UNAVAILABLE"
                ),
            )

            search_navigation = {
                "navigation_plan": navigation_plan_data,
                "journey": journey_state.to_dict(),
                "retrieval": retrieval,
            }

        elif (
            navigation_plan_data is not None
            and navigation_plan_data["required"] is True
            and "search" in navigation_plan_data["capabilities"]
        ):
            navigation_plan = NavigationPlan(
                schema=navigation_plan_data["schema"],
                need_id=navigation_plan_data["need_id"],
                required=navigation_plan_data["required"],
                capabilities=tuple(
                    navigation_plan_data["capabilities"]
                ),
                read_only=navigation_plan_data["read_only"],
                authority_preserved=navigation_plan_data[
                    "authority_preserved"
                ],
                working_context_materialized=(
                    navigation_plan_data[
                        "working_context_materialized"
                    ]
                ),
                retrieval_executed=navigation_plan_data[
                    "retrieval_executed"
                ],
                stopping_conditions=tuple(
                    navigation_plan_data["stopping_conditions"]
                ),
            )

            search_navigation = (
                self.cognitive_coordinator.execute_search_navigation(
                    plan=navigation_plan,
                    journey=journey_state,
                    keyword=effective_question,
                    search=self.evidence_engine.find,
                )
            )

            retrieval = search_navigation.get("retrieval")

            navigation_journey = search_navigation.get("journey")

            if navigation_journey is not None:
                journey_state = JourneyState(
                    schema=navigation_journey["schema"],
                    journey_id=navigation_journey["journey_id"],
                    need_id=navigation_journey["need_id"],
                    status=navigation_journey["status"],
                    step_count=navigation_journey["step_count"],
                    epistemic_gain=navigation_journey[
                        "epistemic_gain"
                    ],
                    visited=tuple(
                        navigation_journey["visited"]
                    ),
                    stopping_reason=navigation_journey[
                        "stopping_reason"
                    ],
                )

        if checkpoint_retrieval is not None:
            read_navigations = list(
                retrieval.get(
                    "read_observations",
                    (),
                )
            )
            read_navigation = (
                read_navigations[0]
                if read_navigations
                else None
            )
            cognitive_loop_guards = []
            cognitive_step_evaluations = []
        else:
            productive_journey = (
                self.activate_productive_bounded_journey(
                    retrieval=retrieval,
                    journey_state=journey_state,
                    search_navigation=search_navigation,
                )
            )

            retrieval = productive_journey["retrieval"]
            journey_state = productive_journey["journey_state"]
            search_navigation = productive_journey[
                "search_navigation"
            ]
            read_navigation = productive_journey[
                "read_navigation"
            ]
            read_navigations = productive_journey[
                "read_navigations"
            ]
            cognitive_loop_guards = productive_journey[
                "cognitive_loop_guards"
            ]
            cognitive_step_evaluations = productive_journey[
                "cognitive_step_evaluations"
            ]

        if checkpoint_retrieval is not None:
            checkpoint_issues = self.checkpoint_integrity_issues(
                checkpoint_retrieval
            )

            if checkpoint_issues:
                persisted_session = self.sessions.get(
                    session["id"]
                )

                if persisted_session:
                    self.sessions.bind_journey(
                        session["id"],
                        journey_state.to_dict(),
                    )
                    self.sessions.mark_journey_interruption(
                        session["id"],
                        reason=(
                            "checkpoint-failure:"
                            + ",".join(checkpoint_issues)
                        ),
                    )

                raise ValueError(
                    "repository checkpoint access is incomplete: "
                    + ", ".join(checkpoint_issues)
                )

        working_context = (
            self.cognitive_coordinator.materialize_working_context(
                need=information_need,
                journey=journey_state,
                retrieval=retrieval,
            )
        )

        working_context_data = working_context.to_dict()

        # Bind the current Journey when the session is owned by the
        # persistent AISessionEngine. Synthetic/test-double sessions may
        # intentionally exist only at the service boundary.
        persisted_session = self.sessions.get(
            session["id"]
        )

        if persisted_session:
            session = self.sessions.bind_journey(
                session["id"],
                journey_state.to_dict(),
            )

        reconstructed_context = self.conversation_context.build(
            session["id"],
            partner_identity={
                "provider": provider_id or session.get(
                    "selected_provider", ""
                ),
                "model": model or session.get(
                    "selected_model", ""
                ),
            },
        )

        provider_cognitive_context = dict(
            reconstructed_context
        )
        provider_cognitive_context[
            "permanent_orientation"
        ] = (
            self.context_builder
            .build_permanent_orientation()
        )
        provider_cognitive_context[
            "working_context"
        ] = working_context_data

        repository_checkpoint = (
            retrieval.get(
                "checkpoint_identity"
            )
            if isinstance(retrieval, Mapping)
            else None
        )

        if repository_checkpoint is not None:
            provider_cognitive_context[
                "repository_checkpoint"
            ] = dict(repository_checkpoint)

        if read_navigation is not None:
            provider_cognitive_context[
                "read_navigation"
            ] = read_navigation

        if read_navigations:
            provider_cognitive_context[
                "read_navigations"
            ] = list(read_navigations)

        if cognitive_loop_guards:
            provider_cognitive_context[
                "cognitive_loop_guards"
            ] = list(cognitive_loop_guards)

        if cognitive_step_evaluations:
            provider_cognitive_context[
                "cognitive_step_evaluations"
            ] = list(
                cognitive_step_evaluations
            )

        _fusion02_log_context_anatomy(
            provider_cognitive_context
        )

        use_cognitive_working_context = getattr(
            self.pipeline,
            "use_cognitive_working_context",
            None,
        )

        if callable(use_cognitive_working_context):
            use_cognitive_working_context(
                working_context
            )

        try:
            result = self.pipeline.run(
                prompt,
                settings,
                provider_id=provider_id,
                model=model,
                context_override=provider_cognitive_context,
            )
        except Exception as exc:
            persisted_session = self.sessions.get(
                session["id"]
            )

            if persisted_session:
                self.sessions.mark_journey_interruption(
                    session["id"],
                    reason=(
                        "provider-failure:"
                        + type(exc).__name__
                    ),
                )

            raise

        access_attestation = None

        if checkpoint_retrieval is not None:
            access_attestation = self.access_attestation(
                retrieval=checkpoint_retrieval,
                working_context=working_context_data,
                pipeline_result=result,
            )

        session = self.sessions.append_interaction(
            session["id"],
            effective_question,
            result["answer"],
            result["usage"],
        )

        ai_sequence = len(
            session.get("raw_sources", [])
        ) + 1

        ai_source = self.conversation_experience.raw_source(
            session=session,
            experience=experience,
            actor="AI",
            content=result["answer"],
            sequence=ai_sequence,
            provider=result["provider"],
            model=result["model"],
            access_attestation=access_attestation,
        )

        session = self.sessions.append_raw_source(
            session["id"],
            ai_source,
        )

        return {
            "session_id": session["id"],
            "experience_id": str(experience.experience_id),
            "question": effective_question,
            "answer": result["answer"],
            "provider": result["provider"],
            "model": result["model"],
            "usage": result["usage"],
            "raw_source_count": len(
                session.get("raw_sources", [])
            ),
            "information_need": cognitive_coordination[
                "information_need"
            ],
            "journey": journey_state.to_dict(),
            "search_navigation": search_navigation,
            "read_navigation": read_navigation,
            "read_navigations": list(
                read_navigations
            ),
            "cognitive_loop_guards": list(
                cognitive_loop_guards
            ),
            "cognitive_step_evaluations": list(
                cognitive_step_evaluations
            ),
            "working_context": working_context_data,
            "repository_checkpoint": repository_checkpoint,
            "full_file_reading": result.get(
                "full_file_reading"
            ),
            "provider_execution": result.get(
                "provider_execution"
            ),
            "runtime_identity": self.runtime_deployment_identity(),
            "access_attestation": access_attestation,
            "context": provider_cognitive_context,
            "context_schema": provider_cognitive_context.get(
                "schema"
            ),
            "epistemic_status": {
                "conversation_is_raw_source": True,
                "conversation_is_evidence": False,
                "conversation_is_canon": False,
                "automatic_sedimentation": False,
                "retrieval_confers_authority": False,
                "human_authority_preserved": True,
                "unknown_is_valid": True,
            },
        }

    def usage_summary(self) -> Dict[str, Any]:
        sessions = self.sessions.list_sessions()
        total = {
            "tokens": 0,
            "estimated_cost": 0.0,
            "latency_ms": 0,
            "requests": 0,
            "success": 0,
            "errors": 0,
        }
        by_provider: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                "tokens": 0,
                "estimated_cost": 0.0,
                "latency_ms": 0,
                "requests": 0,
                "success": 0,
                "errors": 0,
            }
        )
        for session in sessions:
            for usage in session.get("token_usage", []):
                provider = usage.get("provider", "unknown")
                tokens = int(usage.get("input_tokens", 0)) + int(usage.get("output_tokens", 0))
                cost = float(usage.get("estimated_cost", 0.0))
                latency = int(usage.get("latency_ms", 0))
                success = bool(usage.get("success", False))

                total["tokens"] += tokens
                total["estimated_cost"] += cost
                total["latency_ms"] += latency
                total["requests"] += 1
                total["success"] += 1 if success else 0
                total["errors"] += 0 if success else 1

                by_provider[provider]["tokens"] += tokens
                by_provider[provider]["estimated_cost"] += cost
                by_provider[provider]["latency_ms"] += latency
                by_provider[provider]["requests"] += 1
                by_provider[provider]["success"] += 1 if success else 0
                by_provider[provider]["errors"] += 0 if success else 1

        success_rate = (total["success"] / total["requests"] * 100.0) if total["requests"] else 0.0
        avg_latency = (total["latency_ms"] / total["requests"]) if total["requests"] else 0.0
        return {
            "total": {
                **total,
                "estimated_cost": round(total["estimated_cost"], 6),
                "success_rate": round(success_rate, 2),
                "average_latency_ms": round(avg_latency, 2),
            },
            "by_provider": {
                provider: {
                    **stats,
                    "estimated_cost": round(float(stats["estimated_cost"]), 6),
                    "success_rate": round((stats["success"] / stats["requests"] * 100.0) if stats["requests"] else 0.0, 2),
                    "average_latency_ms": round((stats["latency_ms"] / stats["requests"]) if stats["requests"] else 0.0, 2),
                }
                for provider, stats in by_provider.items()
            },
        }

    def control_center(self) -> Dict[str, Any]:
        settings = self.settings.load()
        providers = self.registry.list_providers(settings)
        discovered = self.model_manager.discover_models(providers)
        role_models = self.model_manager.resolve_roles(settings, discovered)
        usage = self.usage_summary()
        return {
            "providers": providers,
            "connections": [
                {
                    "provider": item["id"],
                    "connect": True,
                    "disconnect": True,
                    "test_connection": True,
                    "last_success": item.get("last_success", ""),
                    "last_failure": item.get("last_failure", ""),
                    "last_response_time": item.get("last_response_time", 0),
                    "health_status": item.get("health", "unknown"),
                }
                for item in providers
            ],
            "model_manager": {
                "discovered_models": discovered,
                "role_models": role_models,
            },
            "settings": masked_provider_settings(settings),
            "prompt_library": self.prompt_library.list_categories(),
            "usage": usage,
            "recent_sessions": [
                {
                    "id": item.get("id", ""),
                    "project": item.get("project", ""),
                    "repository": item.get("repository", ""),
                    "branch": item.get("branch", ""),
                    "issue": item.get("issue", ""),
                    "epic": item.get("epic", ""),
                    "sprint": item.get("sprint", ""),
                    "workspace": item.get("workspace", ""),
                    "selected_provider": item.get("selected_provider", ""),
                    "selected_model": item.get("selected_model", ""),
                    "prompt_count": len(item.get("prompt_history", [])),
                    "conversation_count": len(item.get("conversation_history", [])),
                }
                for item in self.sessions.list_sessions()[:10]
            ],
        }
