#!/usr/bin/env bash
set -euo pipefail

cd /home/runner/work/AI-Toolkit/AI-Toolkit

PYTHONPATH=lib python3 - <<'PY'
import subprocess
import tempfile
from pathlib import Path

from python.dashboard.service import EngineeringDashboardService


def make_repo(root: Path, name: str) -> Path:
    repo = root / name
    repo.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-b", "main", str(repo)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    (repo / "README.md").write_text(f"# {name}\n", encoding="utf-8")
    (repo / "requirements.txt").write_text("", encoding="utf-8")
    (repo / "tests").mkdir(exist_ok=True)
    (repo / "tests" / "test_smoke.sh").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    return repo


with tempfile.TemporaryDirectory() as tmp:
    workspace = Path(tmp)
    current_repo = make_repo(workspace, "AI-Toolkit")
    make_repo(workspace, "Trading-Signals-Platform")
    make_repo(workspace, "DROPi")

    service = EngineeringDashboardService(
        repository_root=str(current_repo),
        workspace_root=str(workspace),
    )
    payload = service.build(refresh=True)
    repositories = {item["name"] for item in payload["workspace"]["repositories"]}

    assert repositories == {"AI-Toolkit", "Trading-Signals-Platform", "DROPi"}, repositories
    assert payload["workspace"]["summary"]["total_repositories"] == 3
    assert (current_repo / "AI_CTO_INTEGRATION_REPORT.md").exists()
    print("project manager PASS")
PY
