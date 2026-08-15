# PCC-04 — Sedimentation
## RUN 006B — Exact Anatomy Recovery

### Status

RUNNING

### Git authority

Expected HEAD:

`718256ba9b075d388b6371284a2e0d1208c3c50c`

### Failure being recovered

RUN 006A reached its dedicated physiological examination and produced
14 failures.

The first causal failure was:

`Learning.__init__() got an unexpected keyword argument 'learning_id'`

The failure arose because RUN 006A's examination assumed an anatomy
that does not exist in the conserved organism.

### Authoritative existing anatomy

#### Learning

- `identifier`
- `title`
- `verification_identifier`
- `statement`
- `uncertainty`

#### Sedimentation

- `identifier`
- `title`
- `provenance_identifier`
- `statement`
- `target`
- `authority`
- `uncertainty`

#### GovernedSedimentation

- `sedimentation`
- `governance`
- `reason`

Authority belongs to Sedimentation.

### Recovery rule

The new Sedimented Memory physiology must adapt to the existing
canonical organism.

The existing organism must not be rewritten merely to satisfy the
failed RUN 006A examination.

### Executed Bash

`work/implementation-reports/PCC-04/PCC-04_RUN006B_EXECUTED_BASH.sh`

### Complete Termux output

```text
==========================================================
PCC-04 RUN 006B
EXACT ANATOMY RECOVERY
==========================================================

[1/10] Verify exact Git authority
EXPECTED:    718256ba9b075d388b6371284a2e0d1208c3c50c
LOCAL:       718256ba9b075d388b6371284a2e0d1208c3c50c
origin/main: 718256ba9b075d388b6371284a2e0d1208c3c50c
PASS

[2/10] Verify exact inherited anatomy
Learning: ('identifier', 'title', 'verification_identifier', 'statement', 'uncertainty')
Sedimentation: ('identifier', 'title', 'provenance_identifier', 'statement', 'target', 'authority', 'uncertainty')
GovernedSedimentation: ('sedimentation', 'governance', 'reason')
PASS: exact Learning anatomy
PASS: exact Sedimentation anatomy
PASS: exact GovernedSedimentation anatomy
PASS: authority belongs to Sedimentation

[3/10] Correct RUN 006A physiology against real anatomy
PASS: semantic meaning now uses Sedimentation.statement
PASS: authority now uses Sedimentation.authority
PASS: recovered physiology compiles

[4/10] Replace failed examination with exact organism anatomy
PASS: corrected examination compiles

[5/10] Execute exact RUN 006B examination
.....................                                                    [100%]
21 passed in 0.46s
PASS: RUN 006B dedicated examination

[6/10] Execute complete Sedimentation examination

==================================== ERRORS ====================================
____________ ERROR collecting tests/epistemic/test_sedimentation.py ____________
ImportError while importing test module '/storage/emulated/0/AI-Projects/AI-Toolkit/tests/epistemic/test_sedimentation.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/data/data/com.termux/files/usr/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/epistemic/test_sedimentation.py:5: in <module>
    from python.epistemic.sedimentation import (
E   ModuleNotFoundError: No module named 'python'
=========================== short test summary info ============================
ERROR tests/epistemic/test_sedimentation.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.70s

==========================================================
PCC-04 RUN 006B STOPPED SAFELY
==========================================================
EXIT CODE: 2
FAILURE CONSERVED AS PROJECT EXPERIENCE
NO AUTOMATIC ROLLBACK
==========================================================

```

### Result

FAILED / STOPPED

Exit code: `2`

### Git state at stop
```text
 M lib/python/epistemic/sedimented_memory.py
 M tests/epistemic/test_sedimented_memory.py
 M work/implementation-reports/PCC-04/PCC-04_RUN006A_CANONICAL_SEDIMENTED_MEMORY_PHYSIOLOGY.md
?? work/implementation-reports/PCC-04/PCC-04_RUN006B_EXACT_ANATOMY_RECOVERY.md
?? work/implementation-reports/PCC-04/PCC-04_RUN006B_EXECUTED_BASH.sh
```
[main 4ec2506] evidence: conserve failed PCC-04 RUN 006B
 5 files changed, 391 insertions(+), 77 deletions(-)
 create mode 100644 work/implementation-reports/PCC-04/PCC-04_RUN006B_EXACT_ANATOMY_RECOVERY.md
 create mode 100644 work/implementation-reports/PCC-04/PCC-04_RUN006B_EXECUTED_BASH.sh
To https://github.com/caliofmarian-ai/AI-Toolkit.git
   718256b..4ec2506  main -> main
