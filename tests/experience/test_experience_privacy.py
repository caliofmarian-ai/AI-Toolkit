from copy import deepcopy

from lib.python.experience.model import Experience
from lib.python.experience.persistence import serialize_experience
from lib.python.experience.privacy import (
    REDACTED,
    is_sensitive_field_name,
    redact_private_data,
)


def test_core_experience_persistence_remains_data_minimal():
    experience = Experience.create().activate()

    representation = serialize_experience(experience)

    assert set(representation) == {
        "schema_version",
        "experience_id",
        "created_at",
        "state",
    }


def test_sensitive_field_names_are_explicitly_recognized():
    for field in (
        "password",
        "secret",
        "token",
        "access_token",
        "refresh-token",
        "authorization",
        "api key",
        "private_key",
        "credentials",
        "email",
        "phone",
        "phone_number",
        "address",
        "date_of_birth",
        "dob",
        "ssn",
        "personal_data",
        "pii",
    ):
        assert is_sensitive_field_name(field)


def test_non_sensitive_domain_fields_are_not_reclassified():
    for field in (
        "experience_id",
        "created_at",
        "state",
        "schema_version",
        "keyword",
        "semantic",
    ):
        assert not is_sensitive_field_name(field)


def test_top_level_sensitive_values_are_redacted():
    source = {
        "result": "ordinary evidence",
        "token": "secret-token",
        "email": "person@example.invalid",
    }

    result = redact_private_data(source)

    assert result == {
        "result": "ordinary evidence",
        "token": REDACTED,
        "email": REDACTED,
    }


def test_nested_sensitive_values_are_redacted():
    source = {
        "semantic": {
            "result": "ordinary",
            "credentials": {
                "username": "ordinary-name",
                "password": "do-not-expose",
            },
        },
        "items": [
            {
                "phone_number": "000000",
                "fact": "preserve this",
            }
        ],
    }

    result = redact_private_data(source)

    assert result["semantic"]["result"] == "ordinary"
    assert result["semantic"]["credentials"] == REDACTED
    assert result["items"][0]["phone_number"] == REDACTED
    assert result["items"][0]["fact"] == "preserve this"


def test_redaction_does_not_mutate_source_evidence():
    source = {
        "semantic": {
            "api_key": "private",
            "fact": "public",
        }
    }
    original = deepcopy(source)

    redact_private_data(source)

    assert source == original


def test_ordinary_evidence_structure_is_conserved():
    source = {
        "semantic": {
            "fact": "the organism remembers evidence",
        },
        "files": [
            "a.md",
            "b.md",
        ],
        "count": 2,
    }

    assert redact_private_data(source) == source


def test_redaction_handles_nested_containers():
    source = {
        "items": (
            {"secret": "one"},
            {"fact": "two"},
        ),
    }

    result = redact_private_data(source)

    assert result == {
        "items": (
            {"secret": REDACTED},
            {"fact": "two"},
        )
    }


def test_privacy_boundary_does_not_change_experience_identity():
    experience = Experience.create()
    before = experience.experience_id

    redact_private_data(
        {
            "experience_id": str(experience.experience_id),
            "secret": "private",
        }
    )

    assert experience.experience_id == before
