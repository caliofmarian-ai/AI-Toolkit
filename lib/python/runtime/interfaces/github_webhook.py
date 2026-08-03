"""
CORE-021 — GitHub Webhook Host
CANON-055 §5, CANON-048

Receives GitHub webhook payloads and converts them into canonical
Runtime Events dispatched to the Event Bus.

Supported event types:
    push, pull_request, issues, release, workflow_run,
    discussion, repository, create, delete, ping
"""

import hashlib
import hmac
import json
import logging
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

from python.runtime.event_dispatcher import EventDispatcher, RuntimeEvent

logger = logging.getLogger(__name__)

# Mapping from GitHub event header value to canonical Runtime event type
_EVENT_MAP: Dict[str, str] = {
    "push": "github.push",
    "pull_request": "github.pull_request",
    "issues": "github.issues",
    "issue_comment": "github.issue_comment",
    "release": "github.release",
    "workflow_run": "github.workflow_run",
    "workflow_job": "github.workflow_job",
    "discussion": "github.discussion",
    "discussion_comment": "github.discussion_comment",
    "repository": "github.repository",
    "create": "github.create",
    "delete": "github.delete",
    "ping": "github.ping",
    "check_run": "github.check_run",
    "check_suite": "github.check_suite",
    "status": "github.status",
}


class GitHubWebhookHost:
    """
    Validates and processes incoming GitHub webhook payloads.
    """

    def __init__(
        self,
        dispatcher: EventDispatcher,
        webhook_secret: str = "",
    ):
        self._dispatcher = dispatcher
        self._webhook_secret = webhook_secret
        self._processed_count = 0

    def process(self, event_type: str, signature: str, body: bytes) -> dict:
        """
        Validate signature, parse payload, and emit a Runtime event.

        Returns a result dict indicating success or failure.
        """
        # Signature validation (skip when secret is not configured)
        if self._webhook_secret:
            if not self._verify_signature(body, signature):
                logger.warning("GitHub webhook: invalid signature for event %s", event_type)
                return {"ok": False, "error": "invalid signature"}

        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError as exc:
            logger.warning("GitHub webhook: JSON parse error: %s", exc)
            return {"ok": False, "error": f"invalid JSON: {exc}"}

        canonical_type = _EVENT_MAP.get(event_type, f"github.{event_type}")
        event = RuntimeEvent(
            event_type=canonical_type,
            source="github.webhook",
            payload={
                "github_event": event_type,
                "payload": payload,
            },
        )
        self._dispatcher.publish(event)
        self._processed_count += 1

        logger.info(
            "GitHub webhook processed: %s → %s", event_type, canonical_type
        )
        return {"ok": True, "event_type": canonical_type, "event_id": event.event_id}

    def _verify_signature(self, body: bytes, signature: str) -> bool:
        """Verify the HMAC-SHA256 signature from GitHub."""
        mac = hmac.new(self._webhook_secret.encode(), body, hashlib.sha256)
        expected = "sha256=" + mac.hexdigest()
        return hmac.compare_digest(expected, signature)

    def summary(self) -> dict:
        return {
            "processed_count": self._processed_count,
            "signature_validation": bool(self._webhook_secret),
            "supported_event_types": sorted(_EVENT_MAP.keys()),
        }
