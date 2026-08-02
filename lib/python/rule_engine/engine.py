from python.rule_engine.rules.repository_size_rule import RepositorySizeRule
from python.rule_engine.rules.validation_rule import ValidationRule

class RuleEngine:

    def __init__(self):

        self.rules = [
            RepositorySizeRule(),
            ValidationRule(),
        ]

    def evaluate(self, report):

        findings = []
        recommendations = []

        score = 100

        for rule in self.rules:

            result = rule.evaluate(report)

            if result is None:
                continue

            findings.append({
                "identifier": result.identifier,
                "severity": result.severity,
                "message": result.message
            })

            if result.recommendation:
                recommendations.append(result.recommendation)

            score -= result.score_penalty

        report["findings"] = findings
        report["recommendations"] = recommendations
        report["repository_score"] = max(score, 0)

        return report
