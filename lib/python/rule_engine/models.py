from dataclasses import dataclass

@dataclass
class RuleResult:

    identifier: str

    severity: str

    message: str

    recommendation: str = ""

    score_penalty: int = 0
