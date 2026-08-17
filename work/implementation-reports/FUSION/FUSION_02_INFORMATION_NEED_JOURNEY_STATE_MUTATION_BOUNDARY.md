# FUSION-02 — Information Need and Journey State Mutation Boundary Characterization

## Starting Authority

2e722b82772d676764b198fe077e8b1762942af0

## Characterization Status

COMPLETE — NO PRODUCTION MUTATION

## Previous Conserved Capability

Permanent Epistemic Orientation is implemented.

It provides bounded orientation without materializing RepositoryProfile.

Knowledge Availability remains distinct from Working Context.

## Cognitive Question

The next production unit must determine how a Human request becomes an explicit epistemic need before task-specific knowledge retrieval begins.

The purpose of this characterization is not to invent an InformationNeed or JourneyState architecture.

The purpose is to locate the narrowest real production seam where those responsibilities legitimately belong.

## Required Physiology

The desired future cognitive sequence is conceptually:

Human request
→ Permanent Epistemic Orientation
→ explicit Information Need
→ controlled epistemic journey
→ selective retrieval
→ Working Context
→ provider reasoning

This sequence remains conceptual until repository anatomy proves the exact implementation seam.

## Existing Candidate Production Seams

- lib/python/ai_platform/context_builder.py — score 14: contains navigation physiology; contains retrieval physiology; mentions Working Context
- lib/python/ai_platform/pipeline.py — score 14: accepts or processes a Human question; already controls request context; participates in context assembly
- lib/python/ai_platform/service.py — score 14: accepts or processes a Human question; already controls request context; participates in context assembly
- lib/python/dashboard/service.py — score 8: accepts or processes a Human question; contains navigation physiology
- lib/python/ai_platform/adapters.py — score 5: accepts or processes a Human question
- lib/python/ai_platform/sessions.py — score 5: accepts or processes a Human question
- lib/python/dashboard/server.py — score 5: accepts or processes a Human question
- lib/python/runtime/interfaces/http_server.py — score 5: accepts or processes a Human question
- lib/python/ai_platform/conversation_context.py — score 4: participates in context assembly
- lib/python/ai_cto_scanner/detectors.py — score 3: contains navigation physiology
- lib/python/epistemic/layered_memory.py — score 3: contains navigation physiology
- lib/python/experience/repository.py — score 3: contains retrieval physiology

## Architectural Constraints

Permanent Orientation must remain bounded.

Permanent Orientation must not become Working Context.

Knowledge availability does not imply relevance to the current task.

Retrieval does not confer authority.

Navigation remains read-only.

UNKNOWN remains a legitimate epistemic state.

Semantic identity must not be reduced to physical repository location.

Full RepositoryProfile must not silently return as default provider context.

Human Authority remains superior to retrieved information.

## Mutation Decision Rule

The first production mutation after this report must occur only at a seam demonstrated by repository source and existing tests.

If no existing seam owns Human request interpretation or cognitive journey state, a new minimal organ may be justified.

If an existing seam already owns this responsibility, extend that seam rather than creating a parallel architecture.

## Forbidden Premature Mutations

No provider cutover.

No RepositoryProfile deletion.

No UEM to Knowledge Materialization adapter.

No CSL mutation.

No Canon mutation.

No Knowledge Graph mutation.

No speculative search engine.

No speculative Working Context implementation.

## Production Mutation

NONE

## Canon Mutation

NONE

## CSL Mutation

NONE

## UEM Mutation

NONE

## Knowledge Materialization Mutation

NONE

## Timestamp

2026-08-17T06:23:35.726580+00:00

## Next Authorized Stage

DIRECT AUDIT OF THIS CHARACTERIZATION, THEN AUTHORIZE THE EXACT INFORMATION NEED / JOURNEY STATE PRODUCTION SEAM.
