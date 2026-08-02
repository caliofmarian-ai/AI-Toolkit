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

        path.write_text(
            "\n".join(lines),
            encoding="utf-8"
        )
