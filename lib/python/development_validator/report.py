import json

class ValidationReport:

    def __init__(self):
        self.score = 100
        self.errors = []
        self.warnings = []

    def add_error(self, message):
        self.errors.append(message)
        self.score -= 10

    def as_dict(self):

        return {
            "score": max(self.score, 0),
            "errors": self.errors,
            "warnings": self.warnings,
            "status": self.status()
        }

    def status(self):

        if self.score == 100:
            return "PASS"

        if self.score >= 70:
            return "WARNING"

        return "FAILED"

    def print(self):

        print("==================================")
        print("Development Validator")
        print("==================================")
        print()

        print("Score:", max(self.score, 0))

        print()

        for error in self.errors:
            print("ERROR:", error)

        for warning in self.warnings:
            print("WARNING:", warning)

        print()

        print("STATUS:", self.status())

    def save(self, path):

        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.as_dict(), f, indent=2)
