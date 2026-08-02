from pathlib import Path
import sys

from parser import DevelopmentDocument
from rules import REQUIRED_SECTIONS
from rules import RequiredSectionRule
from report import ValidationReport

def run(document):

    doc = DevelopmentDocument(document)

    report = ValidationReport()

    for section in REQUIRED_SECTIONS:

        ok, error = RequiredSectionRule(section).evaluate(doc)

        if not ok:
            report.add_error(error)

    Path(".ai/work").mkdir(parents=True, exist_ok=True)

    report.save(".ai/work/development_validation.json")

    report.print()

    return 0 if report.status() != "FAILED" else 1


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: main.py <document>")
        raise SystemExit(1)

    raise SystemExit(run(sys.argv[1]))
