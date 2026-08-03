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

        if "workspace_index" in result:
            wi = result["workspace_index"]
            report.append("")
            report.append("## Workspace Index")
            report.append("")
            report.append(f"Scanned files: {wi['files']}")
            report.append(f"Scanned directories: {wi['directories']}")
            report.append(f"Ignored files: {wi['ignored_files']}")
            report.append(f"Ignored directories: {wi['ignored_directories']}")
            report.append(f"Scan duration: {wi['scan_duration']:.4f}s")
            report.append(f"Files per second: {wi['files_per_second']:.0f}")

            inc = wi.get("incremental")
            if inc:
                report.append("")
                report.append("### Incremental Cache")
                report.append("")
                if inc["cache_hit"]:
                    report.append("Status: **cache hit** — no changes detected")
                elif inc["cache_miss"]:
                    report.append("Status: **cache miss** — full rebuild performed")
                else:
                    report.append("Status: **partial rebuild** — only changed files re-scanned")
                report.append(f"Files reused: {inc['files_reused']}")
                report.append(f"Files rebuilt: {inc['files_rebuilt']}")
                report.append(f"Rebuild percentage: {inc['rebuild_percentage']:.1f}%")
                if inc["saved_time_estimate"] > 0:
                    report.append(
                        f"Estimated time saved: {inc['saved_time_estimate']:.4f}s"
                    )

        report.append("")
        report.append("## Health")
        report.append("")
        report.append(f"Health: **{result['inspection']['repository_health']}**")
        report.append(f"Score: **{result['inspection']['repository_score']}/100**")

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
        report.append("## Next Actions")
        report.append("")

        for item in result["recommendations_generated"]:
            report.append(f"- [{item['priority']}] {item['title']}")
            report.append(f"  Reason: {item['reason']}")
            report.append(f"  Estimated: {item['estimated_hours']} h")
            report.append("")


        report.append("")
        report.append("## Generated Batches")
        report.append("")

        for batch in result["generated_batches"]:
            report.append(
                f'- {batch.identifier} [{batch.priority}] {batch.title}'
            )
            report.append(
                f'  Estimate: {batch.estimated_hours} h'
            )
            report.append("")


        report.append("")
        report.append("## Review")
        report.append("")
        report.append(f'Status: **{result["review"]["status"]}**')
        report.append(f'Score: **{result["review"]["score"]}/100**')
        report.append("")

        for item in result["review"]["summary"]:
            report.append(f"- {item}")

        report.append("")


        report.append("")
        report.append("## Roadmap")
        report.append("")
        report.append(f'Total estimate: {result["roadmap"]["estimated_hours"]} h')
        report.append("")

        for phase in result["roadmap"]["phases"]:
            report.append(f'### {phase["name"]}')
            if phase["items"]:
                for item in phase["items"]:
                    report.append(f'- {item}')
            else:
                report.append("- No actions")
            report.append("")


        report.append("")
        report.append("## Execution State")
        report.append("")
        report.append(
            f'Status: **{result["execution_state"]["status"]}**'
        )
        report.append("")

        for phase in result["execution_state"]["phases"]:
            report.append(
                f'- {phase["name"]}: {phase["status"]}'
            )

        report.append("")


        report.append("")
        report.append("## Workspace")
        report.append("")

        for repo in result["workspace"]:
            report.append(
                f'- {repo["name"]}'
            )

        report.append("")

        report.append("## Planning Tasks")
        report.append("")

        for task in result["planning"].tasks:
            report.append(
                f"- [{task.priority}] {task.identifier}: {task.title}"
            )




        report.append("")
        report.append("## Workspace Summary")
        report.append("")
        report.append("Generated by Development Agent.")
        report.append("")

        output = Path(".ai/audit/development_report.md")
        output.parent.mkdir(parents=True, exist_ok=True)

        output.write_text(
            "\n".join(report),
            encoding="utf-8"
        )

        return output
