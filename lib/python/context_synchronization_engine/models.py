from dataclasses import dataclass
from typing import Any, Dict, Mapping, Tuple

SCHEMA_VERSION = "1.0.0"


def _to_tuple(values) -> Tuple[str, ...]:
    return tuple(str(v) for v in values or ())


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
