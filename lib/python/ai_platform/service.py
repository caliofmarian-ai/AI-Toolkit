from __future__ import annotations
import json
import logging

from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Union

from .adapters import builtin_adapters
from .attachments import AttachmentStore
from .chat_models import (
    ChatMessage,
    ChatSession,
    ChatThread,
    PermissionOp,
    ProviderConnectionState,
)
from .context_builder import AIContextBuilder
from .context_csl import ContextCSLExporter
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
from .model_manager import ModelManager
from .pipeline import AIRequestPipeline
from .permissions import PermissionManager
from .prompt_library import PromptLibrary
from .provider_registry import ProviderRegistry as ChatProviderRegistry
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
        self.chat_provider_registry = ChatProviderRegistry()
        self.model_manager = ModelManager()
        self.context_builder = AIContextBuilder(repository_root, workspace_root)
        self.sessions = AISessionEngine(repository_root)
        self.attachments = AttachmentStore(repository_root=repository_root)
        self.permission_manager = PermissionManager()
        self.context_exporter = ContextCSLExporter()
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

                retrieval = (
                    self.cognitive_coordinator.attach_read_evidence(
                        retrieval=retrieval,
                        read_navigation=read_navigation,
                    )
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
            "working_context"
        ] = working_context_data

        if read_navigation is not None:
            provider_cognitive_context[
                "read_navigation"
            ] = read_navigation

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

    def _chat_store_root(self) -> Path:
        root = self.sessions.root / ".ai" / "chat"
        root.mkdir(parents=True, exist_ok=True)
        return root

    def _read_json_record(self, directory: Path, record_id: str) -> Optional[Dict[str, Any]]:
        if not record_id:
            return None
        path = directory / f"{record_id}.json"
        if not path.exists():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        return payload if isinstance(payload, dict) else None

    def _write_json_record(self, directory: Path, record: Mapping[str, Any]) -> Dict[str, Any]:
        directory.mkdir(parents=True, exist_ok=True)
        record_id = str(record.get("id") or "").strip()
        if not record_id:
            raise ValueError("record id is required")
        path = directory / f"{record_id}.json"
        path.write_text(json.dumps(dict(record), indent=2, sort_keys=True), encoding="utf-8")
        return dict(record)

    def _sync_chat_session_to_ai_session_engine(self, session: ChatSession) -> Dict[str, Any]:
        metadata = dict(session.metadata or {})
        engine_payload = {
            "id": session.id,
            "project": metadata.get("project") or self.sessions.root.name,
            "repository": metadata.get("repo") or metadata.get("repository") or self.sessions.root.name,
            "branch": metadata.get("branch") or "",
            "issue": metadata.get("issue") or "",
            "epic": metadata.get("epic") or "",
            "sprint": metadata.get("sprint") or "",
            "workspace": metadata.get("workspace") or str(self.sessions.root),
            "selected_provider": session.provider_id or "",
            "selected_model": metadata.get("model_id") or "",
            "engineering_context": {
                "chat_session_id": session.id,
                "chat_metadata": metadata,
            },
        }
        return self.sessions.create(engine_payload)

    def _require_chat_permission(
        self,
        *,
        user: str,
        operation: PermissionOp,
        session_id: str,
        provider_id: Optional[str] = None,
    ) -> None:
        if not self.check_permission(
            user=user,
            operation=operation.value,
            session=session_id,
            provider=provider_id,
        ):
            raise PermissionError(
                f"'{user}' is not permitted to {operation.value} for chat session "
                f"'{session_id}'"
            )

    def _require_connected_chat_provider(
        self,
        *,
        user: str,
        session_id: str,
        provider_id: Optional[str],
    ) -> None:
        if not provider_id:
            return
        provider = self.chat_provider_registry.get_provider(provider_id)
        if provider is None:
            raise ValueError(f"unknown chat provider '{provider_id}'")
        if provider.state is not ProviderConnectionState.CONNECTED:
            raise ValueError(f"chat provider '{provider_id}' is not connected")
        self._require_chat_permission(
            user=user,
            operation=PermissionOp.USE_PROVIDER,
            session_id=session_id,
            provider_id=provider_id,
        )

    def create_chat_session(self, payload: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        session_payload = dict(payload or {})
        metadata = dict(session_payload.get("metadata") or {})
        metadata.setdefault("repo", session_payload.get("repo") or self.sessions.root.name)
        metadata.setdefault("branch", session_payload.get("branch") or "")
        metadata.setdefault("workspace", session_payload.get("workspace") or str(self.sessions.root))
        session_payload["metadata"] = metadata
        session = ChatSession.from_dict(session_payload)
        self._require_connected_chat_provider(
            user=session.owner,
            session_id=session.id,
            provider_id=session.provider_id,
        )
        self.context_exporter.register_session(session)
        self._write_json_record(self._chat_store_root() / "sessions", session.to_dict())
        self._sync_chat_session_to_ai_session_engine(session)
        thread = self.create_chat_thread(session.id, payload={"messages": []})
        session.active_thread_id = thread["id"]
        session.metadata.setdefault("active_thread_id", thread["id"])
        self._write_json_record(self._chat_store_root() / "sessions", session.to_dict())
        return session.to_dict()

    def update_chat_session(self, session_id: str, *, changes: Mapping[str, Any]) -> Optional[Dict[str, Any]]:
        current = self.get_chat_session(session_id)
        if current is None:
            return None
        updated = dict(current)
        metadata = dict(updated.get("metadata") or {})
        for key, value in dict(changes).items():
            if key == "metadata":
                metadata.update(dict(value or {}))
            elif key == "provider_id":
                updated["provider_id"] = value
            elif key == "active_thread_id":
                updated["active_thread_id"] = value
            elif key == "owner":
                updated["owner"] = value
            else:
                updated[key] = value
        updated["metadata"] = metadata
        session = ChatSession.from_dict(updated)
        self._require_connected_chat_provider(
            user=session.owner,
            session_id=session.id,
            provider_id=session.provider_id,
        )
        self.context_exporter.register_session(session)
        self._write_json_record(self._chat_store_root() / "sessions", session.to_dict())
        self._sync_chat_session_to_ai_session_engine(session)
        return session.to_dict()

    def delete_chat_session(self, session_id: str) -> bool:
        root = self._chat_store_root() / "sessions"
        path = root / f"{session_id}.json"
        if not path.exists():
            return False
        path.unlink(missing_ok=True)
        return True

    def list_chat_sessions(self) -> list[Dict[str, Any]]:
        root = self._chat_store_root() / "sessions"
        if not root.exists():
            return []
        sessions: list[Dict[str, Any]] = []
        for path in sorted(root.glob("*.json")):
            payload = self._read_json_record(root, path.stem)
            if payload:
                sessions.append(payload)
        return sessions

    def get_chat_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._read_json_record(self._chat_store_root() / "sessions", session_id)

    def ensure_chat_session(self, payload: Mapping[str, Any]) -> ChatSession:
        session = ChatSession.from_dict(dict(payload))
        self.context_exporter.register_session(session)
        self._write_json_record(self._chat_store_root() / "sessions", session.to_dict())
        return session

    def create_chat_thread(self, session_id: str, *, payload: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        session = self.get_chat_session(session_id)
        if session is None:
            session = self.ensure_chat_session({"id": session_id, "metadata": {}}).to_dict()
        thread_payload = dict(payload or {})
        thread_payload.setdefault("session_id", session_id)
        thread = ChatThread.from_dict(thread_payload)
        self._write_json_record(self._chat_store_root() / "threads", thread.to_dict())
        return thread.to_dict()

    def list_chat_threads(self, session_id: Optional[str] = None) -> list[Dict[str, Any]]:
        root = self._chat_store_root() / "threads"
        if not root.exists():
            return []
        threads: list[Dict[str, Any]] = []
        for path in sorted(root.glob("*.json")):
            payload = self._read_json_record(root, path.stem)
            if not payload:
                continue
            if session_id and payload.get("session_id") != session_id:
                continue
            threads.append(payload)
        return threads

    def get_chat_thread(self, thread_id: str) -> Optional[Dict[str, Any]]:
        return self._read_json_record(self._chat_store_root() / "threads", thread_id)

    def update_chat_thread(self, thread_id: str, *, changes: Mapping[str, Any]) -> Optional[Dict[str, Any]]:
        current = self.get_chat_thread(thread_id)
        if current is None:
            return None
        updated = dict(current)
        for key, value in dict(changes).items():
            updated[key] = value
        thread = ChatThread.from_dict(updated)
        self._write_json_record(self._chat_store_root() / "threads", thread.to_dict())
        return thread.to_dict()

    def delete_chat_thread(self, thread_id: str) -> bool:
        root = self._chat_store_root() / "threads"
        path = root / f"{thread_id}.json"
        if not path.exists():
            return False
        path.unlink(missing_ok=True)
        return True

    def create_chat_message(
        self,
        *,
        thread_id: str,
        author: str,
        content: str,
        attachments: Optional[list[str]] = None,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        thread = self.get_chat_thread(thread_id)
        if thread is None:
            raise ValueError(f"unknown chat thread '{thread_id}'")
        session = self.get_chat_session(str(thread.get("session_id") or ""))
        if session is None:
            raise ValueError(f"unknown chat session for thread '{thread_id}'")
        self._require_chat_permission(
            user=str(session.get("owner") or "owner"),
            operation=PermissionOp.SEND_MESSAGE,
            session_id=str(session["id"]),
            provider_id=session.get("provider_id"),
        )
        message = ChatMessage(
            id="",
            thread_id=thread_id,
            author=str(author or "user"),
            content=str(content),
            attachments=list(attachments or []),
            metadata=dict(metadata or {}),
        )
        self._write_json_record(self._chat_store_root() / "messages", message.to_dict())
        thread["messages"] = list(thread.get("messages") or []) + [message.id]
        self._write_json_record(self._chat_store_root() / "threads", thread)
        return message.to_dict()

    def list_chat_messages(self, thread_id: Optional[str] = None) -> list[Dict[str, Any]]:
        root = self._chat_store_root() / "messages"
        if not root.exists():
            return []
        messages: list[Dict[str, Any]] = []
        for path in sorted(root.glob("*.json")):
            payload = self._read_json_record(root, path.stem)
            if not payload:
                continue
            if thread_id and payload.get("thread_id") != thread_id:
                continue
            messages.append(payload)
        return messages

    def get_chat_message(self, message_id: str) -> Optional[Dict[str, Any]]:
        return self._read_json_record(self._chat_store_root() / "messages", message_id)

    def update_chat_message(self, message_id: str, *, changes: Mapping[str, Any]) -> Optional[Dict[str, Any]]:
        current = self.get_chat_message(message_id)
        if current is None:
            return None
        updated = dict(current)
        for key, value in dict(changes).items():
            updated[key] = value
        message = ChatMessage.from_dict(updated)
        self._write_json_record(self._chat_store_root() / "messages", message.to_dict())
        return message.to_dict()

    def delete_chat_message(self, message_id: str) -> bool:
        root = self._chat_store_root() / "messages"
        path = root / f"{message_id}.json"
        if not path.exists():
            return False
        path.unlink(missing_ok=True)
        return True

    def add_attachment(
        self,
        *,
        session_id: str,
        original_name: str,
        content: Any,
        mime_type: str = "application/octet-stream",
        linked_thread_id: Optional[str] = None,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        session = self.get_chat_session(session_id)
        if session is None:
            raise ValueError(f"unknown chat session '{session_id}'")
        self._require_chat_permission(
            user=str(session.get("owner") or "owner"),
            operation=PermissionOp.ATTACH_FILE,
            session_id=session_id,
            provider_id=session.get("provider_id"),
        )
        attachment = self.attachments.add_attachment(
            session_id=session_id,
            original_name=original_name,
            content=content,
            mime_type=mime_type,
            linked_thread_id=linked_thread_id,
            metadata=dict(metadata or {}),
        )
        return attachment.to_dict()

    def check_permission(
        self,
        *,
        user: Optional[str] = None,
        operation: str,
        session: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> bool:
        return self.permission_manager.is_allowed(
            user=user,
            op=operation,
            session=session,
            provider=provider,
        )

    def export_session_context(self, session: Union[Mapping[str, Any], ChatSession], **kwargs: Any) -> Dict[str, Any]:
        return self.context_exporter.export_csl(session, **kwargs)

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
