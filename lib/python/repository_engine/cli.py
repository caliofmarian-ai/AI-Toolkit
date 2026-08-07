from datetime import datetime, timezone
from pathlib import Path

from .engine import RepositoryEngine
from .report import MarkdownRenderer
from .serializer import RepositoryProfileSerializer


def inspect(path="."):
    root = Path(path).resolve()
    profile = RepositoryEngine(root).profile()
    report = MarkdownRenderer().render(profile)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    output_dir = root / ".ai" / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / f"inspect-{stamp}.md"
    report_path.write_text(report, encoding="utf-8")

    profile_path = output_dir / f"inspect-{stamp}.json"
    profile_path.write_text(RepositoryProfileSerializer.to_json(profile), encoding="utf-8")

    return {
        "repository": profile.name,
        "path": str(root),
        "report_path": str(report_path),
        "profile_path": str(profile_path),
    }
