from python.rule_engine.base import Rule
from python.rule_engine.models import RuleResult

class RepositorySizeRule(Rule):

    NAME = "Repository Size"

    def evaluate(self, report):

        if report["repository"]["files"] >= 20:
            return None

        return RuleResult(
            identifier="RULE-001",
            severity="WARNING",
            message="Repository contains very few files.",
            recommendation="Continue repository development.",
            score_penalty=5
        )
