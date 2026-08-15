PCC-04 RUN 006D
IMPORT TOPOLOGY RECOVERY

Verified directly from repository:

tests/epistemic/test_sedimented_memory.py imports:
    epistemic.*

tests/epistemic/test_sedimentation.py imports:
    python.epistemic.*

Therefore repository regression requires both import roots:

    lib
    lib/python

Execution environment:

    PYTHONPATH=lib:lib/python

NO PHYSIOLOGY MUTATION.
NO TEST MUTATION.
NO CANON MUTATION.
VERIFICATION + EVIDENCE CONSERVATION ONLY.
