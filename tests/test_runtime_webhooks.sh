#!/usr/bin/env bash
# CORE-021 — GitHub Webhook Tests
# Tests GitHub webhook processing.
set -e

python3 - <<'PY'
import sys, json, hashlib, hmac
sys.path.insert(0, "lib")

from python.runtime.event_dispatcher import EventDispatcher
from python.runtime.interfaces.github_webhook import GitHubWebhookHost

def make_sig(secret: str, body: bytes) -> str:
    mac = hmac.new(secret.encode(), body, hashlib.sha256)
    return "sha256=" + mac.hexdigest()

# --- Push event is converted to github.push ---
disp = EventDispatcher()
events = []
disp.subscribe("github.push", lambda e: events.append(e))
gh = GitHubWebhookHost(dispatcher=disp)
payload = json.dumps({"ref": "refs/heads/main", "commits": []}).encode()
result = gh.process("push", "", payload)
assert result["ok"], result
assert result["event_type"] == "github.push"
assert len(events) == 1
assert events[0].source == "github.webhook"

# --- Pull request event ---
pr_events = []
disp2 = EventDispatcher()
disp2.subscribe("github.pull_request", lambda e: pr_events.append(e))
gh2 = GitHubWebhookHost(dispatcher=disp2)
payload2 = json.dumps({"action": "opened"}).encode()
result2 = gh2.process("pull_request", "", payload2)
assert result2["ok"]
assert len(pr_events) == 1

# --- Unknown event types get generic canonical name ---
disp3 = EventDispatcher()
gh3 = GitHubWebhookHost(dispatcher=disp3)
result3 = gh3.process("custom_event", "", b"{}")
assert result3["ok"]
assert result3["event_type"] == "github.custom_event"

# --- Signature validation succeeds with correct signature ---
secret = "test-secret-123"
disp4 = EventDispatcher()
gh4 = GitHubWebhookHost(dispatcher=disp4, webhook_secret=secret)
body = b'{"ref": "main"}'
sig = make_sig(secret, body)
result4 = gh4.process("push", sig, body)
assert result4["ok"], f"Valid signature should pass: {result4}"

# --- Signature validation fails with wrong signature ---
result5 = gh4.process("push", "sha256=badsig", body)
assert not result5["ok"], "Invalid signature should fail"
assert result5.get("error") == "invalid signature"

# --- Invalid JSON is handled gracefully ---
disp5 = EventDispatcher()
gh5 = GitHubWebhookHost(dispatcher=disp5)
result6 = gh5.process("push", "", b"not valid json")
assert not result6["ok"]
assert "JSON" in result6.get("error", "")

# --- Ping event is processed ---
disp6 = EventDispatcher()
gh6 = GitHubWebhookHost(dispatcher=disp6)
result7 = gh6.process("ping", "", json.dumps({"zen": "Approachable is better than simple."}).encode())
assert result7["ok"]
assert result7["event_type"] == "github.ping"

# --- summary ---
s = gh.summary()
assert "processed_count" in s
assert "supported_event_types" in s
assert "push" in s["supported_event_types"]

print("GitHub webhook tests PASSED")
PY
