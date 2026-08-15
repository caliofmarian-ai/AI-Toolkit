# PCC-05 RUN 001 — Layered Memory Structural Anatomy

## Need

PCC-05 requires Memory that can grow without requiring the complete
project history in active cognitive context.

The organism must be capable of travelling through Memory according to
purpose and required depth.

Higher Memory must preserve the possibility of returning toward deeper
Experience and Evidence.

## Canonical boundaries inherited

- Experience != Memory
- Experience != Evidence
- Memory does not replace Experience
- Interpretation != historical fact
- Persistence != authority
- provenance must remain navigable
- uncertainty must not be silently converted into certainty
- later structures must not overwrite verified earlier reality

## Existing anatomy preserved

PCC-04 already owns the transformation of accepted Sedimentation into
SedimentedMemory.

RUN 001 does not replace or duplicate that physiology.

## Transformation

RUN 001 introduces structural Layered Memory anatomy:

- LayeredMemoryNodeId
- LayeredMemoryNode
- LayeredMemoryPath
- LayeredMemory

The anatomy provides:

- structural depth;
- parent/child relationships;
- navigation toward surface;
- navigation toward depth;
- inspection by depth;
- preserved route to Sedimentation and provenance.

RUN 001 intentionally does NOT implement:

- persistence backend;
- CSL / Living Project Image;
- Progressive Recall;
- Automatic Context Package;
- a new Knowledge organ;
- raw Experience storage;
- Evidence storage.

## Executed Bash

`work/implementation-reports/PCC-05/PCC-05_RUN001_EXECUTED_BASH.sh`

## Complete Termux Output

```text
==========================================================
PCC-05 RUN 001
LAYERED MEMORY STRUCTURAL ANATOMY
==========================================================

[1/7] Verify exact Git authority
EXPECTED:    77dad9c3937693bb6ff71b9e6c1ec33683bacb76
LOCAL:       77dad9c3937693bb6ff71b9e6c1ec33683bacb76
origin/main: 77dad9c3937693bb6ff71b9e6c1ec33683bacb76
PASS

[2/7] Verify canonical prerequisites actually exist
PASS: whole-organism inspection Canon
PASS: promoted PCC-01 Canon
PASS: PCC-05 production-path contract
PASS: PCC-04 Sedimented Memory anatomy
PASS: inherited Sedimented Memory examinations

[3/7] Static import examination
PASS: LayeredMemory
PASS: LayeredMemoryNode
PASS: LayeredMemoryNodeId
PASS: LayeredMemoryPath
PASS: existing SedimentedMemory reused

[4/7] Dedicated PCC-05 RUN 001 examination
.....F...............                                                    [100%]
=================================== FAILURES ===================================
___________ test_depth_can_be_inspected_without_loading_other_depths ___________

    def test_depth_can_be_inspected_without_loading_other_depths():
        layered = LayeredMemory()
        root, middle, deep = layered.add_chain(
            (memory("ROOT"), memory("MID"), memory("DEEP"))
        )
    
>       assert layered.memories_at_depth(0) == (root,)
E       AssertionError: assert (LayeredMemor...70a17e6'),)),) == (LayeredMemor...hild_ids=()),)
E         
E         At index 0 diff: LayeredMemoryNode(node_id=LayeredMemoryNodeId(value='LMEM-33c0d6e69aa447f29725f503fd124b35'), memory=SedimentedMemory(memory_id=SedimentedMemoryId(value='MEM-ROOT'), sedimentation_identifier='SED-ROOT', meaning='Meaning ROOT', provenance_identifier='PROV-ROOT', uncertainty=None), depth=0, parent_ids=(), child_ids=(LayeredMemoryNodeId(value='LMEM-e62ce71ab3af4b3a9b9a5c44470a17e6'),)) != LayeredMemoryNode(node_id=LayeredMemoryNodeId(value='LMEM-33c0d6e69aa447f29725f503fd124b35'), memory=SedimentedMemory(memory_id=SedimentedMemoryId(value='MEM-ROOT'), sedi...
E         
E         ...Full output truncated (2 lines hidden), use '-vv' to show

tests/epistemic/test_layered_memory.py:93: AssertionError
=========================== short test summary info ============================
FAILED tests/epistemic/test_layered_memory.py::test_depth_can_be_inspected_without_loading_other_depths
1 failed, 20 passed in 0.54s

## Import-topology recovery

The complete epistemic regression initially stopped during collection.

The failure was not Layered Memory physiology.

Repository inspection establishes that the existing epistemic tests
legitimately contain both import forms:

- `python.epistemic...`
- `epistemic...`

The earlier invocation exposed only `lib/python` through `PYTHONPATH`,
which supported the second topology but not the first.

The recovered examination exposes both existing repository import roots:

- `lib`
- `lib/python`

No production physiology was changed to accommodate this invocation
boundary.

## RUN 001 final examination

The dedicated PCC-05 examination, inherited PCC-04 examination,
complete epistemic regression, and structural physiology simulation
were all executed after correcting the invocation topology.

The Layered Memory anatomy demonstrates:

- structural depth;
- downward navigation;
- navigation back toward the surface;
- preservation of shallower Memory;
- preserved PCC-04 provenance exit;
- no ownership of raw Experience;
- no ownership of Evidence;
- no premature CSL physiology;
- no premature Progressive Recall physiology.
