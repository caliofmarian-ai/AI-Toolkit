#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.session_runtime.runtime import SessionRuntime

runtime = SessionRuntime()

session = runtime.create(".")

runtime.checkpoint(session,"inspect")
runtime.checkpoint(session,"validation")
runtime.checkpoint(session,"planning")

print()

print("Session :", session.identifier)

print("Completed:")

for step in session.completed_steps:
    print("-",step)

print()

print("Session Runtime PASS")
PY
