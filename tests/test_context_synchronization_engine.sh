#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, "lib")

from python.context_synchronization_engine import (
    ContextCache,
    EngineeringContext,
    EngineeringContextSection,
    ContextPersistence,
    ContextResolver,
    ContextSynchronizationEngine,
    ContextValidator,
    DevelopmentContextProvider,
    GitContextProvider,
    GitHubContextProvider,
    SCHEMA_VERSION,
    SynchronizationCoordinator,
    SynchronizationFinding,
    SynchronizationReport,
    SynchronizationReportGenerator,
    WorkspaceContextProvider,
)
from python.development_state_engine.runtime import DevelopmentStateEngine
from python.executive_briefing_engine import ExecutiveBriefingEngine

REPO_ROOT = Path(".").resolve()

ROADMAP = """# AI TOOLKIT ROADMAP

# PHASE 1 — FOUNDATION
Status: COMPLETE

# PHASE 2 — CORE IMPLEMENTATION

# PHASE 3 — AUTONOMY
"""


def run(cmd, cwd, env=None):
    subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_fixture(root: Path, name: str):
    repo = root / name
    repo.mkdir(parents=True)
    (repo / "docs" / "canonical").mkdir(parents=True)
    for package in (
        "canonical_intelligence",
        "ai_cto_scanner",
        "semantic_repository_intelligence",
        "executable_repository_intelligence",
        "development_state_engine",
        "executive_briefing_engine",
        "workspace_orchestrator",
    ):
        package_dir = repo / "lib" / "python" / package
        package_dir.mkdir(parents=True, exist_ok=True)
        (package_dir / "__init__.py").write_text("", encoding="utf-8")
    (repo / "docs" / "canonical" / "ROADMAP_v2.0.0.md").write_text(ROADMAP, encoding="utf-8")
    (repo / "app.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
    (repo / ".ai" / "batches" / "BATCH-001").mkdir(parents=True)
    (repo / ".ai" / "batches" / "BATCH-002").mkdir(parents=True)
    write_json(repo / ".ai" / "batches" / "BATCH-001" / "metadata.json", {
        "identifier": "BATCH-001",
        "title": "Seed batch",
        "priority": "HIGH",
        "reason": "Fixture seed",
        "estimated_hours": 2,
        "status": "COMPLETED",
        "completed_at": "2026-08-03T00:00:00Z",
    })
    write_json(repo / ".ai" / "batches" / "BATCH-002" / "metadata.json", {
        "identifier": "BATCH-002",
        "title": "Second batch",
        "priority": "MEDIUM",
        "reason": "Fixture follow-up",
        "estimated_hours": 3,
        "status": "PLANNED",
        "completed_at": "2026-08-02T00:00:00Z",
    })
    write_json(repo / ".ai" / "semantic_knowledge.json", {
        "schema_version": "1.0.0",
        "repository": str(repo),
        "captured_at": "2026-08-03T00:00:00Z",
        "analysis": {
            "import_graph": {"node_count": 1, "edge_count": 0, "circular_dependency_count": 0, "critical_modules": [], "orphan_modules": []},
            "call_graph": {"edge_count": 0, "entry_points": ["app.run"]},
            "architecture_graph": {"node_count": 1, "edge_count": 0, "hotspots": [], "extension_points": [], "risk_count": 0},
            "dependency_graph": {"external_dependency_count": 0, "internal_module_count": 1},
            "complexity": {"total_files": 1},
            "recommendation_count": 0,
            "injection_point_count": 0,
            "next_core": "CORE-009 — Development State Engine: Persist full development state for cross-session reasoning.",
        },
    })
    run(["git", "init"], cwd=repo)
    run(["git", "config", "user.email", "copilot@example.com"], cwd=repo)
    run(["git", "config", "user.name", "Copilot"], cwd=repo)
    run(["git", "checkout", "-b", "copilot/core-013-context-sync"], cwd=repo)
    run(["git", "add", "."], cwd=repo)
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_DATE": "2026-08-03T00:00:00+00:00",
        "GIT_COMMITTER_DATE": "2026-08-03T00:00:00+00:00",
    })
    run(["git", "commit", "-m", "init"], cwd=repo, env=env)
    run(["git", "remote", "add", "origin", f"https://github.com/example/{name.lower().replace(' ', '-')} .git".replace(" .git", ".git")], cwd=repo)

    engine = DevelopmentStateEngine(repo)
    state = engine.LoadCurrentState(create_if_missing=True)
    stale = replace(
        state,
        workspace_state=replace(
            state.workspace_state,
            current_milestone="UNSPECIFIED",
            current_batch="UNSPECIFIED",
            current_task="UNSPECIFIED",
            estimated_progress=0.0,
        ),
        repository_state=replace(
            state.repository_state,
            branch="main",
        ),
        planning_state=replace(
            state.planning_state,
            current_roadmap="UNSPECIFIED",
            current_sprint="UNSPECIFIED",
            recommended_batch="UNSPECIFIED",
        ),
    )
    engine.SaveCurrentState(stale, source_event="fixture", timestamp="2026-08-03T00:00:00Z", refresh_integrations=False)
    return repo


class ContextSynchronizationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name)
        self.repo = build_fixture(self.workspace, "Trading Signals Platform")

    def tearDown(self):
        self.tmp.cleanup()

    def test_synchronize_corrects_stale_and_missing_context(self):
        result = ContextSynchronizationEngine(repository=self.repo, workspace_root=self.workspace).synchronize(refresh=False)
        live = result["live_context"]
        self.assertEqual(live["current_branch"], "copilot/core-013-context-sync")
        self.assertEqual(live["current_issue"], "CORE-013")
        self.assertEqual(live["current_recommendation"], "CORE-013")
        self.assertEqual(live["next_core"], "CORE-013")
        self.assertEqual(live["current_batch"], "BATCH-002")
        self.assertEqual(live["current_milestone"], "PHASE 2 — CORE IMPLEMENTATION")
        self.assertEqual(live["metadata"]["obsolete_recommendation"], "CORE-009")

        findings = {item["category"] for item in result["synchronization_report"]["findings"]}
        self.assertTrue("stale_branch" in findings or "conflicting_context" in findings)
        self.assertIn("obsolete_core_recommendation", findings)
        self.assertIn("missing_synchronization", findings)

        current_state = DevelopmentStateEngine(self.repo).LoadCurrentState()
        self.assertEqual(current_state.repository_state.branch, "copilot/core-013-context-sync")
        self.assertEqual(current_state.workspace_state.current_batch, "BATCH-002")
        self.assertEqual(current_state.planning_state.recommended_batch, "CORE-013")

        for relative in (
            ".ai/context/live_context.json",
            ".ai/context/development_context.json",
            ".ai/context/workspace_context.json",
            ".ai/context/git_context.json",
            ".ai/context/github_context.json",
            ".ai/context/synchronization_report.json",
            ".ai/context/engineering_context.json",
            ".ai/context/decision_history.json",
            ".ai/context/AI_CTO_CONTEXT_REPORT.md",
            ".ai/executive/briefing.json",
        ):
            self.assertTrue((self.repo / relative).exists(), relative)

        briefing = json.loads((self.repo / ".ai" / "executive" / "briefing.json").read_text(encoding="utf-8"))
        self.assertEqual(briefing["current_branch"], "copilot/core-013-context-sync")
        self.assertEqual(briefing["current_recommendation"], "CORE-013")
        self.assertNotEqual(briefing["current_milestone"], "UNSPECIFIED")
        engineering_context = json.loads((self.repo / ".ai" / "context" / "engineering_context.json").read_text(encoding="utf-8"))
        self.assertEqual(engineering_context["repository_context"]["owner"], "Repository Engine")
        self.assertEqual(engineering_context["decision_context"]["owner"], "Owner Decision Intelligence")
        self.assertEqual(engineering_context["knowledge_context"]["owner"], "Knowledge Engine")
        self.assertEqual(engineering_context["dashboard_context"]["owner"], "Engineering Dashboard Service")
        self.assertIn("current_branch", engineering_context["repository_context"]["data"])
        self.assertIn("changed_files", engineering_context["repository_context"]["data"])
        self.assertIn("briefing", engineering_context["executive_context"]["data"])
        self.assertIn("decision_history", engineering_context)
        self.assertIn("semantic_knowledge", engineering_context["knowledge_context"]["data"])
        history = json.loads((self.repo / ".ai" / "context" / "decision_history.json").read_text(encoding="utf-8"))
        self.assertIn("decision_history", history)
        self.assertTrue(isinstance(history["decision_history"], list))

    def test_synchronize_is_deterministic_for_identical_repo_state(self):
        engine = ContextSynchronizationEngine(repository=self.repo, workspace_root=self.workspace)
        engine.synchronize(refresh=False)
        engine.synchronize(refresh=False)
        first = {
            name: (self.repo / ".ai" / "context" / name).read_text(encoding="utf-8")
            for name in (
                "live_context.json",
                "development_context.json",
                "workspace_context.json",
                "git_context.json",
                "github_context.json",
                "synchronization_report.json",
                "AI_CTO_CONTEXT_REPORT.md",
            )
        }
        engine.synchronize(refresh=False)
        second = {
            name: (self.repo / ".ai" / "context" / name).read_text(encoding="utf-8")
            for name in first
        }
        self.assertEqual(first, second)

    def test_cli_context_supports_repository_and_workspace_paths(self):
        output = subprocess.run(
            [
                "bash",
                str(REPO_ROOT / "bin" / "ai"),
                "context",
                "--repository",
                str(self.repo),
                "--workspace",
                str(self.workspace),
                "--json",
            ],
            cwd=REPO_ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={**os.environ, "PYTHONPATH": "lib"},
        )
        payload = json.loads(output.stdout)
        self.assertEqual(payload["live_context"]["repository_root"], str(self.repo.resolve()))
        self.assertEqual(payload["workspace_context"]["workspace_root"], str(self.workspace.resolve()))


class RepositoryCoverageValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_fixture_repositories_validate(self):
        repos = [
            build_fixture(self.workspace, "Trading Signals Platform"),
            build_fixture(self.workspace, "DROPi-Mobile"),
            build_fixture(self.workspace, "DROPi-Tycoon"),
        ]
        for repo in repos:
            result = ContextSynchronizationEngine(repository=repo, workspace_root=self.workspace).synchronize(refresh=False)
            self.assertTrue(result["live_context"]["current_branch"].startswith("copilot/core-013"))
            self.assertEqual(result["live_context"]["current_recommendation"], "CORE-013")
            self.assertTrue((repo / ".ai" / "context" / "live_context.json").exists())

    def test_ai_toolkit_repository_integration(self):
        result = ContextSynchronizationEngine(repository=REPO_ROOT, workspace_root=REPO_ROOT.parent).synchronize(refresh=False)
        self.assertTrue(result["live_context"]["current_branch"])
        self.assertTrue((REPO_ROOT / ".ai" / "context" / "live_context.json").exists())


class PublicSurfaceTests(unittest.TestCase):
    def test_public_classes_importable(self):
        for value in (
            ContextCache,
            EngineeringContext,
            EngineeringContextSection,
            ContextPersistence,
            ContextResolver,
            ContextSynchronizationEngine,
            ContextValidator,
            DevelopmentContextProvider,
            GitContextProvider,
            GitHubContextProvider,
            SynchronizationCoordinator,
            SynchronizationFinding,
            SynchronizationReport,
            SynchronizationReportGenerator,
            WorkspaceContextProvider,
        ):
            self.assertTrue(callable(value), value)
        self.assertEqual(SCHEMA_VERSION, "1.0.0")


if __name__ == "__main__":
    unittest.main(verbosity=2)
PY
