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
