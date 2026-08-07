# EPIC 005 — Development Audit (AI Platform + Dashboard Runtime Integration)

Date: 2026-08-07  
Scope: Current AI Platform implementation in `lib/python/ai_platform`, Dashboard integration in `lib/python/dashboard`, Runtime HTTP integration in `lib/python/runtime/interfaces/http_server.py`.

## Executive Summary

The current implementation has a strong modular base (providers, model manager, context builder, pipeline, sessions, prompts) and good local test coverage via shell-driven integration tests.  
Primary delivery risk is integration drift between Dashboard server routes and Runtime server routes. This caused the `/ai-control-center` regression in Railway despite healthy runtime process status.

## Root Cause of Regression

- **Observed symptom:** `/ai-control-center` returned `{"error":"not found"}` on Railway.
- **Root cause:** Route registration in `RuntimeHttpServer` diverged from `DashboardHttpServer`.  
  `DashboardHttpServer` had `/ai-control-center` and `/api/ai/*`; `RuntimeHttpServer` did not.
- **Contributing issue:** No regression test covered all Dashboard navigation endpoints and AI API endpoints through the Runtime entrypoint used by Railway.

## Strengths

- Clear AI Platform separation: settings, providers, model resolution, context building, pipeline, sessions, prompts.
- Minimal dependency footprint (stdlib HTTP and filesystem-first persistence).
- Backward-compatible, file-based operational state in `.ai/`.
- Useful dashboard capability framing and evidence-driven capability metadata.
- Existing tests already validate key AI Platform behavior and runtime lifecycle.

## Domain Review

### 1) Architecture Review
- **Strengths:** Layering exists (`AIPlatformService` orchestration over focused components).
- **Weaknesses:** Integration boundaries rely on duplicated route dispatch logic in two servers.
- **Risks:** Future features can be added to one server and missed in another.
- **Recommended improvements:** Centralize route mapping/constants shared by both servers.

### 2) Routing Review
- **Strengths:** Dashboard server provides complete UI/API route set.
- **Weaknesses:** Runtime server had partial route coverage.
- **Risks:** Production-only regressions when Railway uses runtime entrypoint.
- **Recommended improvements:** Keep canonical route aliases and runtime/dashboard parity tests.

### 3) Runtime Integration Review
- **Strengths:** Runtime bootstrap wires dashboard service cleanly.
- **Weaknesses:** Runtime handler mixes system endpoints and dashboard endpoints inline.
- **Risks:** Harder to reason about route completeness as features expand.
- **Recommended improvements:** Isolate dashboard route handling path in runtime handler.

### 4) Dashboard Integration Review
- **Strengths:** Dashboard uses AI platform control-center and ask flows directly.
- **Weaknesses:** Navigation route targets and runtime route support were not consistently enforced.
- **Risks:** UI links can silently regress depending on hosting entrypoint.
- **Recommended improvements:** Validate every nav target against both server entrypoints.

### 5) Provider Abstraction Review
- **Strengths:** Registry + adapter abstraction is clean and extensible.
- **Weaknesses:** Static adapter completion is synthetic and not transport-backed.
- **Risks:** Functional expectations may diverge from real provider behavior.
- **Recommended improvements:** Add optional live adapter contract tests behind env-gated credentials.

### 6) Context Builder Review
- **Strengths:** Rich context assembled from git/development/workspace/runtime/profile.
- **Weaknesses:** Multiple filesystem reads per request; no structured error telemetry on partial reads.
- **Risks:** Performance and silent context degradation for larger workspaces.
- **Recommended improvements:** Add freshness metadata + partial-read diagnostics in payload.

### 7) Pipeline Review
- **Strengths:** Clear provider/model resolution flow and usage capture.
- **Weaknesses:** No explicit fallback execution when selected provider fails at completion time.
- **Risks:** Single-point request failure despite configured fallback intent.
- **Recommended improvements:** Implement runtime fallback execution path with recorded failover events.

### 8) AI Session Review
- **Strengths:** Simple, transparent JSON session persistence.
- **Weaknesses:** No retention policy, growth controls, or corruption recovery policy.
- **Risks:** Unbounded disk growth and slower session listing over time.
- **Recommended improvements:** Add retention/archival configuration and periodic compaction.

### 9) Prompt Library Review
- **Strengths:** Structured category model and named prompt resolution.
- **Weaknesses:** Static in-code prompts; no versioning metadata.
- **Risks:** Harder governance and change auditing for prompt evolution.
- **Recommended improvements:** Add prompt version/source metadata and optional external catalog loading.

### 10) Repository Integration Review
- **Strengths:** Strong reuse of repository engine/profile serializer.
- **Weaknesses:** Heavy profile/context rebuild can be expensive per request.
- **Risks:** Latency spikes under repeated dashboard/API polling.
- **Recommended improvements:** Introduce tighter TTL and targeted invalidation for expensive artifacts.

### 11) Maintainability Review
- **Strengths:** Readable modules and straightforward data contracts.
- **Weaknesses:** Duplicate route logic and alias handling across servers.
- **Risks:** Regression probability grows with each route/API expansion.
- **Recommended improvements:** Shared route registry + tests derived from same source of truth.

### 12) Extensibility Review
- **Strengths:** Provider registration pattern supports new adapters.
- **Weaknesses:** Capability definitions and routes are hardcoded in multiple places.
- **Risks:** Extension work requires multi-file synchronized edits.
- **Recommended improvements:** Move route/capability metadata to centralized declarative config.

### 13) Security Review
- **Strengths:** API key masking/fingerprinting, no raw key persistence.
- **Weaknesses:** No explicit authn/authz layer on dashboard/runtime HTTP surfaces.
- **Risks:** Exposure risk if service is publicly reachable without edge protection.
- **Recommended improvements:** Add optional token gate / trusted-network mode for sensitive endpoints.

### 14) Performance Considerations
- **Strengths:** Lightweight stack, low overhead execution model.
- **Weaknesses:** Repeated filesystem scans/profile generation can be costly.
- **Risks:** Throughput degradation with repository growth and endpoint polling.
- **Recommended improvements:** Cache stratification for profile/context/reports with independent TTL.

### 15) Technical Debt
- Split route logic across two handlers.
- Inline alias mapping without shared constants.
- Mixed responsibilities in runtime handler (system APIs + dashboard rendering).

### 16) Missing Capabilities
- Unified route contract validation against runtime and dashboard servers.
- Provider failover execution telemetry.
- Session retention policy and lifecycle management.
- Prompt governance metadata.

### 17) Inconsistencies
- Route availability differed between local dashboard entrypoint and Railway runtime entrypoint.
- Navigation target naming (`/projects` vs `/project-manager`, `/session` vs `/engineering-session`) needed alias normalization.

### 18) Duplicated Logic
- Dashboard page dispatch logic duplicated in `dashboard/server.py` and `runtime/interfaces/http_server.py`.
- Similar endpoint condition trees maintained independently.

### 19) Dead Code
- No obvious dead modules in audited scope; however, legacy route variants acted as de facto undocumented compatibility paths.

### 20) Future Scalability Concerns
- Growing `.ai/ai_sessions` and report artifacts without retention.
- Repeated context/profile assembly per request.
- Manual multi-server route synchronization burden.

## Risks Summary

1. **High:** Route parity regressions across runtime/dashboard entrypoints.
2. **Medium:** Performance degradation from repeated heavy context/profile reads.
3. **Medium:** Public endpoint exposure without explicit access control.
4. **Medium:** Session/report artifact growth without retention management.
5. **Low-Medium:** Prompt/provider governance drift as capabilities expand.

## Recommended Improvements (Backward-Compatible)

1. **Route single-source-of-truth** for aliases, dashboard pages, and API endpoints.
2. **Parity regression suite** that validates all dashboard nav/API targets on both servers.
3. **Failover-aware pipeline execution** honoring configured fallback provider.
4. **Session retention/archival policy** with configurable limits.
5. **Context/profile cache improvements** with per-component TTL and diagnostics.
6. **Optional endpoint access guard** for exposed runtime/dashboard deployments.

## Implementation Priorities and Estimated Complexity

| Priority | Improvement | Complexity | Rationale |
|---|---|---:|---|
| P0 | Route parity + shared route contract | Medium | Directly prevents production route regressions. |
| P0 | Runtime+dashboard endpoint parity tests in CI | Low | Fast, high-impact regression protection. |
| P1 | Pipeline fallback execution behavior | Medium | Improves reliability under provider failures. |
| P1 | Session retention + archival | Medium | Controls growth and long-term maintainability. |
| P2 | Context/profile cache stratification | Medium-High | Performance improvement for larger repos. |
| P2 | Optional endpoint access control | Medium | Reduces deployment exposure risk. |
| P3 | Prompt catalog governance metadata | Low-Medium | Improves auditability and evolution discipline. |

## Compatibility Position

All recommendations preserve current behavior and implemented capabilities, add safety and reliability, and improve the platform’s ability to build, maintain, audit, validate, and evolve AI-Toolkit and downstream projects (Trading Signals Platform, DROPi, Practical Beekeeping Handbook, and future repositories).
