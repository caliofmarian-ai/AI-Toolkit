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
OWNER_SESSION_COOKIE = "ai_toolkit_owner_session"
OWNER_SESSION_PURPOSE = b"AI-Toolkit/FUSION-02/owner-web-session/v1"


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

    def session_cookie_value(self) -> str:
        """
        Derive a browser-session verifier from the configured Owner secret.

        The Owner token itself is never returned to the browser after login
        and is never embedded in HTML or JavaScript.
        """
        if not self.configured:
            return ""
        return hmac.new(
            self._token.encode("utf-8"),
            OWNER_SESSION_PURPOSE,
            hashlib.sha256,
        ).hexdigest()

    def authenticate_cookie(
        self,
        cookie_header: str,
    ) -> OwnerAccessDecision:
        if not self.configured:
            return OwnerAccessDecision(
                authenticated=False,
                role="NONE",
                human_authority=False,
                reason="OWNER_ACCESS_NOT_CONFIGURED",
            )

        supplied = ""
        for part in str(cookie_header or "").split(";"):
            name, separator, value = part.strip().partition("=")
            if (
                separator
                and name == OWNER_SESSION_COOKIE
            ):
                supplied = value.strip()
                break

        expected = self.session_cookie_value()

        if (
            not supplied
            or not hmac.compare_digest(expected, supplied)
        ):
            return OwnerAccessDecision(
                authenticated=False,
                role="NONE",
                human_authority=False,
                reason="OWNER_WEB_SESSION_REQUIRED",
            )

        return OwnerAccessDecision(
            authenticated=True,
            role="OWNER",
            human_authority=True,
            reason="AUTHENTICATED_OWNER_WEB_SESSION",
        )

    def authenticate_request(
        self,
        headers: Mapping[str, str] | None = None,
    ) -> OwnerAccessDecision:
        """
        Preserve Bearer authentication and additionally accept the
        server-derived HttpOnly Owner web session.

        URL knowledge alone still confers no authority.
        """
        headers = headers or {}

        bearer = self.authenticate(headers)
        if bearer.authenticated:
            return bearer

        return self.authenticate_cookie(
            str(headers.get("Cookie", ""))
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
