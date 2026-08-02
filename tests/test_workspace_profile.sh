#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
import time
from pathlib import Path

sys.path.insert(0, "lib")

from python.repository_engine.engine import RepositoryEngine
from python.dependency_engine.engine import DependencyEngine
from python.validation_engine.engine import ValidationEngine
from python.planning_engine.engine import PlanningEngine
from python.repository_inspector_v2.engine import RepositoryInspectorV2
from python.canonical_audit.engine import CanonicalAuditEngine
from python.semantic_engine.engine import SemanticEngine
from python.knowledge_graph_v2.engine import KnowledgeGraphEngine
from python.workspace_manager.engine import WorkspaceManager

workspace = Path(".").resolve().parent
repositories = WorkspaceManager().discover(workspace)

ENGINES = [
    ("Repository", lambda r: RepositoryEngine(r).statistics()),
    ("Dependencies", lambda r: DependencyEngine(r).statistics()),
    ("Validation", lambda r: ValidationEngine(r).statistics()),
    ("Planning", lambda r: PlanningEngine(r).build_plan()),
    ("Inspector", lambda r: RepositoryInspectorV2(r).inspect()),
    ("CanonicalAudit", lambda r: CanonicalAuditEngine(r).audit()),
    ("Semantic", lambda r: SemanticEngine(r).analyze()),
    ("KnowledgeGraph", lambda r: KnowledgeGraphEngine(r).build()),
]

print("=" * 90)
print("WORKSPACE PERFORMANCE PROFILE")
print("=" * 90)

summary = []

for repo in repositories:

    print()
    print("=" * 90)
    print(repo["name"])
    print("=" * 90)

    total = 0.0
    row = {"Repository": repo["name"]}

    for name, fn in ENGINES:

        start = time.perf_counter()

        try:
            fn(repo["path"])
            elapsed = time.perf_counter() - start

            total += elapsed
            row[name] = elapsed

            print(f"{name:<20} {elapsed:>8.2f}s")

        except Exception as exc:
            row[name] = None
            print(f"{name:<20} FAILED ({exc})")

    row["Total"] = total
    summary.append(row)

print()
print("=" * 90)
print("SUMMARY")
print("=" * 90)

header = (
    f'{"Repository":25}'
    f'{"Repo":>8}'
    f'{"Dep":>8}'
    f'{"Plan":>8}'
    f'{"Insp":>8}'
    f'{"Audit":>8}'
    f'{"Sem":>8}'
    f'{"Graph":>8}'
    f'{"Total":>10}'
)

print(header)
print("-" * len(header))

for row in summary:

    def fmt(v):
        if v is None:
            return "FAIL"
        return f"{v:.1f}"

    print(
        f'{row["Repository"]:25}'
        f'{fmt(row["Repository"] and row["Repository"] or 0):>8}'
        f'{fmt(row["Dependencies"]):>8}'
        f'{fmt(row["Planning"]):>8}'
        f'{fmt(row["Inspector"]):>8}'
        f'{fmt(row["CanonicalAudit"]):>8}'
        f'{fmt(row["Semantic"]):>8}'
        f'{fmt(row["KnowledgeGraph"]):>8}'
        f'{row["Total"]:>10.1f}'
    )

print()
print("=" * 90)
print("WORKSPACE PROFILE PASS")
print("=" * 90)
PY
