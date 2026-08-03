from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from lib.python.engineering_engine.repository_audit import RepositoryAudit
from lib.python.engineering_engine.gap_analysis import GapAnalysis


def engineering_audit(core: str):
    output = ROOT / "implementation-packages" / core / "repository-audit.md"
    RepositoryAudit(ROOT).write_markdown(output)
    print(f"Repository audit written to {output}")


def engineering_gap(core: str):
    output = ROOT / "implementation-packages" / core / "gap-analysis.md"
    GapAnalysis(ROOT).write_markdown(output)
    print(f"Gap analysis written to {output}")
