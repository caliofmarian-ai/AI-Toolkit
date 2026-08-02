#!/bin/bash
set -e

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.workspace_index import (
    WorkspaceIndexBuilder,
    RepositoryPolicy,
    WorkspaceIndexExporter,
    WorkspaceIndex,
)

print("=" * 60)
print("WorkspaceIndex — Test Suite")
print("=" * 60)
print()

# ---------------------------------------------------------------
# Test 1 — WorkspaceIndex creation
# ---------------------------------------------------------------

policy = RepositoryPolicy()
builder = WorkspaceIndexBuilder(".", policy=policy)
index = builder.build()

assert index is not None, "WorkspaceIndex must not be None"
assert index.repository_name, "Repository name must be set"
assert index.repository_root, "Repository root must be set"
assert index.statistics.total_files > 0, "Must have scanned files"
assert index.statistics.total_directories > 0, "Must have scanned directories"
assert index.statistics.scan_duration > 0, "Scan duration must be positive"
assert index.statistics.files_per_second > 0, "Files per second must be positive"

print(f"[PASS] WorkspaceIndex creation")
print(f"       files={index.statistics.total_files}  dirs={index.statistics.total_directories}")
print(f"       scan={index.statistics.scan_duration:.4f}s  fps={index.statistics.files_per_second:.0f}")

# ---------------------------------------------------------------
# Test 2 — RepositoryPolicy application
# ---------------------------------------------------------------

git_excluded = any(
    ".git" in f.path.split("/")
    for f in index.files
)
pycache_excluded = any(
    "__pycache__" in f.path.split("/")
    for f in index.files
)

assert not git_excluded, ".git entries must be excluded by RepositoryPolicy"
assert not pycache_excluded, "__pycache__ entries must be excluded by RepositoryPolicy"
assert index.statistics.ignored_directories > 0, "RepositoryPolicy must report ignored directories"

print(f"[PASS] RepositoryPolicy application")
print(f"       ignored_dirs={index.statistics.ignored_directories}  ignored_files={index.statistics.ignored_files}")

# ---------------------------------------------------------------
# Test 3 — Exactly one repository traversal
# ---------------------------------------------------------------

traversal_count = [0]
original_walk = __import__("os").walk

def counting_walk(*args, **kwargs):
    traversal_count[0] += 1
    return original_walk(*args, **kwargs)

import os
os.walk = counting_walk

index2 = WorkspaceIndexBuilder(".", policy=policy).build()

os.walk = original_walk

assert traversal_count[0] == 1, (
    f"WorkspaceIndexBuilder must call os.walk exactly once, called {traversal_count[0]} times"
)

print(f"[PASS] Exactly one repository traversal (os.walk called {traversal_count[0]} time)")

# ---------------------------------------------------------------
# Test 4 — Immutable WorkspaceIndex
# ---------------------------------------------------------------

mutation_blocked = False

try:
    index.repository_name = "hacked"
except AttributeError:
    mutation_blocked = True

assert mutation_blocked, "WorkspaceIndex must be immutable"

try:
    index._files = ()
except AttributeError:
    pass

print(f"[PASS] Immutable WorkspaceIndex")

# ---------------------------------------------------------------
# Test 5 — Engine compatibility (engines consume WorkspaceIndex)
# ---------------------------------------------------------------

from python.repository_engine.engine import RepositoryEngine
from python.dependency_engine.engine import DependencyEngine
from python.validation_engine.engine import ValidationEngine
from python.planning_engine.engine import PlanningEngine
from python.canonical_audit.engine import CanonicalAuditEngine
from python.semantic_engine.engine import SemanticEngine
from python.knowledge_graph_v2.engine import KnowledgeGraphEngine
from python.repository_inspector_v2.engine import RepositoryInspectorV2

repo_stats = RepositoryEngine(".", workspace_index=index).statistics()
assert repo_stats["files"] == index.statistics.total_files
assert repo_stats["files"] > 0

dep_stats = DependencyEngine(".", workspace_index=index).statistics()
assert dep_stats["dependencies"] > 0

plan = PlanningEngine(".", workspace_index=index).build_plan()
assert len(plan.tasks) > 0

canonical = CanonicalAuditEngine(".", workspace_index=index).audit()
assert len(canonical["canonical_documents"]) > 0

semantic = SemanticEngine(".", workspace_index=index).analyze()
assert len(semantic) > 0

kg = KnowledgeGraphEngine(".", workspace_index=index).build()
assert len(kg["nodes"]) > 0

inspection = RepositoryInspectorV2(".", workspace_index=index).inspect()
assert "repository_health" in inspection

print(f"[PASS] Engine compatibility")
print(f"       repo_files={repo_stats['files']}  deps={dep_stats['dependencies']}")
print(f"       plan_tasks={len(plan.tasks)}  canonical_docs={len(canonical['canonical_documents'])}")
print(f"       semantic_files={len(semantic)}  kg_nodes={len(kg['nodes'])}")

# ---------------------------------------------------------------
# Test 6 — Performance metrics
# ---------------------------------------------------------------

stats = index.statistics
assert hasattr(stats, "scan_duration"), "statistics must have scan_duration"
assert hasattr(stats, "files_per_second"), "statistics must have files_per_second"
assert hasattr(stats, "total_files"), "statistics must have total_files"
assert hasattr(stats, "total_directories"), "statistics must have total_directories"
assert hasattr(stats, "ignored_files"), "statistics must have ignored_files"
assert hasattr(stats, "ignored_directories"), "statistics must have ignored_directories"
assert stats.scan_duration > 0
assert stats.files_per_second > 0

print(f"[PASS] Performance metrics")
print(f"       scan_duration={stats.scan_duration:.4f}s  files_per_second={stats.files_per_second:.0f}")

# ---------------------------------------------------------------
# Test 7 — Serialization
# ---------------------------------------------------------------

import json
import tempfile
import os as _os

with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as tmp:
    tmp_path = tmp.name

try:
    exported = WorkspaceIndexExporter.export(index, tmp_path)
    data = json.loads(open(tmp_path).read())

    assert data["repository_name"] == index.repository_name
    assert data["statistics"]["total_files"] == index.statistics.total_files
    assert len(data["files"]) == len(index.files)
    assert "extension_histogram" in data

    print(f"[PASS] Serialization")
    print(f"       exported {len(data['files'])} files to JSON")
finally:
    _os.unlink(tmp_path)

# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------

print()
print("=" * 60)
print("All WorkspaceIndex tests PASS")
print("=" * 60)
PY
