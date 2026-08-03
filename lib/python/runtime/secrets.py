"""
CORE-021 — Runtime Secret Manager
CANON-055 §5, CANON-056 §13

Loads secrets from environment variables and validates their presence.
Secrets are never written to disk or logged.
"""

import os
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SecretValidationResult:
    valid: bool
    missing: List[str]
    present: List[str]


class SecretManager:
    """
    Manages Runtime secrets loaded from environment variables.

    Secrets are accessed by symbolic name.  Actual values are never
    exposed in logs or reports.
    """

    # Required secrets (warn if missing)
    _OPTIONAL_SECRETS = [
        "GITHUB_TOKEN",
        "GITHUB_WEBHOOK_SECRET",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
    ]

    def __init__(self):
        self._secrets: Dict[str, str] = {}
        self._loaded = False

    def load(self) -> None:
        """Load secrets from the environment."""
        for key in self._OPTIONAL_SECRETS:
            value = os.environ.get(key, "")
            if value:
                self._secrets[key] = value
        self._loaded = True

    def get(self, key: str, default: str = "") -> str:
        """Return the secret value for *key* or *default*."""
        return self._secrets.get(key, os.environ.get(key, default))

    def validate(self) -> SecretValidationResult:
        """
        Validate that the optional secrets are present.

        The Runtime can operate without all secrets, but some
        integrations (GitHub, Telegram) will be disabled.
        """
        present = [k for k in self._OPTIONAL_SECRETS if self.get(k)]
        missing = [k for k in self._OPTIONAL_SECRETS if not self.get(k)]
        return SecretValidationResult(
            valid=True,  # All secrets are optional
            missing=missing,
            present=present,
        )

    def summary(self) -> dict:
        """Return a redacted summary (no secret values)."""
        return {
            "loaded": self._loaded,
            "present": [k for k in self._OPTIONAL_SECRETS if self.get(k)],
            "missing": [k for k in self._OPTIONAL_SECRETS if not self.get(k)],
        }
