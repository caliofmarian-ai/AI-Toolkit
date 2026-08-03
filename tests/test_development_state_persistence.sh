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
    MODEL_VERSION,
    DevelopmentState,
    WorkspaceState,
    RepositoryState,
    ExecutionState,
    PlanningState,
    ReviewState,
    OwnerState,
    TelegramState,
    SnapshotMetadata,
    IntegrityReport,
)
from python.development_state_engine.repository import DevelopmentStateRepository


class DevelopmentStatePersistenceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.repo = DevelopmentStateRepository(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def _state(self, task="TASK-1", seq=1, snapshot_id=None):
        snapshot_id = snapshot_id or f"SNAP-{seq:03d}"
        return DevelopmentState(
            identifier="DEV-001",
            workspace_state=WorkspaceState(
                identifier="WS-001",
                active_project="AI-Toolkit",
                active_workspace="main",
                current_milestone="M1",
                current_batch="B1",
                current_task=task,
                completed_tasks=("TASK-0",),
                blocked_tasks=(),
                current_objective="Ship CORE-009B",
                estimated_progress=40.0,
            ),
            repository_state=RepositoryState(
                identifier="REPO-001",
                repository="caliofmarian-ai/AI-Toolkit",
                branch="main",
                head_commit="abc1234",
                open_pull_requests=("101",),
                latest_merge="merge-1",
                tags=("v0.1.0",),
                release="",
                repository_health="HEALTHY",
            ),
            execution_state=ExecutionState(
                identifier="EXEC-001",
                current_executor="agent",
                running_jobs=("job-1",),
                completed_jobs=("job-0",),
                failed_jobs=(),
                execution_queue=("job-2",),
                retry_queue=(),
                execution_history=("job-0", "job-1"),
            ),
            planning_state=PlanningState(
                identifier="PLAN-001",
                current_roadmap="RM-Q3",
                current_sprint="SPRINT-1",
                recommended_batch="B2",
                priority_queue=("TASK-2",),
                estimated_roi=5.0,
                estimated_time=8.0,
                dependencies=("dep-A",),
            ),
            review_state=ReviewState(
                identifier="REV-001",
                pending_reviews=("PR-1",),
                open_prs=("PR-1",),
                architecture_findings=(),
                canonical_findings=(),
                testing_status="PASSING",
                approval_status="PENDING",
            ),
            owner_state=OwnerState(
                identifier="OWN-001",
                owner_priorities=("quality",),
                manual_decisions=(),
                overrides=(),
                pinned_tasks=("TASK-2",),
                deferred_tasks=(),
            ),
            telegram_state=TelegramState(
                identifier="TG-001",
                session_id="session-1",
                chat_id="chat-1",
                active_thread="thread-1",
                last_message_at="2026-08-03T00:00:00Z",
                subscribed_channels=("dev",),
                pending_notifications=(),
            ),
            snapshot_metadata=SnapshotMetadata(
                identifier=snapshot_id,
                trigger="pull_request",
                created_at="2026-08-03T00:00:00Z",
                source_event="pr_opened",
                sequence_number=seq,
                tags=("core-009b",),
            ),
            integrity_report=IntegrityReport(
                identifier="INT-001",
                repository_integrity=99,
                canonical_integrity=98,
                memory_integrity=97,
                execution_integrity=96,
                planning_integrity=95,
                resume_integrity=94,
                overall_context_integrity_score=96,
            ),
        )

    def test_save_and_load_state_with_layout_files(self):
        state = self._state()
        self.repo.SaveState(state)

        self.assertTrue((self.root / ".ai" / "development_state" / "current_state.json").exists())
        self.assertTrue((self.root / ".ai" / "development_state" / "snapshots").exists())
        self.assertTrue((self.root / ".ai" / "development_state" / "integrity.json").exists())

        loaded = self.repo.LoadState()
        self.assertEqual(loaded, state)

    def test_deterministic_json_serialization(self):
        state = self._state()
        self.repo.SaveState(state)
        current_path = self.root / ".ai" / "development_state" / "current_state.json"
        integrity_path = self.root / ".ai" / "development_state" / "integrity.json"

        first_current = current_path.read_text(encoding="utf-8")
        first_integrity = integrity_path.read_text(encoding="utf-8")

        self.repo.SaveState(state)

        second_current = current_path.read_text(encoding="utf-8")
        second_integrity = integrity_path.read_text(encoding="utf-8")

        self.assertEqual(first_current, second_current)
        self.assertEqual(first_integrity, second_integrity)

    def test_create_snapshot_tracks_snapshot_history(self):
        self.repo.SaveState(self._state(task="TASK-A", seq=1, snapshot_id="SNAP-A"))
        first = self.repo.CreateSnapshot()

        self.repo.SaveState(self._state(task="TASK-B", seq=2, snapshot_id="SNAP-B"))
        second = self.repo.CreateSnapshot()

        self.assertTrue(first.exists())
        self.assertTrue(second.exists())

        integrity = json.loads((self.root / ".ai" / "development_state" / "integrity.json").read_text(encoding="utf-8"))
        history = integrity["snapshot_history"]
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["snapshot_id"], "SNAP-A")
        self.assertEqual(history[1]["snapshot_id"], "SNAP-B")

    def test_restore_snapshot_replaces_current_state(self):
        first_state = self._state(task="TASK-OLD", seq=1, snapshot_id="SNAP-OLD")
        self.repo.SaveState(first_state)
        first_snapshot = self.repo.CreateSnapshot()

        self.repo.SaveState(self._state(task="TASK-NEW", seq=2, snapshot_id="SNAP-NEW"))
        restored = self.repo.RestoreSnapshot("SNAP-OLD")

        self.assertEqual(restored.workspace_state.current_task, "TASK-OLD")
        self.assertEqual(self.repo.LoadState().workspace_state.current_task, "TASK-OLD")
        self.assertTrue(first_snapshot.exists())

    def test_export_and_import_state(self):
        original = self._state(task="TASK-EXPORT", seq=10, snapshot_id="SNAP-EXPORT")
        self.repo.SaveState(original)

        export_path = self.root / "state_export.json"
        self.repo.ExportState(export_path)
        self.assertTrue(export_path.exists())

        other_root = self.root / "other"
        other_repo = DevelopmentStateRepository(other_root)
        imported = other_repo.ImportState(export_path)

        self.assertEqual(imported, original)
        self.assertEqual(other_repo.LoadState(), original)

    def test_integrity_verification_detects_tampering(self):
        self.repo.SaveState(self._state())
        current_path = self.root / ".ai" / "development_state" / "current_state.json"

        tampered = json.loads(current_path.read_text(encoding="utf-8"))
        tampered["workspace_state"]["current_task"] = "TASK-TAMPERED"
        current_path.write_text(json.dumps(tampered, indent=2), encoding="utf-8")

        with self.assertRaises(ValueError):
            self.repo.LoadState()

    def test_import_supports_legacy_version_migration(self):
        legacy = self._state(task="TASK-LEGACY", seq=3, snapshot_id="SNAP-LEGACY").to_dict()
        legacy["schema_version"] = "0.9.0"
        for key in (
            "workspace_state",
            "repository_state",
            "execution_state",
            "planning_state",
            "review_state",
            "owner_state",
            "telegram_state",
            "snapshot_metadata",
            "integrity_report",
        ):
            legacy[key].pop("schema_version", None)

        source = self.root / "legacy_state.json"
        source.write_text(json.dumps(legacy, indent=2), encoding="utf-8")

        imported = self.repo.ImportState(source)
        self.assertEqual(imported.schema_version, MODEL_VERSION)
        self.assertEqual(imported.workspace_state.schema_version, MODEL_VERSION)
        self.assertEqual(self.repo.LoadState().schema_version, MODEL_VERSION)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DevelopmentStatePersistenceTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("\nDevelopment State Persistence PASS")
PY
