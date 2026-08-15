# PCC-04 — RUN 006D — Import Topology Recovery

## Need

RUN 006C failed because its execution environment did not represent the
two import roots actually present in the repository.

## Verified repository anatomy

New Sedimented Memory examination imports:

`epistemic.*`

Inherited Sedimentation examination imports:

`python.epistemic.*`

Therefore the verified execution environment is:

`PYTHONPATH=lib:lib/python`

## Mutation

No organism physiology is modified.

No examination is modified.

No Canon is modified.

## Executed Bash

`work/implementation-reports/PCC-04/PCC-04_RUN006D_EXECUTED_BASH.sh`

## Complete Termux output

```text
==========================================================
PCC-04 RUN 006D
VERIFIED IMPORT TOPOLOGY RECOVERY
==========================================================

[1/6] Git authority
EXPECTED PREFIX: 9c6ec6f
LOCAL:           9c6ec6f69153108c4d4ec2e190cf9391eac0bc2a
origin/main:     9c6ec6f69153108c4d4ec2e190cf9391eac0bc2a
PASS

[2/6] Prove both actual import forms
PASS: epistemic.sedimentation
PASS: python.epistemic.sedimentation
PASS: both repository import roots coexist

[3/6] Dedicated Sedimented Memory examination
.....................                                                    [100%]
21 passed in 0.26s
PASS: dedicated examination

[4/6] Inherited Sedimentation examination
.........................................                                [100%]
41 passed in 0.52s
PASS: inherited Sedimentation examination

[5/6] Complete epistemic regression
........................................................................ [ 40%]
........................................................................ [ 81%]
................................                                         [100%]
176 passed in 1.63s
PASS: complete epistemic regression

[6/6] Verify RUN 006D changed evidence only
 M work/implementation-reports/PCC-04/PCC-04_RUN006C_VERIFIED_REGRESSION_AND_CONSERVATION.md
?? work/implementation-reports/PCC-04/PCC-04_RUN006D_EXECUTED_BASH.sh
?? work/implementation-reports/PCC-04/PCC-04_RUN006D_IMPORT_TOPOLOGY_RECOVERY.md
?? work/memory/3a93f5bbf282466ea43c9db3125fe9b9.json
ERROR: organism/test mutation detected: work/memory/3a93f5bbf282466ea43c9db3125fe9b9.json

==========================================================
RUN 006D STOPPED
EXIT CODE: 1
==========================================================

```

## Result
STOPPED — exit code 1
