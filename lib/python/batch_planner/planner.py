from python.canonical_entities import DriftSeverity, PlanBatch, Priority


class BatchPlanner:
    """Generate intelligent implementation batches from drift findings."""

    def generate(self, canonical_repo, findings, coverage):
        """Transform drift findings into structured batches."""
        created = {}
        for finding in findings:
            if not finding.canonical_ref:
                continue
            doc = canonical_repo.get_by_id(finding.canonical_ref)
            if doc is None:
                continue
            if finding.category not in (
                "Missing Implementation",
                "Partial Implementation",
                "Dependency Drift",
                "Test Drift",
            ):
                continue

            batch_id = "BATCH-%s" % doc.id.split("-")[-1]
            priority = self._priority_for_severity(finding.severity)
            existing = created.get(batch_id)
            repository_refs = list(existing.repository_refs) if existing is not None else []
            fallback_ref = "lib/python/%s/" % self._slugify(doc.title.replace("Specification", ""))
            for ref in [finding.implementation_ref or fallback_ref]:
                if ref and ref not in repository_refs:
                    repository_refs.append(ref)

            canonical_refs = list(existing.canonical_refs) if existing is not None else []
            if doc.id not in canonical_refs:
                canonical_refs.append(doc.id)

            created[batch_id] = PlanBatch(
                id=batch_id,
                title="Implement %s" % doc.id,
                description=(existing.description if existing is not None else finding.description),
                canonical_refs=canonical_refs,
                repository_refs=repository_refs,
                dependencies=self._resolve_dependencies(canonical_repo, doc.id),
                estimated_hours=max(
                    existing.estimated_hours if existing is not None else 0,
                    self._estimate_effort(doc, finding.severity),
                ),
                confidence=max(existing.confidence if existing is not None else 0.0, finding.confidence),
                priority=self._higher_priority(existing.priority, priority) if existing is not None else priority,
                acceptance_criteria=self._generate_acceptance_criteria(doc),
            )
        return sorted(created.values(), key=self._sort_key)

    def _resolve_dependencies(self, canonical_repo, doc_id):
        doc = canonical_repo.get_by_id(doc_id)
        return list(doc.dependencies) if doc is not None else []

    def _estimate_effort(self, doc, severity):
        """Estimate hours based on doc complexity and severity."""
        base = max(1, len(doc.sections) // 2) + len(doc.objectives)
        severity_weight = {
            DriftSeverity.CRITICAL: 4,
            DriftSeverity.HIGH: 3,
            DriftSeverity.MEDIUM: 2,
            DriftSeverity.LOW: 1,
            DriftSeverity.INFORMATIONAL: 1,
        }.get(severity, 1)
        return max(2, min(40, base + severity_weight))

    def _generate_acceptance_criteria(self, doc):
        criteria = ["Canonical document %s is implemented." % doc.id]
        for objective in doc.objectives[:5]:
            criteria.append("Implements objective: %s" % objective.rstrip("."))
        criteria.append("Tests or validation evidence exist for %s." % doc.id)
        return criteria

    def roadmap(self, batches):
        """Organize batches into time horizons based on priority."""
        roadmap = {
            "immediate": [],
            "short_term": [],
            "medium_term": [],
            "long_term": [],
        }
        for batch in batches:
            if batch.priority == Priority.CRITICAL:
                roadmap["immediate"].append(batch)
            elif batch.priority == Priority.HIGH:
                roadmap["short_term"].append(batch)
            elif batch.priority == Priority.MEDIUM:
                roadmap["medium_term"].append(batch)
            else:
                roadmap["long_term"].append(batch)
        return roadmap

    def _priority_for_severity(self, severity):
        mapping = {
            DriftSeverity.CRITICAL: Priority.CRITICAL,
            DriftSeverity.HIGH: Priority.HIGH,
            DriftSeverity.MEDIUM: Priority.MEDIUM,
            DriftSeverity.LOW: Priority.LOW,
            DriftSeverity.INFORMATIONAL: Priority.DEFERRED,
        }
        return mapping.get(severity, Priority.MEDIUM)

    def _higher_priority(self, left, right):
        ranking = {
            Priority.CRITICAL: 0,
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3,
            Priority.DEFERRED: 4,
        }
        return left if ranking[left] <= ranking[right] else right

    def _sort_key(self, batch):
        ranking = {
            Priority.CRITICAL: 0,
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3,
            Priority.DEFERRED: 4,
        }
        return (ranking.get(batch.priority, 99), len(batch.dependencies), batch.id)

    def _slugify(self, value):
        return "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")
