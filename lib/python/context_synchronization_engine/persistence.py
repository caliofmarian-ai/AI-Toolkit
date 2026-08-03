import json
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping, Optional


class ContextPersistence:
    def __init__(self, repository_root: str = "."):
        self.repository_root = Path(repository_root).resolve()
        self.base_dir = self.repository_root / ".ai" / "context"

    def save_json(self, filename: str, payload: Mapping[str, Any]) -> str:
        path = self.base_dir / filename
        self._atomic_write(path, self._serialize(payload))
        return str(path)

    def save_text(self, filename: str, content: str) -> str:
        path = self.base_dir / filename
        self._atomic_write(path, content if content.endswith("\n") else content + "\n")
        return str(path)

    def load_json(self, filename: str) -> Optional[dict]:
        path = self.base_dir / filename
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

    def exists(self, filename: str) -> bool:
        return (self.base_dir / filename).exists()

    def _serialize(self, payload: Mapping[str, Any]) -> str:
        return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    def _atomic_write(self, path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_path, path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
