#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, "lib")

from python.development_state_engine.runtime import DevelopmentStateEngine
from python.semantic_repository_intelligence.persistence import SemanticPersistence


class RuntimeIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "docs" / "canonical").mkdir(parents=True)
        (self.root / "docs" / "canonical" / "CANON-030_DEVELOPMENT_STATE_ENGINE_SPECIFICATION_v1.0.0.md").write_text(
            "# CANON-030 — Development State Engine Specification\n\nVersion: 1.0.0\n\n## Objective\n- Persist development state\n",
            encoding="utf-8",
        )
        (self.root / "lib" / "python").mkdir(parents=True)
        (self.root / "lib" / "python" / "sample.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
        subprocess.run(["git", "init"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["git", "config", "user.email", "copilot@example.com"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Copilot"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=self.root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        SemanticPersistence(self.root).save(
            {
                "import_graph": {"node_count": 1, "edge_count": 0, "critical_modules": [], "orphan_modules": []},
                "call_graph": {"edge_count": 0, "entry_points": ["sample.run"]},
                "architecture_graph": {"node_count": 1, "edge_count": 0, "hotspots": [], "risks": []},
                "dependency_graph": {"external_dependency_count": 0, "internal_module_count": 1},
                "complexity": {"total_files": 1},
                "recommendations": [],
                "injection_points": [],
                "next_core": "CORE-009",
            }
        )
        self.engine = DevelopmentStateEngine(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_runtime_components_work_together_for_one_repository(self):
        state = self.engine.LoadCurrentState(create_if_missing=True)
        self.assertEqual(state.repository_state.branch, "master")

        self.engine.RecordWorkspaceEvent(
            "sync",
            workspace="workspace-main",
            milestone="M3",
            epic="EPIC-3",
            batch="BATCH-3",
            task="TASK-3",
            timestamp="2026-08-03T03:00:00Z",
        )
        self.engine.RecordIssue("ISSUE-3", task="TASK-3", timestamp="2026-08-03T03:10:00Z")
        self.engine.RecordPullRequest("PR-3", timestamp="2026-08-03T03:20:00Z")
        self.engine.RecordBatch("BATCH-3", status="COMPLETED", timestamp="2026-08-03T03:30:00Z")
        snapshot = self.engine.GenerateExecutiveSnapshot(refresh_integrations=False, timestamp="2026-08-03T03:40:00Z")

        self.assertEqual(snapshot.current_context["current_workspace"], "workspace-main")
        self.assertEqual(snapshot.current_context["current_issue"], "ISSUE-3")
        self.assertEqual(snapshot.current_context["current_pull_request"], "PR-3")
        self.assertEqual(snapshot.current_context["current_batch"], "BATCH-3")
        self.assertEqual(snapshot.integrations["semantic_repository_intelligence"]["analysis"]["next_core"], "CORE-009")
        self.assertGreaterEqual(snapshot.integrations["repository_intelligence"]["statistics"]["files"], 3)

        events = json.loads((self.root / ".ai" / "development_state" / "events.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(events["event_count"], 4)
        self.assertTrue((self.root / ".ai" / "development_state" / "snapshots").exists())
        self.assertTrue((self.root / ".ai" / "development_state" / "executive_snapshot.json").exists())

    def test_multiple_repositories_are_isolated(self):
        self.engine.LoadCurrentState(create_if_missing=True)
        other_tmp = tempfile.TemporaryDirectory()
        other_root = Path(other_tmp.name)
        (other_root / "repo.py").write_text("print('x')\n", encoding="utf-8")
        subprocess.run(["git", "init"], cwd=other_root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["git", "config", "user.email", "copilot@example.com"], cwd=other_root, check=True)
        subprocess.run(["git", "config", "user.name", "Copilot"], cwd=other_root, check=True)
        subprocess.run(["git", "add", "."], cwd=other_root, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=other_root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        second_engine = DevelopmentStateEngine(other_root)
        second_engine.LoadCurrentState(create_if_missing=True)
        second_engine.RecordIssue("ISSUE-X", timestamp="2026-08-03T04:00:00Z")
        self.engine.GenerateExecutiveSnapshot(refresh_integrations=False, timestamp="2026-08-03T04:10:00Z")

        first_snapshot = json.loads((self.root / ".ai" / "development_state" / "executive_snapshot.json").read_text(encoding="utf-8"))
        second_snapshot = json.loads((other_root / ".ai" / "development_state" / "executive_snapshot.json").read_text(encoding="utf-8"))
        self.assertNotEqual(first_snapshot["current_context"]["current_repository"], second_snapshot["current_context"]["current_repository"])
        self.assertEqual(second_snapshot["current_context"]["current_issue"], "ISSUE-X")
        other_tmp.cleanup()


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RuntimeIntegrationTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("\nDevelopment State Runtime Integration PASS")
PY
