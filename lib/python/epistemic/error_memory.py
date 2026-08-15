"""Error Memory and recurrence-prevention physiology.

This organ preserves demonstrated failures as navigable historical
experience and exposes recurrence warnings to future transformations.

It does not turn a failure into Canon, Evidence, or autonomous authority.
It remembers what happened, why it mattered, how it was recovered, and
which recurrence conditions should be examined before repeating a
transformation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Tuple


class FailureKind(str, Enum):
    """Human-readable physiological classification of a demonstrated failure."""

    EXECUTION = "EXECUTION"
    SYNTAX = "SYNTAX"
    PERMISSION = "PERMISSION"
    GIT_STATE = "GIT_STATE"
    VALIDATION = "VALIDATION"
    EVIDENCE = "EVIDENCE"
    CONTRACT = "CONTRACT"
    EPISTEMIC = "EPISTEMIC"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class FailureOrigin:
    """Navigable provenance toward the reality in which a failure occurred."""

    repository_path: str
    run_identity: str
    git_commit: str | None = None

    def __post_init__(self) -> None:
        if not self.repository_path.strip():
            raise ValueError("repository_path must be human-readable")
        if not self.run_identity.strip():
            raise ValueError("run_identity must be human-readable")


@dataclass(frozen=True)
class ErrorMemory:
    """One conserved failure experience.

    The record is deliberately immutable. Remembering a failure must not
    mutate the historical body that demonstrated it.
    """

    identity: str
    title: str
    kind: FailureKind
    symptom: str
    cause: str
    recovery: str
    prevention_rule: str
    origin: FailureOrigin
    demonstrated: bool = True

    def __post_init__(self) -> None:
        textual_fields = {
            "identity": self.identity,
            "title": self.title,
            "symptom": self.symptom,
            "cause": self.cause,
            "recovery": self.recovery,
            "prevention_rule": self.prevention_rule,
        }
        for name, value in textual_fields.items():
            if not value.strip():
                raise ValueError(f"{name} must not be empty")

    @property
    def semantic_identity(self) -> str:
        return f"{self.identity} — {self.title}"


@dataclass(frozen=True)
class RecurrenceWarning:
    """A warning derived from remembered failure, not a truth authority."""

    error_identity: str
    error_title: str
    prevention_rule: str
    origin: FailureOrigin

    @property
    def semantic_identity(self) -> str:
        return f"{self.error_identity} — {self.error_title}"


class ErrorMemoryOrgan:
    """Immutable collection physiology for conserved demonstrated failures."""

    def __init__(self, memories: Iterable[ErrorMemory] = ()) -> None:
        items = tuple(memories)
        identities = [item.identity for item in items]
        if len(identities) != len(set(identities)):
            raise ValueError("error-memory identities must be unique")
        self._memories: Tuple[ErrorMemory, ...] = items

    @property
    def memories(self) -> Tuple[ErrorMemory, ...]:
        return self._memories

    def remember(self, memory: ErrorMemory) -> "ErrorMemoryOrgan":
        """Return a new organ containing the conserved failure.

        The previous organ remains unchanged.
        """
        if any(existing.identity == memory.identity for existing in self._memories):
            raise ValueError(f"error memory already exists: {memory.identity}")
        return ErrorMemoryOrgan((*self._memories, memory))

    def find(self, identity: str) -> ErrorMemory | None:
        for memory in self._memories:
            if memory.identity == identity:
                return memory
        return None

    def by_kind(self, kind: FailureKind) -> Tuple[ErrorMemory, ...]:
        return tuple(memory for memory in self._memories if memory.kind == kind)

    def recurrence_warnings(
        self,
        *,
        kind: FailureKind | None = None,
    ) -> Tuple[RecurrenceWarning, ...]:
        """Expose prior prevention knowledge before a future transformation.

        This method does not decide whether execution is allowed.
        Human Authority and the governing transformation retain authority.
        """
        candidates = self._memories
        if kind is not None:
            candidates = self.by_kind(kind)

        return tuple(
            RecurrenceWarning(
                error_identity=memory.identity,
                error_title=memory.title,
                prevention_rule=memory.prevention_rule,
                origin=memory.origin,
            )
            for memory in candidates
            if memory.demonstrated
        )


def seed_demonstrated_ai_toolkit_failures() -> ErrorMemoryOrgan:
    """Conserve failures demonstrated during the current AI-Toolkit evolution.

    These seeds are historical memories, not Canon and not generic claims.
    Their origins point toward the conserved repository bodies.
    """

    permission_failure = ErrorMemory(
        identity="ERR-0001",
        title="Executed Bash Invoked Through Non-Executable Path",
        kind=FailureKind.PERMISSION,
        symptom=(
            "Termux returned Permission denied when the conserved RUN 002 "
            "Bash body was invoked directly as a pathname."
        ),
        cause=(
            "The historical RUN body was treated as an executable filesystem "
            "object instead of being interpreted explicitly by Bash."
        ),
        recovery=(
            "The already-materialized RUN body was preserved and subsequently "
            "interpreted explicitly through the Bash interpreter."
        ),
        prevention_rule=(
            "Before launching a generated Bash body, validate it with the Bash "
            "parser and invoke it explicitly with bash unless executable-path "
            "semantics have themselves been demonstrated."
        ),
        origin=FailureOrigin(
            repository_path=(
                "work/implementation-reports/PCC-06/"
                "PCC-06_RUN002_LAUNCH_RECOVERY_CONTEXT.txt"
            ),
            run_identity="PCC-06 RUN 002 launch recovery",
            git_commit="83a3962a7d0e80da63fd8f4d52cdc62f3f768dfe",
        ),
    )

    whitespace_failure = ErrorMemory(
        identity="ERR-0002",
        title="Historical Body Misclassified by Whitespace Validation",
        kind=FailureKind.VALIDATION,
        symptom=(
            "git diff --check stopped conservation because trailing whitespace "
            "existed inside the historical Bash body being preserved."
        ),
        cause=(
            "A production-code cleanliness examination was applied without "
            "distinguishing immutable historical execution material from new "
            "production physiology."
        ),
        recovery=(
            "The interrupted body was classified as historical reality and "
            "conserved faithfully without rewriting its contents."
        ),
        prevention_rule=(
            "Classify staged bodies before applying mutation-oriented validation. "
            "Historical execution evidence must be preserved faithfully; validate "
            "new production anatomy separately."
        ),
        origin=FailureOrigin(
            repository_path=(
                "work/implementation-reports/PCC-06/"
                "PCC-06_RUN002_MINIMAL_ANATOMY_OF_THE_LIVING_"
                "EPISTEMIC_IMAGE_EXECUTED_BASH.sh"
            ),
            run_identity="PCC-06 RUN 002 interrupted-state conservation",
            git_commit="83a3962a7d0e80da63fd8f4d52cdc62f3f768dfe",
        ),
    )

    return ErrorMemoryOrgan((permission_failure, whitespace_failure))

@dataclass(frozen=True)
class IntendedTransformation:
    """Minimal description of a transformation before execution.

    This body exists only so Error Memory can determine which demonstrated
    precedents may matter to the intended activity.

    It is not the Transformation organ and does not execute anything.
    """

    identity: str
    title: str
    activities: Tuple[FailureKind, ...]
    context: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.identity.strip():
            raise ValueError("identity must not be empty")
        if not self.title.strip():
            raise ValueError("title must not be empty")
        if not self.activities:
            raise ValueError(
                "an intended transformation must declare at least one activity"
            )

        normalized_context = tuple(
            item.strip() for item in self.context if item.strip()
        )
        object.__setattr__(self, "context", normalized_context)

    @property
    def semantic_identity(self) -> str:
        return f"{self.identity} — {self.title}"


@dataclass(frozen=True)
class PreTransformationRecurrenceAwareness:
    """Read-only preventive awareness formed before a transformation.

    Awareness remembers demonstrated precedents. It does not decide whether
    the intended transformation may proceed.
    """

    transformation_identity: str
    transformation_title: str
    warnings: Tuple[RecurrenceWarning, ...]

    @property
    def semantic_identity(self) -> str:
        return (
            f"{self.transformation_identity} — "
            f"{self.transformation_title}"
        )

    @property
    def has_demonstrated_precedent(self) -> bool:
        return bool(self.warnings)


def form_pre_transformation_recurrence_awareness(
    organ: ErrorMemoryOrgan,
    intended: IntendedTransformation,
) -> PreTransformationRecurrenceAwareness:
    """Consult demonstrated Error Memory before future execution.

    Matching is deliberately conservative and explicit: the intended
    transformation declares the failure kinds relevant to the activity.
    Error Memory exposes demonstrated precedents for those kinds.

    This physiology informs. It does not authorize, block, execute, mutate
    historical memory, or perform the Transformation lifecycle.
    """

    warnings = []
    seen = set()

    for kind in intended.activities:
        for warning in organ.recurrence_warnings(kind=kind):
            if warning.error_identity in seen:
                continue
            seen.add(warning.error_identity)
            warnings.append(warning)

    return PreTransformationRecurrenceAwareness(
        transformation_identity=intended.identity,
        transformation_title=intended.title,
        warnings=tuple(warnings),
    )


def seed_demonstrated_ai_toolkit_failures_run002() -> ErrorMemoryOrgan:
    """Extend RUN 001 memory with failures demonstrated while forming it.

    These additional bodies come from conserved RUN 001 execution history.
    They remain historical Error Memory rather than Canon or authority.
    """

    organ = seed_demonstrated_ai_toolkit_failures()

    import_topology_failure = ErrorMemory(
        identity="ERR-0003",
        title="Epistemic Regression Invoked With Incomplete Import Topology",
        kind=FailureKind.EXECUTION,
        symptom=(
            "Neighboring epistemic examinations stopped during collection "
            "with ModuleNotFoundError for epistemic and python imports."
        ),
        cause=(
            "The examination command did not expose both repository import "
            "roots required by the existing epistemic test population."
        ),
        recovery=(
            "The examinations were repeated with both lib and lib/python "
            "present in PYTHONPATH; neighboring and complete regression then "
            "passed."
        ),
        prevention_rule=(
            "Before executing the AI-Toolkit epistemic examination population, "
            "preserve both repository import roots in PYTHONPATH: lib and "
            "lib/python."
        ),
        origin=FailureOrigin(
            repository_path=(
                "work/implementation-reports/ERROR-MEMORY/"
                "ERROR_MEMORY_RUN001_METABOLIC_CLASSIFICATION_AND_CLOSURE.md"
            ),
            run_identity="ERROR MEMORY RUN 001 import-topology recovery",
            git_commit="d8d16590911967579aeb2762a888dfcdd9ef941b",
        ),
    )

    metabolic_classification_failure = ErrorMemory(
        identity="ERR-0004",
        title="Metabolic Memory Body Rejected Before Semantic Classification",
        kind=FailureKind.EPISTEMIC,
        symptom=(
            "A MemoryStore product under work/memory was initially treated as "
            "an unexpected repository effect and stopped the execution."
        ),
        cause=(
            "Repository effect validation considered path appearance before "
            "establishing producer, triggering execution, actual content, "
            "provenance, and semantic class."
        ),
        recovery=(
            "The actual JSON body, MemoryStore producer, triggering test, "
            "schema, fixed values, identity, and timestamp were inspected "
            "before the product was classified and conserved."
        ),
        prevention_rule=(
            "Before rejecting a new repository body, classify its producer, "
            "triggering execution, actual content, provenance, and semantics. "
            "Unknown remains UNKNOWN and no unexplained body is silently "
            "deleted."
        ),
        origin=FailureOrigin(
            repository_path=(
                "work/implementation-reports/ERROR-MEMORY/"
                "ERROR_MEMORY_RUN001_METABOLIC_CLASSIFICATION_AND_CLOSURE.md"
            ),
            run_identity="ERROR MEMORY RUN 001 metabolic classification",
            git_commit="d8d16590911967579aeb2762a888dfcdd9ef941b",
        ),
    )

    return (
        organ
        .remember(import_topology_failure)
        .remember(metabolic_classification_failure)
    )
