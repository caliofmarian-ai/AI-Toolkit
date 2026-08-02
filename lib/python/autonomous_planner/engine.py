class AutonomousPlanner:

    def build(self, report):

        roadmap = {
            "status": "READY",
            "phases": []
        }

        roadmap["phases"].append({
            "name": "Phase 1 - Critical",
            "priority": "CRITICAL",
            "items": [
                r["title"]
                for r in report["recommendations_generated"]
                if r["priority"] == "HIGH"
            ]
        })

        roadmap["phases"].append({
            "name": "Phase 2 - Improvements",
            "priority": "MEDIUM",
            "items": [
                r["title"]
                for r in report["recommendations_generated"]
                if r["priority"] == "MEDIUM"
            ]
        })

        roadmap["phases"].append({
            "name": "Phase 3 - Enhancements",
            "priority": "LOW",
            "items": [
                r["title"]
                for r in report["recommendations_generated"]
                if r["priority"] == "LOW"
            ]
        })

        roadmap["estimated_hours"] = sum(
            r["estimated_hours"]
            for r in report["recommendations_generated"]
        )

        return roadmap
