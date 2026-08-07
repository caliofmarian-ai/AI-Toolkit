from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Optional


DEFAULT_MODEL_ROLES = {
    "default_model": "",
    "engineering_model": "",
    "planning_model": "",
    "coding_model": "",
    "review_model": "",
    "validation_model": "",
    "documentation_model": "",
    "executive_briefing_model": "",
    "translation_model": "",
}


class AISettingsStore:
    def __init__(self, repository_root: str = ".") -> None:
        self.root = Path(repository_root).resolve()
        self.dir = self.root / ".ai" / "platform"
        self.path = self.dir / "ai_settings.json"

    def load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return self._default()
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                return self._default()
        except (OSError, json.JSONDecodeError):
            return self._default()
        merged = self._default()
        merged.update(payload)
        merged["model_configuration"] = {**DEFAULT_MODEL_ROLES, **dict(payload.get("model_configuration", {}))}
        return merged

    def save(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        current = self._default()
        current.update(dict(payload))
        current["model_configuration"] = {**DEFAULT_MODEL_ROLES, **dict(current.get("model_configuration", {}))}
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(current, indent=2), encoding="utf-8")
        return current

    def configure_provider(
        self,
        provider_id: str,
        *,
        api_key: str = "",
        api_key_env: str = "",
        base_url: str = "",
        timeout_seconds: Optional[int] = None,
        retries: Optional[int] = None,
        rate_limit_per_minute: Optional[int] = None,
    ) -> Dict[str, Any]:
        settings = self.load()
        providers = dict(settings.get("providers", {}))
        provider = dict(providers.get(provider_id, {}))
        if api_key:
            provider["api_key_mask"] = self._mask_secret(api_key)
            provider["api_key_fingerprint"] = self._fingerprint(api_key)
        if api_key_env:
            provider["api_key_env"] = api_key_env
        if base_url:
            provider["base_url"] = base_url
        if timeout_seconds is not None:
            provider["timeout_seconds"] = max(int(timeout_seconds), 1)
        if retries is not None:
            provider["retries"] = max(int(retries), 0)
        if rate_limit_per_minute is not None:
            provider["rate_limit_per_minute"] = max(int(rate_limit_per_minute), 1)
        providers[provider_id] = provider
        settings["providers"] = providers
        return self.save(settings)

    def configure_models(self, roles: Mapping[str, str]) -> Dict[str, Any]:
        settings = self.load()
        model_configuration = dict(settings.get("model_configuration", {}))
        for role, model in roles.items():
            if role in DEFAULT_MODEL_ROLES:
                model_configuration[role] = str(model)
        settings["model_configuration"] = model_configuration
        return self.save(settings)

    def configure_routing(
        self,
        *,
        default_provider: Optional[str] = None,
        fallback_provider: Optional[str] = None,
    ) -> Dict[str, Any]:
        settings = self.load()
        if default_provider is not None:
            settings["default_provider"] = default_provider
        if fallback_provider is not None:
            settings["fallback_provider"] = fallback_provider
        return self.save(settings)

    def _default(self) -> Dict[str, Any]:
        return {
            "providers": {},
            "model_configuration": dict(DEFAULT_MODEL_ROLES),
            "default_provider": "",
            "fallback_provider": "",
            "timeouts": {"request_seconds": 60},
            "retries": {"max_retries": 2},
            "rate_limits": {"requests_per_minute": 60},
        }

    def _mask_secret(self, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            return ""
        if len(stripped) <= 4:
            return "*" * len(stripped)
        return f"{'*' * (len(stripped) - 4)}{stripped[-4:]}"

    def _fingerprint(self, value: str) -> str:
        salt = str(self.root).encode("utf-8")
        digest = hashlib.pbkdf2_hmac("sha256", value.encode("utf-8"), salt, 120_000)
        return digest.hex()


def masked_provider_settings(settings: Mapping[str, Any]) -> Dict[str, Any]:
    providers = {}
    for provider_id, provider in dict(settings.get("providers", {})).items():
        provider_payload = dict(provider)
        provider_payload.pop("api_key_fingerprint", None)
        providers[provider_id] = provider_payload
    return {
        **dict(settings),
        "providers": providers,
    }
