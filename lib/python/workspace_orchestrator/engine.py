from pathlib import Path

from python.workspace_manager.engine import WorkspaceManager
from python.agent_runtime.models import AgentContext
from python.agent_runtime.registry import build_runtime
from python.progress_monitor.engine import ProgressMonitor


class WorkspaceOrchestrator:

    def execute(self, workspace):

        runtime = build_runtime()

        monitor = ProgressMonitor()

        repositories = WorkspaceManager().discover(workspace)

        monitor.section("Workspace Execution")

        monitor.message(
            f"Repositories discovered: {len(repositories)}"
        )

        results = []

        for repo in repositories:

            try:

                started = monitor.start(
                    repo["name"]
                )

                result = runtime.execute(
                    "develop",
                    AgentContext(
                        repository=repo["path"]
                    )
                )

                elapsed = monitor.finish(
                    repo["name"],
                    started
                )

                results.append({
                    "repository": repo["name"],
                    "status": "SUCCESS",
                    "report_score": result.data["inspection"]["repository_score"],
                    "health": result.data["inspection"]["repository_health"],
                    "recommendations": len(
                        result.data["recommendations_generated"]
                    ),
                    "batches": len(
                        result.data["generated_batches"]
                    ),
                    "elapsed": elapsed,
                })

            except Exception as exc:

                elapsed = monitor.finish(
                    repo["name"],
                    started
                )

                results.append({
                    "repository": repo["name"],
                    "status": "FAILED",
                    "error": str(exc),
                })

        monitor.total()

        return results
