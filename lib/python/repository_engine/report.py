from abc import ABC, abstractmethod


class BaseRenderer(ABC):
    """Minimal rendering contract for RepositoryProfile renderers."""

    @abstractmethod
    def render(self, profile) -> str:
        ...


class MarkdownRenderer(BaseRenderer):
    """Renders a RepositoryProfile as a Markdown inspection report."""


    def render(self, profile) -> str:
        metrics = profile.metrics
        health = profile.health_summary

        lines = []
        lines.append("# Repository Inspect Report")
        lines.append("")
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Repository:** `{profile.name}`")
        lines.append(f"- **Path:** `{profile.path}`")
        lines.append(f"- **Repository Health:** **{health['status']}** ({health['score']}/100)")
        lines.append(f"- **Health Notes:** {health['summary']}")
        lines.append(f"- **Total Files:** {metrics.total_files}")
        lines.append(f"- **Total Directories:** {metrics.total_directories}")
        lines.append("")
        lines.append("## File Distribution")
        lines.append("")
        for key, value in metrics.file_class_distribution.items():
            lines.append(f"- **{key}**: {value}")

        lines.append("")
        lines.append("## Language Distribution")
        lines.append("")
        if metrics.language_distribution:
            for key, value in metrics.language_distribution.items():
                lines.append(f"- **{key}**: {value}")
        else:
            lines.append("- No supported source files detected.")

        lines.append("")
        lines.append("## Tech Stack")
        lines.append("")
        if profile.tech_stack:
            for item in profile.tech_stack:
                lines.append(f"- {item}")
        else:
            lines.append("- No stack markers detected.")

        lines.append("")
        lines.append("## Entry Points")
        lines.append("")
        if profile.entry_points:
            for item in profile.entry_points:
                lines.append(f"- `{item}`")
        else:
            lines.append("- No entry points detected.")

        lines.append("")
        lines.append("## Dependencies")
        lines.append("")
        lines.append(f"- **Internal import nodes:** {profile.dependencies.internal_import_nodes}")
        lines.append(f"- **Internal import edges:** {profile.dependencies.internal_import_edges}")
        lines.append(f"- **Unresolved imports:** {profile.dependencies.unresolved_imports}")
        if profile.dependencies.manifests:
            lines.append("")
            for manifest, deps in profile.dependencies.manifests.items():
                lines.append(f"### {manifest}")
                lines.append("")
                for dep in deps:
                    lines.append(f"- {dep}")
                lines.append("")
        else:
            lines.append("- No dependency manifests detected.")
            lines.append("")

        lines.append("## Test Coverage Ratio")
        lines.append("")
        lines.append(
            f"- {metrics.test_file_count} test files / {metrics.total_files} total files "
            f"({metrics.test_coverage_ratio:.2%})"
        )

        lines.append("")
        lines.append("## Documentation Coverage")
        lines.append("")
        lines.append(
            f"- {metrics.documentation_file_count} documentation files / {metrics.total_files} total files "
            f"({metrics.documentation_coverage_ratio:.2%})"
        )

        lines.append("")
        lines.append("## Repository Health Summary")
        lines.append("")
        for check in health["checks"]:
            status = "PASS" if check["passed"] else "FAIL"
            lines.append(f"- **{status}** {check['name']}: {check['message']}")

        return "\n".join(lines) + "\n"

# Backward-compatible alias
ReportRenderer = MarkdownRenderer
