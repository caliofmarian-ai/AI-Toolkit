from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from lib.python.engineering_engine.markdown_renderer import MarkdownRenderer
from lib.python.engineering_engine.models import (
    EngineeringBatch,
    ImplementationPackageModel,
)


class ImplementationPackageGenerator:

    def __init__(self, root: Path):
        self.root = root

    def generate(self, model: ImplementationPackageModel):

        package = self.root / "implementation-packages" / model.core
        package.mkdir(parents=True, exist_ok=True)

        output = package / f"IP-{model.core}.md"

        renderer = MarkdownRenderer()

        with output.open("w", encoding="utf-8") as md:

            md.write(renderer.render_implementation_package(model))

        return output
