class BatchGenerator:

    def generate(self, recommendations):

        batches = []

        for index, rec in enumerate(recommendations, start=1):

            batches.append({
                "identifier": f"BATCH-{index:03d}",
                "title": rec["title"],
                "priority": rec["priority"],
                "reason": rec["reason"],
                "estimated_hours": rec["estimated_hours"],
                "status": "READY",
                "acceptance_criteria": [
                    "Implementation completed",
                    "Tests passing",
                    "Documentation updated"
                ]
            })

        return batches
