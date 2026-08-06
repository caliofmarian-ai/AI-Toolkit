# AI Provider Integration Plan

**Status:** Planning  
**Created:** 2026-08-06  
**Implementation sprint:** Sprint 7 (after core engines are functional)

---

## Principle

No engine communicates directly with an AI provider.

Every LLM request passes through a single `ProviderInterface`.

Engines are provider-agnostic. The provider is selected at runtime via configuration.

---

## Architecture

```
Engine (Knowledge, Validation, Briefing, ...)
    │
    └─► ProviderInterface.complete(prompt, context) -> str
              │
              └─► ProviderRegistry.get(name) -> Provider
                        │
                        ├─► OllamaProvider
                        ├─► OpenAIProvider
                        ├─► AnthropicProvider
                        ├─► GeminiProvider
                        ├─► CopilotProvider
                        └─► StubProvider (testing)
```

---

## Module Structure

```
lib/python/ai_provider/
    __init__.py
    interface.py        # ProviderInterface (abstract base)
    registry.py         # ProviderRegistry (singleton)
    config.py           # ProviderConfig (from env or config file)
    auth.py             # AuthManager (API key management)
    selector.py         # ModelSelector (runtime model selection)
    providers/
        __init__.py
        stub.py         # StubProvider (always available, no network)
        ollama.py       # OllamaProvider (local)
        openai.py       # OpenAIProvider
        anthropic.py    # AnthropicProvider
        gemini.py       # GeminiProvider
        copilot.py      # CopilotProvider (GitHub Copilot API)
```

---

## Interface Specification

```python
# lib/python/ai_provider/interface.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class ProviderRequest:
    prompt: str
    context: Optional[str] = None
    model: Optional[str] = None        # None = use provider default
    max_tokens: int = 2048
    temperature: float = 0.2           # Low for deterministic engineering output

@dataclass
class ProviderResponse:
    content: str
    provider: str
    model: str
    tokens_used: int

class ProviderInterface(ABC):
    """All providers must implement this interface."""

    @abstractmethod
    def complete(self, request: ProviderRequest) -> ProviderResponse:
        """Send a completion request and return the response."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider identifier, e.g. 'ollama', 'openai'."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if the provider can currently accept requests."""
        ...
```

---

## Provider Registry

```python
# lib/python/ai_provider/registry.py

class ProviderRegistry:
    """Singleton registry. Engines call get_default() or get(name)."""

    def register(self, provider: ProviderInterface) -> None: ...
    def get(self, name: str) -> ProviderInterface: ...
    def get_default(self) -> ProviderInterface: ...
    def list_available(self) -> list[str]: ...
```

The registry is populated at runtime startup from `ProviderConfig`.
Engines never instantiate providers directly.

---

## Configuration

Provider selection is controlled by environment variables:

```bash
AI_PROVIDER=ollama                  # default provider
AI_PROVIDER_OLLAMA_HOST=localhost   # Ollama host
AI_PROVIDER_OPENAI_API_KEY=...      # OpenAI key (optional)
AI_PROVIDER_ANTHROPIC_API_KEY=...   # Anthropic key (optional)
AI_PROVIDER_GEMINI_API_KEY=...      # Gemini key (optional)
AI_PROVIDER_MODEL=llama3.2          # default model override
```

If no provider is configured, `StubProvider` is used automatically.
This ensures all engines work in CI without any AI provider.

---

## Authentication Management

`AuthManager` reads API keys from:
1. Environment variables (highest priority)
2. `.ai/config/providers.json` (local config file, git-ignored)
3. Secrets management (Railway secrets in production)

API keys are never committed to the repository.

---

## Model Selection

`ModelSelector.select(task_type) -> str` maps task types to models:

| Task Type | Recommended Model | Fallback |
|---|---|---|
| code_analysis | codellama:7b | llama3.2 |
| document_extraction | llama3.2 | mistral |
| reasoning | llama3.2:70b | llama3.2 |
| summarization | llama3.2 | mistral |
| classification | llama3.2 | llama3.2 |

---

## Provider Implementation Roadmap

### Step 1 — StubProvider (Sprint 7, Day 1)

Returns deterministic fixed responses. Used in all tests.
No network. No dependencies.

### Step 2 — OllamaProvider (Sprint 7, Day 2–3)

Calls `http://localhost:11434/api/generate` via `urllib` (stdlib only).
Requires Ollama running locally.
This is the primary local provider.

### Step 3 — OpenAIProvider (Sprint 7, Day 4)

Calls OpenAI Chat Completions API via `urllib`.
Requires `AI_PROVIDER_OPENAI_API_KEY`.
No `openai` SDK — direct HTTP to avoid dependency.

### Step 4 — AnthropicProvider (Sprint 7, Day 5)

Calls Anthropic Messages API via `urllib`.
Requires `AI_PROVIDER_ANTHROPIC_API_KEY`.

### Step 5 — GeminiProvider (Sprint 8)

Calls Google Generative Language API via `urllib`.
Requires `AI_PROVIDER_GEMINI_API_KEY`.

### Step 6 — CopilotProvider (Sprint 8)

Calls GitHub Copilot API.
Requires GitHub token with Copilot access.

---

## Integration Points

### Knowledge Engine (Issue #5)

The Knowledge Engine may optionally call the provider for:
- semantic classification of ambiguous file types
- relationship extraction from natural language comments
- entity name normalization

The engine must work fully without a provider (rule-based extraction is the default).
The provider enriches results when available.

```python
# Usage in knowledge engine
from lib.python.ai_provider.registry import ProviderRegistry

registry = ProviderRegistry.instance()
if registry.get_default().is_available():
    enhanced = registry.get_default().complete(ProviderRequest(
        prompt=f"Extract entities from: {content}",
        task_type="document_extraction"
    ))
```

### Validation Engine (Issue #6)

The Validation Engine may use the provider for:
- generating remediation suggestions for failed checks
- explaining validation errors in natural language

This is enhancement only. Validation must work without a provider.

### Executive Briefing Engine (Issue #4)

The Briefing Engine already generates briefings from structured data.
The provider can optionally improve the executive summary section.

---

## Constraints

1. Every provider call must have a timeout (default 30 seconds).
2. Provider failures must never crash an engine. On failure, the engine returns
   the rule-based result without LLM enhancement.
3. All provider calls are logged to `.ai/runtime/logs/provider.jsonl`.
4. No provider SDK is added as a dependency. All providers use `urllib.request`.
5. `StubProvider` must be the default when no `AI_PROVIDER` env var is set.
6. Tests never require a real provider. Tests use `StubProvider`.
