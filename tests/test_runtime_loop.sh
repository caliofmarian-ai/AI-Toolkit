#!/usr/bin/env bash
# CORE-021 — Runtime Loop Tests
# Tests the Event Loop and Event Dispatcher.
set -e

python3 - <<'PY'
import sys, time
sys.path.insert(0, "lib")

from lib.python.runtime.event_loop import EventLoop
from lib.python.runtime.event_dispatcher import EventDispatcher, RuntimeEvent

# --- EventLoop runs observers on each tick ---
ticks = [0]
loop = EventLoop(tick_interval_seconds=1)
loop.register_observer(lambda: ticks.__setitem__(0, ticks[0]+1))

loop.run_once()
assert ticks[0] == 1, f"Expected 1 tick, got {ticks[0]}"

# --- EventLoop starts and ticks in background ---
ticks2 = [0]
loop2 = EventLoop(tick_interval_seconds=1)
loop2.register_observer(lambda: ticks2.__setitem__(0, ticks2[0]+1))
loop2.start()
time.sleep(1.5)
loop2.stop()
assert ticks2[0] >= 1, f"Expected >=1 background ticks, got {ticks2[0]}"

# --- Exceptions in observers don't stop the loop ---
ticks3 = [0]
loop3 = EventLoop(tick_interval_seconds=1)
def bad_observer():
    ticks3[0] += 1
    raise RuntimeError("observer error")
loop3.register_observer(bad_observer)
loop3.run_once()
assert ticks3[0] == 1  # Observer was called despite raising

# --- EventDispatcher publish/subscribe ---
disp = EventDispatcher()
received = []
disp.subscribe("test.event", lambda e: received.append(e.payload))
disp.emit("test.event", "test", {"val": 1})
disp.emit("test.event", "test", {"val": 2})
assert len(received) == 2
assert received[0]["val"] == 1

# --- Wildcard subscription receives all events ---
all_events = []
disp2 = EventDispatcher()
disp2.subscribe_all(lambda e: all_events.append(e.event_type))
disp2.emit("type.a", "src")
disp2.emit("type.b", "src")
assert "type.a" in all_events
assert "type.b" in all_events

# --- Exceptions in handlers don't stop the dispatcher ---
disp3 = EventDispatcher()
disp3.subscribe("fail.event", lambda e: 1/0)
ok_received = []
disp3.subscribe("fail.event", lambda e: ok_received.append(True))
disp3.emit("fail.event", "src")
assert len(ok_received) == 1  # Second handler still ran

# --- summary ---
s = disp.summary()
assert s["event_count"] == 2
assert "test.event" in s["subscribed_types"]

# --- EventLoop summary ---
s2 = loop.summary()
assert "running" in s2
assert "tick_count" in s2

print("Runtime loop tests PASSED")
PY
