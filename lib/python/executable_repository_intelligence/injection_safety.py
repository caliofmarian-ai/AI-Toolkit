"""
Executable Repository Intelligence — Injection Safety Classifier
CORE-008C

For every injection point detected by CORE-008B, produces a safety verdict:

  SAFE               — Standard hook pattern, no runtime risk
  SAFE_WITH_CONDITIONS — Callable hook; depends on caller validation
  UNSAFE             — Dynamic code execution or unchecked external input
  READ_ONLY          — Hook only reads state, does not mutate
  GENERATED          — Hook produced by code generation, not hand-authored
  DEPRECATED         — Hook is in a deprecated or legacy file
"""

from typing import List

from .models import FileClassification, InjectionSafetyRecord


# Injection types that are inherently safe (no mutation, structural only)
_SAFE_TYPES = frozenset(["plugin_interface", "service_boundary"])

# Types that are safe with conditions (callees must be validated)
_COND_TYPES = frozenset(["decorator", "middleware", "hook", "di_container"])

# Types that may be unsafe if unconstrained
_RISKY_TYPES = frozenset(["event_bus"])

# Evidence keywords suggesting unsafe dynamic execution
_UNSAFE_KEYWORDS = [
    "eval(", "exec(", "subprocess", "os.system", "__import__",
    "importlib.import_module", "compile(",
]

# Evidence keywords suggesting read-only behaviour
_READONLY_KEYWORDS = [
    "read_only", "readonly", "read only", "observe", "monitor", "listen",
]


class InjectionSafetyClassifier:
    """
    Classifies each CORE-008B injection point with a runtime safety verdict.
    """

    def classify(
        self,
        injection_points: List,          # List[InjectionPoint] from CORE-008B
        file_classifications: List[FileClassification],
        root,
    ) -> List[InjectionSafetyRecord]:
        """
        Produce an InjectionSafetyRecord for each InjectionPoint.
        Result is sorted and deterministic.
        """
        # Build quick lookup: path → FileClassification
        cat_map = {fc.path: fc for fc in file_classifications}

        records: List[InjectionSafetyRecord] = []
        for ip in sorted(injection_points, key=lambda x: (x.file, x.name, x.line)):
            record = self._classify_one(ip, cat_map)
            records.append(record)

        return records

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _classify_one(self, ip, cat_map) -> InjectionSafetyRecord:
        fc = cat_map.get(ip.file)
        category = fc.category if fc else "Unknown"
        evidence_text = " ".join(ip.evidence).lower()

        # Deprecated file → DEPRECATED
        if category == "Deprecated":
            return InjectionSafetyRecord(
                file=ip.file,
                name=ip.name,
                injection_type=ip.type,
                safety="DEPRECATED",
                rationale="Injection point is in a deprecated file.",
                conditions=[],
                confidence=min(ip.confidence, 0.70),
            )

        # Generated artifact → GENERATED
        if category in ("Generated Artifact", "Reports"):
            return InjectionSafetyRecord(
                file=ip.file,
                name=ip.name,
                injection_type=ip.type,
                safety="GENERATED",
                rationale="Injection point resides in a generated artifact.",
                conditions=[],
                confidence=min(ip.confidence, 0.80),
            )

        # Check for read-only patterns
        if any(kw in evidence_text for kw in _READONLY_KEYWORDS):
            return InjectionSafetyRecord(
                file=ip.file,
                name=ip.name,
                injection_type=ip.type,
                safety="READ_ONLY",
                rationale="Hook only observes/reads state; no mutation detected.",
                conditions=[],
                confidence=ip.confidence * 0.90,
            )

        # Check for unsafe dynamic execution patterns
        if any(kw in evidence_text for kw in _UNSAFE_KEYWORDS):
            return InjectionSafetyRecord(
                file=ip.file,
                name=ip.name,
                injection_type=ip.type,
                safety="UNSAFE",
                rationale=(
                    "Injection point uses dynamic code execution "
                    "(%s). Arbitrary code may be injected." % (
                        next(kw for kw in _UNSAFE_KEYWORDS if kw in evidence_text)
                    )
                ),
                conditions=[],
                confidence=ip.confidence,
            )

        # Risky types → SAFE_WITH_CONDITIONS
        if ip.type in _RISKY_TYPES:
            return InjectionSafetyRecord(
                file=ip.file,
                name=ip.name,
                injection_type=ip.type,
                safety="SAFE_WITH_CONDITIONS",
                rationale=(
                    "Event bus pattern: callers must validate event payloads "
                    "before dispatch."
                ),
                conditions=[
                    "Validate all event payloads before dispatch.",
                    "Restrict subscription to trusted modules only.",
                ],
                confidence=ip.confidence * 0.85,
            )

        # Conditionally safe decorator/hook patterns
        if ip.type in _COND_TYPES:
            return InjectionSafetyRecord(
                file=ip.file,
                name=ip.name,
                injection_type=ip.type,
                safety="SAFE_WITH_CONDITIONS",
                rationale=(
                    "Hook/decorator pattern: safe when caller inputs are validated."
                ),
                conditions=[
                    "Ensure all inputs are validated before the handler is invoked.",
                    "Do not expose this hook to unauthenticated callers.",
                ],
                confidence=ip.confidence * 0.90,
            )

        # Structural/interface patterns → SAFE
        if ip.type in _SAFE_TYPES:
            return InjectionSafetyRecord(
                file=ip.file,
                name=ip.name,
                injection_type=ip.type,
                safety="SAFE",
                rationale=(
                    "Plugin interface or service boundary: purely structural, "
                    "no runtime injection risk."
                ),
                conditions=[],
                confidence=ip.confidence,
            )

        # Default → SAFE_WITH_CONDITIONS
        return InjectionSafetyRecord(
            file=ip.file,
            name=ip.name,
            injection_type=ip.type,
            safety="SAFE_WITH_CONDITIONS",
            rationale="Injection point type '%s' requires caller validation." % ip.type,
            conditions=["Validate all inputs before invoking this hook."],
            confidence=ip.confidence * 0.80,
        )
