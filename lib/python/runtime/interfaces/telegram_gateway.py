"""
CORE-021 — Telegram Runtime Gateway
CANON-047, CANON-031

Provides bidirectional Telegram communication for the Runtime:

  Inbound:  commands from the Owner (status, health, reports, etc.)
  Outbound: notifications, alerts, approval requests

All Telegram commands pass through Governance before any Runtime
action is taken (CANON-050).

Uses the Telegram Bot API via the standard `requests` library.
No Telegram command bypasses Governance.
"""

import json
import logging
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

try:
    import requests as _requests
    _REQUESTS_AVAILABLE = True
except ImportError:
    _REQUESTS_AVAILABLE = False
    logger.warning("TelegramGateway: requests library not available — Telegram disabled")

_TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"


class TelegramGateway:
    """
    Telegram Runtime Gateway.

    Sends notifications to the Owner and processes inbound commands.
    When TELEGRAM_BOT_TOKEN is not set, the gateway operates in
    disabled mode (all sends are no-ops, all receives are empty).
    """

    # Inbound command → canonical event type
    _COMMAND_MAP: Dict[str, str] = {
        "/status": "telegram.command.status",
        "/health": "telegram.command.health",
        "/report": "telegram.command.report",
        "/briefing": "telegram.command.briefing",
        "/approve": "telegram.command.approve",
        "/reject": "telegram.command.reject",
        "/pause": "telegram.command.pause",
        "/resume": "telegram.command.resume",
        "/help": "telegram.command.help",
    }

    def __init__(
        self,
        bot_token: str = "",
        chat_id: str = "",
        event_dispatcher: Optional[Any] = None,
        enabled: bool = True,
    ):
        self._bot_token = bot_token
        self._chat_id = chat_id
        self._dispatcher = event_dispatcher
        self._enabled = enabled and bool(bot_token) and _REQUESTS_AVAILABLE
        self._last_update_id = 0
        self._sent_count = 0
        self._received_count = 0

        if not self._enabled:
            logger.info("TelegramGateway: disabled (integration disabled, no token, or requests unavailable)")

    def is_enabled(self) -> bool:
        return self._enabled

    # ------------------------------------------------------------------ #
    # Outbound
    # ------------------------------------------------------------------ #

    def send_message(self, text: str, chat_id: Optional[str] = None) -> bool:
        """Send *text* to the Owner chat.  Returns True on success."""
        if not self._enabled:
            logger.debug("TelegramGateway: skipping send (disabled): %s", text[:80])
            return False

        target_chat = chat_id or self._chat_id
        if not target_chat:
            logger.warning("TelegramGateway: no chat_id configured")
            return False

        try:
            url = _TELEGRAM_API.format(token=self._bot_token, method="sendMessage")
            resp = _requests.post(
                url,
                json={"chat_id": target_chat, "text": text, "parse_mode": "Markdown"},
                timeout=10,
            )
            resp.raise_for_status()
            self._sent_count += 1
            return True
        except Exception as exc:
            logger.error("TelegramGateway: send failed: %s", exc)
            return False

    def send_status_report(self, report_text: str) -> bool:
        return self.send_message(f"*Runtime Status*

{report_text}")

    def send_health_alert(self, message: str) -> bool:
        return self.send_message(f"⚠️ *Health Alert*

{message}")

    def send_notification(self, message: str) -> bool:
        return self.send_message(f"🔔 {message}")

    # ------------------------------------------------------------------ #
    # Inbound (polling)
    # ------------------------------------------------------------------ #

    def poll_updates(self) -> List[dict]:
        """
        Fetch pending Telegram updates via long-poll.
        Returns a list of raw update objects.
        """
        if not self._enabled:
            return []

        try:
            url = _TELEGRAM_API.format(token=self._bot_token, method="getUpdates")
            resp = _requests.get(
                url,
                params={"offset": self._last_update_id + 1, "timeout": 5},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            updates = data.get("result", [])
            if updates:
                self._last_update_id = updates[-1]["update_id"]
            return updates
        except Exception as exc:
            logger.error("TelegramGateway: poll failed: %s", exc)
            return []

    def process_update(self, update: dict) -> Optional[str]:
        """
        Process one Telegram update.
        Emits a canonical Runtime event for recognized commands.
        Returns the command string or None.
        """
        message = update.get("message", {})
        text = message.get("text", "").strip()
        if not text:
            return None

        self._received_count += 1
        command = text.split()[0].lower()
        event_type = self._command_map_lookup(command)

        if event_type and self._dispatcher:
            from lib.python.runtime.event_dispatcher import RuntimeEvent
            event = RuntimeEvent(
                event_type=event_type,
                source="telegram.gateway",
                payload={
                    "command": command,
                    "text": text,
                    "chat_id": str(message.get("chat", {}).get("id", "")),
                    "from": message.get("from", {}),
                },
            )
            self._dispatcher.publish(event)
            logger.info("TelegramGateway: dispatched %s", event_type)

        return command if event_type else None

    def process_webhook_update(self, body: bytes) -> dict:
        """
        Process a Telegram update delivered via webhook POST.
        Returns a result dict.
        """
        try:
            update = json.loads(body)
            cmd = self.process_update(update)
            return {"ok": True, "command": cmd}
        except Exception as exc:
            logger.error("TelegramGateway: webhook error: %s", exc)
            return {"ok": False, "error": str(exc)}

    def _command_map_lookup(self, command: str) -> Optional[str]:
        return self._COMMAND_MAP.get(command)

    def summary(self) -> dict:
        return {
            "enabled": self._enabled,
            "chat_id_configured": bool(self._chat_id),
            "sent_count": self._sent_count,
            "received_count": self._received_count,
            "last_update_id": self._last_update_id,
        }
