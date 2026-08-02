from dataclasses import dataclass

@dataclass
class ValidationResult:

    identifier: str

    target: str

    passed: bool

    message: str

    severity: str = "INFO"
