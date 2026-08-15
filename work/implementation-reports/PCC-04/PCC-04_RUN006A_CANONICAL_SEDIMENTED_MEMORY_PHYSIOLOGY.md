# PCC-04 — Sedimentation
## RUN 006A — Canonical Sedimented Memory Physiology

### Status

RUNNING

### Expected Git authority

`f69964a8127d8468d85ee336e5a170e458397a93`

### Canonical need

The organism already possesses:

- Persistent Experience;
- Transformation;
- Provenance;
- Verification;
- Knowledge;
- Current State;
- Learning;
- Sedimentation;
- Sedimentation governance.

The missing physiology is semantic Memory produced from accepted
Sedimentation without redefining Persistent Experience or duplicating
PCC-03 Knowledge.

### Executed Bash

`work/implementation-reports/PCC-04/PCC-04_RUN006A_EXECUTED_BASH.sh`

### Complete Termux output

```text
==========================================================
PCC-04 RUN 006A
CANONICAL SEDIMENTED MEMORY PHYSIOLOGY
==========================================================

[1/9] Verify exact Git authority
EXPECTED:    f69964a8127d8468d85ee336e5a170e458397a93
LOCAL:       f69964a8127d8468d85ee336e5a170e458397a93
origin/main: f69964a8127d8468d85ee336e5a170e458397a93
PASS

[2/9] Verify required inherited anatomy before mutation
PASS: inherited Sedimentation anatomy
PASS: target distinction
PASS: authority distinction
PASS: provenance
PASS: uncertainty

[3/9] Materialize canonical Sedimented Memory organ
PASS: canonical Sedimented Memory organ compiles

[4/9] Materialize dedicated physiological examination
PASS: dedicated examination compiles

[5/9] Execute dedicated RUN 006A examination
FFFFFFFFFFFFFF                                                           [100%]
=================================== FAILURES ===================================
_______________ test_memory_target_creates_semantic_memory_only ________________

    def test_memory_target_creates_semantic_memory_only():
>       governed = make_governed(
            SedimentationTarget.MEMORY
        )

tests/epistemic/test_sedimented_memory.py:56: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/epistemic/test_sedimented_memory.py:36: in make_governed
    learning = make_learning()
               ^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def make_learning() -> Learning:
>       return Learning(
            learning_id="LEARN-006A",
            verification_identifier="VER-006A",
            meaning="The organism learned a durable semantic conclusion.",
            provenance_identifier="PROV-006A",
            uncertainty="Residual uncertainty remains explicit.",
        )
E       TypeError: Learning.__init__() got an unexpected keyword argument 'learning_id'

tests/epistemic/test_sedimented_memory.py:23: TypeError
_________________ test_memory_preserves_sedimentation_identity _________________

    def test_memory_preserves_sedimentation_identity():
>       governed = make_governed(
            SedimentationTarget.MEMORY
        )

tests/epistemic/test_sedimented_memory.py:70: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/epistemic/test_sedimented_memory.py:36: in make_governed
    learning = make_learning()
               ^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def make_learning() -> Learning:
>       return Learning(
            learning_id="LEARN-006A",
            verification_identifier="VER-006A",
            meaning="The organism learned a durable semantic conclusion.",
            provenance_identifier="PROV-006A",
            uncertainty="Residual uncertainty remains explicit.",
        )
E       TypeError: Learning.__init__() got an unexpected keyword argument 'learning_id'

tests/epistemic/test_sedimented_memory.py:23: TypeError
________________________ test_memory_preserves_meaning _________________________

    def test_memory_preserves_meaning():
>       governed = make_governed(
            SedimentationTarget.MEMORY
        )

tests/epistemic/test_sedimented_memory.py:85: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/epistemic/test_sedimented_memory.py:36: in make_governed
    learning = make_learning()
               ^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def make_learning() -> Learning:
>       return Learning(
            learning_id="LEARN-006A",
            verification_identifier="VER-006A",
            meaning="The organism learned a durable semantic conclusion.",
            provenance_identifier="PROV-006A",
            uncertainty="Residual uncertainty remains explicit.",
        )
E       TypeError: Learning.__init__() got an unexpected keyword argument 'learning_id'

tests/epistemic/test_sedimented_memory.py:23: TypeError
_______________________ test_memory_preserves_provenance _______________________

    def test_memory_preserves_provenance():
>       governed = make_governed(
            SedimentationTarget.MEMORY
        )

tests/epistemic/test_sedimented_memory.py:100: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/epistemic/test_sedimented_memory.py:36: in make_governed
    learning = make_learning()
               ^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def make_learning() -> Learning:
>       return Learning(
            learning_id="LEARN-006A",
            verification_identifier="VER-006A",
            meaning="The organism learned a durable semantic conclusion.",
            provenance_identifier="PROV-006A",
            uncertainty="Residual uncertainty remains explicit.",
        )
E       TypeError: Learning.__init__() got an unexpected keyword argument 'learning_id'

tests/epistemic/test_sedimented_memory.py:23: TypeError
______________________ test_memory_preserves_uncertainty _______________________

    def test_memory_preserves_uncertainty():
>       governed = make_governed(
            SedimentationTarget.MEMORY
        )

tests/epistemic/test_sedimented_memory.py:115: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/epistemic/test_sedimented_memory.py:36: in make_governed
    learning = make_learning()
               ^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def make_learning() -> Learning:
>       return Learning(
            learning_id="LEARN-006A",
            verification_identifier="VER-006A",
            meaning="The organism learned a durable semantic conclusion.",
            provenance_identifier="PROV-006A",
            uncertainty="Residual uncertainty remains explicit.",
        )
E       TypeError: Learning.__init__() got an unexpected keyword argument 'learning_id'

tests/epistemic/test_sedimented_memory.py:23: TypeError
______________________ test_memory_has_distinct_identity _______________________

    def test_memory_has_distinct_identity():
>       governed = make_governed(
            SedimentationTarget.MEMORY
        )

tests/epistemic/test_sedimented_memory.py:130: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/epistemic/test_sedimented_memory.py:36: in make_governed
    learning = make_learning()
               ^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def make_learning() -> Learning:
>       return Learning(
            learning_id="LEARN-006A",
            verification_identifier="VER-006A",
            meaning="The organism learned a durable semantic conclusion.",
            provenance_identifier="PROV-006A",
            uncertainty="Residual uncertainty remains explicit.",
        )
E       TypeError: Learning.__init__() got an unexpected keyword argument 'learning_id'

tests/epistemic/test_sedimented_memory.py:23: TypeError
_________ test_unaccepted_sedimentation_cannot_become_memory[PROPOSED] _________

authority = <SedimentationAuthority.PROPOSED: 'PROPOSED'>

    @pytest.mark.parametrize(
        "authority",
        [
            SedimentationAuthority.PROPOSED,
            SedimentationAuthority.REJECTED,
        ],
    )
    def test_unaccepted_sedimentation_cannot_become_memory(
        authority,
    ):
>       governed = make_governed(
            SedimentationTarget.MEMORY,
            authority=authority,
        )

tests/epistemic/test_sedimented_memory.py:152: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/epistemic/test_sedimented_memory.py:36: in make_governed
    learning = make_learning()
               ^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def make_learning() -> Learning:
>       return Learning(
            learning_id="LEARN-006A",
            verification_identifier="VER-006A",
            meaning="The organism learned a durable semantic conclusion.",
            provenance_identifier="PROV-006A",
            uncertainty="Residual uncertainty remains explicit.",
        )
E       TypeError: Learning.__init__() got an unexpected keyword argument 'learning_id'

tests/epistemic/test_sedimented_memory.py:23: TypeError
_________ test_unaccepted_sedimentation_cannot_become_memory[REJECTED] _________

authority = <SedimentationAuthority.REJECTED: 'REJECTED'>

    @pytest.mark.parametrize(
        "authority",
        [
            SedimentationAuthority.PROPOSED,
            SedimentationAuthority.REJECTED,
        ],
    )
    def test_unaccepted_sedimentation_cannot_become_memory(
        authority,
    ):
>       governed = make_governed(
            SedimentationTarget.MEMORY,
            authority=authority,
        )

tests/epistemic/test_sedimented_memory.py:152: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/epistemic/test_sedimented_memory.py:36: in make_governed
    learning = make_learning()
               ^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def make_learning() -> Learning:
>       return Learning(
            learning_id="LEARN-006A",
            verification_identifier="VER-006A",
            meaning="The organism learned a durable semantic conclusion.",
            provenance_identifier="PROV-006A",
            uncertainty="Residual uncertainty remains explicit.",
        )
E       TypeError: Learning.__init__() got an unexpected keyword argument 'learning_id'

tests/epistemic/test_sedimented_memory.py:23: TypeError
__________ test_knowledge_target_requires_existing_knowledge_receptor __________

    def test_knowledge_target_requires_existing_knowledge_receptor():
>       governed = make_governed(
            SedimentationTarget.KNOWLEDGE
        )

tests/epistemic/test_sedimented_memory.py:164: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/epistemic/test_sedimented_memory.py:36: in make_governed
    learning = make_learning()
               ^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def make_learning() -> Learning:
>       return Learning(
            learning_id="LEARN-006A",
            verification_identifier="VER-006A",
            meaning="The organism learned a durable semantic conclusion.",
            provenance_identifier="PROV-006A",
            uncertainty="Residual uncertainty remains explicit.",
        )
E       TypeError: Learning.__init__() got an unexpected keyword argument 'learning_id'

tests/epistemic/test_sedimented_memory.py:23: TypeError
_________________ test_knowledge_target_does_not_create_memory _________________

    def test_knowledge_target_does_not_create_memory():
>       governed = make_governed(
            SedimentationTarget.KNOWLEDGE
        )

tests/epistemic/test_sedimented_memory.py:175: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/epistemic/test_sedimented_memory.py:36: in make_governed
    learning = make_learning()
               ^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def make_learning() -> Learning:
>       return Learning(
            learning_id="LEARN-006A",
            verification_identifier="VER-006A",
            meaning="The organism learned a durable semantic conclusion.",
            provenance_identifier="PROV-006A",
            uncertainty="Residual uncertainty remains explicit.",
        )
E       TypeError: Learning.__init__() got an unexpected keyword argument 'learning_id'

tests/epistemic/test_sedimented_memory.py:23: TypeError
__________________ test_memory_and_knowledge_remain_distinct ___________________

    def test_memory_and_knowledge_remain_distinct():
>       governed = make_governed(
            SedimentationTarget.MEMORY_AND_KNOWLEDGE
        )

tests/epistemic/test_sedimented_memory.py:193: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/epistemic/test_sedimented_memory.py:36: in make_governed
    learning = make_learning()
               ^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def make_learning() -> Learning:
>       return Learning(
            learning_id="LEARN-006A",
            verification_identifier="VER-006A",
            meaning="The organism learned a durable semantic conclusion.",
            provenance_identifier="PROV-006A",
            uncertainty="Residual uncertainty remains explicit.",
        )
E       TypeError: Learning.__init__() got an unexpected keyword argument 'learning_id'

tests/epistemic/test_sedimented_memory.py:23: TypeError
__________________ test_memory_does_not_mutate_sedimentation ___________________

    def test_memory_does_not_mutate_sedimentation():
>       governed = make_governed(
            SedimentationTarget.MEMORY
        )

tests/epistemic/test_sedimented_memory.py:213: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/epistemic/test_sedimented_memory.py:36: in make_governed
    learning = make_learning()
               ^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def make_learning() -> Learning:
>       return Learning(
            learning_id="LEARN-006A",
            verification_identifier="VER-006A",
            meaning="The organism learned a durable semantic conclusion.",
            provenance_identifier="PROV-006A",
            uncertainty="Residual uncertainty remains explicit.",
        )
E       TypeError: Learning.__init__() got an unexpected keyword argument 'learning_id'

tests/epistemic/test_sedimented_memory.py:23: TypeError
______________________ test_memory_is_not_raw_experience _______________________

    def test_memory_is_not_raw_experience():
>       governed = make_governed(
            SedimentationTarget.MEMORY
        )

tests/epistemic/test_sedimented_memory.py:227: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/epistemic/test_sedimented_memory.py:36: in make_governed
    learning = make_learning()
               ^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def make_learning() -> Learning:
>       return Learning(
            learning_id="LEARN-006A",
            verification_identifier="VER-006A",
            meaning="The organism learned a durable semantic conclusion.",
            provenance_identifier="PROV-006A",
            uncertainty="Residual uncertainty remains explicit.",
        )
E       TypeError: Learning.__init__() got an unexpected keyword argument 'learning_id'

tests/epistemic/test_sedimented_memory.py:23: TypeError
_____________________ test_missing_provenance_is_rejected ______________________

    def test_missing_provenance_is_rejected():
>       governed = make_governed(
            SedimentationTarget.MEMORY
        )

tests/epistemic/test_sedimented_memory.py:250: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/epistemic/test_sedimented_memory.py:36: in make_governed
    learning = make_learning()
               ^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def make_learning() -> Learning:
>       return Learning(
            learning_id="LEARN-006A",
            verification_identifier="VER-006A",
            meaning="The organism learned a durable semantic conclusion.",
            provenance_identifier="PROV-006A",
            uncertainty="Residual uncertainty remains explicit.",
        )
E       TypeError: Learning.__init__() got an unexpected keyword argument 'learning_id'

tests/epistemic/test_sedimented_memory.py:23: TypeError
=========================== short test summary info ============================
FAILED tests/epistemic/test_sedimented_memory.py::test_memory_target_creates_semantic_memory_only
FAILED tests/epistemic/test_sedimented_memory.py::test_memory_preserves_sedimentation_identity
FAILED tests/epistemic/test_sedimented_memory.py::test_memory_preserves_meaning
FAILED tests/epistemic/test_sedimented_memory.py::test_memory_preserves_provenance
FAILED tests/epistemic/test_sedimented_memory.py::test_memory_preserves_uncertainty
FAILED tests/epistemic/test_sedimented_memory.py::test_memory_has_distinct_identity
FAILED tests/epistemic/test_sedimented_memory.py::test_unaccepted_sedimentation_cannot_become_memory[PROPOSED]
FAILED tests/epistemic/test_sedimented_memory.py::test_unaccepted_sedimentation_cannot_become_memory[REJECTED]
FAILED tests/epistemic/test_sedimented_memory.py::test_knowledge_target_requires_existing_knowledge_receptor
FAILED tests/epistemic/test_sedimented_memory.py::test_knowledge_target_does_not_create_memory
FAILED tests/epistemic/test_sedimented_memory.py::test_memory_and_knowledge_remain_distinct
FAILED tests/epistemic/test_sedimented_memory.py::test_memory_does_not_mutate_sedimentation
FAILED tests/epistemic/test_sedimented_memory.py::test_memory_is_not_raw_experience
FAILED tests/epistemic/test_sedimented_memory.py::test_missing_provenance_is_rejected
14 failed in 0.77s

==========================================================
PCC-04 RUN 006A STOPPED SAFELY
==========================================================
EXIT CODE: 1
FAILURE IS EVIDENCE
LOCAL MUTATION PRESERVED
FAILURE EVIDENCE WILL BE COMMITTED
==========================================================

```

### Result

FAILED / STOPPED

Exit code: `1`

### Repository state
```text
 M work/implementation-reports/PCC-04/PCC-04_RUN006_PRE_IMPLEMENTATION_CANON_LOGIC_AND_ORGANISM_AUDIT.md
?? lib/python/epistemic/sedimented_memory.py
?? tests/epistemic/test_sedimented_memory.py
?? work/implementation-reports/PCC-04/PCC-04_RUN006A_CANONICAL_SEDIMENTED_MEMORY_PHYSIOLOGY.md
?? work/implementation-reports/PCC-04/PCC-04_RUN006A_EXECUTED_BASH.sh
```
[main 718256b] evidence: conserve failed PCC-04 RUN 006A
 5 files changed, 1136 insertions(+)
 create mode 100644 lib/python/epistemic/sedimented_memory.py
 create mode 100644 tests/epistemic/test_sedimented_memory.py
 create mode 100644 work/implementation-reports/PCC-04/PCC-04_RUN006A_CANONICAL_SEDIMENTED_MEMORY_PHYSIOLOGY.md
 create mode 100644 work/implementation-reports/PCC-04/PCC-04_RUN006A_EXECUTED_BASH.sh
To https://github.com/caliofmarian-ai/AI-Toolkit.git
   f69964a..718256b  main -> main
