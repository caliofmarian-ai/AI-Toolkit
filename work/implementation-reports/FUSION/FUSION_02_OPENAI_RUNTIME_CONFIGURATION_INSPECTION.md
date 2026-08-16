# FUSION-02 — OpenAI Runtime Configuration Inspection

- Inspection type: READ ONLY
- Repository: `https://github.com/caliofmarian-ai/AI-Toolkit.git`
- Branch: `main`
- HEAD: `33871097ab2192254d7893a0392e7d2a907e4ec5`
- Timestamp UTC: `2026-08-16T14:20:09Z`

## Purpose

Determine the exact environment/configuration contract used by the existing OpenAI integration before changing Railway variables.

## Raw secret-safe inspection

```text
==========================================================
FUSION-02 — OPENAI RUNTIME CONFIGURATION INSPECTION
Human Authority — READ ONLY
==========================================================

PURPOSE:
Determine the exact OpenAI configuration contract implemented
by AI-Toolkit before adding any further Railway variables.

READ ONLY:
  NO production modification
  NO Canon modification
  NO tests
  NO commit
  NO push
  NO reset
  NO cleanup of preserved runtime state
  NO secret values printed

==========================================================
[1/8] REPOSITORY STATE
==========================================================
Repository: https://github.com/caliofmarian-ai/AI-Toolkit.git
Branch: main
HEAD: 33871097ab2192254d7893a0392e7d2a907e4ec5

Worktree (classification only):

==========================================================
[2/8] INVENTORY ENVIRONMENT-VARIABLE REFERENCES
==========================================================
Relevant references found:
lib/python/cli/main.py:882:    host = getattr(args, "host", os.environ.get("HOST", "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"))
lib/python/cli/main.py:883:    port = getattr(args, "port", int(os.environ.get("PORT", "8081")))
lib/python/runtime/bootstrap.py:93:        self.repository_root = os.environ.get("AI_TOOLKIT_REPOSITORY_ROOT", os.getcwd())
lib/python/runtime/bootstrap.py:94:        self.workspace_root = os.environ.get(
lib/python/runtime/bootstrap.py:195:        log_level = os.environ.get("LOG_LEVEL", "INFO")
lib/python/runtime/bootstrap.py:196:        json_logs = os.environ.get("JSON_LOGS", "true").lower() != "false"
lib/python/runtime/bootstrap.py:437:            os.environ.get(
lib/python/runtime/config.py:56:            runtime_mode=os.environ.get("RUNTIME_MODE", "NORMAL").upper(),
lib/python/runtime/config.py:57:            http_host=os.environ.get("RUNTIME_HTTP_HOST", "0.0.0.0"),
lib/python/runtime/config.py:58:            http_port=int(os.environ.get("PORT", os.environ.get("RUNTIME_HTTP_PORT", "8080"))),
lib/python/runtime/config.py:59:            environment=os.environ.get("RAILWAY_ENVIRONMENT", os.environ.get("ENVIRONMENT", "production")),
lib/python/runtime/config.py:60:            github_webhook_secret=os.environ.get("GITHUB_WEBHOOK_SECRET", ""),
lib/python/runtime/config.py:61:            github_token=os.environ.get("GITHUB_TOKEN", ""),
lib/python/runtime/config.py:62:            telegram_bot_token=os.environ.get("TELEGRAM_BOT_TOKEN", ""),
lib/python/runtime/config.py:63:            telegram_chat_id=os.environ.get("TELEGRAM_CHAT_ID", ""),
lib/python/runtime/config.py:64:            scheduler_interval_seconds=int(os.environ.get("SCHEDULER_INTERVAL_SECONDS", "60")),
lib/python/runtime/config.py:65:            runtime_loop_interval_seconds=int(os.environ.get("RUNTIME_LOOP_INTERVAL_SECONDS", "30")),
lib/python/runtime/config.py:66:            state_dir=os.environ.get("RUNTIME_STATE_DIR", ".ai/runtime/state"),
lib/python/runtime/config.py:67:            logs_dir=os.environ.get("RUNTIME_LOGS_DIR", ".ai/runtime/logs"),
lib/python/runtime/config.py:68:            checkpoints_dir=os.environ.get("RUNTIME_CHECKPOINTS_DIR", ".ai/runtime/checkpoints"),
lib/python/runtime/config.py:69:            sessions_dir=os.environ.get("RUNTIME_SESSIONS_DIR", ".ai/runtime/sessions"),
lib/python/runtime/config.py:70:            cache_dir=os.environ.get("RUNTIME_CACHE_DIR", ".ai/runtime/cache"),
lib/python/runtime/config.py:71:            max_recovery_attempts=int(os.environ.get("MAX_RECOVERY_ATTEMPTS", "3")),
lib/python/runtime/identity.py:34:        runtime_id = os.environ.get("RUNTIME_ID") or f"runtime-{uuid.uuid4().hex[:12]}"
lib/python/runtime/identity.py:37:            runtime_version=os.environ.get("RUNTIME_VERSION", "3.0.0"),
lib/python/runtime/identity.py:38:            build_version=os.environ.get("BUILD_VERSION", "unknown"),
lib/python/runtime/identity.py:39:            git_commit=os.environ.get("RAILWAY_GIT_COMMIT_SHA", "unknown"),
lib/python/runtime/identity.py:40:            deployment_id=os.environ.get("RAILWAY_DEPLOYMENT_ID", "local"),
lib/python/runtime/identity.py:41:            railway_deployment_id=os.environ.get("RAILWAY_DEPLOYMENT_ID", "local"),
lib/python/runtime/identity.py:42:            workspace_id=os.environ.get("WORKSPACE_ID", "default"),
lib/python/runtime/identity.py:43:            repository_id=os.environ.get("REPOSITORY_ID", "ai-toolkit"),
lib/python/runtime/interfaces/api_auth.py:9:        self.api_key = os.getenv("RUNTIME_API_KEY", "")
lib/python/runtime/interfaces/api_auth.py:10:        self.bearer [REDACTED] os.getenv("RUNTIME_BEARER_TOKEN", "")
lib/python/runtime/railway.py:53:        project_id=os.environ.get("RAILWAY_PROJECT_ID", "local"),
lib/python/runtime/railway.py:54:        service_id=os.environ.get("RAILWAY_SERVICE_ID", "local"),
lib/python/runtime/railway.py:55:        deployment_id=os.environ.get("RAILWAY_DEPLOYMENT_ID", "local"),
lib/python/runtime/railway.py:56:        environment=os.environ.get("RAILWAY_ENVIRONMENT", "production"),
lib/python/runtime/railway.py:57:        git_commit_sha=os.environ.get("RAILWAY_GIT_COMMIT_SHA", "unknown"),
lib/python/runtime/railway.py:58:        git_branch=os.environ.get("RAILWAY_GIT_BRANCH", "unknown"),
lib/python/runtime/railway.py:59:        public_domain=os.environ.get("RAILWAY_PUBLIC_DOMAIN", ""),
lib/python/runtime/railway.py:60:        private_domain=os.environ.get("RAILWAY_PRIVATE_DOMAIN", ""),
lib/python/runtime/railway.py:61:        port=int(os.environ.get("PORT", "8080")),
lib/python/runtime/railway.py:100:        return bool(os.environ.get("RAILWAY_ENVIRONMENT"))
lib/python/runtime/secrets.py:44:            value = os.environ.get(key, "")
lib/python/runtime/secrets.py:51:        return self._secrets.get(key, os.environ.get(key, default))
lib/python/runtime/diagnostics.py:199:            ("ANTHROPIC_API_KEY", "Anthropic"),
lib/python/runtime/diagnostics.py:200:            ("OPENAI_API_KEY", "OpenAI"),
lib/python/runtime/diagnostics.py:201:            ("GEMINI_API_KEY", "Gemini"),
lib/python/runtime/diagnostics.py:202:            ("GOOGLE_API_KEY", "Google"),
lib/python/runtime/diagnostics.py:203:            ("MISTRAL_API_KEY", "Mistral"),
lib/python/runtime/diagnostics.py:205:            if os.environ.get(env_name):
lib/python/runtime/owner_access.py:30:OWNER_TOKEN_ENV = "AI_TOOLKIT_OWNER_TOKEN"
lib/python/runtime/owner_access.py:60:        configured = token if token is not None else os.environ.get(
lib/python/runtime/owner_access.py:61:            OWNER_TOKEN_ENV, ""
lib/python/ai_platform/adapters.py:39:        if env_name and os.environ.get(env_name):
lib/python/ai_platform/adapters.py:41:        return any(os.environ.get(name) for name in self.descriptor.env_vars)
lib/python/ai_platform/adapters.py:131:            credential = os.environ.get(env_name, "").strip()
lib/python/ai_platform/adapters.py:398:            env_vars=["OPENAI_API_KEY"],
lib/python/ai_platform/adapters.py:407:            env_vars=["ANTHROPIC_API_KEY"],
lib/python/ai_platform/adapters.py:416:            env_vars=["GEMINI_API_KEY", "GOOGLE_API_KEY"],
lib/python/ai_platform/adapters.py:443:            env_vars=["AZURE_OPENAI_API_KEY"],
lib/python/ai_platform/adapters.py:452:            env_vars=["OPENROUTER_API_KEY"],
lib/python/ai_platform/adapters.py:461:            env_vars=["CUSTOM_AI_API_KEY"],
lib/python/dashboard/service.py:838:                "port": int(os.environ.get("PORT", "8081")),
lib/python/dashboard/service.py:839:                "environment": os.environ.get("RAILWAY_ENVIRONMENT", os.environ.get("ENVIRONMENT", "local")),
lib/python/dashboard/service.py:856:                    "http_port": int(os.environ.get("PORT", "8081")),
lib/python/dashboard/service.py:857:                    "environment": os.environ.get("ENVIRONMENT", "local"),
lib/python/dashboard/service.py:1217:                ("ANTHROPIC_API_KEY", "Anthropic"),
lib/python/dashboard/service.py:1218:                ("OPENAI_API_KEY", "OpenAI"),
lib/python/dashboard/service.py:1219:                ("GEMINI_API_KEY", "Gemini"),
lib/python/dashboard/service.py:1220:                ("GOOGLE_API_KEY", "Google"),
lib/python/dashboard/service.py:1221:                ("MISTRAL_API_KEY", "Mistral"),
lib/python/dashboard/service.py:1223:                if os.environ.get(env_name):
lib/python/experience/deployment.py:43:    env = os.environ if environment is None else environment
bin/ai:53:    parser.add_argument("--host", default=os.environ.get("HOST", "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"))
bin/ai:54:    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8081")))
tests/experience/test_experience_real_process_restart.py:30:    env = os.environ.copy()
tests/experience/test_experience_protection_restart.py:30:    env = os.environ.copy()
tests/test_executable_repository_intelligence.sh:543:        env={**os.environ, 'PYTHONPATH': os.path.join(os.getcwd(), 'lib')},
tests/test_context_synchronization_engine.sh:118:    env = dict(os.environ)
tests/test_context_synchronization_engine.sh:255:            env={**os.environ, "PYTHONPATH": "lib"},
tests/test_railway_bootstrap.sh:13:os.environ["RAILWAY_PROJECT_ID"] = "test-project"
tests/test_railway_bootstrap.sh:14:os.environ["RAILWAY_SERVICE_ID"] = "test-service"
tests/test_railway_bootstrap.sh:15:os.environ["RAILWAY_DEPLOYMENT_ID"] = "test-deployment"
tests/test_railway_bootstrap.sh:16:os.environ["RAILWAY_ENVIRONMENT"] = "testing"
tests/test_railway_bootstrap.sh:17:os.environ["PORT"] = "9080"
tests/test_railway_bootstrap.sh:35:del os.environ["RAILWAY_ENVIRONMENT"]
tests/test_runtime_acceptance.sh:13:os.environ["RUNTIME_LOOP_INTERVAL_SECONDS"] = "300"
tests/test_runtime_acceptance.sh:14:os.environ["SCHEDULER_INTERVAL_SECONDS"] = "300"
tests/test_runtime_acceptance.sh:15:os.environ["RUNTIME_HTTP_PORT"] = "19100"
tests/test_runtime_acceptance.sh:16:os.environ["JSON_LOGS"] = "false"
tests/test_runtime_acceptance.sh:48:os.environ["RUNTIME_HTTP_PORT"] = "19101"
tests/test_runtime_bootstrap.sh:9:os.environ["RUNTIME_LOOP_INTERVAL_SECONDS"] = "300"
tests/test_runtime_bootstrap.sh:10:os.environ["SCHEDULER_INTERVAL_SECONDS"] = "300"
tests/test_runtime_bootstrap.sh:11:os.environ["RUNTIME_HTTP_PORT"] = "19001"
tests/test_runtime_bootstrap.sh:12:os.environ["JSON_LOGS"] = "false"
tests/test_runtime_shutdown.sh:10:os.environ["JSON_LOGS"] = "false"
tests/fusion/test_fusion_02_real_provider.py:24:        env_vars=["OPENAI_API_KEY"],
tests/fusion/test_fusion_02_real_provider.py:113:    monkeypatch.setenv("OPENAI_API_KEY", "test-secret-not-real")
tests/fusion/test_fusion_02_real_provider.py:236:    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
tests/fusion/test_fusion_02_real_provider.py:259:        "OPENAI_API_KEY",
tests/fusion/test_fusion_02_real_provider.py:290:        "OPENAI_API_KEY",
tests/fusion/test_fusion_02_real_provider.py:353:        "OPENAI_API_KEY",
tests/fusion/test_fusion_02_real_provider.py:505:    assert os.environ.get("OPENAI_API_KEY") != "test-secret-not-real"
tests/fusion/test_fusion_02_owner_chat_ui.py:14:        "AI_TOOLKIT_OWNER_TOKEN",
tests/fusion/test_fusion_02_owner_chat_ui.py:27:        "AI_TOOLKIT_OWNER_TOKEN",
tests/fusion/test_fusion_02_owner_chat_ui.py:47:        "AI_TOOLKIT_OWNER_TOKEN",
tests/fusion/test_fusion_02_owner_chat_ui.py:66:        "AI_TOOLKIT_OWNER_TOKEN",
tests/fusion/test_fusion_02_owner_chat_ui.py:120:        "AI_TOOLKIT_OWNER_TOKEN",
tests/fusion/test_fusion_02_owner_chat_ui.py:143:    assert "AI_TOOLKIT_OWNER_TOKEN" not in html
tests/test_runtime_dashboard_navigation.sh:17:os.environ["RUNTIME_LOOP_INTERVAL_SECONDS"] = "300"
tests/test_runtime_dashboard_navigation.sh:18:os.environ["SCHEDULER_INTERVAL_SECONDS"] = "300"
tests/test_runtime_dashboard_navigation.sh:19:os.environ["RUNTIME_HTTP_PORT"] = "19121"
tests/test_runtime_dashboard_navigation.sh:20:os.environ["JSON_LOGS"] = "false"
work/audits/REPOSITORY_TAKEOVER_AUDIT_2026-08-11.md:357:**Bug:** `api_auth.py` line ~22: `if self.bearer [REDACTED] auth == f"******":` — the bearer [REDACTED] comparison is a literal `"******"` string, not the actual token. Auth is permanently broken when `RUNTIME_BEARER_TOKEN` is set.
work/audits/REPOSITORY_TAKEOVER_AUDIT_2026-08-11.md:487:- `RUNTIME_API_KEY` — API authentication
work/audits/REPOSITORY_TAKEOVER_AUDIT_2026-08-11.md:488:- `RUNTIME_BEARER_TOKEN` — ****** (currently broken in code)
work/audits/REPOSITORY_TAKEOVER_AUDIT_2026-08-11.md:630:- `RUNTIME_API_KEY` / `RUNTIME_BEARER_TOKEN` — API authentication (bearer [REDACTED] is broken)
work/audits/REPOSITORY_TAKEOVER_AUDIT_2026-08-11.md:992:| `RUNTIME_API_KEY` | `/api/v1/*` auth | API key auth works; bearer [REDACTED] is broken |
work/audits/REPOSITORY_TAKEOVER_AUDIT_2026-08-11.md:993:| `RUNTIME_BEARER_TOKEN` | `/api/v1/*` auth | **BROKEN** — never validates due to `f"******"` bug |
work/implementation-reports/PCC-01/PCC-01_EXPERIENCE_PROTECTION_PERSISTENCE_COORDINATION_INSPECTION_RUN_027.md:1196:lib/python/runtime/config.py:68:            checkpoints_dir=os.environ.get("RUNTIME_CHECKPOINTS_DIR", ".ai/runtime/checkpoints"),
work/implementation-reports/PCC-01/PCC-01_EXPERIENCE_PROTECTION_PERSISTENCE_COORDINATION_INSPECTION_RUN_027.md:1198:lib/python/runtime/identity.py:39:            git_commit=os.environ.get("RAILWAY_GIT_COMMIT_SHA", "unknown"),
work/implementation-reports/PCC-01/PCC-01_EXPERIENCE_PROTECTION_PERSISTENCE_COORDINATION_INSPECTION_RUN_027.md:1203:lib/python/runtime/railway.py:57:        git_commit_sha=os.environ.get("RAILWAY_GIT_COMMIT_SHA", "unknown"),
work/implementation-reports/PCC-01/PCC-01_RUN052_PRODUCTION_REVIEW_EXACT_ANATOMY.md:702:1198: lib/python/runtime/identity.py:39:            git_commit=os.environ.get("RAILWAY_GIT_COMMIT_SHA", "unknown"),
work/implementation-reports/PCC-01/PCC-01_RUN052_PRODUCTION_REVIEW_EXACT_ANATOMY.md:705:1203: lib/python/runtime/railway.py:57:        git_commit_sha=os.environ.get("RAILWAY_GIT_COMMIT_SHA", "unknown"),
work/implementation-reports/PCC-01/PCC-01_RUN058_DEPLOYMENT_BEHAVIOR_VERIFICATION.md:163:assert 'os.environ.get("PORT"' in config
work/implementation-reports/PCC-01/PCC-01_RUN058_DEPLOYMENT_BEHAVIOR_VERIFICATION.md:270:    env = os.environ if environment is None else environment

==========================================================
[3/8] EXTRACT ENVIRONMENT VARIABLE NAMES — NAMES ONLY
==========================================================
AI_TOOLKIT_REPOSITORY_ROOT
  referenced by: lib/python/runtime/bootstrap.py
AI_TOOLKIT_WORKSPACE_ROOT
  referenced by: lib/python/runtime/bootstrap.py
BUILD_VERSION
  referenced by: lib/python/runtime/identity.py
ENVIRONMENT
  referenced by: lib/python/dashboard/service.py, lib/python/runtime/config.py
GITHUB_TOKEN
  referenced by: lib/python/runtime/config.py
GITHUB_WEBHOOK_SECRET
  referenced by: lib/python/runtime/config.py
HOST
  referenced by: bin/ai, lib/python/cli/main.py
JSON_LOGS
  referenced by: lib/python/runtime/bootstrap.py
LOG_LEVEL
  referenced by: lib/python/runtime/bootstrap.py
MAX_RECOVERY_ATTEMPTS
  referenced by: lib/python/runtime/config.py
PORT
  referenced by: bin/ai, lib/python/cli/main.py, lib/python/dashboard/service.py, lib/python/runtime/config.py, lib/python/runtime/railway.py
RAILWAY_DEPLOYMENT_ID
  referenced by: lib/python/runtime/identity.py, lib/python/runtime/railway.py
RAILWAY_ENVIRONMENT
  referenced by: lib/python/dashboard/service.py, lib/python/runtime/config.py, lib/python/runtime/railway.py
RAILWAY_GIT_BRANCH
  referenced by: lib/python/runtime/railway.py
RAILWAY_GIT_COMMIT_SHA
  referenced by: lib/python/runtime/identity.py, lib/python/runtime/railway.py
RAILWAY_PRIVATE_DOMAIN
  referenced by: lib/python/runtime/railway.py
RAILWAY_PROJECT_ID
  referenced by: lib/python/runtime/railway.py
RAILWAY_PUBLIC_DOMAIN
  referenced by: lib/python/runtime/railway.py
RAILWAY_SERVICE_ID
  referenced by: lib/python/runtime/railway.py
REPOSITORY_ID
  referenced by: lib/python/runtime/identity.py
RUNTIME_API_KEY
  referenced by: lib/python/runtime/interfaces/api_auth.py
RUNTIME_BEARER_TOKEN
  referenced by: lib/python/runtime/interfaces/api_auth.py
RUNTIME_CACHE_DIR
  referenced by: lib/python/runtime/config.py
RUNTIME_CHECKPOINTS_DIR
  referenced by: lib/python/runtime/config.py
RUNTIME_CONTEXT_RECONSTRUCTION_TIMEOUT_SECONDS
  referenced by: lib/python/runtime/bootstrap.py
RUNTIME_HTTP_HOST
  referenced by: lib/python/runtime/config.py
RUNTIME_HTTP_PORT
  referenced by: lib/python/runtime/config.py
RUNTIME_ID
  referenced by: lib/python/runtime/identity.py
RUNTIME_LOGS_DIR
  referenced by: lib/python/runtime/config.py
RUNTIME_LOOP_INTERVAL_SECONDS
  referenced by: lib/python/runtime/config.py
RUNTIME_MODE
  referenced by: lib/python/runtime/config.py
RUNTIME_SESSIONS_DIR
  referenced by: lib/python/runtime/config.py
RUNTIME_STATE_DIR
  referenced by: lib/python/runtime/config.py
RUNTIME_VERSION
  referenced by: lib/python/runtime/identity.py
SCHEDULER_INTERVAL_SECONDS
  referenced by: lib/python/runtime/config.py
TELEGRAM_BOT_TOKEN
  referenced by: lib/python/runtime/config.py
TELEGRAM_CHAT_ID
  referenced by: lib/python/runtime/config.py
WORKSPACE_ID
  referenced by: lib/python/runtime/identity.py

==========================================================
[4/8] INSPECT OPENAI ADAPTER — SECRET SAFE
==========================================================
File: lib/python/ai_platform/adapters.py

--- OpenAI-related symbols/lines ---
18:    models: Sequence[Dict[str, Any]]
32:    def models(self) -> List[Dict[str, Any]]:
33:        return [dict(item) for item in self.descriptor.models]
36:        if provider_settings.get("api_key_fingerprint"):
38:        env_name = str(provider_settings.get("api_key_env", "")).strip()
53:    def complete(self, question: str, context: Mapping[str, Any], model: str) -> Dict[str, Any]:
61:            f"Model: {model or 'default'}",
73:            answer_lines.append("Next implementation step: complete provider setup, validate model routing, and run dashboard integration tests.")
104:class OpenAIProviderAdapter(StaticProviderAdapter):
105:    DEFAULT_BASE_URL = "https://api.openai.com/v1"
106:    DEFAULT_TIMEOUT_SECONDS = 60
113:            provider_settings.get("api_key_env", "")
137:            "OpenAI credential unavailable in environment"
184:                "OpenAI response contains no output"
211:                "OpenAI response contains no textual answer"
220:        model: str,
226:        selected_model = str(model or "").strip()
228:        if not selected_model:
229:            models = self.models()
230:            if models:
231:                selected_model = str(models[0].get("id", "")).strip()
233:        if not selected_model:
235:                "OpenAI model is not configured"
243:            timeout_seconds = max(
247:                        "timeout_seconds",
248:                        self.DEFAULT_TIMEOUT_SECONDS,
253:            timeout_seconds = self.DEFAULT_TIMEOUT_SECONDS
264:            "model": selected_model,
295:            f"{base_url}/responses",
301:                "Authorization": f"Bearer {credential}",
310:            with urllib.request.urlopen(
312:                timeout=timeout_seconds,
316:        except urllib.error.HTTPError as exc:
318:                f"OpenAI HTTP failure: status={exc.code}"
323:            TimeoutError,
324:            socket.timeout,
327:                f"OpenAI transport failure: {type(exc).__name__}"
332:                f"OpenAI transport failure: {type(exc).__name__}"
349:                "OpenAI returned invalid JSON"
354:                "OpenAI returned invalid response shape"
371:        actual_model = str(
372:            response_payload.get("model") or selected_model
378:            "model": actual_model,
396:            provider_id="openai",
397:            name="OpenAI",
398:            env_vars=["OPENAI_API_KEY"],
399:            models=[{"id": "gpt-4.1", "capabilities": ["chat", "reasoning"], "token_limit": 128000}],
407:            env_vars=["ANTHROPIC_API_KEY"],
408:            models=[{"id": "claude-sonnet-4.5", "capabilities": ["chat", "reasoning"], "token_limit": 200000}],
416:            env_vars=["GEMINI_API_KEY", "GOOGLE_API_KEY"],
417:            models=[{"id": "gemini-3.6-flash", "capabilities": ["chat", "reasoning"], "token_limit": 1000000}],
423:            provider_id="github-models",
424:            name="GitHub Models",
426:            models=[{"id": "gpt-4o-mini", "capabilities": ["chat"], "token_limit": 128000}],
435:            models=[{"id": "llama3.1", "capabilities": ["chat"], "token_limit": 8192}],
441:            provider_id="azure-openai",
442:            name="Azure OpenAI",
443:            env_vars=["AZURE_OPENAI_API_KEY"],
444:            models=[{"id": "gpt-4o", "capabilities": ["chat", "reasoning"], "token_limit": 128000}],
452:            env_vars=["OPENROUTER_API_KEY"],
453:            models=[{"id": "openrouter/auto", "capabilities": ["chat"], "token_limit": 128000}],
461:            env_vars=["CUSTOM_AI_API_KEY"],
462:            models=[{"id": "custom/default", "capabilities": ["chat"], "token_limit": 64000}],
471:        if descriptor.provider_id == "openai":
473:                OpenAIProviderAdapter(descriptor=descriptor)

--- Exact physiology around reported failure lines 250-340 ---
                ),
            )
        except (TypeError, ValueError):
            timeout_seconds = self.DEFAULT_TIMEOUT_SECONDS

        reconstructed_context = json.dumps(
            dict(context),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )

        payload = {
            "model": selected_model,
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "You are the AI Partner inside AI-Toolkit. "
                                "The following JSON is reconstructed "
                                "FUSION-02 conversation and epistemic "
                                "context. Conversation material is context, "
                                "not automatically Evidence or Canon.\n"
                                + reconstructed_context
                            ),
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": question,
                        }
                    ],
                },
            ],
        }

        request = urllib.request.Request(
            f"{base_url}/responses",
            data=json.dumps(
                payload,
                ensure_ascii=False,
            ).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {credential}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        start = time.perf_counter()

        try:
            with urllib.request.urlopen(
                request,
                timeout=timeout_seconds,
            ) as response:
                raw = response.read()

        except urllib.error.HTTPError as exc:
            raise ProviderExecutionError(
                f"OpenAI HTTP failure: status={exc.code}"
            ) from exc

        except (
            urllib.error.URLError,
            TimeoutError,
            socket.timeout,
        ) as exc:
            raise ProviderExecutionError(
                f"OpenAI transport failure: {type(exc).__name__}"
            ) from exc

        except OSError as exc:
            raise ProviderExecutionError(
                f"OpenAI transport failure: {type(exc).__name__}"
            ) from exc

        latency_ms = max(
            1,
            int((time.perf_counter() - start) * 1000),
        )

        try:

==========================================================
[5/8] INSPECT PROVIDER CONFIGURATION + REGISTRY
==========================================================

----------------------------------------------------------
FILE: lib/python/ai_platform/service.py
----------------------------------------------------------
10:from .model_manager import ModelManager
13:from .registry import ProviderRegistry
15:from .settings import AISettingsStore, masked_provider_settings
21:        self.registry = ProviderRegistry()
22:        self.model_manager = ModelManager()
33:            model_manager=self.model_manager,
39:    def configure_provider(self, provider_id: str, **kwargs: Any) -> Dict[str, Any]:
40:        settings = self.settings.configure_provider(provider_id, **kwargs)
41:        return masked_provider_settings(settings)
43:    def configure_models(self, roles: Mapping[str, str]) -> Dict[str, Any]:
44:        settings = self.settings.configure_models(roles)
45:        return masked_provider_settings(settings)
47:    def configure_routing(self, default_provider: str = "", fallback_provider: str = "") -> Dict[str, Any]:
49:            default_provider=default_provider or None,
50:            fallback_provider=fallback_provider or None,
52:        return masked_provider_settings(settings)
54:    def test_connection(self, provider_id: str) -> Dict[str, Any]:
56:        provider_settings = dict(settings.get("providers", {})).get(provider_id, {})
57:        return self.registry.test_connection(provider_id, provider_settings)
59:    def connect(self, provider_id: str) -> Dict[str, Any]:
60:        result = self.test_connection(provider_id)
64:    def disconnect(self, provider_id: str) -> Dict[str, Any]:
66:            "provider": provider_id,
76:    def ask_repository(
81:        provider_id: str = "",
82:        model: str = "",
101:                    "selected_provider": provider_id,
102:                    "selected_model": model,
127:        # Human input becomes durable RAW SOURCE before provider execution.
136:                "provider": provider_id or session.get(
137:                    "selected_provider", ""
139:                "model": model or session.get(
140:                    "selected_model", ""
148:            provider_id=provider_id,
149:            model=model,
170:            provider=result["provider"],
171:            model=result["model"],
184:            "provider": result["provider"],
185:            "model": result["model"],
209:        by_provider: Dict[str, Dict[str, Any]] = defaultdict(
221:                provider = usage.get("provider", "unknown")
234:                by_provider[provider]["tokens"] += tokens
235:                by_provider[provider]["estimated_cost"] += cost
236:                by_provider[provider]["latency_ms"] += latency
237:                by_provider[provider]["requests"] += 1
238:                by_provider[provider]["success"] += 1 if success else 0
239:                by_provider[provider]["errors"] += 0 if success else 1
250:            "by_provider": {
251:                provider: {
257:                for provider, stats in by_provider.items()
263:        providers = self.registry.list_providers(settings)
264:        discovered = self.model_manager.discover_models(providers)
265:        role_models = self.model_manager.resolve_roles(settings, discovered)
268:            "providers": providers,
271:                    "provider": item["id"],
280:                for item in providers
282:            "model_manager": {
283:                "discovered_models": discovered,
284:                "role_models": role_models,
286:            "settings": masked_provider_settings(settings),
299:                    "selected_provider": item.get("selected_provider", ""),
300:                    "selected_model": item.get("selected_model", ""),

----------------------------------------------------------
FILE: lib/python/ai_platform/pipeline.py
----------------------------------------------------------
7:from .model_manager import ModelManager
8:from .registry import ProviderRegistry
15:        registry: ProviderRegistry,
16:        model_manager: ModelManager,
20:        self.model_manager = model_manager
28:        provider_id: str = "",
29:        model: str = "",
32:        providers = self.registry.list_providers(settings)
33:        discovered = self.model_manager.discover_models(providers)
34:        roles = self.model_manager.resolve_roles(settings, discovered)
35:        fallback_provider = sorted(discovered.keys())[0] if discovered else ""
36:        selected_provider = provider_id or settings.get("default_provider") or fallback_provider
37:        selected_model = model or roles.get("engineering_model") or roles.get("default_model", "")
38:        adapter = self.registry.adapter(str(selected_provider))
40:            raise ValueError(f"no adapter found for provider: {selected_provider!r}")
47:        provider_settings = dict(
48:            settings.get("providers", {})
49:        ).get(str(selected_provider), {})
54:            model=selected_model,
55:            provider_settings=provider_settings,
58:            "provider": selected_provider,
59:            "model": selected_model,
71:            "provider": selected_provider,
72:            "model": selected_model,

----------------------------------------------------------
FILE: lib/python/dashboard/service.py
----------------------------------------------------------
14:from python.context_synchronization_engine.engine import GitContextProvider
55:        outputs=["home page", "project manager page", "engineering explorer pages", "runtime pages", "JSON endpoints"],
92:            "Map repository readiness to implementation progress instead of introducing a second progress model.",
104:        description="Shows current project, repository, branch, sprint, epic, task, runtime, AI provider, and session history.",
123:        justification_documents=["AI_CTO_EXECUTION_MODEL.md", "AI_CTO_EXECUTION_REPORT.md"],
165:        next_milestone="Expose more repository-engine detail through dashboard JSON endpoints.",
167:            "The dashboard reads repository-engine output directly to avoid introducing a second inspection model.",
182:        outputs=["runtime summary", "status view", "health endpoints"],
198:        justification_documents=["AI_CTO_EXECUTION_MODEL.md", "railway.json"],
246:        justification_documents=["standards/css/CSS-000_SPECIFICATION_MODEL.md"],
269:        justification_documents=["standards/cdm/CDM-000_DOCUMENT_MODEL.md"],
440:        result = self.ask_repository(question=question, prompt_name=prompt_name) if (question or prompt_name) else {}
448:                    ("Provider", result.get("provider", "")),
449:                    ("Model", result.get("model", "")),
466:                self._section("Repository-aware Engineering Chat", response_section),
493:                    "Owner AI Chat",
494:                    self._owner_ai_chat_panel(control),
498:                        {"label": "Providers", "value": str(len(control["providers"]))},
499:                        {"label": "Connected Providers", "value": str(sum(1 for item in control["providers"] if item.get("connection")))},
504:                self._section("Providers", self._provider_table(control["providers"])),
505:                self._section("Model Manager", self._model_manager_panel(control["model_manager"])),
563:                self._section("Registered Providers", self._bullet_list(runtime["registered_providers"])),
725:        git_context = GitContextProvider(str(self.repository_root)).collect()
733:        ai_provider = self._detect_ai_provider(ai_control_center=ai_control_center)
770:            "current_ai_provider": ai_provider,
783:                {"label": "Current AI Provider", "value": ai_provider},
833:            provider_value = self._detect_ai_provider()
839:                "environment": os.environ.get("RAILWAY_ENVIRONMENT", os.environ.get("ENVIRONMENT", "local")),
843:                "registered_providers": provider_value.split(", ") if provider_value != "Not configured" else [],
857:                    "environment": os.environ.get("ENVIRONMENT", "local"),
878:        providers = runtime_payload.get("registered_providers") or []
883:            {"label": "Environment", "value": runtime_payload.get("environment", "unknown")},
892:            ("Environment", runtime_payload.get("environment", "unknown")),
896:            ("Registered Providers", ", ".join(providers) or "None"),
936:    def ask_repository(self, question: str, prompt_name: str = "") -> Dict[str, Any]:
937:        return self.ai_platform.ask_repository(question=question, prompt_name=prompt_name)
1096:                {"label": "Current AI Provider", "value": session["current_ai_provider"]},
1112:                ("Current AI Provider", session["current_ai_provider"]),
1120:                ("Environment", runtime.get("environment", "unknown")),
1131:                ("Current AI Provider", session["current_ai_provider"]),
1207:    def _detect_ai_provider(self, ai_control_center: Optional[Mapping[str, Any]] = None) -> str:
1210:        providers = [
1212:            for item in source.get("providers", [])
1215:        if not providers:
1217:                ("ANTHROPIC_API_KEY", "Anthropic"),
1218:                ("OPENAI_API_KEY", "OpenAI"),
1219:                ("GEMINI_API_KEY", "Gemini"),
1220:                ("GOOGLE_API_KEY", "Google"),
1221:                ("MISTRAL_API_KEY", "Mistral"),
1224:                    providers.append(label)
1225:        return ", ".join(providers) if providers else "Not configured"
1269:            ".ai-chat{display:flex;flex-direction:column;gap:14px;}"
1270:            ".chat-toolbar{display:flex;justify-content:space-between;gap:12px;align-items:center;}"
1271:            ".chat-muted{font-size:12px;color:#9ca3af;margin-top:4px;}"
1272:            ".chat-controls{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;}"
1273:            ".chat-controls label{font-size:12px;color:#9ca3af;}"
1274:            ".chat-controls select,.chat-controls input,.chat-composer textarea{width:100%;box-sizing:border-box;margin-top:5px;background:#0b1020;color:#e5e7eb;border:1px solid #374151;border-radius:8px;padding:10px;}"
1275:            ".chat-history{height:420px;overflow:auto;background:#080d19;border:1px solid #1f2937;border-radius:12px;padding:14px;}"
1276:            ".chat-message{max-width:82%;padding:12px 14px;border-radius:12px;margin:10px 0;white-space:pre-wrap;word-break:break-word;}"
1277:            ".chat-message.human{margin-left:auto;background:#1d4ed8;}"
1278:            ".chat-message.ai{margin-right:auto;background:#1f2937;}"
1279:            ".chat-actor{font-size:11px;font-weight:700;text-transform:uppercase;opacity:.75;margin-bottom:5px;}"
1280:            ".chat-empty,.chat-status{color:#9ca3af;}"
1281:            ".chat-status.error{color:#fca5a5;}.chat-status.working{color:#93c5fd;}"
1282:            ".chat-composer{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:end;}"
1283:            ".chat-composer button{background:#2563eb;color:white;border:0;border-radius:8px;padding:12px 20px;font-weight:700;cursor:pointer;}"
1284:            ".chat-composer button:disabled{opacity:.55;cursor:wait;}"
1433:    def _owner_ai_chat_panel(
1437:        providers = [
1439:            for item in control.get("providers", [])
1443:        provider_options = []
1444:        for item in providers:
1445:            provider_id = escape(
1448:                    or item.get("provider_id")
1452:            name = escape(str(item.get("name", provider_id)))
1453:            models = item.get("models", []) or []
1454:            model = escape(str(models[0] if models else ""))
1455:            provider_options.append(
1456:                f'<option value="{provider_id}" '
1457:                f'data-model="{model}">{name}</option>'
1460:        options = "".join(provider_options)
1463:            '<div id="owner-ai-chat" class="ai-chat">'
1464:            '<div class="chat-toolbar">'
1465:            '<div><strong>Owner AI Chat</strong>'
1466:            '<div class="chat-muted">'
1472:            '<div class="chat-controls">'
1473:            '<label>AI Partner / Provider'
1474:            f'<select id="chat-provider">{options}</select>'
1476:            '<label>Model'
1477:            '<input id="chat-model" type="text" '
1478:            'placeholder="provider default">'
1481:            '<select id="chat-session">'
1485:            '<div id="chat-history" class="chat-history">'
1486:            '<div class="chat-empty">'
1489:            '<div id="chat-status" class="chat-status" '
1491:            '<form id="chat-form" class="chat-composer">'
1492:            '<textarea id="chat-question" rows="4" '
1495:            '<button id="chat-send" type="submit">Send</button>'
1501:            'const history=$("chat-history"),'
1502:            'session=$("chat-session"),'
1503:            'provider=$("chat-provider"),'
1504:            'model=$("chat-model"),'
1505:            'status=$("chat-status"),'
1506:            'form=$("chat-form"),'
1507:            'question=$("chat-question"),'
1508:            'send=$("chat-send");'
1516:            '"<div class=\\"chat-empty\\">No messages yet.</div>";'
1521:            'return "<article class=\\"chat-message "+cls+"\\">"'
1522:            '+"<div class=\\"chat-actor\\">"+esc(actorName(actor))'
1526:            'const r=await fetch(url,{credentials:"same-origin",...opts});'
1548:            'if(s.selected_provider)provider.value=s.selected_provider;'
1549:            'if(s.selected_model)model.value=s.selected_model;'
1552:            '"chat-status error";}}'
1553:            'provider.addEventListener("change",()=>{'
1554:            'const o=provider.options[provider.selectedIndex];'
1555:            'if(o&&o.dataset.model)model.value=o.dataset.model;});'
1560:            'status.className="chat-status working";'
1562:            'try{const data=await jsonFetch("/api/ai/chat",{'
1565:            'provider_id:provider.value,model:model.value})});'
1568:            'status.className="chat-status";'
1570:            'catch(e){status.className="chat-status error";'
1573:            'const first=provider.options[provider.selectedIndex];'
1574:            'if(first&&first.dataset.model)model.value=first.dataset.model;'
1582:    def _provider_table(self, providers: Iterable[Mapping[str, Any]]) -> str:
1584:        for item in providers:
1590:                f"<td>{escape(', '.join(item.get('models', [])) or 'None')}</td>"
1597:            rows.append("<tr><td colspan=\"7\">No providers available.</td></tr>")
1598:        return "<table><thead><tr><th>Provider</th><th>Status</th><th>Connected</th><th>Models</th><th>Capabilities</th><th>Latency (ms)</th><th>Health</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
1605:                f"<td>{escape(str(item.get('provider', '')))}</td>"
1614:        return "<table><thead><tr><th>Provider</th><th>Health</th><th>Last Success</th><th>Last Failure</th><th>Last Response Time (ms)</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
1616:    def _model_manager_panel(self, model_manager: Mapping[str, Any]) -> str:
1617:        discovered = model_manager.get("discovered_models", {})
1618:        roles = model_manager.get("role_models", {})
1620:        for provider, models in discovered.items():
1621:            discovered_rows.append((provider, ", ".join(models) or "None"))
1647:                f"<td>{escape(str(item.get('selected_provider', '')))}</td>"
1648:                f"<td>{escape(str(item.get('selected_model', '')))}</td>"
1654:        return "<table><thead><tr><th>Session</th><th>Project</th><th>Repository</th><th>Branch</th><th>Provider</th><th>Model</th><th>Messages</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"

----------------------------------------------------------
FILE: lib/python/runtime/interfaces/http_server.py
----------------------------------------------------------
79:            "<p class=\"error\">Owner credential rejected.</p>"
109:            "<label for=\"owner-token\">Owner credential</label>"
288:            self._send_json(srv.dashboard_service.ask_repository(question=question, prompt_name=prompt_name))
355:        elif path == "/api/ai/chat":
372:            provider_id = str(payload.get("provider_id", "")).strip()
373:            model = str(payload.get("model", "")).strip()
381:                result = srv.dashboard_service.ai_platform.ask_repository(
384:                    provider_id=provider_id,
385:                    model=model,
392:                logger.exception("Owner AI chat failed")
395:                        "error": "AI chat execution failed",

==========================================================
[6/8] SEARCH DEPLOYMENT/RUNTIME CONFIGURATION
==========================================================

----------------------------------------------------------
FILE: railway.json
----------------------------------------------------------
7:    "startCommand": "bash bin/runtime-server",

----------------------------------------------------------
FILE: bin/runtime-server
----------------------------------------------------------
2:# CORE-021 — Runtime Server Entry Point
5:# Starts the AI CTO Runtime Server.
13:export PYTHONPATH="$REPO_ROOT/lib"
14:export AI_TOOLKIT_REPOSITORY_ROOT="$REPO_ROOT"
15:export AI_TOOLKIT_WORKSPACE_ROOT="$(dirname "$REPO_ROOT")"
17:# Ensure canonical runtime directories exist
19:  "$REPO_ROOT/.ai/runtime/state" \
20:  "$REPO_ROOT/.ai/runtime/logs" \
21:  "$REPO_ROOT/.ai/runtime/checkpoints" \
22:  "$REPO_ROOT/.ai/runtime/sessions" \
23:  "$REPO_ROOT/.ai/runtime/cache"
25:echo "Starting AI CTO Runtime Server..."
26:exec python3 -m python.runtime.process "$@"

----------------------------------------------------------
FILE: README.md
----------------------------------------------------------
16:Unlike traditional developer tools, AI Toolkit is designed as a continuously operating Runtime capable of evolving from a local engineering assistant into an autonomous engineering platform operating across multiple repositories and eventually entire software organizations.
18:The platform combines deterministic engineering workflows, canonical governance, continuous evaluation and long-term architectural consistency into a single Runtime.
78:The Runtime must always behave predictably.
84:## Continuous Runtime
88:The Runtime continuously observes engineering activities, generates knowledge and supervises software evolution.
102:Every engineering recommendation should be supported by measurable evidence.
104:Reports, metrics, validations and historical decisions remain permanently traceable.
122:**CORE-021 — AI CTO Runtime Server**
126:**Railway Runtime**
134:**Runtime Foundation Complete**
148:The platform combines multiple engineering capabilities into a single Runtime capable of supervising the complete software development lifecycle.
156:- Continuous Runtime
169:- Runtime Health Monitoring
170:- Runtime Recovery
171:- Runtime Reporting
176:- Portfolio Intelligence
179:- Executive Decision Support
184:# Runtime Foundation
186:Beginning with Version **3.0.0-alpha.1**, AI Toolkit operates as a continuously running Runtime rather than a traditional command-line application.
188:The Runtime provides the execution foundation upon which every future AI CTO capability will be built.
192:- Runtime Bootstrap
194:- Continuous Runtime Loop
198:- Runtime Health
202:- Runtime Reports
207:The Runtime remains operational continuously and supervises engineering activities as they occur.
215:## Runtime Layer
225:- runtime services
263:Supports:
273:# Runtime Lifecycle
275:The Runtime progresses through canonical lifecycle phases.
334:8. Report
338:This workflow remains active throughout the Runtime lifecycle.
342:# Runtime Deployment
348:Runtime deployment includes:
355:- environment configuration
359:The Runtime is designed to remain operational continuously.
369:├── .ai/                         Runtime state and generated engineering artifacts
371:├── bin/                         Runtime entrypoints and CLI launchers
377:├── lib/python/                  Runtime and engineering engines
386:# Runtime Engines
405:Each engine has clearly defined responsibilities and communicates through the Runtime.
417:- CANON-045 Runtime Specification
427:- CANON-055 Runtime Server
429:- CANON-057 Continuous Runtime Lifecycle
430:- CANON-058 Autonomous Runtime Platform
437:# Runtime Services
439:The Runtime provides several infrastructure services.
443:- Runtime Bootstrap
444:- Runtime Lifecycle
445:- Runtime Registry
446:- Runtime Scheduler
447:- Runtime Event Dispatcher
448:- Runtime Event Loop
449:- Runtime Health
450:- Runtime Recovery
451:- Runtime Metrics
452:- Runtime Reports
453:- Runtime Logging
454:- Runtime Configuration
455:- Runtime Identity
456:- Runtime Secrets
458:These services operate continuously while the Runtime is running.
464:AI Toolkit currently supports:
468:Production Runtime hosting.
483:Supports:
498:Supports:
500:- Runtime status
501:- Runtime reports
504:- Runtime alerts
512:The Runtime exposes production endpoints.
535:- CORE-021 Runtime Server
536:- Railway deployment support
537:- Runtime Lifecycle
538:- Runtime Event Loop
539:- Runtime Scheduler
540:- Runtime Recovery
541:- Runtime Reporting
542:- GitHub Runtime Integration
543:- Telegram Runtime Gateway
578:Run the Runtime.
581:bash bin/runtime-server
599:2. Configure Runtime environment variables.
601:4. Verify Runtime Health.
602:5. Verify Runtime Readiness.
603:6. Monitor Runtime logs.
605:The Runtime is designed to restart automatically after unexpected failures.
609:# Environment Variables
613:- GITHUB_TOKEN
615:- TELEGRAM_BOT_TOKEN
618:Additional Runtime configuration may be introduced in future releases.
620:Secrets are loaded exclusively from the execution environment and are never stored inside the repository.
637:10. Runtime Validation
649:- ✅ CORE-021 — AI CTO Runtime Server
650:- 🔄 CORE-022 — Runtime API Platform
651:- ⏳ CORE-023 — Runtime Operations
657:- ⏳ CORE-029 — Runtime Orchestrator
658:- ⏳ CORE-030+ — Portfolio Intelligence and Autonomous Organization
674:- provide supporting engineering evidence;
719:**Status:** Runtime Foundation Complete
725:**Next Milestone:** CORE-022 — Runtime API Platform

==========================================================
[7/8] CLASSIFY OPENAI-RELATED VARIABLE NAMES
==========================================================
STATIC CONFIGURATION CONTRACT
----------------------------------------

AI_TOOLKIT_REPOSITORY_ROOT
  static required signal: NO
  detected fallback(s): os.getcwd(
  locations:
    - lib/python/runtime/bootstrap.py

AI_TOOLKIT_WORKSPACE_ROOT
  static required signal: NO
  detected fallback(s): str(os.path.dirname(self.repository_root
  locations:
    - lib/python/runtime/bootstrap.py

GITHUB_TOKEN
  static required signal: NO
  detected fallback(s): [REDACTED OR SECRET-LIKE DEFAULT]
  locations:
    - lib/python/runtime/config.py

HOST
  static required signal: NO
  detected fallback(s): "0.0.0.0" if os.environ.get("PORT" | "0.0.0.0" if os.environ.get("PORT"
  locations:
    - bin/ai
    - lib/python/cli/main.py

PORT
  static required signal: NO
  detected fallback(s): "8081" | os.environ.get("RUNTIME_HTTP_PORT", "8080" | "8080" | "8081" | "8081" | "8081"
  locations:
    - bin/ai
    - lib/python/cli/main.py
    - lib/python/dashboard/service.py
    - lib/python/runtime/config.py
    - lib/python/runtime/railway.py

RUNTIME_API_KEY
  static required signal: NO
  detected fallback(s): [REDACTED OR SECRET-LIKE DEFAULT]
  locations:
    - lib/python/runtime/interfaces/api_auth.py

RUNTIME_BEARER_TOKEN
  static required signal: NO
  detected fallback(s): [REDACTED OR SECRET-LIKE DEFAULT]
  locations:
    - lib/python/runtime/interfaces/api_auth.py

RUNTIME_HTTP_HOST
  static required signal: NO
  detected fallback(s): "0.0.0.0"
  locations:
    - lib/python/runtime/config.py

TELEGRAM_BOT_TOKEN
  static required signal: NO
  detected fallback(s): [REDACTED OR SECRET-LIKE DEFAULT]
  locations:
    - lib/python/runtime/config.py


==========================================================
[8/8] VERIFY INSPECTION CAUSED NO REPOSITORY MUTATION
==========================================================
Final worktree:

No Railway variable has been changed.
No provider request has been sent.
No test has been executed.
No source file has been modified by this instrument.
```
