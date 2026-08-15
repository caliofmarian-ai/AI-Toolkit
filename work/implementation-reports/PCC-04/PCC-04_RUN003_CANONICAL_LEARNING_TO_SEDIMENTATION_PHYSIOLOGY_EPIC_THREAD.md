# PCC-04 — Sedimentation
## RUN 003 — Canonical Learning → Sedimentation Physiology

### Execution state

RUNNING

### Governing Canon

`canon/EPISTEMIC_CONTINUITY_STRUCTURE_MAP.md`

### Expected Git authority

`2643d72ebde2b0da006b158b935852ab9744ccb8`

### Canonical need

The governing Canon defines:

```text
VERIFICATION
    ↓
LEARNING
    ↓
SEDIMENTATION
    ↓
MEMORY
    ↓
KNOWLEDGE
    ↓
LIVING PROJECT IMAGE
```

RUN 001 established Sedimentation anatomy.

RUN 002 established durable Sedimentation and reconstruction.

The organism still lacks the canonical intermediate physiology:

`Verification → Learning → Sedimentation`

RUN 003 implements exactly this missing boundary.

### Executed Bash

`work/implementation-reports/PCC-04/PCC-04_RUN003_EXECUTED_BASH.sh`

### Complete Termux output

```text
==========================================================
PCC-04 RUN 003
VERIFICATION -> LEARNING -> SEDIMENTATION
==========================================================

[1/10] Verify exact Git authority
Expected:    2643d72ebde2b0da006b158b935852ab9744ccb8
LOCAL:       2643d72ebde2b0da006b158b935852ab9744ccb8
origin/main: 2643d72ebde2b0da006b158b935852ab9744ccb8
PASS

[2/10] Verify canonical physiology from Canon itself
PASS: Canon establishes Verification -> Learning
PASS: Canon establishes Learning -> Sedimentation
PASS: Canon places Memory after Sedimentation
PASS: Canon places Knowledge after Memory
PASS: automatic proposal != automatic Canon

[3/10] Verify actual organism gap
PASS: Verification exists
PASS: Sedimentation exists
PASS: Learning executable anatomy absent
PASS: canonical gap genuine

[4/10] Implement Learning as canonical intermediate physiology
PASS: Learning physiology compiled

[5/10] Add canonical behavioral examinations
PASS: canonical examinations compiled

[6/10] Execute dedicated PCC-04 examination
............................FFFF.                                        [100%]
=================================== FAILURES ===================================
___________________ test_learning_can_propose_sedimentation ____________________

    def test_learning_can_propose_sedimentation():
        verification = make_verified_learning_source()
        repository = SedimentationRepository()
    
        physiology = LearningSedimentationPhysiology(repository)
    
        learning = physiology.learn(
            verification,
            identifier="LRN-000001",
            title="Learning candidate",
            statement="Repeated verified behavior should be retained.",
        )
    
>       sedimentation = physiology.propose_sedimentation(
            learning,
            identifier="SED-000101",
            title="Sedimentation candidate",
            target=SedimentationTarget.MEMORY,
        )

tests/epistemic/test_sedimentation.py:408: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <python.epistemic.sedimentation.LearningSedimentationPhysiology object at 0x7c17c9be00>
learning = Learning(identifier='LRN-000001', title='Learning candidate', verification_identifier='VER-000001', statement='Repeated verified behavior should be retained.', uncertainty=None)
identifier = 'SED-000101', title = 'Sedimentation candidate'
target = <SedimentationTarget.MEMORY: 'MEMORY'>, uncertainty = None

    def propose_sedimentation(
        self,
        learning: Learning,
        *,
        identifier: str,
        title: str,
        target: SedimentationTarget,
        uncertainty: str | None = None,
    ) -> Sedimentation:
        registered = self.learning(learning.identifier)
    
        if registered != learning:
            raise LearningSedimentationError(
                "Learning anatomy does not match registered Learning"
            )
    
>       sedimentation = Sedimentation.propose(
                        ^^^^^^^^^^^^^^^^^^^^^
            identifier=identifier,
            title=title,
            provenance_identifier=learning.identifier,
            statement=learning.statement,
            target=target,
            uncertainty=(
                uncertainty
                if uncertainty is not None
                else learning.uncertainty
            ),
        )
E       AttributeError: type object 'Sedimentation' has no attribute 'propose'

lib/python/epistemic/sedimentation.py:465: AttributeError
___________ test_sedimentation_does_not_automatically_become_memory ____________

    def test_sedimentation_does_not_automatically_become_memory():
        verification = make_verified_learning_source()
        repository = SedimentationRepository()
    
        physiology = LearningSedimentationPhysiology(repository)
    
        learning = physiology.learn(
            verification,
            identifier="LRN-000001",
            title="Learning candidate",
            statement="Learning may deserve memory.",
        )
    
>       sedimentation = physiology.propose_sedimentation(
            learning,
            identifier="SED-000101",
            title="Memory proposal",
            target=SedimentationTarget.MEMORY,
        )

tests/epistemic/test_sedimentation.py:433: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <python.epistemic.sedimentation.LearningSedimentationPhysiology object at 0x7c17c9b8c0>
learning = Learning(identifier='LRN-000001', title='Learning candidate', verification_identifier='VER-000001', statement='Learning may deserve memory.', uncertainty=None)
identifier = 'SED-000101', title = 'Memory proposal'
target = <SedimentationTarget.MEMORY: 'MEMORY'>, uncertainty = None

    def propose_sedimentation(
        self,
        learning: Learning,
        *,
        identifier: str,
        title: str,
        target: SedimentationTarget,
        uncertainty: str | None = None,
    ) -> Sedimentation:
        registered = self.learning(learning.identifier)
    
        if registered != learning:
            raise LearningSedimentationError(
                "Learning anatomy does not match registered Learning"
            )
    
>       sedimentation = Sedimentation.propose(
                        ^^^^^^^^^^^^^^^^^^^^^
            identifier=identifier,
            title=title,
            provenance_identifier=learning.identifier,
            statement=learning.statement,
            target=target,
            uncertainty=(
                uncertainty
                if uncertainty is not None
                else learning.uncertainty
            ),
        )
E       AttributeError: type object 'Sedimentation' has no attribute 'propose'

lib/python/epistemic/sedimentation.py:465: AttributeError
_________________ test_learning_to_sedimentation_is_navigable __________________

    def test_learning_to_sedimentation_is_navigable():
        verification = make_verified_learning_source()
        repository = SedimentationRepository()
    
        physiology = LearningSedimentationPhysiology(repository)
    
        learning = physiology.learn(
            verification,
            identifier="LRN-000001",
            title="Navigable learning",
            statement="Learning retains its sedimentation descendants.",
        )
    
>       first = physiology.propose_sedimentation(
            learning,
            identifier="SED-000101",
            title="First proposal",
            target=SedimentationTarget.MEMORY,
        )

tests/epistemic/test_sedimentation.py:460: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <python.epistemic.sedimentation.LearningSedimentationPhysiology object at 0x7c17c99370>
learning = Learning(identifier='LRN-000001', title='Navigable learning', verification_identifier='VER-000001', statement='Learning retains its sedimentation descendants.', uncertainty=None)
identifier = 'SED-000101', title = 'First proposal'
target = <SedimentationTarget.MEMORY: 'MEMORY'>, uncertainty = None

    def propose_sedimentation(
        self,
        learning: Learning,
        *,
        identifier: str,
        title: str,
        target: SedimentationTarget,
        uncertainty: str | None = None,
    ) -> Sedimentation:
        registered = self.learning(learning.identifier)
    
        if registered != learning:
            raise LearningSedimentationError(
                "Learning anatomy does not match registered Learning"
            )
    
>       sedimentation = Sedimentation.propose(
                        ^^^^^^^^^^^^^^^^^^^^^
            identifier=identifier,
            title=title,
            provenance_identifier=learning.identifier,
            statement=learning.statement,
            target=target,
            uncertainty=(
                uncertainty
                if uncertainty is not None
                else learning.uncertainty
            ),
        )
E       AttributeError: type object 'Sedimentation' has no attribute 'propose'

lib/python/epistemic/sedimentation.py:465: AttributeError
_________________ test_sedimentation_to_learning_is_navigable __________________

    def test_sedimentation_to_learning_is_navigable():
        verification = make_verified_learning_source()
        repository = SedimentationRepository()
    
        physiology = LearningSedimentationPhysiology(repository)
    
        learning = physiology.learn(
            verification,
            identifier="LRN-000001",
            title="Navigable learning",
            statement="Sedimentation retains its Learning origin.",
        )
    
>       sedimentation = physiology.propose_sedimentation(
            learning,
            identifier="SED-000101",
            title="Proposal",
            target=SedimentationTarget.MEMORY,
        )

tests/epistemic/test_sedimentation.py:492: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <python.epistemic.sedimentation.LearningSedimentationPhysiology object at 0x7c17cfcfb0>
learning = Learning(identifier='LRN-000001', title='Navigable learning', verification_identifier='VER-000001', statement='Sedimentation retains its Learning origin.', uncertainty=None)
identifier = 'SED-000101', title = 'Proposal'
target = <SedimentationTarget.MEMORY: 'MEMORY'>, uncertainty = None

    def propose_sedimentation(
        self,
        learning: Learning,
        *,
        identifier: str,
        title: str,
        target: SedimentationTarget,
        uncertainty: str | None = None,
    ) -> Sedimentation:
        registered = self.learning(learning.identifier)
    
        if registered != learning:
            raise LearningSedimentationError(
                "Learning anatomy does not match registered Learning"
            )
    
>       sedimentation = Sedimentation.propose(
                        ^^^^^^^^^^^^^^^^^^^^^
            identifier=identifier,
            title=title,
            provenance_identifier=learning.identifier,
            statement=learning.statement,
            target=target,
            uncertainty=(
                uncertainty
                if uncertainty is not None
                else learning.uncertainty
            ),
        )
E       AttributeError: type object 'Sedimentation' has no attribute 'propose'

lib/python/epistemic/sedimentation.py:465: AttributeError
=========================== short test summary info ============================
FAILED tests/epistemic/test_sedimentation.py::test_learning_can_propose_sedimentation
FAILED tests/epistemic/test_sedimentation.py::test_sedimentation_does_not_automatically_become_memory
FAILED tests/epistemic/test_sedimentation.py::test_learning_to_sedimentation_is_navigable
FAILED tests/epistemic/test_sedimentation.py::test_sedimentation_to_learning_is_navigable
4 failed, 29 passed in 0.99s

==========================================================
PCC-04 RUN 003 STOPPED SAFELY
==========================================================
EXIT CODE: 1
FAILURE CONSERVED AS EPISTEMIC EXPERIENCE
==========================================================

```

### Result

FAILED / STOPPED

EXIT CODE: 1

### Repository state
```text
 M lib/python/epistemic/sedimentation.py
 M tests/epistemic/test_sedimentation.py
 M work/implementation-reports/CANON/CANON_EXECUTION_EVIDENCE_SUPERVISION_ADMISSION_001_RECOVERY.md
 M work/implementation-reports/PCC-04/PCC-04_RUN002_PERSISTENT_SEDIMENTATION_AND_RECONSTRUCTION_EPIC_THREAD.md
?? work/implementation-reports/PCC-04/PCC-04_RUN003_CANONICAL_LEARNING_TO_SEDIMENTATION_PHYSIOLOGY_EPIC_THREAD.md
?? work/implementation-reports/PCC-04/PCC-04_RUN003_EXECUTED_BASH.sh
```
