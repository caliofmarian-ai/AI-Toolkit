#!/usr/bin/env python3

from pathlib import Path
import sys

REQUIRED_SECTIONS = [
    "PURPOSE",
    "OBJECTIVES",
    "INPUTS",
    "OUTPUTS",
    "VALIDATION MODULES",
    "CHECKLIST",
    "STATUS"
]

def validate(document):
    path = Path(document)

    if not path.exists():
        print("ERROR: document not found")
        return 1

    text = path.read_text(encoding="utf-8")

    score = 100
    warnings = []

    for section in REQUIRED_SECTIONS:
        if section not in text:
            score -= 10
            warnings.append(f"Missing section: {section}")

    print("==================================")
    print("Development Validator")
    print("==================================")
    print()
    print("Document:", path)
    print("Score:", max(score, 0), "/100")
    print()

    if warnings:
        print("Warnings")
        for warning in warnings:
            print("-", warning)
        print()

    if score == 100:
        print("STATUS: PASS")
        return 0

    if score >= 70:
        print("STATUS: WARNING")
        return 0

    print("STATUS: FAILED")
    return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:")
        print("python3 development_validator.py <document>")
        raise SystemExit(1)

    raise SystemExit(validate(sys.argv[1]))
