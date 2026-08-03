#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.canonical_parser import CanonicalParser
from pathlib import Path

parser = CanonicalParser()

# Parse a known file
docs_path = Path("docs/canonical")
canon_files = list(docs_path.glob("CANON-*.md"))
assert len(canon_files) > 0, "No canonical files found"

doc = parser.parse_file(canon_files[0])
assert doc.id is not None
assert doc.title is not None
assert doc.version is not None

# Parse all
docs = parser.parse_directory(docs_path)
assert len(docs) >= 10, f"Expected >= 10 docs, got {len(docs)}"

print(f"Parsed {len(docs)} canonical documents")
print("Canonical Parser PASS")
PY
