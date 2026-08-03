from datetime import datetime
from pathlib import Path

from python.canonical_entities import DriftFinding, DriftSeverity


class DriftEngine:
    """Detect architecture drift between canonical specs and implementation."""

    def __init__(self, repository=".", workspace_index=None):
        self.root = Path(repository).resolve()
        self._workspace_index = workspace_index

    def _get_index(self):
        if self._workspace_index is not None:
            return self._workspace_index
        from python.workspace_index import WorkspaceIndexBuilder
        return WorkspaceIndexBuilder(self.root).build()

    def detect(self, canonical_repo, matches, coverage):
        """Detect drift between canonical repository and implementation evidence."""
        index = self._get_index()
        findings = []
        dependency_graph = canonical_repo.dependency_graph()
        timestamp = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

        for doc in canonical_repo.all_documents():
            doc_matches = matches.get(doc.id, [])
            best = self._best_match(doc_matches)
            best_confidence = best.confidence if best is not None else 0.0

            if best is None or best_confidence < 0.3:
                findings.append(self._finding(
                    "missing-implementation-%s" % doc.id.lower(),
                    "Missing Implementation",
                    DriftSeverity.CRITICAL,
                    doc.id,
                    "",
                    "Canonical document %s has no implementation match." % doc.id,
                    [doc.title],
                    "Implement the canonical module and connect it to repository architecture.",
                    1.0 if best is None else 0.7,
                    timestamp,
                ))
            elif best_confidence < 0.75:
                findings.append(self._finding(
                    "partial-implementation-%s" % doc.id.lower(),
                    "Partial Implementation",
                    DriftSeverity.MEDIUM,
                    doc.id,
                    best.implementation_ref,
                    "Canonical document %s is only partially represented in code." % doc.id,
                    list(best.evidence),
                    "Strengthen implementation coverage and align behavior with the canonical specification.",
                    best_confidence,
                    timestamp,
                ))

            if not doc.dependencies and not canonical_repo.dependents_of(doc.id):
                findings.append(self._finding(
                    "orphan-documentation-%s" % doc.id.lower(),
                    "Orphan Documentation",
                    DriftSeverity.LOW,
                    doc.id,
                    best.implementation_ref if best else "",
                    "Canonical document %s is isolated in the dependency graph." % doc.id,
                    [doc.filename],
                    "Review whether the document should declare dependencies or be linked from adjacent canonical specs.",
                    0.6,
                    timestamp,
                ))

            if not self._has_test_evidence(doc, doc_matches, index):
                findings.append(self._finding(
                    "test-drift-%s" % doc.id.lower(),
                    "Test Drift",
                    DriftSeverity.MEDIUM,
                    doc.id,
                    best.implementation_ref if best else "",
                    "Canonical document %s lacks clear test coverage evidence." % doc.id,
                    [match.implementation_ref for match in doc_matches[:3]],
                    "Add or align tests that validate the canonical behavior.",
                    0.65,
                    timestamp,
                ))

            if doc.dependencies and best_confidence >= 0.5:
                missing_dependencies = [dep for dep in dependency_graph.get(doc.id, []) if self._best_confidence(matches.get(dep, [])) < 0.3]
                if missing_dependencies:
                    findings.append(self._finding(
                        "dependency-drift-%s" % doc.id.lower(),
                        "Dependency Drift",
                        DriftSeverity.HIGH,
                        doc.id,
                        best.implementation_ref if best else "",
                        "Canonical dependencies for %s are not implemented consistently." % doc.id,
                        missing_dependencies,
                        "Implement or restore dependent canonical modules first.",
                        0.8,
                        timestamp,
                    ))

        findings.extend(self._orphan_implementation_findings(index, matches, timestamp))
        return findings

    def severity_distribution(self, findings):
        distribution = {}
        for finding in findings:
            key = finding.severity.value
            distribution[key] = distribution.get(key, 0) + 1
        return distribution

    def remediation_plan(self, findings):
        prioritized = sorted(findings, key=self._severity_rank)
        return [
            {
                "finding_id": finding.id,
                "category": finding.category,
                "severity": finding.severity.value,
                "canonical_ref": finding.canonical_ref,
                "implementation_ref": finding.implementation_ref,
                "recommendation": finding.recommendation,
            }
            for finding in prioritized
        ]

    def _finding(self, finding_id, category, severity, canonical_ref, implementation_ref, description, evidence, recommendation, confidence, detected_at):
        return DriftFinding(
            id=finding_id,
            category=category,
            severity=severity,
            canonical_ref=canonical_ref,
            implementation_ref=implementation_ref,
            description=description,
            evidence=[item for item in evidence if item][:10],
            recommendation=recommendation,
            confidence=max(0.0, min(1.0, confidence)),
            detected_at=detected_at,
        )

    def _best_match(self, matches):
        if not matches:
            return None
        return sorted(matches, key=lambda item: (-item.confidence, item.match_level, item.implementation_ref))[0]

    def _best_confidence(self, matches):
        match = self._best_match(matches)
        return match.confidence if match is not None else 0.0

    def _has_test_evidence(self, doc, doc_matches, index):
        tokens = self._tokens(doc.title)[:3]
        for match in doc_matches:
            if "test" in match.implementation_ref.lower():
                return True
        for wf in index.files:
            lowered = wf.path.lower()
            if "test" not in lowered:
                continue
            if any(token in lowered for token in tokens if token):
                return True
        return False

    def _orphan_implementation_findings(self, index, matches, timestamp):
        matched_refs = set()
        for doc_matches in matches.values():
            for match in doc_matches:
                matched_refs.add(match.implementation_ref)
        findings = []
        for wf in index.python_files():
            lowered = wf.path.lower()
            if wf.name == "__init__.py" or lowered.startswith("lib/python/workspace_index/"):
                continue
            if not any(keyword in lowered for keyword in ["engine", "graph", "planner", "runtime", "coordinator", "audit", "validator"]):
                continue
            if wf.path in matched_refs:
                continue
            findings.append(
                DriftFinding(
                    id="orphan-implementation-%s" % wf.name.replace(".", "-").lower(),
                    category="Orphan Implementation",
                    severity=DriftSeverity.LOW,
                    canonical_ref="",
                    implementation_ref=wf.path,
                    description="Implementation artifact %s lacks a strong canonical reference." % wf.path,
                    evidence=[wf.path],
                    recommendation="Link this implementation to a canonical document or document why it is exploratory.",
                    confidence=0.4,
                    detected_at=timestamp,
                )
            )
            if len(findings) >= 10:
                break
        return findings

    def _severity_rank(self, finding):
        order = {
            DriftSeverity.CRITICAL: 0,
            DriftSeverity.HIGH: 1,
            DriftSeverity.MEDIUM: 2,
            DriftSeverity.LOW: 3,
            DriftSeverity.INFORMATIONAL: 4,
        }
        return (order.get(finding.severity, 99), finding.category, finding.id)

    def _tokens(self, value):
        normalized = "".join(ch.lower() if ch.isalnum() else " " for ch in value)
        return [token for token in normalized.split() if token not in ("specification", "canonical")]
