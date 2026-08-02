class RecommendationEngine:

    def build(self, report):

        recommendations = []

        inspection = report["inspection"]

        if inspection["repository_score"] < 100:
            recommendations.append({
                "priority": "HIGH",
                "title": "Resolve repository findings",
                "reason": "Repository score is below 100.",
                "estimated_hours": 2
            })

        if report["canonical"]["missing_modules"]:
            recommendations.append({
                "priority": "HIGH",
                "title": "Implement missing canonical modules",
                "reason": f'{len(report["canonical"]["missing_modules"])} canonical specifications have no detected implementation.',
                "estimated_hours": len(report["canonical"]["missing_modules"])
            })

        if len(report["knowledge_graph"]["edges"]) < 100:
            recommendations.append({
                "priority": "MEDIUM",
                "title": "Expand architectural relationships",
                "reason": "Knowledge graph is still small.",
                "estimated_hours": 4
            })

        if len(report["semantic"]) < 100:
            recommendations.append({
                "priority": "LOW",
                "title": "Increase semantic coverage",
                "reason": "Repository semantic model can be enriched.",
                "estimated_hours": 3
            })

        if not recommendations:
            recommendations.append({
                "priority": "LOW",
                "title": "Repository is healthy",
                "reason": "Continue implementing new capabilities.",
                "estimated_hours": 0
            })

        return recommendations
