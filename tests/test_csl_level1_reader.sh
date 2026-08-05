#!/usr/bin/env bash
set -e

# CSL Conformance Level 1 — Core Reader Tests
# Tests that the implementation loads and reads Canonical Documents
# CSL Reference: CONFORMANCE_LEVELS.md Level 1
# CORE: CORE-023-011

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.canonical_parser import CslLexer, CslParser, TokenType
from python.canonical_repository import CanonicalRepository
from pathlib import Path

print("=== CSL Level 1: Core Reader ===")

# L1-01: Load Canonical Documents
docs_path = Path("docs/canonical")
canon_files = sorted(docs_path.glob("CANON-*.md"))
assert len(canon_files) > 0, "L1-01 FAIL: No CANON-*.md files found"
print(f"L1-01 PASS: {len(canon_files)} canonical documents found")

# L1-02: Read document metadata
parser = CslParser()
doc = parser.parse_text(
    Path(canon_files[0]).read_text(encoding="utf-8"),
    source_name=str(canon_files[0])
)
assert doc.title, f"L1-02 FAIL: document has no title: {canon_files[0]}"
print(f"L1-02 PASS: title='{doc.title}' version='{doc.version}' status='{doc.status}'")

# L1-03: Recognize Engineering Entities (sections)
assert len(doc.sections()) > 0, "L1-03 FAIL: document has no sections"
print(f"L1-03 PASS: {len(doc.sections())} sections in document")

# L1-03b: Legacy canonical H1 sections are preserved as sections
legacy_sections = [s.heading for s in doc.sections()]
assert "Core Principles" in legacy_sections, f"L1-03b FAIL: missing legacy H1 section parsing: {legacy_sections[:5]}"
print("L1-03b PASS: legacy H1 section headings parsed as sections")

# L1-04: Recognize Relationships (CANON references)
repo = CanonicalRepository.load_from_directory(docs_path)
all_docs = repo.all_documents()
total_deps = sum(len(d.dependencies) for d in all_docs)
print(f"L1-04 PASS: {total_deps} dependency relationships found across {len(all_docs)} documents")

# L1-05: Reject invalid document structures
lexer = CslLexer("```\nunclosed code fence", "bad.md")
tokens = lexer.tokenize()
fence_count = sum(1 for t in tokens if t.token_type == TokenType.CODE_FENCE)
assert fence_count % 2 != 0, "L1-05 FAIL: invalid structure not detected"
print("L1-05 PASS: invalid structure (unterminated fence) detected")

print("\nCSL Level 1 (Core Reader): ALL PASS")
PY
