from pathlib import Path

class MarkdownReport:

    @staticmethod
    def generate(report, filename):

        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        lines = []

        lines.append("# Repository Inspection Report")
        lines.append("")
        lines.append(f"Repository Health: **{report['repository_health']}**")
        lines.append("")

        lines.append("## Repository")
        lines.append("")
        for key, value in report["repository"].items():
            lines.append(f"- **{key}**: {value}")

        lines.append("")
        lines.append("## Dependencies")
        lines.append("")
        for key, value in report["dependencies"].items():
            lines.append(f"- **{key}**: {value}")

        lines.append("")
        lines.append("## Validation")
        lines.append("")
        for key, value in report["validation"].items():
            lines.append(f"- **{key}**: {value}")

        lines.append("")
        lines.append("## Execution Plan")
        lines.append("")

        for task in report["plan"]["tasks"]:
            lines.append(
                f"- [{task['priority']}] {task['identifier']} — {task['title']}"
            )



        lines.append("")
        lines.append("## Repository Score")
        lines.append("")
        lines.append(f'**{report["repository_score"]}/100**')

        lines.append("")
        lines.append("## Findings")
        lines.append("")

        if report["findings"]:
            for item in report["findings"]:
                lines.append(
                    f'- **{item["severity"]}**: {item["message"]}'
                )
        else:
            lines.append("- No findings.")

        lines.append("")
        lines.append("## Recommendations")
        lines.append("")

        if report["recommendations"]:
            for item in report["recommendations"]:
                lines.append(f"- {item}")
        else:
            lines.append("- No recommendations.")


        path.write_text(
            "\n".join(lines),
            encoding="utf-8"
        )
