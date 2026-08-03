"""
AI CTO Scanner Agent — CORE-008A

Agent wrapper for the AI CTO Integration Scanner.
Registered under the "inspect" name in the agent runtime.
"""

from python.agent_runtime.base import BaseAgent
from python.agent_runtime.models import AgentResult
from python.ai_cto_scanner.engine import AICTOScannerEngine


class AICTOScannerAgent(BaseAgent):
    """
    AI CTO Integration Scanner Agent.

    Inspects an arbitrary repository and produces an AI CTO integration
    report covering Telegram, Runtime, State, Owner Control, Configuration,
    Canonical, and Project Memory dimensions.
    """

    NAME = "inspect"

    def run(self, context):
        repository = context.repository or "."
        output_dir = context.metadata.get("output_dir", ".")

        engine = AICTOScannerEngine(repository=repository, output_dir=output_dir)
        scan_result = engine.scan()

        return AgentResult(
            agent=self.NAME,
            success=True,
            data={
                "repository": scan_result["repository"],
                "repository_name": scan_result["repository_name"],
                "workspace": scan_result["workspace"],
                "scores": scan_result["scores"],
                "detection_summary": {
                    cat: {
                        "score": data["score"],
                        "detected": data["detected"],
                        "total": data["total"],
                    }
                    for cat, data in scan_result["detection"].items()
                },
                "canonical_stats": scan_result.get("canonical_stats", {}),
                "report_path": scan_result.get("report_path", ""),
                "semantic_summary": self._semantic_summary(scan_result.get("semantic") or {}),
            },
            messages=[
                "AI CTO Integration Scanner completed.",
                "Report: %s" % scan_result.get("report_path", ""),
            ],
        )

    def _semantic_summary(self, semantic):
        """Extract a compact summary of the semantic analysis for agent output."""
        if not semantic:
            return {}
        ig = semantic.get("import_graph", {})
        ag = semantic.get("architecture_graph", {})
        return {
            "files_analyzed": semantic.get("file_count", 0),
            "import_graph_nodes": ig.get("node_count", 0),
            "import_graph_edges": ig.get("edge_count", 0),
            "circular_dependencies": ig.get("circular_dependency_count", 0),
            "architecture_nodes": ag.get("node_count", 0),
            "architecture_risks": len(ag.get("risks", [])),
            "injection_points": len(semantic.get("injection_points", [])),
            "recommendations": len(semantic.get("recommendations", [])),
            "next_core": semantic.get("next_core", ""),
        }
