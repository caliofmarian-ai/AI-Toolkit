from datetime import datetime, timezone

import pytest

from lib.python.experience.model import Experience
from lib.python.experience.provenance_integration import (
    ExperienceProvenance,
    ExperienceProvenanceError,
)


def make_experience():
    return Experience.create()


def test_provenance_preserves_experience_identity():
    experience = make_experience()

    provenance = ExperienceProvenance.observe(
        experience_id=experience.experience_id,
        provenance="dialogue:user",
        mechanism="human-ai-dialogue",
    )

    assert (
        provenance.experience_id
        == experience.experience_id
    )


def test_minimal_provenance_contract_is_traceable():
    experience = make_experience()

    provenance = ExperienceProvenance.observe(
        experience_id=experience.experience_id,
        provenance="terminal:execution",
        mechanism="termux",
        session_context="session:S-001",
        derived_from=(
            "dialogue:instruction",
        ),
    )

    assert (
        provenance.provenance
        == "terminal:execution"
    )
    assert provenance.mechanism == "termux"
    assert (
        provenance.session_context
        == "session:S-001"
    )
    assert provenance.derived_from == (
        "dialogue:instruction",
    )


def test_historical_fact_and_interpretation_are_distinct():
    experience = make_experience()

    provenance = ExperienceProvenance.observe(
        experience_id=experience.experience_id,
        provenance="terminal:evidence",
        mechanism="observation",
        historical_fact="exit_status=1",
        interpretation="execution failed",
    )

    assert (
        provenance.historical_fact
        == "exit_status=1"
    )
    assert (
        provenance.interpretation
        == "execution failed"
    )
    assert (
        provenance.historical_fact
        != provenance.interpretation
    )


def test_provenance_round_trip_preserves_identity():
    experience = make_experience()

    original = ExperienceProvenance.observe(
        experience_id=experience.experience_id,
        provenance="repository:artifact",
        mechanism="git",
        session_context="session:S-002",
        derived_from=(
            "terminal:execution",
            "dialogue:instruction",
        ),
        historical_fact="artifact conserved",
        interpretation="history preserved",
    )

    restored = (
        ExperienceProvenance.from_dict(
            original.to_dict()
        )
    )

    assert restored == original


def test_provenance_does_not_mutate_core_experience():
    experience = make_experience()

    original_id = experience.experience_id
    original_state = experience.state
    original_created_at = experience.created_at

    ExperienceProvenance.observe(
        experience_id=experience.experience_id,
        provenance="dialogue:user",
        mechanism="capture",
    )

    assert (
        experience.experience_id
        == original_id
    )
    assert experience.state == original_state
    assert (
        experience.created_at
        == original_created_at
    )


@pytest.mark.parametrize(
    "field,value",
    [
        ("provenance", ""),
        ("provenance", "   "),
        ("mechanism", ""),
        ("mechanism", "   "),
    ],
)
def test_required_traceability_fields_reject_empty_values(
    field,
    value,
):
    experience = make_experience()

    kwargs = {
        "experience_id": (
            experience.experience_id
        ),
        "provenance": "dialogue:user",
        "mechanism": "capture",
    }

    kwargs[field] = value

    with pytest.raises(
        ExperienceProvenanceError
    ):
        ExperienceProvenance.observe(
            **kwargs
        )


def test_naive_observation_time_is_rejected():
    experience = make_experience()

    with pytest.raises(
        ExperienceProvenanceError
    ):
        ExperienceProvenance(
            experience_id=(
                experience.experience_id
            ),
            provenance="dialogue:user",
            mechanism="capture",
            observed_at=datetime.now(),
        )


def test_invalid_serialized_identity_is_rejected():
    with pytest.raises(
        ExperienceProvenanceError
    ):
        ExperienceProvenance.from_dict(
            {
                "experience_id": "invalid",
                "provenance": "dialogue:user",
                "mechanism": "capture",
                "observed_at": (
                    datetime.now(
                        timezone.utc
                    ).isoformat()
                ),
                "derived_from": [],
            }
        )
