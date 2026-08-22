# FUSION-02 — Organism Historical Experience Continuity

## Demonstrated production failure

Real Railway browser continuation reached:

Browser
-> AIPlatformService.ask_repository
-> ConversationContext.build
-> EpistemicOrganism.conversation_session
-> PersistentExperienceRepository.get
-> ExperienceNotFoundError

This demonstrated that the earlier ConversationExperienceBridge recovery
was not the only Experience lookup boundary involved in conversation
continuation.

## Root cause

EpistemicOrganism.conversation_session treated every non-empty historical
session Experience reference as requiring a physically persisted canonical
Experience.

That assumption is invalid for sessions created before Experience storage
became durable.

## Integration

The organism now preserves the following authority order:

1. Read durable AI session.
2. Read its Experience identity.
3. Query PersistentExperienceRepository first.
4. If canonical Experience exists, use it unchanged.
5. Only ExperienceNotFoundError may enter historical continuity.
6. Historical continuity preserves the original Experience identity.
7. Historical continuity does not fabricate exact created_at.
8. Historical continuity is not inserted into the Experience repository.
9. Unrelated repository failures continue to propagate.

## Epistemic conservation

Historical continuity is recovery evidence, not a reconstructed canonical
Experience.

For the historical orphan:

- Experience identity: demonstrated.
- Historical ACTIVE state: demonstrated by accepted FUSION-02 recovery physiology.
- Exact original created_at: irrecoverable.
- Recovery provenance: HISTORICAL_ORPHAN_RECOVERY.
- Canonical repository insertion: prohibited.

## Real target

Session:
AI-SESSION-3BAD91C0B88C

Historical Experience:
3e264780-2ce0-491d-8903-41f0af66c6cb

## Acceptance

Targeted historical recovery, bridge continuity, and organism continuity
tests must pass.

The complete FUSION regression must pass before commit or deployment.

## Deployment status

Not committed by this implementation run.
Not pushed by this implementation run.
Not deployed by this implementation run.

The next operation is certification and inspection before commit.
