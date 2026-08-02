#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

import python.knowledge_engine
import python.repository_engine
import python.dependency_engine
import python.validation_engine

print("Python package import PASS")
PY
