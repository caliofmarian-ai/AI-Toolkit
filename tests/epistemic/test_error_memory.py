from dataclasses import FrozenInstanceError

import pytest

from lib.python.epistemic.error_memory import (
    ErrorMemory,
    ErrorMemoryOrgan,
    FailureKind,
    FailureOrigin,
    seed_demonstrated_ai_toolkit_failures,
)


def make_memory(identity: str = "ERR-TEST-001") -> ErrorMemory:
    return ErrorMemory(
        identity=identity,
        title="Demonstrated Test Failure",
        kind=FailureKind.EXECUTION,
        symptom="A demonstrated execution stopped.",
        cause="A known precondition was not satisfied.",
        recovery="The precondition was restored.",
        prevention_rule="Verify the precondition before execution.",
        origin=FailureOrigin(
            repository_path="work/implementation-reports/example.md",
            run_identity="TEST RUN",
            git_commit="abc123",
        ),
    )


def test_error_memory_has_human_readable_semantic_identity():
    memory = make_memory()

    assert memory.semantic_identity == (
        "ERR-TEST-001 — Demonstrated Test Failure"
    )


def test_error_memory_preserves_navigable_origin():
    memory = make_memory()

    assert memory.origin.repository_path == (
        "work/implementation-reports/example.md"
    )
    assert memory.origin.run_identity == "TEST RUN"
    assert memory.origin.git_commit == "abc123"


def test_error_memory_is_immutable():
    memory = make_memory()

    with pytest.raises(FrozenInstanceError):
        memory.title = "Rewritten history"


def test_organ_remember_returns_new_body_without_mutating_previous_body():
    empty = ErrorMemoryOrgan()
    memory = make_memory()

    evolved = empty.remember(memory)

    assert empty.memories == ()
    assert evolved.memories == (memory,)


def test_duplicate_error_identity_is_rejected():
    memory = make_memory()

    with pytest.raises(ValueError):
        ErrorMemoryOrgan((memory, memory))


def test_failure_can_be_classified_by_kind():
    execution = make_memory("ERR-TEST-EXECUTION")
    permission = ErrorMemory(
        identity="ERR-TEST-PERMISSION",
        title="Permission Failure",
        kind=FailureKind.PERMISSION,
        symptom="Permission denied.",
        cause="Execution mode was invalid.",
        recovery="Used explicit interpreter.",
        prevention_rule="Use explicit interpreter.",
        origin=FailureOrigin(
            repository_path="history/permission.txt",
            run_identity="RUN PERMISSION",
        ),
    )

    organ = ErrorMemoryOrgan((execution, permission))

    assert organ.by_kind(FailureKind.PERMISSION) == (permission,)
    assert organ.by_kind(FailureKind.EXECUTION) == (execution,)


def test_recurrence_warning_preserves_rule_and_origin():
    memory = make_memory()
    organ = ErrorMemoryOrgan((memory,))

    warnings = organ.recurrence_warnings(kind=FailureKind.EXECUTION)

    assert len(warnings) == 1
    warning = warnings[0]

    assert warning.error_identity == memory.identity
    assert warning.error_title == memory.title
    assert warning.prevention_rule == memory.prevention_rule
    assert warning.origin == memory.origin


def test_recurrence_warning_does_not_claim_execution_authority():
    memory = make_memory()
    warning = ErrorMemoryOrgan((memory,)).recurrence_warnings()[0]

    assert not hasattr(warning, "allow_execution")
    assert not hasattr(warning, "block_execution")
    assert not hasattr(warning, "canonical")


def test_non_demonstrated_memory_does_not_generate_prevention_warning():
    memory = ErrorMemory(
        identity="ERR-HYPOTHESIS",
        title="Hypothetical Failure",
        kind=FailureKind.UNKNOWN,
        symptom="Possible symptom.",
        cause="Possible cause.",
        recovery="Possible recovery.",
        prevention_rule="Possible prevention.",
        origin=FailureOrigin(
            repository_path="research/hypothesis.md",
            run_identity="RESEARCH",
        ),
        demonstrated=False,
    )

    organ = ErrorMemoryOrgan((memory,))

    assert organ.recurrence_warnings() == ()


def test_seed_contains_demonstrated_pcc06_failures():
    organ = seed_demonstrated_ai_toolkit_failures()

    identities = {memory.identity for memory in organ.memories}

    assert "ERR-0001" in identities
    assert "ERR-0002" in identities

    permission = organ.find("ERR-0001")
    validation = organ.find("ERR-0002")

    assert permission is not None
    assert validation is not None

    assert permission.kind == FailureKind.PERMISSION
    assert validation.kind == FailureKind.VALIDATION

    assert "PCC-06" in permission.origin.repository_path
    assert "PCC-06" in validation.origin.repository_path


def test_seeded_memories_generate_recurrence_warnings():
    organ = seed_demonstrated_ai_toolkit_failures()

    warnings = organ.recurrence_warnings()

    assert len(warnings) == 2
    assert {warning.error_identity for warning in warnings} == {
        "ERR-0001",
        "ERR-0002",
    }


@pytest.mark.parametrize(
    "field,value",
    [
        ("identity", ""),
        ("title", " "),
        ("symptom", ""),
        ("cause", ""),
        ("recovery", ""),
        ("prevention_rule", ""),
    ],
)
def test_structurally_empty_error_memory_is_rejected(field, value):
    kwargs = dict(
        identity="ERR-VALID",
        title="Valid",
        kind=FailureKind.EXECUTION,
        symptom="Symptom",
        cause="Cause",
        recovery="Recovery",
        prevention_rule="Prevention",
        origin=FailureOrigin(
            repository_path="history/body.md",
            run_identity="RUN",
        ),
    )
    kwargs[field] = value

    with pytest.raises(ValueError):
        ErrorMemory(**kwargs)


def test_empty_origin_is_rejected():
    with pytest.raises(ValueError):
        FailureOrigin(
            repository_path="",
            run_identity="RUN",
        )

    with pytest.raises(ValueError):
        FailureOrigin(
            repository_path="history/body.md",
            run_identity="",
        )
