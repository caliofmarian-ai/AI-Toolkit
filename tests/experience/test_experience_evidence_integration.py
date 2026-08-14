from pathlib import Path

import pytest

from lib.python.evidence_engine.engine import EvidenceEngine
from lib.python.experience.evidence_integration import (
    ExperienceEvidenceIntegrator,
    ExperienceEvidenceReference,
    InvalidEvidenceKeywordError,
)
from lib.python.experience.model import Experience


def _build_repository(root: Path) -> None:
    package = root / "sample"
    package.mkdir(parents=True)

    (package / "persistent_experience_evidence.md").write_text(
        "# Persistent Experience Evidence\n",
        encoding="utf-8",
    )


def test_experience_can_reference_inherited_evidence_without_identity_change(
    tmp_path,
):
    _build_repository(tmp_path)

    experience = Experience.create()
    identity_before = experience.experience_id

    engine = EvidenceEngine(tmp_path)
    integrator = ExperienceEvidenceIntegrator(engine)

    reference = integrator.find_for_experience(
        experience_id=experience.experience_id,
        keyword="experience",
    )

    assert isinstance(reference, ExperienceEvidenceReference)
    assert reference.experience_id == identity_before
    assert experience.experience_id == identity_before


def test_evidence_remains_evidence_and_does_not_become_experience(
    tmp_path,
):
    _build_repository(tmp_path)

    experience = Experience.create()

    reference = ExperienceEvidenceIntegrator(
        EvidenceEngine(tmp_path)
    ).find_for_experience(
        experience_id=experience.experience_id,
        keyword="evidence",
    )

    assert isinstance(reference.evidence, dict)
    assert reference is not experience
    assert reference.evidence is not experience


def test_inherited_evidence_engine_is_used_directly(tmp_path):
    _build_repository(tmp_path)

    experience = Experience.create()
    engine = EvidenceEngine(tmp_path)

    direct = engine.find("evidence")

    integrated = ExperienceEvidenceIntegrator(
        engine
    ).find_for_experience(
        experience_id=experience.experience_id,
        keyword="evidence",
    )

    assert integrated.evidence == direct


def test_evidence_reference_preserves_query_provenance(tmp_path):
    _build_repository(tmp_path)

    experience = Experience.create()

    reference = ExperienceEvidenceIntegrator(
        EvidenceEngine(tmp_path)
    ).find_for_experience(
        experience_id=experience.experience_id,
        keyword="experience",
    )

    assert reference.keyword == "experience"
    assert reference.experience_id == experience.experience_id


def test_discovered_repository_evidence_is_explicit(tmp_path):
    _build_repository(tmp_path)

    experience = Experience.create()

    reference = ExperienceEvidenceIntegrator(
        EvidenceEngine(tmp_path)
    ).find_for_experience(
        experience_id=experience.experience_id,
        keyword="evidence",
    )

    assert reference.has_evidence is True
    assert (
        "sample/persistent_experience_evidence.md"
        in reference.evidence["docs"]
    )


def test_absence_of_evidence_remains_explicit(tmp_path):
    _build_repository(tmp_path)

    experience = Experience.create()

    reference = ExperienceEvidenceIntegrator(
        EvidenceEngine(tmp_path)
    ).find_for_experience(
        experience_id=experience.experience_id,
        keyword="definitely-not-present",
    )

    assert reference.has_evidence is False
    assert reference.experience_id == experience.experience_id


@pytest.mark.parametrize("keyword", ["", "   "])
def test_empty_evidence_keyword_is_rejected(tmp_path, keyword):
    experience = Experience.create()

    integrator = ExperienceEvidenceIntegrator(
        EvidenceEngine(tmp_path)
    )

    with pytest.raises(InvalidEvidenceKeywordError):
        integrator.find_for_experience(
            experience_id=experience.experience_id,
            keyword=keyword,
        )


def test_evidence_lookup_does_not_mutate_experience(tmp_path):
    _build_repository(tmp_path)

    experience = Experience.create()

    before = (
        experience.experience_id,
        experience.created_at,
        experience.state,
    )

    ExperienceEvidenceIntegrator(
        EvidenceEngine(tmp_path)
    ).find_for_experience(
        experience_id=experience.experience_id,
        keyword="evidence",
    )

    after = (
        experience.experience_id,
        experience.created_at,
        experience.state,
    )

    assert after == before
