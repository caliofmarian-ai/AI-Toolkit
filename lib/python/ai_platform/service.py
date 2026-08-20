from __future__ import annotations
import logging

from collections import defaultdict
from typing import Any, Dict, Mapping, Optional

from .adapters import builtin_adapters
from .context_builder import AIContextBuilder
from .conversation_experience import ConversationExperienceBridge
from .conversation_context import ConversationContextReconstructor
from .cognitive_coordination import (
    EpistemicCognitiveCoordinator,
    InformationNeed,
    JourneyState,
    NavigationPlan,
)
from python.evidence_engine.engine import EvidenceEngine
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
    def __init__(self, repository_root: str = ".", workspace_root: Optional[str] = None) -> None:
        self.settings = AISettingsStore(repository_root)
        self.registry = ProviderRegistry()
        self.model_manager = ModelManager()
        self.context_builder = AIContextBuilder(repository_root, workspace_root)
        self.sessions = AISessionEngine(repository_root)
        self.conversation_experience = ConversationExperienceBridge(repository_root)
        self.conversation_context = ConversationContextReconstructor(
            repository_root,
            workspace_root,
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

    def ask_repository(
        self,
        question: str,
        *,
        session_id: str = "",
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

        if (
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

        working_context = (
            self.cognitive_coordinator.materialize_working_context(
                need=information_need,
                journey=journey_state,
                retrieval=retrieval,
            )
        )

        working_context_data = working_context.to_dict()

        read_navigation = None

        if isinstance(retrieval, dict):
            source_paths = retrieval.get(
                "source_paths",
                (),
            )

            if source_paths:
                selected_source_path = source_paths[0]

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

                read_navigation = (
                    self.cognitive_coordinator.execute_read_navigation(
                        selected_source_path,
                        read=_bounded_repository_read,
                        repository_root=self.sessions.root,
                    )
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
            "working_context"
        ] = working_context_data

        if read_navigation is not None:
            provider_cognitive_context[
                "read_navigation"
            ] = read_navigation

        _fusion02_log_context_anatomy(
            provider_cognitive_context
        )

        observe_working_context = getattr(
            self.pipeline,
            "observe_working_context",
            None,
        )

        if callable(observe_working_context):
            observe_working_context(
                working_context
            )

        result = self.pipeline.run(
            prompt,
            settings,
            provider_id=provider_id,
            model=model,
            context_override=provider_cognitive_context,
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
            "working_context": working_context_data,
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
