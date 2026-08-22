from pathlib import Path

import pytest

from python.ai_platform.historical_experience_recovery import (
    HistoricalExperienceContinuity,
)
from python.experience.repository import ExperienceNotFoundError


TARGET_SESSION = "AI-SESSION-3BAD91C0B88C"
TARGET_EXPERIENCE = "3e264780-2ce0-491d-8903-41f0af66c6cb"


def _source() -> str:
    return Path(
        "lib/python/runtime/organism.py"
    ).read_text(encoding="utf-8")


def test_real_context_reconstruction_calls_conversation_session():
    source = Path(
        "lib/python/ai_platform/conversation_context.py"
    ).read_text(encoding="utf-8")

    assert (
        "recovered = self.organism.conversation_session(session_id)"
        in source
    )


def test_organism_repository_lookup_remains_first_authority():
    source = _source()

    repository_index = source.index(
        "experience = repository.get("
    )
    continuity_index = source.index(
        "continuity = historical_continuity(session)"
    )

    assert repository_index < continuity_index


def test_only_experience_not_found_enters_continuity():
    source = _source()

    assert "except ExperienceNotFoundError:" in source

    exception_index = source.index(
        "except ExperienceNotFoundError:"
    )
    continuity_index = source.index(
        "continuity = historical_continuity(session)"
    )

    assert exception_index < continuity_index


def test_no_broad_exception_is_used_for_historical_continuity():
    source = _source()

    lookup_start = source.index(
        "try:",
        source.index(
            "repository = prepare_experience_repository("
        ),
    )

    lookup_end = source.index(
        "else:",
        lookup_start,
    )

    boundary = source[lookup_start:lookup_end]

    assert "except Exception" not in boundary
    assert "except BaseException" not in boundary


def test_historical_created_at_is_not_fabricated():
    source = _source()

    continuity_start = source.index(
        "continuity = historical_continuity(session)"
    )

    canonical_else = source.index(
        "            else:",
        continuity_start,
    )

    branch = source[
        continuity_start:canonical_else
    ]

    assert '"created_at": None' in branch
    assert "isoformat()" not in branch


def test_original_historical_identity_is_exposed():
    source = _source()

    assert (
        '"experience_id": str(continuity.experience_id)'
        in source
    )


def test_recovery_provenance_is_exposed():
    source = _source()

    assert '"recovery_provenance": (' in source
    assert "continuity.recovery_provenance" in source


def test_created_at_epistemic_status_is_exposed():
    source = _source()

    assert '"exact_created_at_recoverable": (' in source
    assert (
        "continuity.exact_created_at_recoverable"
        in source
    )


def test_canonical_experience_still_uses_persisted_created_at():
    source = _source()

    assert (
        '"created_at": experience.created_at.isoformat()'
        in source
    )


def test_canonical_experience_is_not_marked_historical():
    source = _source()

    assert '"historical_continuity": False' in source


def test_historical_continuity_is_not_added_to_repository():
    source = _source()

    continuity_start = source.index(
        "continuity = historical_continuity(session)"
    )

    canonical_else = source.index(
        "            else:",
        continuity_start,
    )

    historical_branch = source[
        continuity_start:canonical_else
    ]

    assert "repository.add(" not in historical_branch
    assert "repository.save(" not in historical_branch
    assert "repository.create(" not in historical_branch


def test_recovery_module_is_not_canonical_experience():
    recovery = Path(
        "lib/python/ai_platform/historical_experience_recovery.py"
    ).read_text(encoding="utf-8")

    assert "This is deliberately not an Experience domain entity." in recovery
    assert "exact original created_at must remain explicitly irrecoverable" in recovery


def test_demonstrated_historical_identity_remains_fixed():
    recovery_test = Path(
        "tests/fusion/test_fusion_02_historical_orphan_experience_recovery.py"
    ).read_text(encoding="utf-8")

    continuity_test = Path(
        "tests/fusion/test_fusion_02_historical_orphan_experience_continuity.py"
    ).read_text(encoding="utf-8")

    assert TARGET_EXPERIENCE in recovery_test
    assert TARGET_SESSION in continuity_test


def test_required_runtime_types_exist():
    assert issubclass(
        ExperienceNotFoundError,
        Exception,
    )

    assert HistoricalExperienceContinuity is not None
