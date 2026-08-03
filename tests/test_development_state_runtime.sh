#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, "lib")

from python.development_state_engine.models import (
    DevelopmentState,
    ExecutionState,
    IntegrityReport,
    OwnerState,
    PlanningState,
    RepositoryState,
    ReviewState,
    SnapshotMetadata,
    TelegramState,
    WorkspaceState,
)
from python.development_state_engine.runtime import (
    DevelopmentStateEngine,
    DevelopmentStateEventBus,
    DevelopmentStateManager,
)


class FakeRepositoryEngine:
    def __init__(self, root="."):
        self.root = root

    def statistics(self):
        return {"items": 3, "files": 2, "directories": 1}


class FakeCanonicalIntelligenceEngine:
    def __init__(self, repository=".", **_kwargs):
        self.repository = repository

    def run(self):
        return {"coverage": [], "compliance": [], "drift": [], "batches": [], "canonical_repository": None, "graph": None}

    def statistics(self, _result):
        return {"canonical_documents": 4, "overall_coverage": 92.5}


class FakeSemanticRepositoryEngine:
    def __init__(self, repository=".", persist=True, **_kwargs):
        self.repository = repository
        self.persist = persist

    def analyze(self):
        return {
            "import_graph": {"node_count": 4, "edge_count": 6},
            "architecture_graph": {"node_count": 3, "edge_count": 2, "hotspots": ["lib/python/development_state_engine/runtime.py"]},
            "complexity": {"total_files": 4},
            "recommendations": [{"id": "REC-1", "title": "Adopt runtime orchestration", "priority": "high"}],
            "next_core": "CORE-010",
        }


class FakeAICTOScannerEngine:
    def __init__(self, repository=".", output_dir=None):
        self.repository = repository
        self.output_dir = output_dir

    def scan(self):
        return {
            "repository_name": Path(self.repository).name,
            "scores": {"overall": 98},
            "workspace": {"total_files": 2, "total_directories": 1},
            "detection": {"state": {}, "runtime": {}},
        }


class RuntimeUnitTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "docs" / "canonical").mkdir(parents=True)
        (self.root / "docs" / "canonical" / "CANON-001_TEST.md").write_text("# Canon\n", encoding="utf-8")
        self.engine = DevelopmentStateEngine(
            self.root,
            repository_engine_class=FakeRepositoryEngine,
            canonical_engine_class=FakeCanonicalIntelligenceEngine,
            semantic_engine_class=FakeSemanticRepositoryEngine,
            ai_cto_scanner_class=FakeAICTOScannerEngine,
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_event_bus_deduplicates_same_event(self):
        bus = DevelopmentStateEventBus(self.root)
        first = bus.Publish(
            "execution",
            payload={"execution_id": "JOB-1", "status": "RUNNING"},
            context={"current_executor": "agent-1"},
            timestamp="2026-08-03T00:00:00Z",
        )
        second = bus.Publish(
            "execution",
            payload={"execution_id": "JOB-1", "status": "RUNNING"},
            context={"current_executor": "agent-1"},
            timestamp="2026-08-03T00:00:10Z",
        )
        self.assertEqual(first["fingerprint"], second["fingerprint"])
        payload = bus.LoadEvents()
        self.assertEqual(payload["event_count"], 1)
        self.assertEqual(payload["events"][0]["sequence_number"], 1)

    def test_runtime_updates_outputs_and_integrations(self):
        state = self.engine.LoadCurrentState(create_if_missing=True)
        self.assertIsNotNone(state)

        updated = self.engine.UpdateState(
            {
                "current_workspace": "workspace-A",
                "current_milestone": "M2",
                "current_epic": "EPIC-9",
                "current_task": "TASK-55",
                "current_pull_request": "PR-101",
                "current_canon_version": "CANON-v1",
            },
            timestamp="2026-08-03T01:00:00Z",
            refresh_integrations=True,
        )
        self.assertEqual(updated.workspace_state.active_workspace, "workspace-A")
        self.assertEqual(updated.workspace_state.current_task, "TASK-55")
        self.assertEqual(updated.planning_state.current_roadmap, "EPIC-9")

        snapshot = json.loads((self.root / ".ai" / "development_state" / "executive_snapshot.json").read_text(encoding="utf-8"))
        self.assertEqual(snapshot["current_context"]["current_pull_request"], "PR-101")
        self.assertEqual(snapshot["current_context"]["current_canon_version"], "CANON-v1")
        self.assertEqual(snapshot["integrations"]["repository_intelligence"]["statistics"]["files"], 2)
        self.assertEqual(snapshot["integrations"]["canonical_intelligence"]["canonical_documents"], 4)
        self.assertEqual(snapshot["integrations"]["semantic_repository_intelligence"]["analysis"]["top_recommendation"]["id"], "REC-1")
        self.assertEqual(snapshot["integrations"]["ai_cto_scanner"]["scores"]["overall"], 98)

        events = json.loads((self.root / ".ai" / "development_state" / "events.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(events["event_count"], 2)
        self.assertTrue((self.root / ".ai" / "development_state" / "current_state.json").exists())
        self.assertTrue((self.root / ".ai" / "development_state" / "integrity.json").exists())

    def test_record_methods_create_snapshots_and_preserve_unique_state(self):
        self.engine.LoadCurrentState(create_if_missing=True)
        self.engine.RecordExecution("JOB-1", status="RUNNING", executor="agent-1", timestamp="2026-08-03T02:00:00Z")
        self.engine.RecordExecution("JOB-1", status="RUNNING", executor="agent-1", timestamp="2026-08-03T02:00:00Z")
        self.engine.RecordDecision("DEC-1", decision="Ship it", recommendation="BATCH-9", timestamp="2026-08-03T02:10:00Z")
        self.engine.RecordPullRequest("PR-9", status="OPEN", timestamp="2026-08-03T02:20:00Z")
        self.engine.RecordBatch("BATCH-9", status="COMPLETED", recommendation="BATCH-9", timestamp="2026-08-03T02:30:00Z")
        self.engine.RecordMerge("MERGE-9", branch="main", head_commit="abc1234", timestamp="2026-08-03T02:40:00Z")

        state = self.engine.LoadCurrentState()
        self.assertEqual(state.execution_state.running_jobs, ("JOB-1",))
        self.assertEqual(state.execution_state.execution_history, ("JOB-1",))
        self.assertEqual(state.repository_state.open_pull_requests, ("PR-9",))
        self.assertEqual(state.workspace_state.current_batch, "BATCH-9")

        integrity = json.loads((self.root / ".ai" / "development_state" / "integrity.json").read_text(encoding="utf-8"))
        self.assertEqual(len(integrity["snapshot_history"]), 4)
        self.assertEqual(integrity["snapshot_history"][-1]["snapshot_id"], "SNAP-000004")


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RuntimeUnitTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("\nDevelopment State Runtime PASS")
PY
