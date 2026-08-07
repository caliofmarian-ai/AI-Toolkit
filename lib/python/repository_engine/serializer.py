import json
from dataclasses import asdict


class RepositoryProfileSerializer:
    """Serializes RepositoryProfile to various formats.

    Centralises all serialization logic so RepositoryProfile itself
    does not carry format concerns.  New formats (Markdown, HTML, etc.)
    can be added here without touching the model.
    """

    @staticmethod
    def to_dict(profile) -> dict:
        return asdict(profile)

    @staticmethod
    def to_json(profile, indent: int = 2) -> str:
        return json.dumps(RepositoryProfileSerializer.to_dict(profile), indent=indent)
