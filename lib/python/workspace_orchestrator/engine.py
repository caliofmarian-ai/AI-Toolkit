from pathlib import Path

from python.workspace_manager.engine import WorkspaceManager
from python.agent_runtime.models import AgentContext
from python.agent_runtime.registry import build_runtime


class WorkspaceOrchestrator:

    def execute(self, workspace):

        runtime = build_runtime()

        repositories = WorkspaceManager().discover(workspace)

        results = []

        for repo in repositories:

            try:

                result = runtime.execute(
                    "develop",
                    AgentContext(
                        repository=repo["path"]
                    )
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
                })

            except Exception as exc:

                results.append({
                    "repository": repo["name"],
                    "status": "FAILED",
                    "error": str(exc),
                })

        return results
