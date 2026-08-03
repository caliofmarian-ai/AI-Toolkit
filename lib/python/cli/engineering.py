from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from lib.python.engineering_engine.repository_audit import RepositoryAudit
from lib.python.engineering_engine.gap_analysis import GapAnalysis
from lib.python.engineering_engine.ip_generator import ImplementationPackageGenerator
from lib.python.engineering_engine.validation_engine import ValidationEngine


def engineering_audit(core):
    RepositoryAudit(ROOT).write_markdown(
        ROOT / "implementation-packages" / core / "repository-audit.md"
    )


def engineering_gap(core):
    GapAnalysis(ROOT).write_markdown(
        ROOT / "implementation-packages" / core / "gap-analysis.md"
    )


def engineering_ip(core):
    print(
        ImplementationPackageGenerator(ROOT).generate(core)
    )


def engineering_validate(core):
    result = ValidationEngine(ROOT).validate(core)
    print()
    print("========================================")
    print("ENGINEERING VALIDATION")
    print("========================================")
    print(f"PASSED : {result.passed}")
    print(f"FAILED : {result.failed}")
