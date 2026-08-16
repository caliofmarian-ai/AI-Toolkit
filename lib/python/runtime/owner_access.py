"""
FUSION-02 — private single-owner application access boundary.

This is deliberately NOT a multi-user identity system.

The current AI-Toolkit generation is:
PRIVATE
SINGLE-OWNER
OWNER-OPERATED

Knowledge of the deployment URL confers no authority.

The owner credential is supplied through runtime environment configuration.
No owner secret is persisted in the repository.

This boundary does not create tenants, collaborators, Partner Portal,
public registration, or external-user privileges.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
from dataclasses import dataclass
from typing import Mapping


OWNER_TOKEN_ENV = "AI_TOOLKIT_OWNER_TOKEN"


@dataclass(frozen=True)
class OwnerAccessDecision:
    authenticated: bool
    role: str
    human_authority: bool
    reason: str

    def as_dict(self) -> dict:
        return {
            "authenticated": self.authenticated,
            "role": self.role,
            "human_authority": self.human_authority,
            "reason": self.reason,
        }


class OwnerAccessBoundary:
    """
    Fail-closed authentication boundary for privileged AI-Toolkit routes.

    Authentication proves access to the private owner surface.
    It does not itself mutate Canon or manufacture epistemic authority.
    """

    def __init__(self, token: str | None = None) -> None:
        configured = token if token is not None else os.environ.get(
            OWNER_TOKEN_ENV, ""
        )
        self._token = configured.strip()

    @property
    def configured(self) -> bool:
        return bool(self._token)

    @staticmethod
    def generate_token() -> str:
        return secrets.token_urlsafe(48)

    def authenticate(
        self,
        headers: Mapping[str, str] | None = None,
    ) -> OwnerAccessDecision:
        if not self.configured:
            return OwnerAccessDecision(
                authenticated=False,
                role="NONE",
                human_authority=False,
                reason="OWNER_ACCESS_NOT_CONFIGURED",
            )

        headers = headers or {}
        authorization = str(headers.get("Authorization", "")).strip()

        if not authorization.startswith("Bearer "):
            return OwnerAccessDecision(
                authenticated=False,
                role="NONE",
                human_authority=False,
                reason="OWNER_CREDENTIAL_REQUIRED",
            )

        supplied = authorization[7:].strip()

        expected_digest = hashlib.sha256(
            self._token.encode("utf-8")
        ).digest()
        supplied_digest = hashlib.sha256(
            supplied.encode("utf-8")
        ).digest()

        if not hmac.compare_digest(expected_digest, supplied_digest):
            return OwnerAccessDecision(
                authenticated=False,
                role="NONE",
                human_authority=False,
                reason="OWNER_CREDENTIAL_REJECTED",
            )

        return OwnerAccessDecision(
            authenticated=True,
            role="OWNER",
            human_authority=True,
            reason="AUTHENTICATED_OWNER",
        )

    def public_state(self) -> dict:
        return {
            "mode": "PRIVATE_SINGLE_OWNER",
            "configured": self.configured,
            "public_operational_access": False,
            "multi_user": False,
            "external_repository_access": False,
            "partner_portal": False,
        }
