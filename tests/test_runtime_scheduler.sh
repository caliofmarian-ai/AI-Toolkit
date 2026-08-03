#!/usr/bin/env bash
# CORE-021 — Runtime Scheduler Tests
# Tests the Scheduler Host.
set -e

python3 - <<'PY'
import sys, time
sys.path.insert(0, "lib")

from lib.python.runtime.scheduler import SchedulerHost

# --- Jobs are registered and run ---
counter = [0]
sched = SchedulerHost(tick_interval=0.05)
sched.register("job1", "Test Job 1", lambda: counter.__setitem__(0, counter[0]+1), interval_seconds=1)
assert "job1" in sched.list_jobs()
sched.start()
time.sleep(1.2)
sched.stop()
assert counter[0] >= 1, f"Job should have run at least once, got {counter[0]}"
print(f"  Scheduler: job ran {counter[0]} time(s)")

# --- Multiple jobs run independently ---
a = [0]
b = [0]
sched2 = SchedulerHost(tick_interval=0.05)
sched2.register("job_a", "A", lambda: a.__setitem__(0, a[0]+1), interval_seconds=1)
sched2.register("job_b", "B", lambda: b.__setitem__(0, b[0]+1), interval_seconds=2)
sched2.start()
time.sleep(2.2)
sched2.stop()
assert a[0] >= 2, f"job_a should run >=2 times, got {a[0]}"
assert b[0] >= 1, f"job_b should run >=1 time, got {b[0]}"

# --- Jobs can be unregistered ---
sched3 = SchedulerHost(tick_interval=0.05)
sched3.register("rm_job", "Removable", lambda: None, interval_seconds=1)
sched3.unregister("rm_job")
assert "rm_job" not in sched3.list_jobs()

# --- Exceptions in jobs don't stop the scheduler ---
errored = [0]
def bad_job():
    errored[0] += 1
    raise RuntimeError("intentional error")

sched4 = SchedulerHost(tick_interval=0.05)
sched4.register("bad", "Bad Job", bad_job, interval_seconds=1)
sched4.start()
time.sleep(1.2)
sched4.stop()
assert errored[0] >= 1, "Bad job should have been attempted"

# --- summary returns expected keys ---
sched5 = SchedulerHost()
sched5.register("test", "Test", lambda: None, interval_seconds=60)
summary = sched5.summary()
assert "running" in summary
assert "job_count" in summary
assert "jobs" in summary
assert summary["job_count"] == 1

print("Scheduler tests PASSED")
PY
