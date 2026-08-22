# FUSION-02 — Durable Experience State-Root Integration

## Purpose

Integrate Persistent Experience with the durable Railway state-root anatomy already used by AISessionEngine.

## Demonstrated root cause

AISessionEngine resolves durable session state through AI_TOOLKIT_STATE_ROOT.

Persistent Experience previously defaulted to .ai/runtime/state/experience.json beneath the replaceable repository/runtime filesystem unless PCC01_EXPERIENCE_STORE was explicitly configured.

This allowed an AI session file to survive Railway redeployment while its referenced Experience disappeared.

## Implemented physiology

Resolution precedence is now:

1. Explicit absolute PCC01_EXPERIENCE_STORE remains authoritative.
2. Explicit relative PCC01_EXPERIENCE_STORE preserves its established repository-relative semantics.
3. Without explicit PCC01_EXPERIENCE_STORE, AI_TOOLKIT_STATE_ROOT becomes the durable deployment authority.
4. Without either durable configuration, historical repository-local behavior remains available.

## Durable production location

With Railway AI_TOOLKIT_STATE_ROOT=/data/ai-toolkit-state:

/data/ai-toolkit-state/.ai/runtime/state/experience.json

## Existing orphaned session

The implementation does not fabricate or silently reconstruct the missing Experience referenced by AI-SESSION-3BAD91C0B88C.

That session must be handled separately after durable Experience storage is deployed.

## Conservation

- no reset performed;
- no restore performed;
- no stash performed;
- no force push performed;
- existing session files are not modified by this implementation.

## Validation

- targeted Experience deployment acceptance executed;
- full FUSION regression executed.

## Current worktree
 M lib/python/experience/deployment.py
 M tests/experience/test_experience_deployment_behavior.py
?? work/implementation-reports/FUSION/FUSION_02_DURABLE_EXPERIENCE_STATE_ROOT_INTEGRATION.md

## Diff summary
 lib/python/experience/deployment.py                |  22 ++++
 .../test_experience_deployment_behavior.py         | 123 +++++++++++++++++++++
 2 files changed, 145 insertions(+)
