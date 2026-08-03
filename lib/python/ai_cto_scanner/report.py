"""
AI CTO Integration Scanner — Report Generator

Generates AI_CTO_INTEGRATION_REPORT.md from scanner results.
"""

from datetime import datetime
from pathlib import Path


class AICTOReportGenerator:
    """Generate the AI_CTO_INTEGRATION_REPORT.md file."""

    def generate(self, scan_result, output_path):
        """Write the integration report to output_path."""
        content = self._build_report(scan_result)
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return content

    def _build_report(self, r):
        sections = [
            self._header(r),
            self._executive_summary(r),
            self._architecture_map(r),
            self._integration_points(r),
            self._injection_points(r),
            self._detected_components(r),
            self._missing_components(r),
            self._development_order(r),
            self._risk_analysis(r),
            self._implementation_roadmap(r),
            self._estimated_effort(r),
            self._readiness_scores(r),
        ]
        # CORE-008B — Semantic intelligence sections
        semantic = r.get("semantic")
        if semantic:
            sections += [
                self._semantic_architecture_graph(semantic),
                self._semantic_dependency_summary(semantic),
                self._semantic_injection_point_summary(semantic),
                self._semantic_critical_modules(semantic),
                self._semantic_architecture_risks(semantic),
                self._semantic_extension_points(semantic),
                self._semantic_recommendations(semantic),
                self._semantic_findings(semantic),
                self._repository_complexity(semantic),
                self._suggested_next_core(semantic),
            ]
        return "\n\n".join(sections) + "\n"

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------

    def _header(self, r):
        ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        return "\n".join([
            "# AI CTO Integration Report",
            "",
            "| Field | Value |",
            "| --- | --- |",
            "| Repository | `%s` |" % r["repository"],
            "| Generated | %s |" % ts,
            "| Scanner | CORE-008A AI CTO Integration Scanner |",
            "| Overall AI CTO Readiness | **%d / 100** |" % r["scores"].get("Overall AI CTO Readiness", 0),
        ])

    # ------------------------------------------------------------------
    # Executive Summary
    # ------------------------------------------------------------------

    def _executive_summary(self, r):
        scores = r["scores"]
        detection = r["detection"]
        total_detected = sum(d["detected"] for d in detection.values())
        total_components = sum(d["total"] for d in detection.values())
        canonical = r.get("canonical_stats", {})
        lines = [
            "## Executive Summary",
            "",
            "The AI CTO Integration Scanner analysed **`%s`** and produced the following assessment." % r["repository"],
            "",
            "| Dimension | Score |",
            "| --- | ---: |",
        ]
        for dim, score in scores.items():
            bar = self._score_bar(score)
            lines.append("| %s | %s %d%% |" % (dim, bar, score))
        lines += [
            "",
            "**Components detected:** %d / %d" % (total_detected, total_components),
        ]
        if canonical:
            lines += [
                "",
                "**Canonical documents:** %d" % canonical.get("canonical_documents", 0),
                "**Knowledge graph nodes:** %d" % canonical.get("graph_nodes", 0),
                "**Overall coverage:** %.0f%%" % (canonical.get("overall_coverage", 0) * 100),
                "**Overall compliance:** %.0f%%" % (canonical.get("overall_compliance", 0) * 100),
                "**Drift findings:** %d" % canonical.get("drift_findings", 0),
            ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Architecture Map
    # ------------------------------------------------------------------

    def _architecture_map(self, r):
        detection = r["detection"]
        lines = [
            "## Architecture Map",
            "",
            "Discovered architectural layers and their detection confidence.",
            "",
            "| Layer | Components Found | Coverage | Status |",
            "| --- | ---: | --- | --- |",
        ]
        for category, data in detection.items():
            detected = data["detected"]
            total = data["total"]
            score = data["score"]
            bar = self._score_bar(int(score * 100))
            status = self._status_emoji(score)
            lines.append("| %s | %d / %d | %s %.0f%% | %s |" % (
                self._fmt_category(category), detected, total, bar, score * 100, status
            ))
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Integration Points
    # ------------------------------------------------------------------

    def _integration_points(self, r):
        detection = r["detection"]
        lines = [
            "## Integration Points",
            "",
            "Key files and locations where AI CTO can integrate with the repository.",
            "",
        ]
        for category, data in detection.items():
            found_files = []
            for comp in data["components"]:
                if comp["found"]:
                    found_files.extend(comp["files"])
            if not found_files:
                continue
            found_files = sorted(set(found_files))[:8]
            lines.append("### %s" % self._fmt_category(category))
            lines.append("")
            for f in found_files:
                lines.append("- `%s`" % f)
            lines.append("")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Injection Points
    # ------------------------------------------------------------------

    def _injection_points(self, r):
        detection = r["detection"]
        lines = [
            "## Injection Points",
            "",
            "Recommended locations where AI CTO instrumentation should be injected.",
            "",
        ]
        injection_map = {
            "Telegram": [
                "Inject AI CTO supervisor after bot initialization",
                "Wrap update handlers with AI CTO tracing decorator",
                "Add context awareness to FSM state transitions",
            ],
            "Runtime": [
                "Register AI CTO lifecycle hooks at startup",
                "Inject scheduler monitoring into existing schedulers",
                "Wrap service initialization with AI CTO bootstrap",
            ],
            "State": [
                "Extend state store to persist AI CTO context",
                "Add AI CTO snapshot hooks to existing snapshot logic",
                "Integrate resume engine with restart recovery",
            ],
            "OwnerControl": [
                "Extend owner permission layer with AI CTO approval gates",
                "Register AI CTO admin commands in admin dashboard",
            ],
            "Configuration": [
                "Add AI CTO configuration block to existing config file",
                "Register AI_CTO_TOKEN and AI_CTO_MODE environment variables",
            ],
            "Canonical": [
                "Extend canonical specification pipeline with AI CTO specs",
                "Register AI CTO compliance checks in existing drift engine",
            ],
            "ProjectMemory": [
                "Connect project memory to AI CTO context persistence layer",
                "Bind snapshot engine to AI CTO resume engine",
            ],
        }
        for category, suggestions in injection_map.items():
            data = detection.get(category, {})
            score = data.get("score", 0.0)
            if score > 0.0:
                priority = "HIGH" if score < 0.5 else "MEDIUM"
            else:
                priority = "CRITICAL"
            lines.append("### %s `[%s]`" % (self._fmt_category(category), priority))
            lines.append("")
            for s in suggestions:
                lines.append("- %s" % s)
            lines.append("")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Detected Components
    # ------------------------------------------------------------------

    def _detected_components(self, r):
        detection = r["detection"]
        lines = [
            "## Detected Components",
            "",
        ]
        for category, data in detection.items():
            comps = [c for c in data["components"] if c["found"]]
            if not comps:
                continue
            lines.append("### %s" % self._fmt_category(category))
            lines.append("")
            lines.append("| Component | Confidence | Key Signal |")
            lines.append("| --- | ---: | --- |")
            for c in comps:
                signal = c["signals"][0] if c["signals"] else "—"
                lines.append("| %s | %.0f%% | `%s` |" % (c["name"], c["confidence"] * 100, signal))
            lines.append("")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Missing Components
    # ------------------------------------------------------------------

    def _missing_components(self, r):
        detection = r["detection"]
        lines = [
            "## Missing Components",
            "",
            "Components not yet detected in the repository.",
            "",
        ]
        for category, data in detection.items():
            missing = [c for c in data["components"] if not c["found"]]
            if not missing:
                continue
            lines.append("### %s" % self._fmt_category(category))
            lines.append("")
            for c in missing:
                lines.append("- **%s** — not detected" % c["name"])
            lines.append("")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Recommended Development Order
    # ------------------------------------------------------------------

    def _development_order(self, r):
        detection = r["detection"]
        scores = r["scores"]

        order = [
            ("Runtime", "Runtime Readiness", "Establish startup and lifecycle management"),
            ("Configuration", None, "Establish configuration and secrets management"),
            ("State", "State Readiness", "Implement state persistence and session management"),
            ("OwnerControl", "Owner Readiness", "Implement owner identity and permission layer"),
            ("Telegram", "Telegram Readiness", "Implement bot entry point and all handlers"),
            ("Canonical", "Canonical Readiness", "Align implementation with canonical specifications"),
            ("ProjectMemory", "Project Memory Readiness", "Implement project memory and context persistence"),
        ]

        lines = [
            "## Recommended Development Order",
            "",
            "| Priority | Layer | Readiness | Rationale |",
            "| ---: | --- | ---: | --- |",
        ]
        for idx, (cat, score_key, rationale) in enumerate(order, 1):
            score = scores.get(score_key, 0) if score_key else None
            score_str = ("%d%%" % score) if score is not None else "—"
            lines.append("| %d | %s | %s | %s |" % (idx, self._fmt_category(cat), score_str, rationale))
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Risk Analysis
    # ------------------------------------------------------------------

    def _risk_analysis(self, r):
        detection = r["detection"]
        scores = r["scores"]
        lines = [
            "## Risk Analysis",
            "",
            "| Risk | Severity | Affected Layer | Mitigation |",
            "| --- | --- | --- | --- |",
        ]

        risk_threshold = 40
        for category, data in detection.items():
            score = int(data["score"] * 100)
            if score < risk_threshold:
                sev = "CRITICAL" if score == 0 else "HIGH"
                lines.append("| %s layer not detected or incomplete | %s | %s | Implement missing components before AI CTO integration |" % (
                    self._fmt_category(category), sev, self._fmt_category(category)
                ))

        if scores.get("Overall AI CTO Readiness", 0) < 30:
            lines.append("| Repository not ready for AI CTO integration | CRITICAL | All | Address missing components in priority order |")

        if scores.get("Canonical Readiness", 0) == 0:
            lines.append("| No canonical specifications found | HIGH | Canonical | Add CANON-*.md specification documents |")

        if scores.get("Project Memory Readiness", 0) == 0:
            lines.append("| No project memory infrastructure | HIGH | ProjectMemory | Implement project memory and context persistence |")

        if len(lines) == 5:
            lines.append("| No critical risks identified | LOW | All | Continue implementation and monitor drift |")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Implementation Roadmap
    # ------------------------------------------------------------------

    def _implementation_roadmap(self, r):
        scores = r["scores"]
        lines = [
            "## Implementation Roadmap",
            "",
            "### Phase 1 — Foundation (Weeks 1–2)",
            "",
        ]
        phase1 = []
        phase2 = []
        phase3 = []

        for dim, score in scores.items():
            if dim == "Overall AI CTO Readiness":
                continue
            if score < 30:
                phase1.append((dim, score))
            elif score < 70:
                phase2.append((dim, score))
            else:
                phase3.append((dim, score))

        if phase1:
            for dim, score in phase1:
                lines.append("- [ ] Implement **%s** (current: %d%%)" % (dim, score))
        else:
            lines.append("- All foundation layers are sufficiently implemented.")
        lines += [
            "",
            "### Phase 2 — Integration (Weeks 3–5)",
            "",
        ]
        if phase2:
            for dim, score in phase2:
                lines.append("- [ ] Strengthen **%s** (current: %d%%)" % (dim, score))
        else:
            lines.append("- All integration layers are sufficiently implemented.")
        lines += [
            "",
            "### Phase 3 — AI CTO Activation (Weeks 6+)",
            "",
        ]
        if phase3:
            for dim, score in phase3:
                lines.append("- [x] **%s** ready (current: %d%%)" % (dim, score))
        lines += [
            "- [ ] Deploy AI CTO runtime alongside the application",
            "- [ ] Enable context integrity monitoring",
            "- [ ] Activate project memory and resume engine",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Estimated Effort
    # ------------------------------------------------------------------

    def _estimated_effort(self, r):
        scores = r["scores"]
        total_gap = sum(max(0, 100 - s) for k, s in scores.items() if k != "Overall AI CTO Readiness")
        total_dimensions = len([k for k in scores if k != "Overall AI CTO Readiness"])
        avg_gap = total_gap / total_dimensions if total_dimensions else 0

        if avg_gap < 10:
            weeks = "1–2"
            effort = "Low"
        elif avg_gap < 30:
            weeks = "2–4"
            effort = "Moderate"
        elif avg_gap < 60:
            weeks = "4–8"
            effort = "Significant"
        else:
            weeks = "8–16"
            effort = "Substantial"

        lines = [
            "## Estimated Effort",
            "",
            "| Dimension | Gap | Estimated Hours |",
            "| --- | ---: | ---: |",
        ]
        for dim, score in scores.items():
            if dim == "Overall AI CTO Readiness":
                continue
            gap = max(0, 100 - score)
            hours = max(1, int(gap * 0.2))
            lines.append("| %s | %d%% | %d h |" % (dim, gap, hours))

        lines += [
            "",
            "**Overall effort:** %s (%s weeks)" % (effort, weeks),
            "",
            "> Estimates assume one senior engineer working on AI CTO integration.",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Readiness Scores
    # ------------------------------------------------------------------

    def _readiness_scores(self, r):
        scores = r["scores"]
        lines = [
            "## AI CTO Readiness Score",
            "",
            "| Dimension | Score | Rating |",
            "| --- | ---: | --- |",
        ]
        for dim, score in scores.items():
            rating = self._rating(score)
            bar = self._score_bar(score)
            lines.append("| **%s** | %s %d%% | %s |" % (dim, bar, score, rating))
        lines += [
            "",
            "---",
            "",
            "> *Report generated by CORE-008A AI CTO Integration Scanner / CORE-008B Semantic Repository Intelligence.*",
            "> *Reuse the `ai inspect <path>` command to refresh this report after changes.*",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # CORE-008B — Semantic intelligence sections
    # ------------------------------------------------------------------

    def _semantic_architecture_graph(self, semantic):
        ag = semantic.get("architecture_graph", {})
        nodes = ag.get("nodes", [])
        edges = ag.get("edges", [])
        lines = [
            "## Architecture Graph Summary",
            "",
            "Semantic architecture layers discovered and their inter-layer dependencies.",
            "",
            "| Layer | Modules | In-Degree | Out-Degree |",
            "| --- | ---: | ---: | ---: |",
        ]
        for node in nodes:
            lines.append("| **%s** | %d | %d | %d |" % (
                node["name"], node["module_count"], node["in_degree"], node["out_degree"]
            ))
        lines += [
            "",
            "**Architecture edges (inter-layer dependencies):** %d" % len(edges),
        ]
        if edges:
            lines += [
                "",
                "| From Layer | To Layer | Relationship | Strength |",
                "| --- | --- | --- | ---: |",
            ]
            for edge in sorted(edges, key=lambda e: -e.get("strength", 0))[:15]:
                lines.append("| %s | %s | %s | %.2f |" % (
                    edge["source"], edge["target"],
                    edge["relationship"], edge["strength"]
                ))
        return "\n".join(lines)

    def _semantic_dependency_summary(self, semantic):
        dg = semantic.get("dependency_graph", {})
        ig = semantic.get("import_graph", {})
        lines = [
            "## Dependency Summary",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            "| External dependencies | %d |" % dg.get("external_dependency_count", 0),
            "| Internal Python modules | %d |" % dg.get("internal_module_count", 0),
            "| Import graph edges | %d |" % ig.get("edge_count", 0),
            "| Circular dependencies | %d |" % ig.get("circular_dependency_count", 0),
            "| Orphan modules | %d |" % len(ig.get("orphan_modules", [])),
        ]
        ext_deps = dg.get("external_dependencies", [])
        if ext_deps:
            lines += [
                "",
                "**Top external dependencies:**",
                "",
            ]
            for dep in ext_deps[:10]:
                lines.append("- `%s` %s (%s)" % (dep["name"], dep.get("version_spec", ""), dep["ecosystem"]))
        circulars = ig.get("circular_dependencies", [])
        if circulars:
            lines += [
                "",
                "**Circular dependencies detected:**",
                "",
            ]
            for cycle in circulars[:5]:
                lines.append("- %s" % " → ".join(cycle + [cycle[0]]))
        return "\n".join(lines)

    def _semantic_injection_point_summary(self, semantic):
        ips = semantic.get("injection_points", [])
        type_counts: dict = {}
        for ip in ips:
            t = ip.get("type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1
        lines = [
            "## Injection Point Summary",
            "",
            "Semantically discovered extension and injection points.",
            "",
            "| Type | Count |",
            "| --- | ---: |",
        ]
        for t, cnt in sorted(type_counts.items()):
            lines.append("| %s | %d |" % (t, cnt))
        lines += ["", "**Total injection points:** %d" % len(ips)]
        if ips:
            lines += [
                "",
                "**Key injection points:**",
                "",
                "| Name | Type | File | Confidence |",
                "| --- | --- | --- | ---: |",
            ]
            for ip in sorted(ips, key=lambda x: -x.get("confidence", 0))[:10]:
                lines.append("| %s | %s | `%s` | %.0f%% |" % (
                    ip["name"], ip["type"],
                    ip["file"][:60], ip.get("confidence", 0) * 100
                ))
        return "\n".join(lines)

    def _semantic_critical_modules(self, semantic):
        ig = semantic.get("import_graph", {})
        critical = ig.get("critical_modules", [])
        top_imported = ig.get("top_imported", [])
        lines = [
            "## Critical Modules",
            "",
            "Modules with the highest import in-degree — the architectural backbone of the repository.",
            "",
        ]
        if top_imported:
            lines += [
                "| Module | In-Degree |",
                "| --- | ---: |",
            ]
            for module, degree in top_imported[:10]:
                marker = " ⭐" if module in critical else ""
                lines.append("| `%s`%s | %d |" % (module, marker, degree))
        else:
            lines.append("*No critical modules identified.*")
        return "\n".join(lines)

    def _semantic_architecture_risks(self, semantic):
        ag = semantic.get("architecture_graph", {})
        risks = ag.get("risks", [])
        lines = [
            "## Architecture Risks",
            "",
            "| Risk | Severity | Confidence | Affected Modules |",
            "| --- | --- | ---: | --- |",
        ]
        if risks:
            severity_emoji = {
                "critical": "🔴 Critical",
                "high": "🟠 High",
                "medium": "🟡 Medium",
                "low": "🟢 Low",
            }
            for risk in risks:
                sev = severity_emoji.get(risk.get("severity", "low"), risk.get("severity", ""))
                modules = ", ".join("`%s`" % m[:40] for m in risk.get("affected_modules", [])[:3])
                conf = risk.get("confidence", 0)
                lines.append("| %s | %s | %.0f%% | %s |" % (
                    risk["title"], sev, conf * 100, modules or "—"
                ))
        else:
            lines.append("| No architecture risks identified | — | — | — |")
        return "\n".join(lines)

    def _semantic_extension_points(self, semantic):
        ag = semantic.get("architecture_graph", {})
        extension_points = ag.get("extension_points", [])
        lines = [
            "## Recommended Extension Points",
            "",
            "Architectural layers identified as high-value extension targets.",
            "",
        ]
        if extension_points:
            for ep in extension_points:
                lines.append("- **%s**" % ep)
        else:
            lines.append("*No extension points identified yet — add plugin interfaces or event buses.*")
        return "\n".join(lines)

    def _semantic_recommendations(self, semantic):
        recs = semantic.get("recommendations", [])
        lines = [
            "## Semantic Recommendations",
            "",
            "Evidence-based architectural recommendations generated by CORE-008B.",
            "",
            "| # | Priority | Recommendation | Confidence | Effort | Impact | Risk |",
            "| ---: | --- | --- | ---: | --- | --- | --- |",
        ]
        priority_emoji = {
            "critical": "🔴 Critical",
            "high": "🟠 High",
            "medium": "🟡 Medium",
            "low": "🟢 Low",
        }
        for rec in recs[:20]:
            pri = priority_emoji.get(rec.get("priority", "low"), rec.get("priority", ""))
            conf = rec.get("confidence", 0)
            lines.append("| %d | %s | %s | %.0f%% | %s | %s | %s |" % (
                rec.get("implementation_order", 0),
                pri,
                rec["title"],
                conf * 100,
                rec.get("estimated_effort", "—"),
                rec.get("estimated_impact", "—"),
                rec.get("estimated_risk", "—"),
            ))
        if not recs:
            lines.append("| — | — | No recommendations generated | — | — | — | — |")
        return "\n".join(lines)

    def _semantic_findings(self, semantic):
        findings = semantic.get("semantic_findings", [])
        lines = [
            "## Semantic Findings",
            "",
            "Architectural observations produced by semantic analysis.",
            "",
        ]
        if findings:
            lines += [
                "| Finding | Category | Severity | Confidence |",
                "| --- | --- | --- | ---: |",
            ]
            for finding in findings[:20]:
                sev_emoji = {
                    "info": "ℹ️ Info",
                    "warning": "⚠️ Warning",
                    "error": "🔴 Error",
                }.get(finding.get("severity", "info"), finding.get("severity", ""))
                lines.append("| %s | %s | %s | %.0f%% |" % (
                    finding["title"],
                    finding.get("category", "—"),
                    sev_emoji,
                    finding.get("confidence", 0) * 100,
                ))
        else:
            lines.append("*No semantic findings produced.*")
        return "\n".join(lines)

    def _repository_complexity(self, semantic):
        cx = semantic.get("complexity", {})
        lines = [
            "## Repository Complexity",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            "| Total files analysed | %d |" % cx.get("total_files", 0),
            "| Total symbols (classes + functions) | %d |" % cx.get("total_symbols", 0),
            "| Total import statements | %d |" % cx.get("total_imports", 0),
            "| Total functions | %d |" % cx.get("total_functions", 0),
            "| Total classes | %d |" % cx.get("total_classes", 0),
            "| Avg imports per module | %.1f |" % cx.get("avg_imports_per_module", 0),
            "| Avg functions per file | %.1f |" % cx.get("avg_functions_per_file", 0),
            "| Max imports in one module | %d |" % cx.get("max_imports_in_module", 0),
            "| Max functions in one file | %d |" % cx.get("max_functions_in_file", 0),
            "| Cyclomatic complexity estimate | %.2f |" % cx.get("cyclomatic_complexity_estimate", 0),
        ]
        lang_dist = cx.get("language_distribution", {})
        if lang_dist:
            lines += [
                "",
                "**Language distribution:**",
                "",
                "| Language | Files |",
                "| --- | ---: |",
            ]
            for lang, count in sorted(lang_dist.items(), key=lambda kv: -kv[1]):
                lines.append("| %s | %d |" % (lang, count))
        return "\n".join(lines)

    def _suggested_next_core(self, semantic):
        next_core = semantic.get("next_core", "")
        lines = [
            "## Suggested Next CORE Implementation",
            "",
        ]
        if next_core:
            lines.append("> **%s**" % next_core)
        else:
            lines.append("> *Continue implementing canonical specifications.*")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _fmt_category(self, category):
        mapping = {
            "Telegram": "Telegram",
            "OwnerControl": "Owner Control",
            "Runtime": "Runtime",
            "State": "State",
            "Configuration": "Configuration",
            "Canonical": "Canonical",
            "ProjectMemory": "Project Memory",
        }
        return mapping.get(category, category)

    def _score_bar(self, score):
        filled = score // 10
        empty = 10 - filled
        return "█" * filled + "░" * empty

    def _status_emoji(self, score):
        if score >= 0.8:
            return "✅ Ready"
        if score >= 0.5:
            return "⚠️ Partial"
        if score > 0.0:
            return "🔶 Minimal"
        return "❌ Missing"

    def _rating(self, score):
        if score >= 80:
            return "✅ Ready"
        if score >= 60:
            return "⚠️ Mostly Ready"
        if score >= 40:
            return "🔶 Partial"
        if score > 0:
            return "🔴 Minimal"
        return "❌ Not Detected"
