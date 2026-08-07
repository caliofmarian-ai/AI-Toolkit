#!/usr/bin/env bash
set -euo pipefail

cd /home/runner/work/AI-Toolkit/AI-Toolkit

PORT=8102 python3 bin/ai dashboard serve --repository . --workspace .. >/tmp/ai-dashboard-cli.log 2>&1 &
server_pid=$!
trap 'kill $server_pid >/dev/null 2>&1 || true' EXIT

python3 - <<'PY'
import time
from urllib.request import urlopen

deadline = time.time() + 30
last_error = None
while time.time() < deadline:
    try:
        body = urlopen("http://127.0.0.1:8102/").read().decode("utf-8")
        assert "Engineering Operating System" in body
        assert "Runtime Status" in body
        print("dashboard cli PASS")
        break
    except Exception as exc:  # noqa: BLE001
        last_error = exc
        time.sleep(0.5)
else:
    raise SystemExit(f"dashboard cli failed: {last_error}")
PY
