#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
import unittest
from dataclasses import FrozenInstanceError

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


class DevelopmentStateModelsTest(unittest.TestCase):
    def make_workspace(self):
        return WorkspaceState(
            identifier="WS-001",
            active_project="AI-Toolkit",
            active_workspace="main",
            current_milestone="M1",
            current_batch="BATCH-9",
            current_task="TASK-91",
            completed_tasks=("TASK-1", "TASK-2"),
            blocked_tasks=("TASK-7",),
            current_objective="Ship CORE-009A",
            estimated_progress=42.5,
        )

    def make_repository(self):
        return RepositoryState(
            identifier="REPO-001",
            repository="caliofmarian-ai/AI-Toolkit",
            branch="main",
            head_commit="abcdef1",
            open_pull_requests=("101", "102"),
            latest_merge="merge-commit",
            tags=("v0.1.0",),
            release="v0.2.0-alpha",
            repository_health="HEALTHY",
        )

    def make_execution(self):
        return ExecutionState(
            identifier="EXEC-001",
            current_executor="copilot-agent",
            running_jobs=("job-1",),
            completed_jobs=("job-0",),
            failed_jobs=("job-x",),
            execution_queue=("job-2", "job-3"),
            retry_queue=("job-r1",),
            execution_history=("job-0", "job-x", "job-1"),
        )

    def make_planning(self):
        return PlanningState(
            identifier="PLAN-001",
            current_roadmap="RM-2026-Q3",
            current_sprint="SPRINT-32",
            recommended_batch="BATCH-10",
            priority_queue=("TASK-93", "TASK-92"),
            estimated_roi=7.5,
            estimated_time=12.0,
            dependencies=("dep-A", "dep-B"),
        )

    def make_review(self):
        return ReviewState(
            identifier="REV-001",
            pending_reviews=("PR-101",),
            open_prs=("PR-101", "PR-102"),
            architecture_findings=("risk-1",),
            canonical_findings=("canon-gap-1",),
            testing_status="PASSING",
            approval_status="PENDING",
        )

    def make_owner(self):
        return OwnerState(
            identifier="OWN-001",
            owner_priorities=("stability", "delivery"),
            manual_decisions=("defer-x",),
            overrides=("override-y",),
            pinned_tasks=("TASK-90",),
            deferred_tasks=("TASK-89",),
        )

    def make_telegram(self):
        return TelegramState(
            identifier="TG-001",
            session_id="sess-1",
            chat_id="chat-777",
            active_thread="thread-main",
            last_message_at="2026-08-03T03:53:31Z",
            subscribed_channels=("ops", "dev"),
            pending_notifications=("notif-1",),
        )

    def make_snapshot(self):
        return SnapshotMetadata(
            identifier="SNAP-001",
            trigger="pull_request",
            created_at="2026-08-03T03:53:31Z",
            source_event="pr_opened",
            sequence_number=9,
            tags=("core-009a", "canonical"),
        )

    def make_integrity(self):
        return IntegrityReport(
            identifier="INT-001",
            repository_integrity=98.0,
            canonical_integrity=96.0,
            memory_integrity=97.0,
            execution_integrity=99.0,
            planning_integrity=95.0,
            resume_integrity=94.0,
            overall_context_integrity_score=96.5,
        )

    def make_development_state(self):
        return DevelopmentState(
            identifier="DEV-001",
            workspace_state=self.make_workspace(),
            repository_state=self.make_repository(),
            execution_state=self.make_execution(),
            planning_state=self.make_planning(),
            review_state=self.make_review(),
            owner_state=self.make_owner(),
            telegram_state=self.make_telegram(),
            snapshot_metadata=self.make_snapshot(),
            integrity_report=self.make_integrity(),
        )

    def test_round_trip_serialization_for_all_models(self):
        ws = WorkspaceState.from_dict(self.make_workspace().to_dict())
        repo = RepositoryState.from_dict(self.make_repository().to_dict())
        exec_state = ExecutionState.from_dict(self.make_execution().to_dict())
        plan = PlanningState.from_dict(self.make_planning().to_dict())
        review = ReviewState.from_dict(self.make_review().to_dict())
        owner = OwnerState.from_dict(self.make_owner().to_dict())
        tg = TelegramState.from_dict(self.make_telegram().to_dict())
        snap = SnapshotMetadata.from_dict(self.make_snapshot().to_dict())
        integrity = IntegrityReport.from_dict(self.make_integrity().to_dict())
        dev = DevelopmentState.from_dict(self.make_development_state().to_dict())

        self.assertEqual(ws, self.make_workspace())
        self.assertEqual(repo, self.make_repository())
        self.assertEqual(exec_state, self.make_execution())
        self.assertEqual(plan, self.make_planning())
        self.assertEqual(review, self.make_review())
        self.assertEqual(owner, self.make_owner())
        self.assertEqual(tg, self.make_telegram())
        self.assertEqual(snap, self.make_snapshot())
        self.assertEqual(integrity, self.make_integrity())
        self.assertEqual(dev, self.make_development_state())

    def test_versioning_defaults_and_is_serialized(self):
        dev = self.make_development_state()
        data = dev.to_dict()

        self.assertEqual(dev.schema_version, MODEL_VERSION)
        self.assertEqual(data["schema_version"], MODEL_VERSION)
        self.assertEqual(data["workspace_state"]["schema_version"], MODEL_VERSION)
        self.assertEqual(data["integrity_report"]["schema_version"], MODEL_VERSION)

    def test_identifier_is_immutable_for_all_models(self):
        models = [
            self.make_workspace(),
            self.make_repository(),
            self.make_execution(),
            self.make_planning(),
            self.make_review(),
            self.make_owner(),
            self.make_telegram(),
            self.make_snapshot(),
            self.make_integrity(),
            self.make_development_state(),
        ]

        for model in models:
            with self.assertRaises(FrozenInstanceError):
                model.identifier = "MUTATED"

    def test_validation_rejects_invalid_values(self):
        with self.assertRaises(ValueError):
            WorkspaceState(
                identifier="",
                active_project="AI-Toolkit",
                active_workspace="main",
                current_milestone="M1",
                current_batch="B1",
                current_task="T1",
                estimated_progress=10,
            )

        with self.assertRaises(ValueError):
            IntegrityReport(
                identifier="INT-ERR",
                repository_integrity=110,
                canonical_integrity=90,
                memory_integrity=90,
                execution_integrity=90,
                planning_integrity=90,
                resume_integrity=90,
                overall_context_integrity_score=90,
            )

        with self.assertRaises(ValueError):
            SnapshotMetadata(
                identifier="SNAP-ERR",
                trigger="merge",
                created_at="2026-08-03",
                source_event="merge_completed",
                sequence_number=-1,
            )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DevelopmentStateModelsTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("\nDevelopment State Engine Models PASS")
PY
