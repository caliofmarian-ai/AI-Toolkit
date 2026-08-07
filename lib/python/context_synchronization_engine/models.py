from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional, Tuple

SCHEMA_VERSION = "1.0.0"


def _to_tuple(values) -> Tuple[str, ...]:
    return tuple(str(v) for v in values or ())


def _normalize_mapping(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {
            str(key): _normalize_mapping(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, tuple):
        return [_normalize_mapping(item) for item in value]
    if isinstance(value, list):
        return [_normalize_mapping(item) for item in value]
    return value


@dataclass(frozen=True)
class SynchronizationFinding:
    category: str
    severity: str
    message: str
    evidence: Tuple[str, ...] = ()
    corrected: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "severity": self.severity,
            "message": self.message,
            "evidence": list(self.evidence),
            "corrected": bool(self.corrected),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SynchronizationFinding":
        return cls(
            category=str(data.get("category", "")),
            severity=str(data.get("severity", "info")),
            message=str(data.get("message", "")),
            evidence=_to_tuple(data.get("evidence", ())),
            corrected=bool(data.get("corrected", False)),
        )


@dataclass(frozen=True)
class SynchronizationReport:
    repository: str
    workspace: str
    generated_at: str
    findings: Tuple[SynchronizationFinding, ...] = ()
    corrected_fields: Tuple[str, ...] = ()
    missing_fields: Tuple[str, ...] = ()
    conflicts: Dict[str, Tuple[str, ...]] = None
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> Dict[str, Any]:
        conflict_map = self.conflicts or {}
        return {
            "schema_version": self.schema_version,
            "repository": self.repository,
            "workspace": self.workspace,
            "generated_at": self.generated_at,
            "corrected_fields": list(self.corrected_fields),
            "missing_fields": list(self.missing_fields),
            "conflicts": {
                str(key): list(value)
                for key, value in sorted(conflict_map.items(), key=lambda item: str(item[0]))
            },
            "finding_count": len(self.findings),
            "findings": [finding.to_dict() for finding in self.findings],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SynchronizationReport":
        conflicts = {
            str(key): _to_tuple(value)
            for key, value in dict(data.get("conflicts", {})).items()
        }
        return cls(
            repository=str(data.get("repository", "")),
            workspace=str(data.get("workspace", "")),
            generated_at=str(data.get("generated_at", "")),
            corrected_fields=_to_tuple(data.get("corrected_fields", ())),
            missing_fields=_to_tuple(data.get("missing_fields", ())),
            conflicts=dict(sorted(conflicts.items())),
            findings=tuple(
                SynchronizationFinding.from_dict(item)
                for item in data.get("findings", ())
            ),
            schema_version=str(data.get("schema_version", SCHEMA_VERSION)),
        )


@dataclass(frozen=True)
class EngineeringContextSection:
    name: str
    owner: str
    loader: str
    generated_at: str
    artifacts: Tuple[str, ...] = ()
    provenance: Optional[Dict[str, Any]] = None
    traceability: Optional[Dict[str, Any]] = None
    validation: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "owner": self.owner,
            "loader": self.loader,
            "generated_at": self.generated_at,
            "artifacts": list(self.artifacts),
            "provenance": _normalize_mapping(self.provenance or {}),
            "traceability": _normalize_mapping(self.traceability or {}),
            "validation": _normalize_mapping(self.validation or {}),
            "data": _normalize_mapping(self.data or {}),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EngineeringContextSection":
        return cls(
            name=str(data.get("name", "")),
            owner=str(data.get("owner", "")),
            loader=str(data.get("loader", "")),
            generated_at=str(data.get("generated_at", "")),
            artifacts=_to_tuple(data.get("artifacts", ())),
            provenance=dict(_normalize_mapping(data.get("provenance", {}))),
            traceability=dict(_normalize_mapping(data.get("traceability", {}))),
            validation=dict(_normalize_mapping(data.get("validation", {}))),
            data=dict(_normalize_mapping(data.get("data", {}))),
            schema_version=str(data.get("schema_version", SCHEMA_VERSION)),
        )


@dataclass(frozen=True)
class EngineeringContext:
    generated_at: str
    repository: str
    workspace: str
    repository_context: EngineeringContextSection
    canonical_context: EngineeringContextSection
    governance_context: EngineeringContextSection
    runtime_context: EngineeringContextSection
    implementation_context: EngineeringContextSection
    dashboard_context: EngineeringContextSection
    knowledge_context: EngineeringContextSection
    decision_context: EngineeringContextSection
    executive_context: EngineeringContextSection
    project_context: EngineeringContextSection
    decision_history: Tuple[Dict[str, Any], ...] = ()
    validation_summary: Optional[Dict[str, Any]] = None
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "repository": self.repository,
            "workspace": self.workspace,
            "repository_context": self.repository_context.to_dict(),
            "canonical_context": self.canonical_context.to_dict(),
            "governance_context": self.governance_context.to_dict(),
            "runtime_context": self.runtime_context.to_dict(),
            "implementation_context": self.implementation_context.to_dict(),
            "dashboard_context": self.dashboard_context.to_dict(),
            "knowledge_context": self.knowledge_context.to_dict(),
            "decision_context": self.decision_context.to_dict(),
            "executive_context": self.executive_context.to_dict(),
            "project_context": self.project_context.to_dict(),
            "decision_history_count": len(self.decision_history),
            "decision_history": [_normalize_mapping(item) for item in self.decision_history],
            "validation_summary": _normalize_mapping(self.validation_summary or {}),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EngineeringContext":
        return cls(
            generated_at=str(data.get("generated_at", "")),
            repository=str(data.get("repository", "")),
            workspace=str(data.get("workspace", "")),
            repository_context=EngineeringContextSection.from_dict(
                data.get("repository_context", {})
            ),
            canonical_context=EngineeringContextSection.from_dict(
                data.get("canonical_context", {})
            ),
            governance_context=EngineeringContextSection.from_dict(
                data.get("governance_context", {})
            ),
            runtime_context=EngineeringContextSection.from_dict(
                data.get("runtime_context", {})
            ),
            implementation_context=EngineeringContextSection.from_dict(
                data.get("implementation_context", {})
            ),
            dashboard_context=EngineeringContextSection.from_dict(
                data.get("dashboard_context", {})
            ),
            knowledge_context=EngineeringContextSection.from_dict(
                data.get("knowledge_context", {})
            ),
            decision_context=EngineeringContextSection.from_dict(
                data.get("decision_context", {})
            ),
            executive_context=EngineeringContextSection.from_dict(
                data.get("executive_context", {})
            ),
            project_context=EngineeringContextSection.from_dict(
                data.get("project_context", {})
            ),
            decision_history=tuple(
                dict(_normalize_mapping(item))
                for item in data.get("decision_history", ())
            ),
            validation_summary=dict(
                _normalize_mapping(data.get("validation_summary", {}))
            ),
            schema_version=str(data.get("schema_version", SCHEMA_VERSION)),
        )
