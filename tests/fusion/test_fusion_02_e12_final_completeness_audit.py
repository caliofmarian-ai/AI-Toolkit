from __future__ import annotations

import ast
from pathlib import Path

from python.ai_platform.cognitive_coordination import (
    InformationNeed,
    JourneyState,
)


PRODUCTION = Path(
    "lib/python/ai_platform/cognitive_coordination.py"
)

ARCHITECTURE = Path(
    "audit/PHASE I–XI → EXECUTABLE ARCHITECTURE.md"
)

PHYSIOLOGY = Path(
    "audit/PHASE III — NATIVE COGNITIVE PHYSIOLOGY SYNTHESIS.md"
)


def _production_source() -> str:
    return PRODUCTION.read_text(encoding="utf-8")


def _method_names() -> set[str]:
    tree = ast.parse(_production_source())

    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        )
    }


def test_e12_contract_documents_remain_present():
    architecture = ARCHITECTURE.read_text(
        encoding="utf-8",
    )

    physiology = PHYSIOLOGY.read_text(
        encoding="utf-8",
    )

    for token in (
        "Cognitive Coordination Loop",
        "SATISFIED",
        "PARTIAL",
        "UNKNOWN",
        "BLOCKED",
        "HUMAN_REQUIRED",
        "FORBIDDEN",
        "NO_EPISTEMIC_GAIN",
    ):
        assert token.lower() in architecture.lower()

    for token in (
        "Information Need",
        "Cognitive Traversal Loop",
        "Need satisfied",
        "Authority boundary",
        "Repeated identity",
        "Traversal cycle",
        "Diminishing epistemic gain",
        "Human decision required",
    ):
        assert token.lower() in physiology.lower()


def test_e12_has_one_coordinator_not_parallel_organ():
    source = _production_source()

    assert source.count(
        "class EpistemicCognitiveCoordinator"
    ) == 1


def test_e12_preserves_search_and_read_as_separate_organs():
    methods = _method_names()

    assert "execute_search_navigation" in methods
    assert "execute_read_navigation" in methods


def test_e12_exposes_mandatory_outcome_vocabulary():
    source = _production_source()

    for status in (
        "SATISFIED",
        "PARTIAL",
        "UNKNOWN",
        "BLOCKED",
        "HUMAN_REQUIRED",
        "FORBIDDEN",
        "NO_EPISTEMIC_GAIN",
    ):
        assert status in source


def test_information_need_remains_distinct_from_journey():
    assert InformationNeed is not JourneyState

    assert "question" in InformationNeed.__annotations__
    assert "objective" in InformationNeed.__annotations__

    assert "status" in JourneyState.__annotations__
    assert "visited" in JourneyState.__annotations__
    assert "stopping_reason" in JourneyState.__annotations__


def test_journey_remains_distinct_from_working_context():
    source = _production_source()

    assert "JourneyState" in source
    assert "WorkingContext" in source


def test_e12_contains_bounded_step_evaluation():
    methods = _method_names()

    candidates = {
        name
        for name in methods
        if (
            "step" in name.lower()
            or "evaluate" in name.lower()
            or "transition" in name.lower()
        )
    }

    assert candidates


def test_e12_contains_loop_guard():
    methods = _method_names()

    candidates = {
        name
        for name in methods
        if (
            "guard" in name.lower()
            or "cycle" in name.lower()
            or "repeat" in name.lower()
        )
    }

    assert candidates


def test_e12_stop_vocabulary_is_observable():
    source = _production_source().lower()

    stop_semantics = (
        "repeated_need",
        "repeated_result",
        "repeated_identity",
        "cycle",
        "authority",
        "ambiguous",
        "unavailable",
        "epistemic_gain",
    )

    missing = [
        token
        for token in stop_semantics
        if token not in source
    ]

    assert not missing, (
        "Missing E12 stop semantics: "
        + ", ".join(missing)
    )


def test_e12_does_not_claim_retrieval_is_authority():
    source = _production_source()

    assert "authority_conferred" in source
    assert "human_authority_preserved" in source


def test_e12_unknown_remains_valid():
    source = _production_source()

    assert "unknown_is_valid" in source


def test_e12_does_not_own_provider_invocation():
    source = _production_source()

    for term in (
        ".complete(",
        "adapter.complete(",
    ):
        assert term not in source


def test_e12_production_file_is_ast_valid():
    ast.parse(_production_source())
