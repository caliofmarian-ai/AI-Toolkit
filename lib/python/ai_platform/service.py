from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, Mapping, Optional

from .adapters import builtin_adapters
from .context_builder import AIContextBuilder
from .model_manager import ModelManager
from .pipeline import AIRequestPipeline
from .prompt_library import PromptLibrary
from .registry import ProviderRegistry
from .sessions import AISessionEngine
from .settings import AISettingsStore, masked_provider_settings


class AIPlatformService:
    def __init__(self, repository_root: str = ".", workspace_root: Optional[str] = None) -> None:
        self.settings = AISettingsStore(repository_root)
        self.registry = ProviderRegistry()
        self.model_manager = ModelManager()
        self.context_builder = AIContextBuilder(repository_root, workspace_root)
        self.sessions = AISessionEngine(repository_root)
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

    def ask_repository(self, question: str, *, session_id: str = "", provider_id: str = "", model: str = "", prompt_name: str = "") -> Dict[str, Any]:
        settings = self.settings.load()
        prompt = self.prompt_library.resolve(prompt_name, fallback=question)
        result = self.pipeline.run(prompt, settings, provider_id=provider_id, model=model)
        if session_id:
            session = self.sessions.append_interaction(session_id, question, result["answer"], result["usage"])
        else:
            context = result["context"]
            session = self.sessions.create(
                {
                    "project": context.get("engineering_session", {}).get("workspace_state", {}).get("active_project", ""),
                    "repository": context.get("repository_profile", {}).get("name", ""),
                    "branch": context.get("current_branch", ""),
                    "issue": context.get("current_issue", ""),
                    "epic": context.get("current_epic", ""),
                    "sprint": context.get("current_sprint", ""),
                    "workspace": context.get("workspace", {}).get("workspace", ""),
                    "repository_profile": context.get("repository_profile", {}),
                    "engineering_context": context,
                    "selected_provider": result["provider"],
                    "selected_model": result["model"],
                }
            )
            session = self.sessions.append_interaction(session["id"], question, result["answer"], result["usage"])
        return {
            "session_id": session["id"],
            "question": question,
            "answer": result["answer"],
            "provider": result["provider"],
            "model": result["model"],
            "usage": result["usage"],
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
