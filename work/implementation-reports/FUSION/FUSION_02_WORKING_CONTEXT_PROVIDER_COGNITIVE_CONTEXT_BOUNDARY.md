# FUSION-02 — Working Context / Provider Cognitive Context Boundary

## Starting Authority

3e325b67b497dd3f1361a177fa0786cac4719c82

## Purpose

Characterize the exact boundary between the newly materialized bounded Working Context and the cognitive context currently supplied to the AI provider.

This unit performs no production mutation.

## Demonstrated Current Physiology

HUMAN RAW SOURCE
→ INFORMATION NEED
→ NEED EVALUATION
→ NAVIGATION PLAN
→ SERVICE-LEVEL READ-ONLY SEARCH
→ RETRIEVED CANDIDATE EVIDENCE

The Working Context materializer now exists in the cognitive coordinator, but the service does not yet invoke it.

The active service path continues:

SEARCH NAVIGATION
→ LEGACY CONVERSATION CONTEXT RECONSTRUCTION
→ AIRequestPipeline.run(context_override=reconstructed_context)
→ PROVIDER

## Working Context Status

IMPLEMENTED AS A BOUNDED REPRESENTATION

Working Context is distinct from raw retrieval.

It preserves bounded repository-relative source identity and selected evidence-family information.

It explicitly does not confer epistemic authority.

## Provider Cognitive Context Status

NOT YET COMPOSED FROM WORKING CONTEXT

The provider currently receives the legacy reconstructed conversation context.

## Required Next Composition Boundary

The next production mutation must compose Working Context into the provider-facing cognitive context without replacing the existing reconstructed conversation context.

The composition must preserve the distinction between:

- durable conversation / persistent experience;
- reconstructed conversational context;
- retrieval candidate evidence;
- bounded Working Context;
- provider-facing cognitive context.

## Prohibited Composition

The next mutation must not:

- inject the complete raw search result;
- inject a full repository profile by default;
- treat retrieval as Canon;
- treat retrieval as Evidence merely because it was found;
- confer authority through retrieval;
- erase persistent conversation context;
- collapse Working Context into Permanent Orientation;
- create a UEM to Knowledge Materialization dependency;
- introduce write-capable navigation.

## Human Authority

MUST REMAIN PRESERVED

Working Context is epistemic material available to cognition. It is not Human authorization and does not become Canon automatically.

## Unknown

UNKNOWN remains a legitimate Working Context state.

An empty retrieval must not be converted into invented context.

## Source Identity

Repository-relative source identity must survive provider-context composition.

## Boundedness

Provider cognitive context must receive only the bounded Working Context representation, not the wholesale retrieval payload.

## Existing Conversation Physiology

PRESERVE

The existing ConversationContextReconstructor remains the demonstrated source of reconstructed conversational context.

## Exact First Production Mutation Boundary

PRIMARY PRODUCTION BOUNDARY:

lib/python/ai_platform/service.py

The service is the demonstrated convergence location because it already owns:

- cognitive initialization;
- navigation execution;
- conversation-context reconstruction;
- provider pipeline invocation.

The next mutation should invoke the existing Working Context materializer after bounded search retrieval and before provider execution, then compose its serialized bounded representation into a provider-facing context derived from the existing reconstructed context.

## Cognitive Coordinator

NO NEW WORKING CONTEXT REPRESENTATION REQUIRED

The existing materialize_working_context boundary should be reused rather than duplicated.

## Conversation Context Reconstructor

NO MUTATION AUTHORIZED BY THIS CHARACTERIZATION

No evidence currently requires changing its durable reconstruction responsibility.

## Pipeline

NO MUTATION AUTHORIZED BY THIS CHARACTERIZATION

The existing context_override boundary is sufficient for the first integration if service-level composition can preserve the required semantics.

## Provider

NO ADAPTER MUTATION AUTHORIZED

Provider-specific adapters must remain unaware of repository retrieval physiology at this stage.

## Working Context to Provider Contract

Required semantic properties:

1. explicit Working Context branch;
2. bounded source set;
3. repository-relative source identity;
4. authority_conferred remains false;
5. human_authority_preserved remains true;
6. unknown_is_valid remains true;
7. no wholesale raw retrieval payload;
8. legacy reconstructed conversation context remains present;
9. provider receives one explicit composed cognitive context;
10. no write-capable navigation is introduced.

## Characterization Verdict

FIRST SERVICE-LEVEL WORKING CONTEXT TO PROVIDER COGNITIVE CONTEXT COMPOSITION REQUIRED

## Production Modified

NO

## Canon Modified

NO

## CSL Modified

NO

## UEM Modified

NO

## Knowledge Materialization Modified

NO

## Next Authorized Stage

FIRST SERVICE-LEVEL WORKING CONTEXT TO PROVIDER COGNITIVE CONTEXT MUTATION

The mutation must remain bounded to the demonstrated service-level convergence boundary plus one focused acceptance test and one implementation report.
