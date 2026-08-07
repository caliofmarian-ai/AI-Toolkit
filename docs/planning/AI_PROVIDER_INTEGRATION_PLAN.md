# AI Provider and Agent Layer Plan

**Status:** Planning  
**Created:** 2026-08-06  
**Implementation sprint:** Sprint 6 (after Dashboard, Project Manager, and core engine outputs are working)

---

## Principle

No engine communicates directly with an AI provider.

When AI-assisted reasoning is required, engines communicate with an agent.
Agents communicate with providers.
Providers communicate with external model APIs.

This preserves four important properties:
- engines remain deterministic and provider-agnostic;
- prompt construction stays out of engine logic;
- provider failures remain isolated from core engine behavior;
- AI-assisted enrichment remains optional rather than architecturally mandatory.

---

## Alignment Decision

AI-Toolkit requires both an AI Provider Layer and an AI Agent Layer.

### Provider Layer
The Provider Layer is responsible for:
- provider registration;
- authentication;
- model selection;
- request execution;
- timeout and failure handling.

### Agent Layer
The Agent Layer is responsible for:
- task-specific prompt logic;
- task-specific response parsing;
- provider selection requests;
- AI-assisted enrichment for engines;
- preserving a stable contract between engines and providers.

### Architectural Position
The Agent Layer should not be introduced as a new product-facing architecture track.
It should be implemented by aligning the existing:
- `lib/python/agent_runtime/`
- `lib/python/agents/`

The Project Manager, Dashboard, and engines remain unchanged in identity.
The Agent Layer is internal infrastructure that simplifies future implementation.

---

## Runtime Flow

```
Engine (Knowledge, Validation, Briefing, ...)
    │
    └─► AgentRuntime / AgentRegistry
              │
              └─► Task Agent
                        │
                        └─► ProviderInterface.complete(request)
                                  │
                                  └─► ProviderRegistry.get(name) -> Provider
                                            │
                                            ├─► StubProvider
                                            ├─► OllamaProvider
                                            ├─► OpenAIProvider
                                            ├─► AnthropicProvider
                                            ├─► GeminiProvider
                                            └─► CopilotProvider
```

Engines never call provider SDKs or provider HTTP endpoints directly.

---

## Module Structure

### Agent Layer (reuse existing foundations)
```
lib/python/agent_runtime/
    base.py
    models.py
    registry.py
    runtime.py

lib/python/agents/
    __init__.py
    knowledge_extractor_agent.py      # new
    canonical_validator_agent.py      # new
    executive_briefer_agent.py        # new
    planning_assistant_agent.py       # later
    documentation_writer_agent.py     # later
    implementation_assistant_agent.py # later
    review_assistant_agent.py         # later
    merge_assistant_agent.py          # later
```

### Provider Layer
```
lib/python/ai_provider/
    __init__.py
    interface.py
    registry.py
    config.py
    auth.py
    selector.py
    providers/
        __init__.py
        stub.py
        ollama.py
        openai.py
        anthropic.py
        gemini.py
        copilot.py
```

---

## Interface Direction

### Engine-to-Agent Contract
Engines should request named capabilities, not provider completions.

Examples:
- `knowledge_extractor`
- `canonical_validator`
- `executive_briefer`

The engine provides structured input and receives structured or well-defined output.
The agent owns prompt construction and provider interaction.

### Provider Interface Specification

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class ProviderRequest:
    prompt: str
    context: Optional[str] = None
    model: Optional[str] = None
    max_tokens: int = 2048
    temperature: float = 0.2
    task_type: Optional[str] = None
    agent_name: Optional[str] = None

@dataclass
class ProviderResponse:
    content: str
    provider: str
    model: str
    tokens_used: int

class ProviderInterface(ABC):
    @abstractmethod
    def complete(self, request: ProviderRequest) -> ProviderResponse:
        ...
```

`task_type` supports model selection and logging.
`agent_name` supports traceability.

---

## Configuration

Provider selection remains configuration-driven:

```bash
AI_PROVIDER=ollama
AI_PROVIDER_OLLAMA_HOST=localhost
AI_PROVIDER_OPENAI_API_KEY=...
AI_PROVIDER_ANTHROPIC_API_KEY=...
AI_PROVIDER_GEMINI_API_KEY=...
AI_PROVIDER_MODEL=llama3.2
```

If no provider is configured, `StubProvider` is used automatically.
This keeps CI and rule-based engine behavior working without external AI access.

---

## Model Selection

`ModelSelector.select(task_type) -> str` maps task types to models.

| Task Type | Recommended Model | Fallback |
|---|---|---|
| knowledge_extraction | llama3.2 | mistral |
| canonical_validation | llama3.2 | llama3.2 |
| executive_briefing | llama3.2:70b | llama3.2 |
| planning_assistance | llama3.2:70b | llama3.2 |
| review_assistance | codellama:7b | llama3.2 |

---

## Initial Agent Set

The first implementation should stay small.
Only introduce agents that immediately reduce duplicated provider logic inside engines.

### Phase 1 agents
- **Knowledge Extractor Agent** — optional enrichment for semantic extraction and normalization
- **Canonical Validator Agent** — optional explanation and remediation suggestions for validation failures
- **Executive Briefer Agent** — optional narrative enhancement for executive summaries

### Later agents
- Planning Assistant
- Documentation Writer
- Implementation Assistant
- Coding Assistant
- Review Assistant
- Merge Assistant

These later agents should be registered only when a real engine integration is needed.

---

## Integration Points

### Knowledge Engine
The Knowledge Engine may optionally call `knowledge_extractor` for:
- semantic classification of ambiguous file types;
- relationship extraction from natural-language comments;
- entity normalization.

Rule-based extraction remains the default.

### Validation Engine
The Validation Engine may optionally call `canonical_validator` for:
- remediation suggestions;
- natural-language explanation of failures.

Scoring and rule execution remain deterministic and local.

### Executive Briefing Engine
The Briefing Engine may optionally call `executive_briefer` to improve narrative summary quality.

Structured evidence assembly remains inside the engine.

---

## Implementation Strategy

### Step 1 — Agent Alignment Layer
Use the existing `agent_runtime` and `agents` packages as the internal Agent Layer contract.
Add only the minimal agent registrations needed for Knowledge, Validation, and Briefing.

### Step 2 — Stub Provider
Implement `StubProvider` first.
This keeps tests deterministic and allows engine-to-agent-to-provider flow to exist before any network provider is added.

### Step 3 — Ollama Provider
Implement `OllamaProvider` as the primary local provider using `urllib`.

### Step 4 — Additional Hosted Providers
Add OpenAI, Anthropic, Gemini, and Copilot providers only after the contract is stable.

### Step 5 — Dashboard Visibility
Expose active provider, provider availability, and agent activity in the Dashboard once the internal path exists.

---

## Constraints

1. Provider failures must never crash an engine.
2. Engines must still work without any configured provider.
3. All provider calls must be logged.
4. No provider SDK is required; direct HTTP via stdlib is preferred.
5. Agents must not replace core rule-based engine behavior.
6. Agent introduction must reduce duplicated prompt logic, not create a second engine layer.
7. Dashboard and Project Manager must treat AI provider selection as Engineering Session state.

---

## Acceptance Criteria

- an engine can invoke an agent without knowing which provider is behind it
- an agent can invoke `ProviderInterface.complete()` without provider-specific engine logic
- `StubProvider` supports all automated tests
- at least one real provider implementation works behind the same interface
- rule-based engine output still functions when no provider is available
