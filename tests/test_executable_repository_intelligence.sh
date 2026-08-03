#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="${1:-.}"

echo "==========================================="
echo "Executable Repository Intelligence Test"
echo "CORE-008C"
echo "==========================================="

cd "$ROOT"

echo
echo "[1/12] Module import check"
PYTHONPATH=lib python3 -c "
from python.executable_repository_intelligence import (
    ExecutableRepositoryEngine,
    FileClassifier,
    RuntimeMapBuilder,
    ExecutableDependencyGraphBuilder,
    InjectionSafetyClassifier,
    ZoneClassifier,
    ExecutableRecommendationEngine,
    ExecutablePersistence,
    ExecutionModelReportGenerator,
)
print('All 9 components imported OK')
"

echo
echo "[2/12] FileClassifier — canonical categories"
PYTHONPATH=lib python3 -c "
from pathlib import Path
from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
from python.executable_repository_intelligence.file_classifier import FileClassifier
from python.executable_repository_intelligence.models import FILE_CATEGORIES

root = Path('.')
file_analyses = ASTAnalyzer(root).analyze()
classifier = FileClassifier()
fcs = classifier.classify_all(file_analyses, root)

assert len(fcs) > 0, 'No files classified'
for fc in fcs:
    assert fc.category in FILE_CATEGORIES, 'Invalid category: %s' % fc.category
    assert isinstance(fc.is_executable, bool)
    assert 0.0 <= fc.confidence <= 1.0
    d = fc.to_dict()
    assert 'path' in d
    assert 'category' in d
    assert 'is_executable' in d
    assert 'confidence' in d

categories_found = set(fc.category for fc in fcs)
print('Files classified:', len(fcs))
print('Categories found:', sorted(categories_found))

# Must classify Python files as executable or bootstrap
py_files = [fc for fc in fcs if fc.path.endswith('.py')]
exec_py = [fc for fc in py_files if fc.is_executable]
assert exec_py, 'No Python files classified as executable'

# Must classify Markdown files as Documentation or Reports
md_files = [fc for fc in fcs if fc.path.endswith('.md')]
assert all(fc.category in ('Documentation', 'Reports', 'Canonical Specification') for fc in md_files), \
    'Markdown file classified incorrectly'

print('FileClassifier OK')
"

echo
echo "[3/12] RuntimeMapBuilder — runtime topology"
PYTHONPATH=lib python3 -c "
from pathlib import Path
from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
from python.executable_repository_intelligence.file_classifier import FileClassifier
from python.executable_repository_intelligence.runtime_map import RuntimeMapBuilder
from python.executable_repository_intelligence.models import RepositoryRuntimeMap

root = Path('.')
file_analyses = ASTAnalyzer(root).analyze()
fcs = FileClassifier().classify_all(file_analyses, root)
rm = RuntimeMapBuilder().build(fcs, file_analyses, root)

assert isinstance(rm, RepositoryRuntimeMap)
assert isinstance(rm.execution_chain, list)
assert isinstance(rm.bootstrap_sequence, list)
assert isinstance(rm.runtime_components, list)
assert isinstance(rm.initialization_order, list)
assert isinstance(rm.background_workers, list)
assert isinstance(rm.shutdown_hooks, list)

d = rm.to_dict()
assert 'main_entry_point' in d
assert 'execution_chain' in d
assert 'bootstrap_sequence' in d
assert 'runtime_components' in d
assert 'initialization_order' in d
assert 'background_workers' in d
assert 'telegram_runtime' in d
assert 'owner_runtime' in d
assert 'admin_runtime' in d
assert 'persistence_runtime' in d
assert 'shutdown_hooks' in d
assert 'restart_hooks' in d
assert 'resume_hooks' in d

print('Main entry point:', d['main_entry_point'])
print('Execution chain:', len(d['execution_chain']), 'files')
print('Bootstrap sequence:', len(d['bootstrap_sequence']), 'files')
print('Runtime components:', len(d['runtime_components']))
print('RuntimeMapBuilder OK')
"

echo
echo "[4/12] ExecutableDependencyGraphBuilder"
PYTHONPATH=lib python3 -c "
from pathlib import Path
from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
from python.semantic_repository_intelligence.import_graph import ImportGraphBuilder
from python.executable_repository_intelligence.file_classifier import FileClassifier
from python.executable_repository_intelligence.executable_dep_graph import ExecutableDependencyGraphBuilder
from python.executable_repository_intelligence.models import (
    ExecutableDependencyGraph, FILE_CATEGORIES,
)

root = Path('.')
file_analyses = ASTAnalyzer(root).analyze()
import_graph = ImportGraphBuilder().build(file_analyses, root)
fcs = FileClassifier().classify_all(file_analyses, root)

dep_graph = ExecutableDependencyGraphBuilder().build(fcs, file_analyses, import_graph, root)

assert isinstance(dep_graph, ExecutableDependencyGraph)
assert isinstance(dep_graph.nodes, list)
assert isinstance(dep_graph.edges, list)
assert isinstance(dep_graph.excluded, list)
assert isinstance(dep_graph.exclusion_reasons, dict)

d = dep_graph.to_dict()
assert 'node_count' in d
assert 'edge_count' in d
assert 'excluded_count' in d
assert 'nodes' in d
assert 'edges' in d

# Nodes must all be executable
exec_set = {fc.path for fc in fcs if fc.is_executable}
for node in dep_graph.nodes:
    assert node in exec_set, 'Non-executable node in graph: %s' % node

# Excluded must not contain executable code
for path in dep_graph.excluded:
    assert path not in exec_set, 'Executable file incorrectly excluded: %s' % path

# No Markdown files should appear as nodes
for node in dep_graph.nodes:
    assert not node.endswith('.md'), 'Markdown file in dep graph: %s' % node

print('Executable dep nodes:', d['node_count'])
print('Executable dep edges:', d['edge_count'])
print('Excluded files:', d['excluded_count'])
print('ExecutableDependencyGraphBuilder OK')
"

echo
echo "[5/12] InjectionSafetyClassifier"
PYTHONPATH=lib python3 -c "
from pathlib import Path
from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
from python.semantic_repository_intelligence.injection_point_analyzer import InjectionPointAnalyzer
from python.executable_repository_intelligence.file_classifier import FileClassifier
from python.executable_repository_intelligence.injection_safety import InjectionSafetyClassifier
from python.executable_repository_intelligence.models import SAFETY_CLASSIFICATIONS

root = Path('.')
file_analyses = ASTAnalyzer(root).analyze()
fcs = FileClassifier().classify_all(file_analyses, root)
injection_points = InjectionPointAnalyzer().analyze(file_analyses, root)

records = InjectionSafetyClassifier().classify(injection_points, fcs, root)

assert isinstance(records, list)
for r in records:
    assert r.safety in SAFETY_CLASSIFICATIONS, 'Invalid safety: %s' % r.safety
    assert 0.0 <= r.confidence <= 1.0
    d = r.to_dict()
    assert 'file' in d
    assert 'name' in d
    assert 'safety' in d
    assert 'rationale' in d
    assert 'conditions' in d

print('Injection safety records:', len(records))
verdicts = set(r.safety for r in records)
print('Safety verdicts found:', sorted(verdicts))
print('InjectionSafetyClassifier OK')
"

echo
echo "[6/12] ZoneClassifier"
PYTHONPATH=lib python3 -c "
from pathlib import Path
from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
from python.executable_repository_intelligence.file_classifier import FileClassifier
from python.executable_repository_intelligence.zone_classifier import ZoneClassifier
from python.executable_repository_intelligence.models import ZONE_CATEGORIES

root = Path('.')
file_analyses = ASTAnalyzer(root).analyze()
fcs = FileClassifier().classify_all(file_analyses, root)
zones = ZoneClassifier().classify(fcs, root)

assert isinstance(zones, list)
assert len(zones) > 0, 'No zones classified'

for z in zones:
    assert z.zone in ZONE_CATEGORIES, 'Invalid zone: %s' % z.zone
    assert isinstance(z.file_count, int) and z.file_count > 0
    d = z.to_dict()
    assert 'path' in d
    assert 'zone' in d
    assert 'file_count' in d

zone_names = set(z.zone for z in zones)
print('Zones found:', sorted(zone_names))
print('Directory count:', len(zones))

# Python lib should be Runtime
runtime_zones = [z for z in zones if 'lib' in z.path and z.zone == 'Runtime']
assert runtime_zones, 'lib/ directory not classified as Runtime'

# tests/ should be Testing
test_zones = [z for z in zones if 'tests' in z.path and z.zone == 'Testing']
assert test_zones, 'tests/ directory not classified as Testing'

print('ZoneClassifier OK')
"

echo
echo "[7/12] ExecutableRecommendationEngine"
PYTHONPATH=lib python3 -c "
from pathlib import Path
from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
from python.semantic_repository_intelligence.import_graph import ImportGraphBuilder
from python.semantic_repository_intelligence.injection_point_analyzer import InjectionPointAnalyzer
from python.executable_repository_intelligence.file_classifier import FileClassifier
from python.executable_repository_intelligence.runtime_map import RuntimeMapBuilder
from python.executable_repository_intelligence.executable_dep_graph import ExecutableDependencyGraphBuilder
from python.executable_repository_intelligence.injection_safety import InjectionSafetyClassifier
from python.executable_repository_intelligence.zone_classifier import ZoneClassifier
from python.executable_repository_intelligence.recommendations import ExecutableRecommendationEngine

root = Path('.')
file_analyses = ASTAnalyzer(root).analyze()
import_graph = ImportGraphBuilder().build(file_analyses, root)
injection_points = InjectionPointAnalyzer().analyze(file_analyses, root)
fcs = FileClassifier().classify_all(file_analyses, root)
rm = RuntimeMapBuilder().build(fcs, file_analyses, root)
dep_graph = ExecutableDependencyGraphBuilder().build(fcs, file_analyses, import_graph, root)
safety = InjectionSafetyClassifier().classify(injection_points, fcs, root)
zones = ZoneClassifier().classify(fcs, root)

recs = ExecutableRecommendationEngine().generate(fcs, rm, dep_graph, zones, safety)

assert isinstance(recs, list)
for rec in recs:
    assert rec.id.startswith('EXEC-REC-'), 'Bad ID: %s' % rec.id
    assert rec.priority in ('critical', 'high', 'medium', 'low')
    assert 0.0 <= rec.confidence <= 1.0
    d = rec.to_dict()
    assert 'id' in d
    assert 'title' in d
    assert 'category' in d
    assert 'priority' in d
    assert 'confidence' in d
    assert 'evidence' in d
    assert 'affected_files' in d

print('Recommendations generated:', len(recs))
print('ExecutableRecommendationEngine OK')
"

echo
echo "[8/12] ExecutablePersistence"
PYTHONPATH=lib python3 -c "
import json
import tempfile
from pathlib import Path
from python.executable_repository_intelligence.persistence import ExecutablePersistence

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    p = ExecutablePersistence(root)

    sample = {
        'repository': str(root),
        'executable_file_count': 42,
        'non_executable_file_count': 13,
        'category_distribution': {'Executable Code': 42},
        'zone_distribution': {'Runtime': 3},
        'safety_distribution': {'SAFE': 10},
        'runtime_map': {
            'main_entry_point': 'main.py',
            'execution_chain': ['main.py'],
            'bootstrap_sequence': [],
            'runtime_components': [],
            'initialization_order': [],
            'scheduler_entry': None,
            'background_workers': [],
            'telegram_runtime': [],
            'owner_runtime': [],
            'admin_runtime': [],
            'persistence_runtime': [],
            'shutdown_hooks': [],
            'restart_hooks': [],
            'resume_hooks': [],
        },
        'executable_dependency_graph': {
            'node_count': 5,
            'edge_count': 3,
            'excluded_count': 2,
            'nodes': [],
            'edges': [],
            'exclusion_reasons': {},
        },
        'injection_safety': [],
        'zones': [],
        'recommendations': [],
        'file_classifications': [],
    }

    path1 = p.save_runtime_model(sample)
    path2 = p.save_executable_map(sample)

    assert path1.exists(), 'runtime_repository_model.json not written'
    assert path2.exists(), 'executable_repository_map.json not written'

    loaded1 = p.load_runtime_model()
    loaded2 = p.load_executable_map()

    assert loaded1 is not None
    assert loaded2 is not None
    assert loaded1['schema_version'] == '1.0.0'
    assert loaded2['schema_version'] == '1.0.0'
    assert loaded1['model']['executable_file_count'] == 42
    assert loaded2['executable_map']['main_entry_point'] == 'main.py'

    print('runtime_repository_model.json written to:', path1)
    print('executable_repository_map.json written to:', path2)
    print('ExecutablePersistence OK')
"

echo
echo "[9/12] ExecutionModelReportGenerator"
PYTHONPATH=lib python3 -c "
import tempfile
from pathlib import Path
from python.executable_repository_intelligence.report import ExecutionModelReportGenerator

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    output = root / 'AI_CTO_EXECUTION_MODEL.md'

    sample = {
        'repository': str(root),
        'executable_file_count': 10,
        'non_executable_file_count': 5,
        'category_distribution': {'Executable Code': 10, 'Documentation': 5},
        'zone_distribution': {'Runtime': 2, 'Documentation': 1},
        'safety_distribution': {'SAFE': 3, 'SAFE_WITH_CONDITIONS': 2},
        'runtime_map': {
            'main_entry_point': 'main.py',
            'execution_chain': ['main.py', 'app.py'],
            'bootstrap_sequence': [],
            'runtime_components': [
                {'name': 'main', 'file': 'main.py', 'role': 'entry_point', 'layer': 'Core', 'dependencies': []}
            ],
            'initialization_order': ['main.py'],
            'scheduler_entry': None,
            'background_workers': [],
            'telegram_runtime': [],
            'owner_runtime': [],
            'admin_runtime': [],
            'persistence_runtime': [],
            'shutdown_hooks': [],
            'restart_hooks': [],
            'resume_hooks': [],
        },
        'executable_dependency_graph': {
            'node_count': 10, 'edge_count': 5,
            'nodes': ['main.py'],
            'edges': [{'source': 'main.py', 'target': 'app.py', 'kind': 'import'}],
            'excluded_count': 5,
            'exclusion_reasons': {'README.md': 'Category: Documentation'},
        },
        'injection_safety': [
            {'file': 'main.py', 'name': 'hook1', 'injection_type': 'decorator',
             'safety': 'SAFE_WITH_CONDITIONS', 'rationale': 'needs validation',
             'conditions': ['validate inputs'], 'confidence': 0.8}
        ],
        'zones': [
            {'path': '.', 'zone': 'Runtime', 'file_count': 5, 'evidence': ['Zone: Runtime']},
            {'path': 'docs', 'zone': 'Documentation', 'file_count': 3, 'evidence': ['Zone: Documentation']},
        ],
        'recommendations': [
            {'id': 'EXEC-REC-001', 'title': 'Test rec', 'description': 'Test',
             'category': 'isolation', 'priority': 'medium', 'confidence': 0.8,
             'evidence': ['evidence1'], 'affected_files': ['main.py']},
        ],
        'file_classifications': [
            {'path': 'main.py', 'category': 'Runtime Entry Point',
             'subcategory': 'Main entry point', 'is_executable': True,
             'confidence': 0.95, 'evidence': ['matched']}
        ],
    }

    gen = ExecutionModelReportGenerator()
    content = gen.generate(sample, output)

    assert output.exists(), 'AI_CTO_EXECUTION_MODEL.md not written'
    assert len(content) > 500, 'Report too short: %d chars' % len(content)
    assert '# AI CTO Execution Model' in content
    assert 'CORE-008C' in content
    assert 'Runtime Map' in content
    assert 'File Classifications' in content
    assert 'Executable Dependency Graph' in content
    assert 'Injection Safety' in content
    assert 'Repository Zones' in content
    assert 'Recommendations' in content
    print('Report length:', len(content), 'chars')
    print('ExecutionModelReportGenerator OK')
"

echo
echo "[10/12] ExecutableRepositoryEngine — full pipeline (AI-Toolkit)"
PYTHONPATH=lib python3 -c "
from python.executable_repository_intelligence import ExecutableRepositoryEngine
from python.executable_repository_intelligence.models import (
    FILE_CATEGORIES, ZONE_CATEGORIES, SAFETY_CLASSIFICATIONS
)

engine = ExecutableRepositoryEngine(repository='.', persist=False)
result = engine.analyze()

# Structural assertions
assert 'repository' in result
assert 'executable_file_count' in result
assert 'non_executable_file_count' in result
assert 'category_distribution' in result
assert 'zone_distribution' in result
assert 'safety_distribution' in result
assert 'file_classifications' in result
assert 'runtime_map' in result
assert 'executable_dependency_graph' in result
assert 'injection_safety' in result
assert 'zones' in result
assert 'recommendations' in result

# Sanity checks
assert result['executable_file_count'] > 0
assert result['non_executable_file_count'] > 0
assert len(result['file_classifications']) > 0
assert len(result['zones']) > 0

# All categories must be valid
for fc in result['file_classifications']:
    assert fc['category'] in FILE_CATEGORIES, 'Bad category: %s' % fc['category']

# All zones must be valid
for z in result['zones']:
    assert z['zone'] in ZONE_CATEGORIES, 'Bad zone: %s' % z['zone']

# All safety verdicts must be valid
for s in result['injection_safety']:
    assert s['safety'] in SAFETY_CLASSIFICATIONS, 'Bad safety: %s' % s['safety']

# Runtime map must have all required keys
rm = result['runtime_map']
for key in [
    'main_entry_point', 'execution_chain', 'bootstrap_sequence',
    'runtime_components', 'initialization_order', 'scheduler_entry',
    'background_workers', 'telegram_runtime', 'owner_runtime',
    'admin_runtime', 'persistence_runtime', 'shutdown_hooks',
    'restart_hooks', 'resume_hooks',
]:
    assert key in rm, 'Missing runtime_map key: %s' % key

# Executable dep graph must have all required keys
dg = result['executable_dependency_graph']
for key in ['node_count', 'edge_count', 'nodes', 'edges', 'excluded_count']:
    assert key in dg, 'Missing dep_graph key: %s' % key

# Recommendations must have valid IDs
for rec in result['recommendations']:
    assert rec['id'].startswith('EXEC-REC-'), 'Bad rec ID: %s' % rec['id']

print('Repository:', result['repository'])
print('Executable files:', result['executable_file_count'])
print('Non-executable files:', result['non_executable_file_count'])
print('Categories:', sorted(result['category_distribution'].keys()))
print('Zones:', sorted(result['zone_distribution'].keys()))
print('Safety verdicts:', sorted(result['safety_distribution'].keys()))
print('Main entry point:', result['runtime_map']['main_entry_point'])
print('Exec dep nodes:', result['executable_dependency_graph']['node_count'])
print('Exec dep edges:', result['executable_dependency_graph']['edge_count'])
print('Recommendations:', len(result['recommendations']))
print('Zones:', len(result['zones']))
print('ExecutableRepositoryEngine full pipeline OK')
"

echo
echo "[11/12] CLI — --runtime flag"
PYTHONPATH=lib python3 -m python.cli.main inspect . --runtime 2>&1 | python3 -c "
import json, sys
data = json.load(sys.stdin)
assert 'executable_file_count' in data
assert 'main_entry_point' in data
assert 'category_distribution' in data
print('--runtime CLI summary OK')
print('Executable files:', data['executable_file_count'])
print('Main entry point:', data['main_entry_point'])
"

echo
echo "[12/12] Determinism check"
PYTHONPATH=lib python3 -c "
import json
from python.executable_repository_intelligence import ExecutableRepositoryEngine

def run():
    engine = ExecutableRepositoryEngine(repository='.', persist=False)
    result = engine.analyze()
    return {
        'executable_file_count': result['executable_file_count'],
        'non_executable_file_count': result['non_executable_file_count'],
        'category_distribution': result['category_distribution'],
        'zone_distribution': result['zone_distribution'],
        'safety_distribution': result['safety_distribution'],
        'main_entry_point': result['runtime_map']['main_entry_point'],
        'exec_dep_nodes': result['executable_dependency_graph']['node_count'],
        'exec_dep_edges': result['executable_dependency_graph']['edge_count'],
        'recommendation_count': len(result['recommendations']),
        'zone_count': len(result['zones']),
    }

r1 = run()
r2 = run()

assert r1 == r2, 'Non-deterministic output!\nRun 1: %s\nRun 2: %s' % (r1, r2)
print('Deterministic output confirmed:', json.dumps(r1, indent=2))
print('Determinism check OK')
"

echo
echo "==========================================="
echo "Executable Repository Intelligence PASS"
echo "CORE-008C"
echo "==========================================="
