import json
from pathlib import Path


class ExecutionCoordinator:

    STATE_FILE = Path(".ai/execution_state.json")

    def coordinate(self, roadmap):

        state = {
            "status": "RUNNING",
            "phases": []
        }

        for phase in roadmap["phases"]:

            phase_state = {
                "name": phase["name"],
                "priority": phase["priority"],
                "status": (
                    "READY"
                    if phase["items"]
                    else "SKIPPED"
                ),
                "items": phase["items"],
            }

            state["phases"].append(phase_state)

        if all(
            p["status"] == "SKIPPED"
            for p in state["phases"]
        ):
            state["status"] = "COMPLETED"

        self.STATE_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.STATE_FILE.write_text(
            json.dumps(state, indent=2),
            encoding="utf-8"
        )

        return state
