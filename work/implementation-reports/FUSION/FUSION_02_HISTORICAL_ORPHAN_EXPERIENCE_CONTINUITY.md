
## Acceptance-test recovery

The first continuity acceptance run exposed an acceptance-test boundary
error, not a production defect.

The failing assertion inspected an arbitrary textual window after the
historical continuity branch. That window crossed into the separate
new-Experience branch and observed the legitimate repository insertion
for newly created Experiences.

Recovery:
- production implementation unchanged
- test constrained to exact historical-orphan branch
- historical continuity must not be persisted as Experience
- new Experience creation must still persist normally

Failure classification:
ACCEPTANCE_TEST_BOUNDARY_ERROR
