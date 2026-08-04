from __future__ import annotations

from dataclasses import dataclass

from lib.python.engineering_engine.roadmap_engine import Roadmap


@dataclass(slots=True)
class GitHubMilestone:

    title: str

    description: str

    batch_id: str

    priority: str


class GitHubMilestoneGenerator:

    def generate(
        self,
        roadmap: Roadmap,
    ) -> list[GitHubMilestone]:

        milestones = []

        for phase, batch in enumerate(
            roadmap.phases,
            start=1,
        ):

            milestones.append(
                GitHubMilestone(
                    title=f"Phase {phase:02} - {batch.id}",
                    description=(
                        f"Engineering execution batch "
                        f"{batch.id} "
                        f"({len(batch.tasks)} tasks)"
                    ),
                    batch_id=batch.id,
                    priority=batch.priority,
                )
            )

        return milestones
