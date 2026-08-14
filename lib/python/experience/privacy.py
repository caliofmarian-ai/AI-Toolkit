"""Privacy boundary for PCC-01 Persistent Experience.

Privacy does not redefine Experience, Memory, Evidence, or authority.

The boundary minimizes information leaving Experience integrations and
redacts values associated with explicitly sensitive field names.

Redaction is structural and conservative. It does not claim to discover
arbitrary secrets hidden inside unrestricted prose.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


REDACTED = "[REDACTED]"

_SENSITIVE_FIELD_NAMES = frozenset(
    {
        "password",
        "passwd",
        "secret",
        "token",
        "access_token",
        "refresh_token",
        "authorization",
        "api_key",
        "apikey",
        "private_key",
        "credential",
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
    }
)


def _normalized_field_name(value: Any) -> str:
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")


def is_sensitive_field_name(value: Any) -> bool:
    """Return whether a mapping key is explicitly privacy-sensitive."""

    return _normalized_field_name(value) in _SENSITIVE_FIELD_NAMES


def redact_private_data(value: Any) -> Any:
    """Return a privacy-safe structural copy of integration data.

    Mapping values under explicitly sensitive field names are replaced
    by REDACTED. Nested mappings and ordinary containers are traversed.

    Input objects are never mutated.
    """

    if isinstance(value, Mapping):
        return {
            key: (
                REDACTED
                if is_sensitive_field_name(key)
                else redact_private_data(item)
            )
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [redact_private_data(item) for item in value]

    if isinstance(value, tuple):
        return tuple(redact_private_data(item) for item in value)

    if isinstance(value, set):
        return {redact_private_data(item) for item in value}

    return value
