"""Performance characterization for PCC-01 Persistent Experience.

Performance measurements are evidence about execution cost.

They are not Experience.
They are not authority.
They do not change persistence semantics.
They do not weaken durability.

No absolute wall-clock Production-Ready threshold is encoded here because
execution environments differ. The organ produces reproducible measurements
and structural operation counts that can be audited.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

from .model import Experience
from .persistent_repository import JsonFileExperienceRepository


@dataclass(frozen=True, slots=True)
class ExperiencePerformanceSample:
    """One reproducible persistent-repository workload measurement."""

    experience_count: int
    add_seconds: float
    contains_seconds: float
    get_seconds: float
    save_seconds: float
    store_bytes: int

    @property
    def total_seconds(self) -> float:
        return (
            self.add_seconds
            + self.contains_seconds
            + self.get_seconds
            + self.save_seconds
        )

    def to_dict(self) -> dict[str, int | float]:
        return {
            "experience_count": self.experience_count,
            "add_seconds": self.add_seconds,
            "contains_seconds": self.contains_seconds,
            "get_seconds": self.get_seconds,
            "save_seconds": self.save_seconds,
            "total_seconds": self.total_seconds,
            "store_bytes": self.store_bytes,
        }


def characterize_persistent_repository(
    path: str | Path,
    *,
    experience_count: int,
) -> ExperiencePerformanceSample:
    """Execute a deterministic PCC-01 persistence workload.

    The workload exercises the real persistent repository:

    1. create and add N Experiences;
    2. contains() each identity;
    3. get() each identity;
    4. transition each Experience and save() it.

    The resulting timings describe the environment in which the examination
    ran. Correctness is verified during the workload.
    """

    if (
        isinstance(experience_count, bool)
        or not isinstance(experience_count, int)
        or experience_count <= 0
    ):
        raise ValueError(
            "experience_count must be a positive integer"
        )

    repository = JsonFileExperienceRepository(path)
    experiences = [
        Experience.create()
        for _ in range(experience_count)
    ]

    started = perf_counter()

    for experience in experiences:
        repository.add(experience)

    add_seconds = perf_counter() - started

    started = perf_counter()

    for experience in experiences:
        if not repository.contains(experience.experience_id):
            raise AssertionError(
                "persistent repository lost admitted Experience"
            )

    contains_seconds = perf_counter() - started

    started = perf_counter()

    recovered = [
        repository.get(experience.experience_id)
        for experience in experiences
    ]

    get_seconds = perf_counter() - started

    for before, after in zip(
        experiences,
        recovered,
        strict=True,
    ):
        if before.experience_id != after.experience_id:
            raise AssertionError(
                "performance workload changed Experience identity"
            )

    activated = [
        experience.activate()
        for experience in recovered
    ]

    started = perf_counter()

    for experience in activated:
        repository.save(experience)

    save_seconds = perf_counter() - started

    store_path = Path(path)

    return ExperiencePerformanceSample(
        experience_count=experience_count,
        add_seconds=add_seconds,
        contains_seconds=contains_seconds,
        get_seconds=get_seconds,
        save_seconds=save_seconds,
        store_bytes=store_path.stat().st_size,
    )
