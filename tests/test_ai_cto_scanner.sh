#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="${1:-.}"

echo "=================================="
echo "AI CTO Integration Scanner Test"
echo "CORE-008A"
echo "=================================="

cd "$ROOT"

echo
echo "[1/6] Module import check"
PYTHONPATH=lib python3 -c "
from python.ai_cto_scanner import AICTOScanner, AICTOScannerEngine
from python.ai_cto_scanner.detectors import (
    TelegramDetector, OwnerControlDetector, RuntimeDetector,
    StateDetector, ConfigurationDetector, CanonicalDetector,
    ProjectMemoryDetector,
)
from python.ai_cto_scanner.scoring import ReadinessScorer
from python.ai_cto_scanner.report import AICTOReportGenerator
from python.agents.ai_cto_scanner_agent import AICTOScannerAgent
print('Module import OK')
assert AICTOScanner is AICTOScannerEngine
print('Backward compatibility alias OK')
"

echo
echo "[2/6] Agent registration check"
PYTHONPATH=lib python3 -c "
from python.agent_runtime.registry import build_runtime
runtime = build_runtime()
agents = runtime.list_agents()
assert 'inspect' in agents, 'inspect agent not registered'
print('Registered agents:', agents)
print('Agent registration OK')
"

echo
echo "[3/6] Scanner engine smoke test"
PYTHONPATH=lib python3 -c "
import tempfile, os
from python.ai_cto_scanner.engine import AICTOScannerEngine

with tempfile.TemporaryDirectory() as tmp:
    engine = AICTOScannerEngine(repository='.', output_dir=tmp)
    result = engine.scan()

    assert 'scores' in result
    assert 'detection' in result
    assert 'Overall AI CTO Readiness' in result['scores']
    assert 'repository' in result
    assert 'workspace' in result

    categories = ['Telegram', 'OwnerControl', 'Runtime', 'State',
                  'Configuration', 'Canonical', 'ProjectMemory']
    for cat in categories:
        assert cat in result['detection'], 'Missing detection category: ' + cat

    report_path = result['report_path']
    assert os.path.exists(report_path), 'Report file not generated'

    print('Scores:', result['scores'])
    print('Report written to:', report_path)
    print('Scanner engine OK')
"

echo
echo "[4/6] Readiness scores check"
PYTHONPATH=lib python3 -c "
from python.ai_cto_scanner.engine import AICTOScannerEngine
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    engine = AICTOScannerEngine(repository='.', output_dir=tmp)
    result = engine.scan()

    scores = result['scores']
    required_scores = [
        'Telegram Readiness',
        'Runtime Readiness',
        'State Readiness',
        'Persistence Readiness',
        'Owner Readiness',
        'Canonical Readiness',
        'Development Readiness',
        'Project Memory Readiness',
        'Context Integrity Readiness',
        'Overall AI CTO Readiness',
    ]
    for key in required_scores:
        assert key in scores, 'Missing score: ' + key
        assert 0 <= scores[key] <= 100, 'Score out of range: ' + key + '=' + str(scores[key])
    print('All readiness dimensions present and in range')
    print('Readiness scores OK')
"

echo
echo "[5/6] CLI interface check"
PYTHONPATH=lib python3 -m python.cli.main --help | grep -q inspect && echo "inspect command present in help"

echo
echo "[6/6] Report content check"
PYTHONPATH=lib python3 -c "
import tempfile, os
from python.ai_cto_scanner.engine import AICTOScannerEngine

with tempfile.TemporaryDirectory() as tmp:
    engine = AICTOScannerEngine(repository='.', output_dir=tmp)
    result = engine.scan()
    report_path = result['report_path']
    content = open(report_path, encoding='utf-8').read()

    required_sections = [
        '# AI CTO Integration Report',
        '## Executive Summary',
        '## Architecture Map',
        '## Integration Points',
        '## Injection Points',
        '## Detected Components',
        '## Missing Components',
        '## Recommended Development Order',
        '## Risk Analysis',
        '## Implementation Roadmap',
        '## Estimated Effort',
        '## AI CTO Readiness Score',
    ]
    for section in required_sections:
        assert section in content, 'Missing section in report: ' + section
    print('All required sections present in AI_CTO_INTEGRATION_REPORT.md')
    print('Report content OK')
"

echo
echo "=================================="
echo "AI CTO Integration Scanner PASS"
echo "=================================="
