#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.project_profiles.trading_signals import TradingSignalsProfile

profile = TradingSignalsProfile()

report = profile.inspect(".")

print()
print("Profile:", report["profile"])
print("Canonical Found:", len(report["canonical_found"]))
print("Canonical Missing:", len(report["canonical_missing"]))

if report["canonical_missing"]:
    print()
    print("Missing:")
    for item in report["canonical_missing"]:
        print("-", item)

print()
print("Trading Profile PASS")
PY
