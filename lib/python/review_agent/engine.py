class ReviewAgent:

    def review(self, report):

        review = {
            "score": report["inspection"]["repository_score"],
            "status": "READY",
            "critical": [],
            "major": [],
            "minor": [],
            "summary": [],
        }

        if report["inspection"]["repository_score"] < 80:
            review["status"] = "NEEDS_CHANGES"

        for finding in report["inspection"]["findings"]:

            severity = finding["severity"].upper()

            if severity == "CRITICAL":
                review["critical"].append(finding)

            elif severity == "WARNING":
                review["major"].append(finding)

            else:
                review["minor"].append(finding)

        review["summary"].append(
            f'Score: {review["score"]}/100'
        )

        review["summary"].append(
            f'Critical: {len(review["critical"])}'
        )

        review["summary"].append(
            f'Major: {len(review["major"])}'
        )

        review["summary"].append(
            f'Minor: {len(review["minor"])}'
        )

        return review
