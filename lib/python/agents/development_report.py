from pathlib import Path


class DevelopmentReport:

    @staticmethod
    def generate(result):

        report = []

        report.append("# AI Toolkit Development Report")
        report.append("")

        report.append("## Executive Summary")
        report.append("")
        report.append(f"Repository files: {result['repository']['files']}")
        report.append(f"Dependencies: {result['dependencies']['dependencies']}")
        report.append(f"Validation passed: {result['validation']['passed']}")
        report.append(f"Canonical documents: {len(result['canonical']['canonical_documents'])}")
        report.append(f"Semantic files: {len(result['semantic'])}")
        report.append(f"Knowledge graph nodes: {len(result['knowledge_graph']['nodes'])}")
        report.append("")

        report.append("## Health")
        report.append("")
        health = result["inspection"]["repository_health"]
        score = result["inspection"]["repository_score"]

        report.append(f"Health: **{health}**")
        report.append(f"Score: **{score}/100**")
        report.append("")

        report.append("## Findings")
        report.append("")

        findings = result["inspection"]["findings"]

        if findings:
            for item in findings:
                report.append(
                    f"- [{item['severity']}] {item['message']}"
                )
        else:
            report.append("- No findings.")

        report.append("")
        report.append("## Recommendations")
        report.append("")

        recommendations = result["inspection"]["recommendations"]

        if recommendations:
            for item in recommendations:
                report.append(f"- {item}")
        else:
            report.append("- No recommendations.")

        report.append("")
        report.append("## Planning Tasks")
        report.append("")

        for task in result["planning"].tasks:
            report.append(
                f"- [{task.priority}] {task.identifier}: {task.title}"
            )



        report.append("")
        report.append("## Next Actions")
        report.append("")

        for item in result["recommendations_generated"]:
            report.append(
                f'- [{item["priority"]}] {item["title"]}'
            )
            report.append(
                f'  Reason: {item["reason"]}'
            )
            report.append(
                f'  Estimated: {item["estimated_hours"]} h'
            )
            report.append("")

                path = Path(".ai/audit/development_report.md")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "\n".join(report),
            encoding="utf-8"
        )

        return path
