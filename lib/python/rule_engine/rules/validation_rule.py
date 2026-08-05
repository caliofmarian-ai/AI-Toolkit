from python.rule_engine.base import Rule
from python.rule_engine.models import RuleResult

class ValidationRule(Rule):

    NAME = "Validation"

    def evaluate(self, report):

        failed = report["validation"]["failed"]

        if failed == 0:
            return None

        return RuleResult(
            identifier="ATK-RULE-002",
            severity="CRITICAL",
            message=f"{failed} validation checks failed.",
            recommendation="Resolve validation failures.",
            score_penalty=failed * 10
        )
