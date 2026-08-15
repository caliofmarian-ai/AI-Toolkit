# ERROR MEMORY RUN 006 — Exact Interrupted Local Anatomy

Generated: 2026-08-15T22:09:14+01:00

## Git state

```text
BRANCH: organ/error-memory-run-006
HEAD:   fac00d00d95b5a1b19d867c39382fa1520a6b680

 M lib/python/autonomous_execution_engine/engine.py
 M lib/python/autonomous_execution_engine/models.py
 M lib/python/epistemic/error_memory.py
?? tests/epistemic/test_error_memory_execution_handoff.py
?? work/implementation-reports/ERROR-MEMORY/ERROR_MEMORY_RUN006_EXACT_INTERRUPTED_LOCAL_ANATOMY.md
```

## Diff summary

```text
 lib/python/autonomous_execution_engine/engine.py | 150 ++++++++++++++++++++++-
 lib/python/autonomous_execution_engine/models.py |   2 +
 lib/python/epistemic/error_memory.py             | 113 +++++++++++++++++
 3 files changed, 264 insertions(+), 1 deletion(-)
```

## Changed and untracked bodies

```text
lib/python/autonomous_execution_engine/engine.py
lib/python/autonomous_execution_engine/models.py
lib/python/epistemic/error_memory.py
tests/epistemic/test_error_memory_execution_handoff.py
work/implementation-reports/ERROR-MEMORY/ERROR_MEMORY_RUN006_EXACT_INTERRUPTED_LOCAL_ANATOMY.md
```

## FailureOrigin canonical runtime anatomy

```text
('repository_path', 'run_identity', 'git_commit')
```

## RUN 006 handoff anatomy currently present

```text
958-        awareness,
959-        statements,
960-    )
961-
962-    return prepare_transformation_with_recurrence_evidence(
963-        transformation,
964-        examination,
965-    )
966-
967-# ---------------------------------------------------------------------------
968-# Error Memory RUN 006
969-# Recurrence Evidence Handoff to Execution Context
970-# ---------------------------------------------------------------------------
971-
972-@dataclass(frozen=True)
973:class RecurrenceEvidenceHandoff:
974-    """Serializable preventive evidence carried toward execution context.
975-
976-    This body is a handoff, not an execution decision.
977-
978-    It conserves the recurrence examination already formed during
979-    TransformationPreparation so downstream execution physiology cannot
980-    silently lose the preventive evidence.
981-
982-    It does not execute, validate, approve, reject, block, canonicalize,
983-    or mutate historical Error Memory.
984-    """
985-
986-    transformation_identity: str
987-    transformation_title: str
988-    evidence: Tuple[RecurrenceExamination, ...]
989-    unresolved: Tuple[RecurrenceExamination, ...]
990-
991-    def __post_init__(self) -> None:
992-        if not self.transformation_identity.strip():
993-            raise ValueError(
994-                "transformation_identity must not be empty"
995-            )
996-
997-        if not self.transformation_title.strip():
998-            raise ValueError(
999-                "transformation_title must not be empty"
1000-            )
1001-
1002-        evidence_ids = tuple(
1003-            item.error_identity for item in self.evidence
1004-        )
1005-        unresolved_ids = tuple(
1006-            item.error_identity for item in self.unresolved
1007-        )
1008-
1009-        if len(evidence_ids) != len(set(evidence_ids)):
1010-            raise ValueError(
1011-                "recurrence handoff evidence identities must be unique"
1012-            )
1013-
1014-        if len(unresolved_ids) != len(set(unresolved_ids)):
1015-            raise ValueError(
1016-                "unresolved recurrence identities must be unique"
1017-            )
1018-
1019-        unknown_unresolved = set(unresolved_ids) - set(evidence_ids)
1020-
1021-        if unknown_unresolved:
1022-            raise ValueError(
1023-                "unresolved recurrence evidence must belong to the "
1024-                "complete recurrence evidence set"
1025-            )
1026-
1027-    @property
1028-    def has_unresolved(self) -> bool:
1029-        return bool(self.unresolved)
1030-
1031-    def to_dict(self) -> dict:
1032-        def serialize(item: RecurrenceExamination) -> dict:
1033-            return {
1034-                "error_identity": item.error_identity,
1035-                "error_title": item.error_title,
1036-                "prevention_rule": item.prevention_rule,
1037-                "origin": {
1038-                    "source": item.origin.source,
1039-                    "reference": item.origin.reference,
1040-                },
1041-                "disposition": item.disposition.value,
1042-                "explanation": item.explanation,
1043-            }
1044-
1045-        return {
1046-            "transformation_identity": self.transformation_identity,
1047-            "transformation_title": self.transformation_title,
1048-            "evidence": [
1049-                serialize(item)
1050-                for item in self.evidence
1051-            ],
1052-            "unresolved": [
1053-                serialize(item)
1054-                for item in self.unresolved
1055-            ],
1056-            "has_unresolved": self.has_unresolved,
1057-            "evidence_count": len(self.evidence),
1058-            "unresolved_count": len(self.unresolved),
1059-        }
1060-
1061-
1062-def form_recurrence_evidence_handoff(
1063-    preparation: TransformationPreparation,
1064-) -> RecurrenceEvidenceHandoff:
1065-    """Carry RUN 005 recurrence evidence toward execution physiology.
1066-
1067-    The handoff is deterministic and read-only.
1068-
1069-    No new recurrence classification is invented here.  It carries exactly
1070-    what the pre-execution examination already established.
1071-    """
1072-
1073-    return RecurrenceEvidenceHandoff(
```

## All current origin serialization references

```text
37:    repository_path: str
38:    run_identity: str
39:    git_commit: str | None = None
42:        if not self.repository_path.strip():
43:            raise ValueError("repository_path must be human-readable")
44:        if not self.run_identity.strip():
45:            raise ValueError("run_identity must be human-readable")
185:            repository_path=(
189:            run_identity="PCC-06 RUN 002 launch recovery",
190:            git_commit="83a3962a7d0e80da63fd8f4d52cdc62f3f768dfe",
217:            repository_path=(
222:            run_identity="PCC-06 RUN 002 interrupted-state conservation",
223:            git_commit="83a3962a7d0e80da63fd8f4d52cdc62f3f768dfe",
351:            repository_path=(
355:            run_identity="ERROR MEMORY RUN 001 import-topology recovery",
356:            git_commit="d8d16590911967579aeb2762a888dfcdd9ef941b",
385:            repository_path=(
389:            run_identity="ERROR MEMORY RUN 001 metabolic classification",
390:            git_commit="d8d16590911967579aeb2762a888dfcdd9ef941b",
521:    responsible for preserving their own source reality and provenance.
1038:                    "source": item.origin.source,
1039:                    "reference": item.origin.reference,
```

## Focused serialization test currently present

```text
84-    assert {
85-        item.error_identity
86-        for item in handoff.unresolved
87-    } == {
88-        "ERR-0002",
89-        "ERR-0003",
90-        "ERR-0004",
91-    }
92-
93-
94:def test_handoff_is_serializable():
95-    organ = seed_demonstrated_ai_toolkit_failures_run002()
96-
97-    preparation = prepare_intended_transformation_from_error_memory(
98-        organ,
99-        _transformation(),
100-    )
101-
102-    body = form_recurrence_evidence_handoff(
103-        preparation
104-    ).to_dict()
105-
106-    assert body["transformation_identity"] == (
107-        "RUN006-TRANSFORMATION"
108-    )
109-    assert body["evidence_count"] == 3
110-    assert body["unresolved_count"] == 3
111-    assert body["has_unresolved"] is True
112-
113-    for item in body["evidence"]:
114-        assert "error_identity" in item
115-        assert "prevention_rule" in item
116-        assert "origin" in item
117-        assert "disposition" in item
118-        assert "explanation" in item
119-
120-
121-def test_handoff_does_not_mutate_error_memory():
122-    organ = seed_demonstrated_ai_toolkit_failures_run002()
123-    before = organ.memories
124-
125-    preparation = prepare_intended_transformation_from_error_memory(
126-        organ,
127-        _transformation(),
128-    )
129-
130-    form_recurrence_evidence_handoff(preparation)
131-
132-    assert organ.memories == before
133-
134-
135-def test_handoff_is_immutable():
136-    organ = seed_demonstrated_ai_toolkit_failures_run002()
137-
138-    preparation = prepare_intended_transformation_from_error_memory(
139-        organ,
140-        _transformation(),
141-    )
142-
143-    handoff = form_recurrence_evidence_handoff(preparation)
144-
145-    with pytest.raises(FrozenInstanceError):
146-        handoff.transformation_title = "rewritten"
147-
148-
149-def test_handoff_has_no_execution_authority():
150-    organ = seed_demonstrated_ai_toolkit_failures_run002()
151-
152-    preparation = prepare_intended_transformation_from_error_memory(
153-        organ,
154-        _transformation(),
155-    )
156-
157-    handoff = form_recurrence_evidence_handoff(preparation)
158-
159-    for forbidden in (
```

## ExecutionContext local RUN 006 modifications

```text
120-    milestone: str
121-    core: str
122-    roadmap: str
123-    planning_id: str
124-    state_id: str
125-    synchronization_id: str
126-    briefing_id: str
127-    owner: str
128-    timestamp: str
129-    environment: str
130-    policy: str
131-    approval: str
132-    confidence: float
133-    mode: str
134-    schema_version: str
135:    recurrence_evidence: Dict[str, Any] = field(default_factory=dict)
136-
137-    def to_dict(self) -> Dict[str, Any]:
138-        return {
139-            "execution_id": self.execution_id,
140-            "repository": self.repository,
141-            "workspace": self.workspace,
142-            "branch": self.branch,
143-            "commit": self.commit,
144-            "issue": self.issue,
145-            "batch": self.batch,
146-            "milestone": self.milestone,
147-            "core": self.core,
148-            "roadmap": self.roadmap,
149-            "planning_id": self.planning_id,
150-            "state_id": self.state_id,
151-            "synchronization_id": self.synchronization_id,
152-            "briefing_id": self.briefing_id,
153-            "owner": self.owner,
154-            "timestamp": self.timestamp,
155-            "environment": self.environment,
156-            "policy": self.policy,
157-            "approval": self.approval,
158-            "confidence": self.confidence,
159-            "mode": self.mode,
160-            "schema_version": self.schema_version,
161:            "recurrence_evidence": dict(self.recurrence_evidence),
162-        }
163-
164-
165-# ---------------------------------------------------------------------------
166-# ExecutionStageResult
167-# ---------------------------------------------------------------------------
168-
169-@dataclass
170-class ExecutionStageResult:
171-    """Outcome of a single pipeline stage."""
172-
173-    stage: str
174-    status: str
175-    duration_ms: float
176-    evidence: Dict[str, Any]
177-    errors: List[str]
178-    warnings: List[str]
179-
180-    def to_dict(self) -> Dict[str, Any]:
181-        return {
182-            "stage": self.stage,
183-            "status": self.status,
184-            "duration_ms": self.duration_ms,
185-            "evidence": self.evidence,
186-            "errors": self.errors,
187-            "warnings": self.warnings,
188-        }
189-
190-
191-# ---------------------------------------------------------------------------
192-# ValidationResult
193-# ---------------------------------------------------------------------------
194-
195-@dataclass
196-class ValidationResult:
197-    """Result of a single validation check."""
198-
199-    validator: str
200-    status: str
201-    score: float
202-    findings: List[str]
203-    evidence: Dict[str, Any]
204-
205-    def to_dict(self) -> Dict[str, Any]:
206-        return {
207-            "validator": self.validator,
208-            "status": self.status,
209-            "score": self.score,
210-            "findings": self.findings,
211-            "evidence": self.evidence,
212-        }
213-
214-
215-# ---------------------------------------------------------------------------
216-# ExecutionMetrics
```

## CORE-015 local RUN 006 integration

```text
342-        )
343-
344-        # ------------------------------------------------------------------
345-        # STAGE: Validate Approvals
346-        # ------------------------------------------------------------------
347-        t0 = time.monotonic()
348-        approval_resolver = ExecutionApproval()
349-        approval = approval_resolver.resolve(state_data, briefing_data, self.mode)
350-        permissions = ExecutionPermissions()
351-        perm_result = permissions.check(policy, approval)
352-        validation_results.append(perm_result)
353-
354-        perm_status = VALIDATION_PASS if perm_result.status == VALIDATION_PASS else VALIDATION_FAIL
355-        stage_results.append(
356-            _stage_result(STAGE_VALIDATE_APPROVALS, perm_status, _ms(t0),
357-                          evidence={"approval": approval, "mode": self.mode},
358-                          errors=perm_result.findings if perm_result.status == VALIDATION_FAIL else [])
359-        )
360-        if perm_result.status == VALIDATION_FAIL:
361-            errors.extend(perm_result.findings)
362-
363-        # ------------------------------------------------------------------
364-        # STAGE: Prepare Execution Context
365-        # ------------------------------------------------------------------
366-        t0 = time.monotonic()
367:        recurrence_evidence = self._prepare_recurrence_evidence_handoff(
368-            queue_data=queue_data,
369-            state_data=state_data,
370-            context_data=context_data,
371-        )
372-
373-        exec_context = self._build_execution_context(
374-            execution_id=execution_id,
375-            generated_at=generated_at,
376-            context_data=context_data,
377-            state_data=state_data,
378-            briefing_data=briefing_data,
379-            queue_data=queue_data,
380-            approval=approval,
381-            policy=policy,
382-            recurrence_evidence=recurrence_evidence,
383-        )
384-
385-        self._evidence.record(
386-            "ERROR_MEMORY",
387-            "pre_execution_recurrence_evidence",
388-            recurrence_evidence,
389-        )
390-
391-        unresolved_count = recurrence_evidence.get(
392-            "unresolved_count",
393-            0,
394-        )
395-
396-        stage_results.append(
397-            _stage_result(
398-                STAGE_PREPARE_CONTEXT,
399-                VALIDATION_WARNING
400-                if unresolved_count
401-                else VALIDATION_PASS,
402-                _ms(t0),
403-                evidence={
404-                    "recurrence_evidence_count":
405-                        recurrence_evidence.get("evidence_count", 0),
406-                    "unresolved_recurrence_count":
407-                        unresolved_count,
408-                    "execution_authority": False,
409-                },
410-                warnings=(
411-                    [
412-                        f"{unresolved_count} demonstrated recurrence "
413-                        "precedent(s) remain UNRESOLVED; evidence is "
414-                        "preserved for Human Authority."
415-                    ]
416-                    if unresolved_count
417-                    else []
418-                ),
419-            )
420-        )
421-
422-        # ------------------------------------------------------------------
423-        # STAGE: Execute Approved Step
424-        # ------------------------------------------------------------------
425-        t0 = time.monotonic()
426-        step_result, step_warnings = self._execute_approved_step(
427-            policy=policy,
428-            approval=approval,
429-            queue_data=queue_data,
430-            state_data=state_data,
431-        )
432-        warnings.extend(step_warnings)
433-        stage_results.append(
434-            _stage_result(STAGE_EXECUTE_STEP, step_result, _ms(t0),
435-                          warnings=step_warnings)
436-        )
437-
438-        # ------------------------------------------------------------------
439-        # STAGE: Collect Evidence
440-        # ------------------------------------------------------------------
441-        t0 = time.monotonic()
442-        evidence_dict = self._evidence.collect()
443-        stage_results.append(
444-            _stage_result(STAGE_COLLECT_EVIDENCE, VALIDATION_PASS, _ms(t0),
445-                          evidence={"evidence_count": evidence_dict.get("evidence_count", 0)})
446-        )
447-
448-        # ------------------------------------------------------------------
449-        # STAGE: Run Validation
450-        # ------------------------------------------------------------------
451-        t0 = time.monotonic()
452-        snapshot_for_regression = ExecutionSnapshot.capture(
453-            execution_id=execution_id,
454-            context=exec_context.to_dict(),
455-            planning_queue=queue_data,
456-            development_state=state_data,
457-            briefing=briefing_data,
458-            live_context=context_data,
459-            schema_version=EXECUTION_VERSION,
460-        )
461-
462-        repo_vr = self._validator.validate_repository()
463-        sem_vr = self._validator.validate_semantic()
464-        canon_vr = self._validator.validate_canonical()
465-        reg_vr = self._validator.validate_regression(snapshot_for_regression)
466-        acc_vr = self._validator.validate_acceptance(
467-            self.mode, [repo_vr, sem_vr, canon_vr, reg_vr]
468-        )
469-        validation_results.extend([repo_vr, sem_vr, canon_vr, reg_vr, acc_vr])
470-
471-        stage_results.append(
472-            _stage_result(STAGE_RUN_VALIDATION, VALIDATION_PASS, _ms(t0),
473-                          evidence={"validator_count": len(validation_results)})
474-        )
475-
476-        # ------------------------------------------------------------------
477-        # STAGE: Update State
478-        # ------------------------------------------------------------------
479-        t0 = time.monotonic()
480-        stage_results.append(
481-            _stage_result(STAGE_UPDATE_STATE, VALIDATION_PASS, _ms(t0),
482-                          evidence={"note": "State read-only in safe modes"})
483-        )
484-
485-        # ------------------------------------------------------------------
486-        # Build metrics
487-        # ------------------------------------------------------------------
--
677-            execution_id=execution_id,
678-            repository=str(self.root),
679-            workspace=str(self.workspace_root),
680-            branch=context_data.get("current_branch", ""),
681-            commit=context_data.get("current_commit", ""),
682-            issue=state_data.get("current_issue", context_data.get("current_issue", "")),
683-            batch=state_data.get("current_batch", context_data.get("current_batch", "")),
684-            milestone=state_data.get("current_milestone", ""),
685-            core=context_data.get("next_core", ""),
686-            roadmap=state_data.get("current_roadmap", ""),
687-            planning_id=planning_id,
688-            state_id=str(state_id),
689-            synchronization_id=str(sync_id),
690-            briefing_id=str(briefing_id),
691-            owner=state_data.get("owner", ""),
692-            timestamp=generated_at,
693-            environment=str(self.root),
694-            policy=self.mode,
695-            approval=approval,
696-            confidence=round(confidence, 3),
697-            mode=self.mode,
698-            schema_version=EXECUTION_VERSION,
699-            recurrence_evidence=recurrence_evidence or {},
700-        )
701-
702:    def _prepare_recurrence_evidence_handoff(
703-        self,
704-        queue_data: Dict[str, Any],
705-        state_data: Dict[str, Any],
706-        context_data: Dict[str, Any],
707-    ) -> Dict[str, Any]:
708-        """Carry Error Memory preventive evidence to ExecutionContext.
709-
710-        RUN 006 deliberately does not convert recurrence evidence into
711-        execution authority.
712-
713-        CORE-015 policy and approval physiology remain unchanged.
714-        """
715-
716-        scheduler = ExecutionScheduler()
717-        next_entry = scheduler.next_executable(
718-            queue_data,
719-            state_data,
720-        )
721-
722-        if not next_entry:
723-            return {
724-                "transformation_identity": "",
725-                "transformation_title": "",
726-                "evidence": [],
727-                "unresolved": [],
728-                "has_unresolved": False,
729-                "evidence_count": 0,
730-                "unresolved_count": 0,
731-                "status": "NO_EXECUTABLE_TRANSFORMATION",
732-            }
733-
734-        try:
735-            from python.epistemic.error_memory import (
736-                FailureKind,
737-                IntendedTransformation,
738-                form_recurrence_evidence_handoff,
739-                prepare_intended_transformation_from_error_memory,
740-                seed_demonstrated_ai_toolkit_failures_run002,
741-            )
742-        except ImportError:
743-            from epistemic.error_memory import (
744-                FailureKind,
745-                IntendedTransformation,
746-                form_recurrence_evidence_handoff,
747-                prepare_intended_transformation_from_error_memory,
748-                seed_demonstrated_ai_toolkit_failures_run002,
749-            )
750-
751-        identity = str(
752-            next_entry.get("entry_id")
753-            or next_entry.get("planning_id")
754-            or next_entry.get("id")
755-            or "UNIDENTIFIED-TRANSFORMATION"
756-        )
757-
758-        title = str(
759-            next_entry.get("title")
760-            or next_entry.get("summary")
761-            or next_entry.get("description")
762-            or identity
763-        )
764-
765-        context_values = tuple(
766-            value
767-            for value in (
768-                str(self.root),
769-                str(context_data.get("current_branch", "")),
770-                str(context_data.get("current_commit", "")),
771-                str(state_data.get("current_issue", "")),
772-                str(state_data.get("current_batch", "")),
773-            )
774-            if value
775-        )
776-
777-        intended = IntendedTransformation(
778-            identity=identity,
779-            title=title,
780-            activities=(
781-                FailureKind.EXECUTION,
782-                FailureKind.VALIDATION,
783-                FailureKind.EPISTEMIC,
784-            ),
785-            context=context_values,
786-        )
787-
788-        organ = seed_demonstrated_ai_toolkit_failures_run002()
789-
790-        preparation = prepare_intended_transformation_from_error_memory(
791-            organ,
792-            intended,
793-        )
794-
795-        handoff = form_recurrence_evidence_handoff(
796-            preparation,
797-        )
798-
799-        body = handoff.to_dict()
800-        body["status"] = "RECURRENCE_EVIDENCE_ATTACHED"
801-        body["execution_authority"] = False
802-        body["approval_authority"] = False
803-        body["validation_authority"] = False
804-
805-        return body
806-
807-    def _execute_approved_step(
808-        self,
809-        policy: ExecutionPolicy,
810-        approval: str,
811-        queue_data: Dict[str, Any],
812-        state_data: Dict[str, Any],
813-    ) -> tuple:
814-        """
815-        Perform the approved execution step.
816-
817-        In safe modes this is always a no-op — the engine observes and
818-        reports without mutating any state.
819-        """
820-        warnings: List[str] = []
821-
822-        if policy.is_safe_mode():
```

## Exact unstaged diff — Error Memory

```diff
diff --git a/lib/python/epistemic/error_memory.py b/lib/python/epistemic/error_memory.py
index 49f6be2..c70dc73 100644
--- a/lib/python/epistemic/error_memory.py
+++ b/lib/python/epistemic/error_memory.py
@@ -963,3 +963,116 @@ def prepare_intended_transformation_from_error_memory(
         transformation,
         examination,
     )
+
+# ---------------------------------------------------------------------------
+# Error Memory RUN 006
+# Recurrence Evidence Handoff to Execution Context
+# ---------------------------------------------------------------------------
+
+@dataclass(frozen=True)
+class RecurrenceEvidenceHandoff:
+    """Serializable preventive evidence carried toward execution context.
+
+    This body is a handoff, not an execution decision.
+
+    It conserves the recurrence examination already formed during
+    TransformationPreparation so downstream execution physiology cannot
+    silently lose the preventive evidence.
+
+    It does not execute, validate, approve, reject, block, canonicalize,
+    or mutate historical Error Memory.
+    """
+
+    transformation_identity: str
+    transformation_title: str
+    evidence: Tuple[RecurrenceExamination, ...]
+    unresolved: Tuple[RecurrenceExamination, ...]
+
+    def __post_init__(self) -> None:
+        if not self.transformation_identity.strip():
+            raise ValueError(
+                "transformation_identity must not be empty"
+            )
+
+        if not self.transformation_title.strip():
+            raise ValueError(
+                "transformation_title must not be empty"
+            )
+
+        evidence_ids = tuple(
+            item.error_identity for item in self.evidence
+        )
+        unresolved_ids = tuple(
+            item.error_identity for item in self.unresolved
+        )
+
+        if len(evidence_ids) != len(set(evidence_ids)):
+            raise ValueError(
+                "recurrence handoff evidence identities must be unique"
+            )
+
+        if len(unresolved_ids) != len(set(unresolved_ids)):
+            raise ValueError(
+                "unresolved recurrence identities must be unique"
+            )
+
+        unknown_unresolved = set(unresolved_ids) - set(evidence_ids)
+
+        if unknown_unresolved:
+            raise ValueError(
+                "unresolved recurrence evidence must belong to the "
+                "complete recurrence evidence set"
+            )
+
+    @property
+    def has_unresolved(self) -> bool:
+        return bool(self.unresolved)
+
+    def to_dict(self) -> dict:
+        def serialize(item: RecurrenceExamination) -> dict:
+            return {
+                "error_identity": item.error_identity,
+                "error_title": item.error_title,
+                "prevention_rule": item.prevention_rule,
+                "origin": {
+                    "source": item.origin.source,
+                    "reference": item.origin.reference,
+                },
+                "disposition": item.disposition.value,
+                "explanation": item.explanation,
+            }
+
+        return {
+            "transformation_identity": self.transformation_identity,
+            "transformation_title": self.transformation_title,
+            "evidence": [
+                serialize(item)
+                for item in self.evidence
+            ],
+            "unresolved": [
+                serialize(item)
+                for item in self.unresolved
+            ],
+            "has_unresolved": self.has_unresolved,
+            "evidence_count": len(self.evidence),
+            "unresolved_count": len(self.unresolved),
+        }
+
+
+def form_recurrence_evidence_handoff(
+    preparation: TransformationPreparation,
+) -> RecurrenceEvidenceHandoff:
+    """Carry RUN 005 recurrence evidence toward execution physiology.
+
+    The handoff is deterministic and read-only.
+
+    No new recurrence classification is invented here.  It carries exactly
+    what the pre-execution examination already established.
+    """
+
+    return RecurrenceEvidenceHandoff(
+        transformation_identity=preparation.transformation.identity,
+        transformation_title=preparation.transformation.title,
+        evidence=preparation.recurrence_evidence,
+        unresolved=preparation.unresolved_recurrence_evidence,
+    )
```

## Exact unstaged diff — ExecutionContext

```diff
diff --git a/lib/python/autonomous_execution_engine/models.py b/lib/python/autonomous_execution_engine/models.py
index 9c849c1..b9ae448 100644
--- a/lib/python/autonomous_execution_engine/models.py
+++ b/lib/python/autonomous_execution_engine/models.py
@@ -132,6 +132,7 @@ class ExecutionContext:
     confidence: float
     mode: str
     schema_version: str
+    recurrence_evidence: Dict[str, Any] = field(default_factory=dict)
 
     def to_dict(self) -> Dict[str, Any]:
         return {
@@ -157,6 +158,7 @@ class ExecutionContext:
             "confidence": self.confidence,
             "mode": self.mode,
             "schema_version": self.schema_version,
+            "recurrence_evidence": dict(self.recurrence_evidence),
         }
 
 
```

## Exact unstaged diff — CORE-015

```diff
diff --git a/lib/python/autonomous_execution_engine/engine.py b/lib/python/autonomous_execution_engine/engine.py
index c15825a..4b887c5 100644
--- a/lib/python/autonomous_execution_engine/engine.py
+++ b/lib/python/autonomous_execution_engine/engine.py
@@ -364,6 +364,12 @@ class AutonomousExecutionEngine:
         # STAGE: Prepare Execution Context
         # ------------------------------------------------------------------
         t0 = time.monotonic()
+        recurrence_evidence = self._prepare_recurrence_evidence_handoff(
+            queue_data=queue_data,
+            state_data=state_data,
+            context_data=context_data,
+        )
+
         exec_context = self._build_execution_context(
             execution_id=execution_id,
             generated_at=generated_at,
@@ -373,9 +379,44 @@ class AutonomousExecutionEngine:
             queue_data=queue_data,
             approval=approval,
             policy=policy,
+            recurrence_evidence=recurrence_evidence,
         )
+
+        self._evidence.record(
+            "ERROR_MEMORY",
+            "pre_execution_recurrence_evidence",
+            recurrence_evidence,
+        )
+
+        unresolved_count = recurrence_evidence.get(
+            "unresolved_count",
+            0,
+        )
+
         stage_results.append(
-            _stage_result(STAGE_PREPARE_CONTEXT, VALIDATION_PASS, _ms(t0))
+            _stage_result(
+                STAGE_PREPARE_CONTEXT,
+                VALIDATION_WARNING
+                if unresolved_count
+                else VALIDATION_PASS,
+                _ms(t0),
+                evidence={
+                    "recurrence_evidence_count":
+                        recurrence_evidence.get("evidence_count", 0),
+                    "unresolved_recurrence_count":
+                        unresolved_count,
+                    "execution_authority": False,
+                },
+                warnings=(
+                    [
+                        f"{unresolved_count} demonstrated recurrence "
+                        "precedent(s) remain UNRESOLVED; evidence is "
+                        "preserved for Human Authority."
+                    ]
+                    if unresolved_count
+                    else []
+                ),
+            )
         )
 
         # ------------------------------------------------------------------
@@ -618,6 +659,7 @@ class AutonomousExecutionEngine:
         queue_data: Dict[str, Any],
         approval: str,
         policy: ExecutionPolicy,
+        recurrence_evidence: Optional[Dict[str, Any]] = None,
     ) -> ExecutionContext:
         planning_id = queue_data.get("queue_id", "")
         state_id = state_data.get("state_id", "")
@@ -654,8 +696,114 @@ class AutonomousExecutionEngine:
             confidence=round(confidence, 3),
             mode=self.mode,
             schema_version=EXECUTION_VERSION,
+            recurrence_evidence=recurrence_evidence or {},
+        )
+
+    def _prepare_recurrence_evidence_handoff(
+        self,
+        queue_data: Dict[str, Any],
+        state_data: Dict[str, Any],
+        context_data: Dict[str, Any],
+    ) -> Dict[str, Any]:
+        """Carry Error Memory preventive evidence to ExecutionContext.
+
+        RUN 006 deliberately does not convert recurrence evidence into
+        execution authority.
+
+        CORE-015 policy and approval physiology remain unchanged.
+        """
+
+        scheduler = ExecutionScheduler()
+        next_entry = scheduler.next_executable(
+            queue_data,
+            state_data,
+        )
+
+        if not next_entry:
+            return {
+                "transformation_identity": "",
+                "transformation_title": "",
+                "evidence": [],
+                "unresolved": [],
+                "has_unresolved": False,
+                "evidence_count": 0,
+                "unresolved_count": 0,
+                "status": "NO_EXECUTABLE_TRANSFORMATION",
+            }
+
+        try:
+            from python.epistemic.error_memory import (
+                FailureKind,
+                IntendedTransformation,
+                form_recurrence_evidence_handoff,
+                prepare_intended_transformation_from_error_memory,
+                seed_demonstrated_ai_toolkit_failures_run002,
+            )
+        except ImportError:
+            from epistemic.error_memory import (
+                FailureKind,
+                IntendedTransformation,
+                form_recurrence_evidence_handoff,
+                prepare_intended_transformation_from_error_memory,
+                seed_demonstrated_ai_toolkit_failures_run002,
+            )
+
+        identity = str(
+            next_entry.get("entry_id")
+            or next_entry.get("planning_id")
+            or next_entry.get("id")
+            or "UNIDENTIFIED-TRANSFORMATION"
+        )
+
+        title = str(
+            next_entry.get("title")
+            or next_entry.get("summary")
+            or next_entry.get("description")
+            or identity
+        )
+
+        context_values = tuple(
+            value
+            for value in (
+                str(self.root),
+                str(context_data.get("current_branch", "")),
+                str(context_data.get("current_commit", "")),
+                str(state_data.get("current_issue", "")),
+                str(state_data.get("current_batch", "")),
+            )
+            if value
+        )
+
+        intended = IntendedTransformation(
+            identity=identity,
+            title=title,
+            activities=(
+                FailureKind.EXECUTION,
+                FailureKind.VALIDATION,
+                FailureKind.EPISTEMIC,
+            ),
+            context=context_values,
         )
 
+        organ = seed_demonstrated_ai_toolkit_failures_run002()
+
+        preparation = prepare_intended_transformation_from_error_memory(
+            organ,
+            intended,
+        )
+
+        handoff = form_recurrence_evidence_handoff(
+            preparation,
+        )
+
+        body = handoff.to_dict()
+        body["status"] = "RECURRENCE_EVIDENCE_ATTACHED"
+        body["execution_authority"] = False
+        body["approval_authority"] = False
+        body["validation_authority"] = False
+
+        return body
+
     def _execute_approved_step(
         self,
         policy: ExecutionPolicy,
```

## Exact unstaged diff — RUN 006 focused test

```diff
```

## Existing RUN 006 report bodies

```text
work/implementation-reports/ERROR-MEMORY/ERROR_MEMORY_RUN006_EXACT_INTERRUPTED_LOCAL_ANATOMY.md
```

## Safety verdict

- Production code modified by this inspection: NO
- Git reset: NO
- Git checkout: NO
- Commit: NO
- Push: NO
- Existing interrupted RUN 006 state preserved: YES
