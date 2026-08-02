from pathlib import Path


class WorkspaceManager:

    def discover(self, workspace):

        workspace = Path(workspace).resolve()

        repositories = []

        for item in sorted(workspace.iterdir()):

            if not item.is_dir():
                continue

            if (item / ".git").exists():

                repositories.append({
                    "name": item.name,
                    "path": str(item),
                })

        return repositories
