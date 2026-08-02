import json
from pathlib import Path


class GitHubMaterializationEngine:

    ROOT = Path(".ai/batches")

    def generate(self, batches):

        generated = []

        self.ROOT.mkdir(parents=True, exist_ok=True)

        for batch in batches:

            directory = self.ROOT / batch["identifier"]
            directory.mkdir(parents=True, exist_ok=True)

            metadata = dict(batch)

            (directory / "metadata.json").write_text(
                json.dumps(metadata, indent=2),
                encoding="utf-8"
            )

            (directory / "issue.md").write_text(
f"""# {batch["identifier"]}

## Title

{batch["title"]}

## Priority

{batch["priority"]}

## Reason

{batch["reason"]}

## Estimated Work

{batch["estimated_hours"]} hours
""",
                encoding="utf-8"
            )

            (directory / "checklist.md").write_text(
"""# Checklist

- [ ] Implementation completed
- [ ] Tests passing
- [ ] Documentation updated
""",
                encoding="utf-8"
            )

            (directory / "implementation_plan.md").write_text(
f"""# Implementation Plan

Target:
{batch["title"]}

Reason:
{batch["reason"]}
""",
                encoding="utf-8"
            )

            (directory / "pull_request.md").write_text(
f"""# Pull Request

Implements:

{batch["identifier"]}

Summary

{batch["title"]}
""",
                encoding="utf-8"
            )

            generated.append(str(directory))

        return generated
