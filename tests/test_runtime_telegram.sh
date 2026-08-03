#!/usr/bin/env bash
# CORE-021 — Telegram Runtime Gateway Tests
# Tests the Telegram Gateway in disabled mode (no live token required).
set -e

python3 - <<'PY'
import sys, json
sys.path.insert(0, "lib")

from lib.python.runtime.interfaces.telegram_gateway import TelegramGateway
from lib.python.runtime.event_dispatcher import EventDispatcher

# --- Gateway is disabled when no token is provided ---
tg = TelegramGateway(bot_token="", chat_id="")
assert not tg._enabled, "Gateway should be disabled without token"

# --- Send returns False when disabled ---
result = tg.send_message("test")
assert result is False

# --- Poll returns empty list when disabled ---
updates = tg.poll_updates()
assert updates == []

# --- summary returns expected keys ---
summary = tg.summary()
for key in ["enabled", "sent_count", "received_count", "last_update_id"]:
    assert key in summary, f"Missing key: {key}"
assert summary["enabled"] is False

# --- process_update dispatches command events ---
disp = EventDispatcher()
received = []
disp.subscribe("telegram.command.status", lambda e: received.append(e))
tg2 = TelegramGateway(bot_token="", chat_id="", event_dispatcher=disp)
update = {
    "update_id": 1,
    "message": {
        "message_id": 1,
        "chat": {"id": 12345},
        "from": {"id": 12345, "first_name": "Test"},
        "text": "/status",
    }
}
tg2.process_update(update)
assert len(received) == 1, f"Expected 1 event, got {len(received)}"
assert received[0].event_type == "telegram.command.status"

# --- Unknown commands are ignored gracefully ---
received2 = []
disp2 = EventDispatcher()
disp2.subscribe_all(lambda e: received2.append(e))
tg3 = TelegramGateway(bot_token="", chat_id="", event_dispatcher=disp2)
update2 = {
    "update_id": 2,
    "message": {"message_id": 2, "chat": {"id": 1}, "from": {}, "text": "/unknown_command"}
}
tg3.process_update(update2)
# unknown_command should not dispatch any event
assert len(received2) == 0

# --- process_webhook_update handles valid JSON ---
disp3 = EventDispatcher()
tg4 = TelegramGateway(bot_token="", chat_id="", event_dispatcher=disp3)
body = json.dumps({
    "update_id": 3,
    "message": {"message_id": 3, "chat": {"id": 1}, "from": {}, "text": "/health"}
}).encode()
result = tg4.process_webhook_update(body)
assert result["ok"] is True

# --- process_webhook_update handles invalid JSON ---
result2 = tg4.process_webhook_update(b"not json")
assert result2["ok"] is False
assert "error" in result2

print("Telegram gateway tests PASSED")
PY
