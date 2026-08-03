from dataclasses import asdict, is_dataclass


class ReportingEngine:
    """Generate markdown and JSON reports from canonical intelligence data."""

    def generate(self, canonical_repo, graph, matches, coverage, compliance, findings, batches):
        """Generate all reports, returns dict with 'markdown' and 'json' keys."""
        markdown = {
            "executive": self.executive_report(canonical_repo, graph, matches, coverage, compliance, findings, batches),
            "coverage": self.coverage_report(canonical_repo, coverage),
            "compliance": self.compliance_report(canonical_repo, compliance),
            "drift": self.drift_report(canonical_repo, findings),
            "planning": self.planning_report(canonical_repo, batches),
        }
        markdown["canonical_intelligence"] = self.canonical_intelligence_report(canonical_repo, graph, matches, coverage, compliance, findings, batches)
        return {"markdown": markdown, "json": self.to_json(canonical_repo, graph, matches, coverage, compliance, findings, batches)}

    def executive_report(self, canonical_repo, graph, matches, coverage, compliance, findings, batches):
        total_docs = len(canonical_repo.all_documents())
        matched_docs = sum(1 for doc_id in matches if matches[doc_id])
        coverage_score = self._average([metric.score for metric in coverage])
        compliance_score = self._average([metric.score for metric in compliance])
        return "\n".join([
            "# Executive Summary",
            "",
            "- Canonical documents: %s" % total_docs,
            "- Graph nodes: %s" % graph.node_count(),
            "- Documents with matches: %s" % matched_docs,
            "- Coverage: %.0f%%" % (coverage_score * 100.0),
            "- Compliance: %.0f%%" % (compliance_score * 100.0),
            "- Drift findings: %s" % len(findings),
            "- Planned batches: %s" % len(batches),
        ])

    def coverage_report(self, canonical_repo, coverage):
        lines = ["# Coverage Report", "", "| Category | Score | Covered | Total |", "| --- | ---: | ---: | ---: |"]
        for metric in coverage:
            lines.append("| %s | %.0f%% | %s | %s |" % (metric.category, metric.score * 100.0, metric.covered, metric.total))
        return "\n".join(lines)

    def compliance_report(self, canonical_repo, compliance):
        lines = ["# Compliance Report", "", "| Category | State | Score |", "| --- | --- | ---: |"]
        for metric in compliance:
            lines.append("| %s | %s | %.0f%% |" % (metric.category, metric.state.value, metric.score * 100.0))
        return "\n".join(lines)

    def drift_report(self, canonical_repo, findings):
        lines = ["# Drift Report", ""]
        if not findings:
            lines.append("No drift findings detected.")
            return "\n".join(lines)
        for finding in findings[:50]:
            lines.extend([
                "## %s" % finding.id,
                "- Category: %s" % finding.category,
                "- Severity: %s" % finding.severity.value,
                "- Canonical: %s" % (finding.canonical_ref or "n/a"),
                "- Implementation: %s" % (finding.implementation_ref or "n/a"),
                "- Description: %s" % finding.description,
                "- Recommendation: %s" % finding.recommendation,
                "",
            ])
        return "\n".join(lines)

    def planning_report(self, canonical_repo, batches):
        lines = ["# Planning Report", ""]
        if not batches:
            lines.append("No implementation batches generated.")
            return "\n".join(lines)
        for batch in batches:
            lines.extend([
                "## %s — %s" % (batch.id, batch.title),
                "- Priority: %s" % batch.priority.value,
                "- Estimated Hours: %s" % batch.estimated_hours,
                "- Canonical Refs: %s" % ", ".join(batch.canonical_refs),
                "- Dependencies: %s" % (", ".join(batch.dependencies) if batch.dependencies else "none"),
                "",
            ])
        return "\n".join(lines)

    def canonical_intelligence_report(self, canonical_repo, graph, matches, coverage, compliance, findings, batches):
        sections = [
            self.executive_report(canonical_repo, graph, matches, coverage, compliance, findings, batches),
            self.coverage_report(canonical_repo, coverage),
            self.compliance_report(canonical_repo, compliance),
            self.drift_report(canonical_repo, findings),
            self.planning_report(canonical_repo, batches),
        ]
        return "\n\n".join(sections)

    def to_json(self, canonical_repo, graph, matches, coverage, compliance, findings, batches):
        return {
            "canonical_repository": self._serialize(canonical_repo.all_documents()),
            "graph": graph.to_dict(),
            "matches": dict((key, self._serialize(value)) for key, value in matches.items()),
            "coverage": self._serialize(coverage),
            "compliance": self._serialize(compliance),
            "drift": self._serialize(findings),
            "batches": self._serialize(batches),
        }

    def _serialize(self, value):
        if is_dataclass(value):
            return self._serialize(asdict(value))
        if isinstance(value, dict):
            return dict((key, self._serialize(item)) for key, item in value.items())
        if isinstance(value, (list, tuple)):
            return [self._serialize(item) for item in value]
        if hasattr(value, "value"):
            return value.value
        return value

    def _average(self, values):
        return (sum(values) / float(len(values))) if values else 0.0
