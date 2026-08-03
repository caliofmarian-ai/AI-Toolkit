"""
Executable Repository Intelligence — Execution Model Report Generator
CORE-008C

Generates AI_CTO_EXECUTION_MODEL.md from the executable analysis result.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class ExecutionModelReportGenerator:
    """Generates AI_CTO_EXECUTION_MODEL.md."""

    def generate(self, result: Dict[str, Any], output_path: Path) -> str:
        """Write the report and return its content."""
        content = self._build(result)
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return content

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _build(self, r: Dict[str, Any]) -> str:
        sections = [
            self._header(r),
            self._executive_summary(r),
            self._runtime_map(r),
            self._file_classification_summary(r),
            self._executable_dependency_graph(r),
            self._injection_safety_summary(r),
            self._zone_summary(r),
            self._recommendations(r),
        ]
        return "\n\n".join(sections) + "\n"

    def _header(self, r: Dict[str, Any]) -> str:
        ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        repo = r.get("repository", ".")
        return "\n".join([
            "# AI CTO Execution Model",
            "",
            "**CORE-008C — Executable Repository Intelligence**",
            "",
            "| Field | Value |",
            "| ----- | ----- |",
            "| Repository | `%s` |" % repo,
            "| Generated | %s |" % ts,
            "| Executable Files | %d |" % r.get("executable_file_count", 0),
            "| Non-Executable Files | %d |" % r.get("non_executable_file_count", 0),
            "| Total Files | %d |" % (
                r.get("executable_file_count", 0) + r.get("non_executable_file_count", 0)
            ),
        ])

    def _executive_summary(self, r: Dict[str, Any]) -> str:
        lines = [
            "## Executive Summary",
            "",
            "This document is the authoritative **Executable Repository Model** "
            "for this repository.  It distinguishes files that participate in "
            "**runtime execution** from documentation, generated artifacts, and "
            "informational files.",
            "",
        ]

        # Category distribution
        cat_dist = r.get("category_distribution", {})
        if cat_dist:
            lines.append("### File Category Distribution")
            lines.append("")
            lines.append("| Category | Files |")
            lines.append("| -------- | ----- |")
            for cat, cnt in sorted(cat_dist.items()):
                lines.append("| %s | %d |" % (cat, cnt))
            lines.append("")

        # Zone distribution
        zone_dist = r.get("zone_distribution", {})
        if zone_dist:
            lines.append("### Directory Zone Distribution")
            lines.append("")
            lines.append("| Zone | Directories |")
            lines.append("| ---- | ----------- |")
            for zone, cnt in sorted(zone_dist.items()):
                lines.append("| %s | %d |" % (zone, cnt))
            lines.append("")

        return "\n".join(lines)

    def _runtime_map(self, r: Dict[str, Any]) -> str:
        rm = r.get("runtime_map", {})
        lines = [
            "## Repository Runtime Map",
            "",
        ]

        entry = rm.get("main_entry_point")
        lines.append("**Main Entry Point:** `%s`" % (entry or "_(not detected)_"))
        lines.append("")

        sched = rm.get("scheduler_entry")
        if sched:
            lines.append("**Scheduler Entry:** `%s`" % sched)
            lines.append("")

        def _list_section(title: str, items) -> str:
            if not items:
                return "**%s:** _(none detected)_" % title
            bullet = "\n".join("- `%s`" % x for x in items[:15])
            return "**%s:**\n\n%s" % (title, bullet)

        lines.append(_list_section("Execution Chain", rm.get("execution_chain", [])))
        lines.append("")
        lines.append(_list_section("Bootstrap Sequence", rm.get("bootstrap_sequence", [])))
        lines.append("")
        lines.append(_list_section("Background Workers", rm.get("background_workers", [])))
        lines.append("")
        lines.append(_list_section("Telegram Runtime", rm.get("telegram_runtime", [])))
        lines.append("")
        lines.append(_list_section("Owner Runtime", rm.get("owner_runtime", [])))
        lines.append("")
        lines.append(_list_section("Admin Runtime", rm.get("admin_runtime", [])))
        lines.append("")
        lines.append(_list_section("Persistence Runtime", rm.get("persistence_runtime", [])))
        lines.append("")
        lines.append(_list_section("Shutdown Hooks", rm.get("shutdown_hooks", [])))
        lines.append("")
        lines.append(_list_section("Restart Hooks", rm.get("restart_hooks", [])))
        lines.append("")
        lines.append(_list_section("Resume Hooks", rm.get("resume_hooks", [])))
        lines.append("")

        # Runtime components table
        components = rm.get("runtime_components", [])
        if components:
            lines.append("### Runtime Components")
            lines.append("")
            lines.append("| Component | File | Role | Layer |")
            lines.append("| --------- | ---- | ---- | ----- |")
            for c in components[:25]:
                lines.append("| %s | `%s` | %s | %s |" % (
                    c.get("name", ""), c.get("file", ""),
                    c.get("role", ""), c.get("layer", ""),
                ))
            if len(components) > 25:
                lines.append("| _…%d more_  | | | |" % (len(components) - 25))
            lines.append("")

        return "\n".join(lines)

    def _file_classification_summary(self, r: Dict[str, Any]) -> str:
        fcs = r.get("file_classifications", [])
        lines = [
            "## File Classifications",
            "",
            "All %d repository files classified into canonical categories." % len(fcs),
            "",
            "| Path | Category | Executable | Confidence |",
            "| ---- | -------- | ---------- | ---------- |",
        ]
        for fc in fcs[:50]:
            lines.append("| `%s` | %s | %s | %.2f |" % (
                fc.get("path", ""),
                fc.get("category", ""),
                "✓" if fc.get("is_executable") else "✗",
                fc.get("confidence", 0.0),
            ))
        if len(fcs) > 50:
            lines.append("| _…%d more files_ | | | |" % (len(fcs) - 50))
        lines.append("")
        return "\n".join(lines)

    def _executable_dependency_graph(self, r: Dict[str, Any]) -> str:
        dg = r.get("executable_dependency_graph", {})
        lines = [
            "## Executable Dependency Graph",
            "",
            "Contains **only executable files**.  Documentation, generated "
            "artifacts, and reports are excluded.",
            "",
            "| Metric | Value |",
            "| ------ | ----- |",
            "| Executable nodes | %d |" % dg.get("node_count", 0),
            "| Executable edges | %d |" % dg.get("edge_count", 0),
            "| Excluded files | %d |" % dg.get("excluded_count", 0),
            "",
        ]

        edges = dg.get("edges", [])
        if edges:
            lines.append("### Dependency Edges (sample)")
            lines.append("")
            lines.append("| Source | Target | Kind |")
            lines.append("| ------ | ------ | ---- |")
            for e in edges[:20]:
                lines.append("| `%s` | `%s` | %s |" % (
                    e.get("source", ""), e.get("target", ""), e.get("kind", "")
                ))
            if len(edges) > 20:
                lines.append("| _…%d more_ | | |" % (len(edges) - 20))
            lines.append("")

        return "\n".join(lines)

    def _injection_safety_summary(self, r: Dict[str, Any]) -> str:
        safety = r.get("injection_safety", [])
        safety_dist = r.get("safety_distribution", {})

        lines = [
            "## Injection Safety",
            "",
        ]

        if safety_dist:
            lines.append("| Safety Verdict | Count |")
            lines.append("| -------------- | ----- |")
            for verdict, cnt in sorted(safety_dist.items()):
                lines.append("| %s | %d |" % (verdict, cnt))
            lines.append("")

        if safety:
            unsafe = [s for s in safety if s.get("safety") == "UNSAFE"]
            if unsafe:
                lines.append("### ⚠ UNSAFE Injection Points")
                lines.append("")
                for s in unsafe[:10]:
                    lines.append("- **%s** in `%s`: %s" % (
                        s.get("name", ""), s.get("file", ""), s.get("rationale", "")
                    ))
                lines.append("")

            cond = [s for s in safety if s.get("safety") == "SAFE_WITH_CONDITIONS"]
            if cond:
                lines.append("### ⚡ SAFE WITH CONDITIONS (%d)" % len(cond))
                lines.append("")
                for s in cond[:10]:
                    lines.append("- **%s** in `%s`" % (s.get("name", ""), s.get("file", "")))
                lines.append("")

        return "\n".join(lines)

    def _zone_summary(self, r: Dict[str, Any]) -> str:
        zones = r.get("zones", [])
        lines = [
            "## Repository Zones",
            "",
            "| Directory | Zone | Files |",
            "| --------- | ---- | ----- |",
        ]
        for z in zones[:30]:
            lines.append("| `%s` | %s | %d |" % (
                z.get("path", ""), z.get("zone", ""), z.get("file_count", 0)
            ))
        if len(zones) > 30:
            lines.append("| _…%d more_ | | |" % (len(zones) - 30))
        lines.append("")
        return "\n".join(lines)

    def _recommendations(self, r: Dict[str, Any]) -> str:
        recs = r.get("recommendations", [])
        lines = [
            "## Recommendations",
            "",
        ]
        if not recs:
            lines.append("_No executable-layer recommendations generated._")
            lines.append("")
            return "\n".join(lines)

        for rec in recs:
            priority_badge = {
                "critical": "🔴",
                "high": "🟠",
                "medium": "🟡",
                "low": "🟢",
            }.get(rec.get("priority", "low"), "")
            lines.append("### %s %s — %s" % (
                priority_badge, rec.get("id", ""), rec.get("title", "")
            ))
            lines.append("")
            lines.append(rec.get("description", ""))
            lines.append("")
            evidence = rec.get("evidence", [])
            if evidence:
                lines.append("**Evidence:**")
                for e in evidence[:3]:
                    lines.append("- %s" % e)
                lines.append("")
            affected = rec.get("affected_files", [])
            if affected:
                lines.append("**Affected files:** %s" % ", ".join("`%s`" % f for f in affected[:5]))
                lines.append("")

        return "\n".join(lines)
