class RepositoryAnalyzer:

    def analyze(self, report):

        findings = []
        recommendations = []

        score = 100

        validation = report["validation"]

        if validation["failed"] > 0:
            findings.append({
                "severity": "CRITICAL",
                "message": f'{validation["failed"]} validation checks failed.'
            })
            recommendations.append(
                "Resolve all validation failures."
            )
            score -= validation["failed"] * 10

        repository = report["repository"]

        if repository["files"] < 20:
            findings.append({
                "severity": "WARNING",
                "message": "Repository is very small."
            })
            recommendations.append(
                "Continue repository development."
            )
            score -= 5

        dependencies = report["dependencies"]

        if dependencies["dependencies"] != repository["files"]:
            findings.append({
                "severity": "INFO",
                "message": "Dependency/file count differs."
            })

        report["findings"] = findings
        report["recommendations"] = recommendations
        report["repository_score"] = max(score, 0)

        return report
