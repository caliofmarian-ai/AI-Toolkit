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

# ---------------------------------------------------------------------------
# Error Memory RUN 003 — Demonstrated Failure Intake
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DemonstratedFailureObservation:
    """Conserved observation offered to Error Memory for possible formation.

    This body represents what the intake boundary has actually been given.
    It does not infer cause, recovery, or prevention knowledge.

    The observation is not automatically Evidence, Canon, or Error Memory.
    """

    identity: str
    title: str
    kind: FailureKind
    symptom: str
    origin: FailureOrigin
    demonstrated: bool
    cause: str | None = None
    recovery: str | None = None
    prevention_rule: str | None = None

    def __post_init__(self) -> None:
        required = {
            "identity": self.identity,
            "title": self.title,
            "symptom": self.symptom,
        }

        for name, value in required.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must not be empty")

        for name in ("cause", "recovery", "prevention_rule"):
            value = getattr(self, name)
            if value is not None and (
                not isinstance(value, str) or not value.strip()
            ):
                raise ValueError(
                    f"{name} must be non-empty when supplied"
                )

    @property
    def semantic_identity(self) -> str:
        return f"{self.identity} — {self.title}"


@dataclass(frozen=True)
class FailureIntakeResult:
    """Read-only result of examining one failure observation.

    Intake can legitimately refuse Error Memory formation.

    Refusal preserves epistemic absence instead of manufacturing missing
    historical knowledge.
    """

    observation_identity: str
    observation_title: str
    accepted: bool
    state: str
    reason: str
    memory: ErrorMemory | None = None

    def __post_init__(self) -> None:
        if not self.observation_identity.strip():
            raise ValueError(
                "observation_identity must not be empty"
            )

        if not self.observation_title.strip():
            raise ValueError(
                "observation_title must not be empty"
            )

        if not self.state.strip():
            raise ValueError("state must not be empty")

        if not self.reason.strip():
            raise ValueError("reason must not be empty")

        if self.accepted and self.memory is None:
            raise ValueError(
                "accepted intake must contain formed Error Memory"
            )

        if not self.accepted and self.memory is not None:
            raise ValueError(
                "rejected intake must not contain Error Memory"
            )

    @property
    def semantic_identity(self) -> str:
        return (
            f"{self.observation_identity} — "
            f"{self.observation_title}"
        )


def form_error_memory_from_demonstrated_failure(
    observation: DemonstratedFailureObservation,
) -> FailureIntakeResult:
    """Form Error Memory only from structurally sufficient demonstrated reality.

    RUN 003 deliberately does not infer historical facts.

    A failure observation can become Error Memory only when:

    * the failure is explicitly demonstrated;
    * navigable origin already exists;
    * symptom is explicitly present;
    * cause is explicitly supplied;
    * recovery is explicitly supplied;
    * prevention knowledge is explicitly supplied.

    Missing interpretation remains missing.

    The function does not inspect arbitrary files, conversations, stdout,
    stderr, or repository state by itself. Producers of observations remain
    responsible for preserving their own source reality and provenance.
    """

    if not observation.demonstrated:
        return FailureIntakeResult(
            observation_identity=observation.identity,
            observation_title=observation.title,
            accepted=False,
            state="UNCONFIRMED",
            reason=(
                "Failure observation is not explicitly demonstrated."
            ),
        )

    missing = tuple(
        name
        for name, value in (
            ("cause", observation.cause),
            ("recovery", observation.recovery),
            ("prevention_rule", observation.prevention_rule),
        )
        if value is None
    )

    if missing:
        return FailureIntakeResult(
            observation_identity=observation.identity,
            observation_title=observation.title,
            accepted=False,
            state="INCOMPLETE",
            reason=(
                "Demonstrated failure remains epistemically incomplete; "
                "missing explicitly conserved fields: "
                + ", ".join(missing)
            ),
        )

    memory = ErrorMemory(
        identity=observation.identity,
        title=observation.title,
        kind=observation.kind,
        symptom=observation.symptom,
        cause=observation.cause,
        recovery=observation.recovery,
        prevention_rule=observation.prevention_rule,
        origin=observation.origin,
        demonstrated=True,
    )

    return FailureIntakeResult(
        observation_identity=observation.identity,
        observation_title=observation.title,
        accepted=True,
        state="FORMED",
        reason=(
            "Demonstrated failure contained the complete explicit "
            "historical anatomy required by Error Memory."
        ),
        memory=memory,
    )


def remember_demonstrated_failure(
    organ: ErrorMemoryOrgan,
    observation: DemonstratedFailureObservation,
) -> tuple[ErrorMemoryOrgan, FailureIntakeResult]:
    """Attempt intake without mutating the existing Error Memory organ.

    Rejected or incomplete observations leave the organ exactly unchanged.
    Accepted observations produce a new immutable organ through the existing
    remember() physiology.
    """

    result = form_error_memory_from_demonstrated_failure(
        observation
    )

    if not result.accepted:
        return organ, result

    assert result.memory is not None

    return organ.remember(result.memory), result

# ---------------------------------------------------------------------------
# Error Memory RUN 004 — Pre-Execution Recurrence Examination
# ---------------------------------------------------------------------------

class RecurrenceDisposition(str, Enum):
    """Human-readable disposition of one demonstrated recurrence warning.

    A disposition records examination state.  It is not permission to execute.
    """

    ADDRESSED = "ADDRESSED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class RecurrenceExamination:
    """Explicit examination of one demonstrated recurrence precedent.

    RUN 004 makes the previously implicit step visible:

    a future transformation must be able to show how a relevant remembered
    failure was considered before execution.

    Examination does not authorize, block, execute, mutate Canon, or rewrite
    historical Error Memory.
    """

    error_identity: str
    error_title: str
    prevention_rule: str
    origin: FailureOrigin
    disposition: RecurrenceDisposition
    explanation: str

    def __post_init__(self) -> None:
        textual_fields = {
            "error_identity": self.error_identity,
            "error_title": self.error_title,
            "prevention_rule": self.prevention_rule,
            "explanation": self.explanation,
        }

        for name, value in textual_fields.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must not be empty")

    @property
    def semantic_identity(self) -> str:
        return f"{self.error_identity} — {self.error_title}"


@dataclass(frozen=True)
class PreExecutionRecurrenceExamination:
    """Read-only pre-execution examination for an intended transformation.

    Every demonstrated warning exposed by recurrence awareness remains visible.

    Warnings for which no explicit examination has been supplied are conserved
    as UNRESOLVED rather than silently disappearing.

    This object is physiological awareness only.  It has no execution or
    approval authority.
    """

    transformation_identity: str
    transformation_title: str
    examinations: Tuple[RecurrenceExamination, ...]

    def __post_init__(self) -> None:
        if not self.transformation_identity.strip():
            raise ValueError("transformation_identity must not be empty")

        if not self.transformation_title.strip():
            raise ValueError("transformation_title must not be empty")

        identities = [
            examination.error_identity
            for examination in self.examinations
        ]

        if len(identities) != len(set(identities)):
            raise ValueError(
                "recurrence examinations must have unique error identities"
            )

    @property
    def semantic_identity(self) -> str:
        return (
            f"{self.transformation_identity} — "
            f"{self.transformation_title}"
        )

    @property
    def unresolved(self) -> Tuple[RecurrenceExamination, ...]:
        return tuple(
            examination
            for examination in self.examinations
            if examination.disposition == RecurrenceDisposition.UNRESOLVED
        )

    @property
    def addressed(self) -> Tuple[RecurrenceExamination, ...]:
        return tuple(
            examination
            for examination in self.examinations
            if examination.disposition == RecurrenceDisposition.ADDRESSED
        )

    @property
    def not_applicable(self) -> Tuple[RecurrenceExamination, ...]:
        return tuple(
            examination
            for examination in self.examinations
            if examination.disposition
            == RecurrenceDisposition.NOT_APPLICABLE
        )

    @property
    def has_unresolved_precedent(self) -> bool:
        return bool(self.unresolved)


@dataclass(frozen=True)
class RecurrenceExaminationStatement:
    """Explicit statement supplied for one remembered precedent.

    The statement is intentionally separate from the warning itself so that
    historical Error Memory remains immutable.
    """

    error_identity: str
    disposition: RecurrenceDisposition
    explanation: str

    def __post_init__(self) -> None:
        if not self.error_identity.strip():
            raise ValueError("error_identity must not be empty")

        if not self.explanation.strip():
            raise ValueError("explanation must not be empty")


def form_pre_execution_recurrence_examination(
    awareness: PreTransformationRecurrenceAwareness,
    statements: Iterable[RecurrenceExaminationStatement] = (),
) -> PreExecutionRecurrenceExamination:
    """Make examination of demonstrated recurrence warnings explicit.

    Rules:

    * awareness remains read-only;
    * only warnings actually exposed by awareness can be examined;
    * duplicate statements are rejected;
    * a warning without a statement remains explicitly UNRESOLVED;
    * statements cannot invent warnings that Error Memory did not expose;
    * the result has no authority to permit or deny execution.

    Human Authority and the governing transformation retain decision authority.
    """

    supplied = tuple(statements)

    supplied_ids = [statement.error_identity for statement in supplied]

    if len(supplied_ids) != len(set(supplied_ids)):
        raise ValueError(
            "recurrence examination statements must have unique "
            "error identities"
        )

    warnings_by_identity = {
        warning.error_identity: warning
        for warning in awareness.warnings
    }

    unknown = tuple(
        identity
        for identity in supplied_ids
        if identity not in warnings_by_identity
    )

    if unknown:
        raise ValueError(
            "cannot examine recurrence precedent not exposed by awareness: "
            + ", ".join(unknown)
        )

    statements_by_identity = {
        statement.error_identity: statement
        for statement in supplied
    }

    examinations = []

    for warning in awareness.warnings:
        statement = statements_by_identity.get(warning.error_identity)

        if statement is None:
            examinations.append(
                RecurrenceExamination(
                    error_identity=warning.error_identity,
                    error_title=warning.error_title,
                    prevention_rule=warning.prevention_rule,
                    origin=warning.origin,
                    disposition=RecurrenceDisposition.UNRESOLVED,
                    explanation=(
                        "Relevant demonstrated precedent was exposed by "
                        "Error Memory but no explicit examination statement "
                        "was supplied."
                    ),
                )
            )
            continue

        examinations.append(
            RecurrenceExamination(
                error_identity=warning.error_identity,
                error_title=warning.error_title,
                prevention_rule=warning.prevention_rule,
                origin=warning.origin,
                disposition=statement.disposition,
                explanation=statement.explanation,
            )
        )

    return PreExecutionRecurrenceExamination(
        transformation_identity=awareness.transformation_identity,
        transformation_title=awareness.transformation_title,
        examinations=tuple(examinations),
    )

# ---------------------------------------------------------------------------
# Error Memory RUN 005
# Transformation Preparation with Recurrence Evidence
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TransformationPreparation:
    """Prepared transformation carrying recurrence examination evidence.

    RUN 005 closes the physiological gap between pre-execution recurrence
    examination and the later transformation lifecycle.

    The preparation body carries:

    * the identity and title of the intended transformation;
    * the intended activities and context;
    * the complete pre-execution recurrence examination;
    * explicit visibility of unresolved demonstrated precedent.

    It does not execute, approve, reject, validate, canonicalize, or mutate
    the intended transformation or historical Error Memory.
    """

    transformation: IntendedTransformation
    recurrence_examination: PreExecutionRecurrenceExamination

    def __post_init__(self) -> None:
        if (
            self.transformation.identity
            != self.recurrence_examination.transformation_identity
        ):
            raise ValueError(
                "transformation preparation identity must match "
                "recurrence examination identity"
            )

        if (
            self.transformation.title
            != self.recurrence_examination.transformation_title
        ):
            raise ValueError(
                "transformation preparation title must match "
                "recurrence examination title"
            )

    @property
    def semantic_identity(self) -> str:
        return (
            f"{self.transformation.identity} — "
            f"{self.transformation.title}"
        )

    @property
    def recurrence_evidence(
        self,
    ) -> Tuple[RecurrenceExamination, ...]:
        return self.recurrence_examination.examinations

    @property
    def unresolved_recurrence_evidence(
        self,
    ) -> Tuple[RecurrenceExamination, ...]:
        return self.recurrence_examination.unresolved

    @property
    def has_unresolved_recurrence_evidence(self) -> bool:
        return self.recurrence_examination.has_unresolved_precedent


def prepare_transformation_with_recurrence_evidence(
    transformation: IntendedTransformation,
    recurrence_examination: PreExecutionRecurrenceExamination,
) -> TransformationPreparation:
    """Carry recurrence examination into transformation preparation.

    The function does not infer an execution decision from the examination.

    In particular:

    * ADDRESSED is not equivalent to execution approval;
    * NOT_APPLICABLE is not equivalent to execution approval;
    * UNRESOLVED remains visible but does not grant Error Memory authority
      to block execution;
    * an empty examination remains legitimate when Error Memory exposed no
      relevant demonstrated precedent.

    Human Authority and the governing transformation lifecycle retain
    decision authority.
    """

    return TransformationPreparation(
        transformation=transformation,
        recurrence_examination=recurrence_examination,
    )


def prepare_intended_transformation_from_error_memory(
    organ: ErrorMemoryOrgan,
    transformation: IntendedTransformation,
    statements: Iterable[RecurrenceExaminationStatement] = (),
) -> TransformationPreparation:
    """Form recurrence awareness, examine it, and carry the evidence forward.

    This is the complete read-only Error Memory preparation physiology formed
    by RUN 001 through RUN 005:

        demonstrated failures
            -> recurrence awareness
            -> explicit recurrence examination
            -> transformation preparation

    The function does not execute the transformation and does not mutate the
    Error Memory organ.
    """

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        transformation,
    )

    examination = form_pre_execution_recurrence_examination(
        awareness,
        statements,
    )

    return prepare_transformation_with_recurrence_evidence(
        transformation,
        examination,
    )
