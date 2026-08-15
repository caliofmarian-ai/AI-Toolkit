PCC-04 RUN 003A — CAUSAL REPAIR

CAUSE ESTABLISHED FROM COMMITTED ORGANISM:

RUN 003 correctly materialized the canonical physiology:

VERIFICATION -> LEARNING -> SEDIMENTATION

but LearningSedimentationPhysiology.propose_sedimentation() called:

Sedimentation.propose(...)

The actual inherited Sedimentation anatomy has no such method.

The actual anatomy is:

Sedimentation(
    identifier=...,
    title=...,
    provenance_identifier=...,
    statement=...,
    target=...,
    authority=SedimentationAuthority.PROPOSED,
    uncertainty=...,
)

followed by:

SedimentationRepository.register(...)

RUN 003A performs ONLY this causal correction.

NO:
- Canon modification
- Learning redesign
- Sedimentation redesign
- repository redesign
- Memory implementation
- Knowledge implementation
- Living Project Image implementation
- automatic Canonization
- automatic Human Authority
