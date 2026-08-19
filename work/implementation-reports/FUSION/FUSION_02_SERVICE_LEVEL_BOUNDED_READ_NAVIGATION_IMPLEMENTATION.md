# FUSION-02 — Service-Level Bounded Read Navigation Implementation

## Authority

`a55393feb0eb7aed1f68391127bddbc4ddecce3f`

## Direct GitHub audit finding

The authoritative coordinator already contained the bounded Read organ, but an unreadable or missing selected source could escape as an operating-system exception.

The authoritative service had Search and Working Context integration but did not yet invoke bounded Read at service level.

## Implemented physiology

HUMAN RAW SOURCE
-> INFORMATION NEED
-> NAVIGATION PLAN
-> SEARCH
-> CANDIDATE SOURCE IDENTITIES
-> FIRST BOUNDED SOURCE SELECTION
-> READ OBSERVATION
-> WORKING CONTEXT remains independently bounded
-> PROVIDER COGNITIVE CONTEXT

## Search conservation

Search preserves the complete candidate source inventory.

Read does not rewrite, truncate, or replace Search retrieval.

## Read boundary

Only the first selected repository-relative candidate is read.

The second candidate may remain present in Search evidence but is not read by this cognitive unit.

## Failure physiology

Missing or unreadable selected sources become UNKNOWN rather than escaping as FileNotFoundError or another OSError.

## Authority

Read-only retrieval confers no authority.

Human authority remains preserved.

UNKNOWN remains a valid epistemic outcome.

## Repository root

The service reuses the existing AISessionEngine.root dependency. No duplicate repository_root field was introduced into AIPlatformService.

## Working Context

Working Context semantics remain separate from raw Read content.

Read is exposed as a separate cognitive observation to the provider context and service result.

## Validation

Focused bounded-read acceptance: PASS

Full Fusion regression: PASS

## Repository state before commit

 M lib/python/ai_platform/cognitive_coordination.py
 M lib/python/ai_platform/service.py
?? tests/fusion/test_fusion_02_service_level_bounded_read_navigation.py
?? work/implementation-reports/FUSION/.fusion02-read-contract-recovery-20260819-170902/
?? work/implementation-reports/FUSION/.fusion02-service-read-backup-20260819-165758/
?? work/implementation-reports/FUSION/.fusion02-service-read-final-recovery-20260819-171147/
?? work/implementation-reports/FUSION/.fusion02-service-read-recovery-20260819-170421/
?? work/implementation-reports/FUSION/FUSION_02_SERVICE_LEVEL_BOUNDED_READ_NAVIGATION_EXECUTION_ERROR.md

## Generated

2026-08-19T16:12:13.221563+00:00
