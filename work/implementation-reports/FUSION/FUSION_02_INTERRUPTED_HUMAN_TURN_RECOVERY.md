# FUSION-02 — Interrupted Human Turn Recovery

## Purpose

Resume a durably persisted interrupted HUMAN turn without
duplicating its raw source.

## Historical target

- Session: AI-SESSION-3BAD91C0B88C
- Experience: 3e264780-2ce0-491d-8903-41f0af66c6cb
- HUMAN raw source #3 is already durable.
- Expected successful continuation is AI raw source #4.

## Recovery physiology

- Detect final HUMAN raw source.
- Require INTERRUPTED Journey.
- Require restart_recoverable=true.
- Reuse HUMAN #3 as effective question.
- Do not append HUMAN #3 again.
- Continue cognition/context/provider physiology.
- Successful completion should append AI #4.

## Execution recovery

Initial pytest collection failure was caused by missing
repository/lib in Termux PYTHONPATH.

No production rollback was performed.

## Current worktree
 M lib/python/ai_platform/service.py
 M work/implementation-reports/FUSION/FUSION_02_TERMUX_EXECUTION_ERROR_MEMORY.md
?? lib/python/ai_platform/interrupted_turn.py
?? tests/fusion/test_fusion_02_interrupted_human_turn_recovery.py
?? work/implementation-reports/FUSION/FUSION_02_INTERRUPTED_HUMAN_TURN_RECOVERY.md
