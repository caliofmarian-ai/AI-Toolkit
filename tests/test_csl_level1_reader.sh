#!/usr/bin/env bash
set -e

python3 - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, 'lib')

from python.canonical_parser import CslLexer, CslParser, TokenType

print('=== CSL Level 1: Core Reader ===')
source = Path('tests/fixtures_csl_minimal_project.csl').read_text(encoding='utf-8')
lexer = CslLexer(source, 'fixtures_csl_minimal_project.csl')
tokens = lexer.tokenize()
assert any(t.token_type == TokenType.KEYWORD and t.value == 'Project' for t in tokens), 'L1-01 FAIL: Project keyword not tokenized'
print('L1-01 PASS: declaration keywords tokenized')
assert any(t.token_type == TokenType.INDENT for t in tokens), 'L1-02 FAIL: indentation not tokenized'
print('L1-02 PASS: indentation tokens emitted deterministically')
parser = CslParser()
doc = parser.parse_text(source, source_name='fixtures_csl_minimal_project.csl')
assert doc.title == 'AI Toolkit', 'L1-03 FAIL: title not parsed'
print(f"L1-03 PASS: title='{doc.title}' version='{doc.version}' status='{doc.status}'")
assert len(doc.entities()) == 3, 'L1-04 FAIL: expected 3 entity declarations'
assert len(doc.relationships()) == 2, 'L1-04 FAIL: expected 2 relationships'
print('L1-04 PASS: entities and relationships parsed')
try:
    CslLexer('Project:\n\tIdentifier: Bad\n', 'bad.csl').tokenize()
    raise AssertionError('L1-05 FAIL: tab indentation not rejected')
except ValueError:
    print('L1-05 PASS: invalid indentation rejected')
print('\nCSL Level 1 (Core Reader): ALL PASS')
PY
