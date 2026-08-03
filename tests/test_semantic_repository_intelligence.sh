#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="${1:-.}"

echo "==========================================="
echo "Semantic Repository Intelligence Test"
echo "CORE-008B"
echo "==========================================="

cd "$ROOT"

echo
echo "[1/12] Module import check"
PYTHONPATH=lib python3 -c "
from python.semantic_repository_intelligence import (
    SemanticRepositoryEngine,
    ASTAnalyzer,
    ImportGraphBuilder,
    CallGraphBuilder,
    DependencyGraphBuilder,
    ArchitectureGraphBuilder,
    InjectionPointAnalyzer,
    RelationshipResolver,
    ConfidenceEngine,
    SemanticRecommendationEngine,
    SemanticPersistence,
)
print('All 11 components imported OK')
"

echo
echo "[2/12] ASTAnalyzer — Python analysis"
PYTHONPATH=lib python3 -c "
from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
analyzer = ASTAnalyzer('.', workspace_index=None)
results = analyzer.analyze()
py_results = {p: fa for p, fa in results.items() if fa.language == 'python'}
assert len(py_results) > 10, 'Expected >10 Python files, got %d' % len(py_results)

# Check that a known file is analysed
known = [p for p in py_results if 'ai_cto_scanner' in p and 'engine' in p]
assert known, 'Known engine.py not in AST results'

# Verify classes and functions are extracted
fa = py_results[known[0]]
assert len(fa.classes) > 0 or len(fa.functions) > 0, 'No symbols in engine.py'
print('Python files analysed:', len(py_results))
print('ASTAnalyzer Python OK')
"

echo
echo "[3/12] ASTAnalyzer — multi-language"
PYTHONPATH=lib python3 -c "
from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
analyzer = ASTAnalyzer('.', workspace_index=None)
results = analyzer.analyze()
langs = set(fa.language for fa in results.values())
print('Languages detected:', sorted(langs))
assert 'python' in langs, 'Python not detected'
assert 'markdown' in langs, 'Markdown not detected'
print('Multi-language analysis OK')
"

echo
echo "[4/12] ImportGraphBuilder"
PYTHONPATH=lib python3 -c "
from pathlib import Path
from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
from python.semantic_repository_intelligence.import_graph import ImportGraphBuilder

root = Path('.')
analyzer = ASTAnalyzer(root)
file_analyses = analyzer.analyze()

builder = ImportGraphBuilder()
ig = builder.build(file_analyses, root)

assert ig.nodes, 'Import graph has no nodes'
assert ig.edges, 'Import graph has no edges'
assert isinstance(ig.circular_dependencies, list), 'circular_dependencies must be list'
assert isinstance(ig.critical_modules, list), 'critical_modules must be list'
assert isinstance(ig.orphan_modules, list), 'orphan_modules must be list'
assert isinstance(ig.in_degree, dict), 'in_degree must be dict'

d = ig.to_dict()
assert 'node_count' in d
assert 'edge_count' in d
assert 'circular_dependency_count' in d

print('Import graph nodes:', ig.to_dict()[\"node_count\"])
print('Import graph edges:', ig.to_dict()[\"edge_count\"])
print('Circular dependencies:', ig.to_dict()[\"circular_dependency_count\"])
print('ImportGraphBuilder OK')
"

echo
echo "[5/12] CallGraphBuilder"
PYTHONPATH=lib python3 -c "
from pathlib import Path
from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
from python.semantic_repository_intelligence.call_graph import CallGraphBuilder

root = Path('.')
analyzer = ASTAnalyzer(root)
file_analyses = analyzer.analyze()

builder = CallGraphBuilder()
cg = builder.build(file_analyses, root)

assert isinstance(cg.edges, list)
assert isinstance(cg.entry_points, list)
assert isinstance(cg.execution_chains, list)

d = cg.to_dict()
assert 'edge_count' in d
assert 'entry_points' in d

print('Call graph edges:', d['edge_count'])
print('Entry points:', len(d['entry_points']))
print('CallGraphBuilder OK')
"

echo
echo "[6/12] DependencyGraphBuilder"
PYTHONPATH=lib python3 -c "
from pathlib import Path
from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
from python.semantic_repository_intelligence.dependency_graph import DependencyGraphBuilder

root = Path('.')
analyzer = ASTAnalyzer(root)
file_analyses = analyzer.analyze()

builder = DependencyGraphBuilder()
dg = builder.build(file_analyses, root)

assert isinstance(dg.external_dependencies, list)
assert isinstance(dg.internal_modules, list)
assert isinstance(dg.dependency_count, int)

d = dg.to_dict()
assert 'external_dependency_count' in d
assert 'internal_module_count' in d

print('External dependencies:', d['external_dependency_count'])
print('Internal modules:', d['internal_module_count'])
print('DependencyGraphBuilder OK')
"

echo
echo "[7/12] ArchitectureGraphBuilder"
PYTHONPATH=lib python3 -c "
from pathlib import Path
from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
from python.semantic_repository_intelligence.import_graph import ImportGraphBuilder
from python.semantic_repository_intelligence.architecture_graph import ArchitectureGraphBuilder

root = Path('.')
analyzer = ASTAnalyzer(root)
file_analyses = analyzer.analyze()

ig = ImportGraphBuilder().build(file_analyses, root)
ag = ArchitectureGraphBuilder().build(file_analyses, ig, root)

assert ag.nodes, 'Architecture graph has no nodes'
assert isinstance(ag.edges, list)
assert isinstance(ag.hotspots, list)
assert isinstance(ag.risks, list)
assert isinstance(ag.extension_points, list)

d = ag.to_dict()
assert 'node_count' in d
assert d['node_count'] > 0

print('Architecture nodes:', d['node_count'])
print('Architecture edges:', d['edge_count'])
print('Architecture risks:', len(ag.risks))
print('ArchitectureGraphBuilder OK')
"

echo
echo "[8/12] InjectionPointAnalyzer"
PYTHONPATH=lib python3 -c "
from pathlib import Path
from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
from python.semantic_repository_intelligence.injection_point_analyzer import InjectionPointAnalyzer

root = Path('.')
analyzer = ASTAnalyzer(root)
file_analyses = analyzer.analyze()

ips = InjectionPointAnalyzer().analyze(file_analyses, root)
assert isinstance(ips, list)

for ip in ips:
    assert hasattr(ip, 'name')
    assert hasattr(ip, 'type')
    assert hasattr(ip, 'file')
    assert hasattr(ip, 'confidence')
    assert 0.0 <= ip.confidence <= 1.0
    d = ip.to_dict()
    assert 'name' in d

print('Injection points found:', len(ips))
types_found = set(ip.type for ip in ips)
print('Types:', sorted(types_found))
print('InjectionPointAnalyzer OK')
"

echo
echo "[9/12] ConfidenceEngine"
PYTHONPATH=lib python3 -c "
from python.semantic_repository_intelligence.confidence_engine import ConfidenceEngine

engine = ConfidenceEngine()

# Basic scoring
c = engine.score(0.8, ['evidence1', 'evidence2'], cross_reference_count=3, evidence_tier='ast')
assert 0.0 <= c <= 1.0, 'Confidence out of range: %s' % c

# Zero evidence
c0 = engine.score(0.5, [], cross_reference_count=0, evidence_tier='heuristic')
assert 0.0 <= c0 <= 1.0

# Aggregate
agg = engine.aggregate([0.8, 0.9, 0.7, 0.6])
assert 0.0 <= agg <= 1.0

# Batch
findings = [
    {'base_confidence': 0.7, 'evidence': ['a', 'b'], 'evidence_tier': 'ast'},
    {'base_confidence': 0.5, 'evidence': [], 'evidence_tier': 'heuristic'},
]
scored = engine.score_batch(findings)
assert len(scored) == 2
assert 'confidence' in scored[0]

print('ConfidenceEngine OK')
"

echo
echo "[10/12] SemanticRecommendationEngine"
PYTHONPATH=lib python3 -c "
from pathlib import Path
from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
from python.semantic_repository_intelligence.import_graph import ImportGraphBuilder
from python.semantic_repository_intelligence.call_graph import CallGraphBuilder
from python.semantic_repository_intelligence.dependency_graph import DependencyGraphBuilder
from python.semantic_repository_intelligence.architecture_graph import ArchitectureGraphBuilder
from python.semantic_repository_intelligence.injection_point_analyzer import InjectionPointAnalyzer
from python.semantic_repository_intelligence.recommendation_engine import SemanticRecommendationEngine

root = Path('.')
file_analyses = ASTAnalyzer(root).analyze()
ig = ImportGraphBuilder().build(file_analyses, root)
cg = CallGraphBuilder().build(file_analyses, root)
dg = DependencyGraphBuilder().build(file_analyses, root)
ag = ArchitectureGraphBuilder().build(file_analyses, ig, root)
ips = InjectionPointAnalyzer().analyze(file_analyses, root)

engine = SemanticRecommendationEngine()
recs = engine.generate(ig, cg, dg, ag, ips)
findings = engine.generate_findings(ig, ag, ips)

assert isinstance(recs, list)
assert isinstance(findings, list)

for rec in recs:
    d = rec.to_dict()
    assert 'id' in d
    assert 'title' in d
    assert 'confidence' in d
    assert 'evidence' in d
    assert 'affected_modules' in d
    assert 'estimated_effort' in d
    assert 'estimated_impact' in d
    assert 'estimated_risk' in d
    assert 'implementation_order' in d
    assert rec.implementation_order >= 1

# Verify implementation_order is stable and starts at 1
orders = [r.implementation_order for r in recs]
assert orders == list(range(1, len(recs) + 1)), 'Implementation order not sequential: %s' % orders

print('Recommendations:', len(recs))
print('Findings:', len(findings))
print('SemanticRecommendationEngine OK')
"

echo
echo "[11/12] SemanticRepositoryEngine — full pipeline (AI-Toolkit)"
PYTHONPATH=lib python3 -c "
from python.semantic_repository_intelligence import SemanticRepositoryEngine

engine = SemanticRepositoryEngine(repository='.', persist=False)
result = engine.analyze()

# Structural assertions
assert 'repository' in result
assert 'file_count' in result
assert 'import_graph' in result
assert 'call_graph' in result
assert 'dependency_graph' in result
assert 'architecture_graph' in result
assert 'injection_points' in result
assert 'recommendations' in result
assert 'semantic_findings' in result
assert 'complexity' in result
assert 'next_core' in result

# Sanity checks
assert result['file_count'] > 0
assert result['import_graph']['node_count'] > 0
assert result['architecture_graph']['node_count'] > 0
assert isinstance(result['injection_points'], list)
assert isinstance(result['recommendations'], list)
assert isinstance(result['next_core'], str) and result['next_core']

# Complexity fields
cx = result['complexity']
required_cx = [
    'total_files', 'total_symbols', 'total_imports', 'total_functions',
    'total_classes', 'avg_imports_per_module', 'avg_functions_per_file',
    'max_imports_in_module', 'max_functions_in_file',
    'cyclomatic_complexity_estimate', 'language_distribution',
]
for k in required_cx:
    assert k in cx, 'Missing complexity key: %s' % k

print('File count:', result['file_count'])
print('Import graph:', result['import_graph']['node_count'], 'nodes')
print('Architecture:', result['architecture_graph']['node_count'], 'layers')
print('Recommendations:', len(result['recommendations']))
print('Injection points:', len(result['injection_points']))
print('Next CORE:', result['next_core'])
print('SemanticRepositoryEngine full pipeline OK')
"

echo
echo "[12/12] Determinism check"
PYTHONPATH=lib python3 -c "
import json
from python.semantic_repository_intelligence import SemanticRepositoryEngine

def run():
    engine = SemanticRepositoryEngine(repository='.', persist=False)
    result = engine.analyze()
    return {
        'file_count': result['file_count'],
        'import_nodes': result['import_graph']['node_count'],
        'import_edges': result['import_graph']['edge_count'],
        'circular_deps': result['import_graph']['circular_dependency_count'],
        'arch_nodes': result['architecture_graph']['node_count'],
        'arch_edges': result['architecture_graph']['edge_count'],
        'injection_points': len(result['injection_points']),
        'recommendations': len(result['recommendations']),
        'complexity_files': result['complexity']['total_files'],
        'next_core': result['next_core'],
    }

r1 = run()
r2 = run()

assert r1 == r2, 'Non-deterministic output! Run 1: %s\nRun 2: %s' % (r1, r2)
print('Deterministic output confirmed:', json.dumps(r1, indent=2))
print('Determinism check OK')
"

echo
echo "==========================================="
echo "Semantic Repository Intelligence PASS"
echo "CORE-008B"
echo "==========================================="
