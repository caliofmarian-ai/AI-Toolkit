from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(slots=True)
class TransactionRecord:
    operation: str
    title: str
    status: str


@dataclass(slots=True)
class TransactionLog:
    records: list[TransactionRecord] = field(default_factory=list)


class GitHubTransactionLogger:

    def load(
        self,
        path: Path,
    ) -> TransactionLog:

        if not path.exists():
            return TransactionLog()

        data = json.loads(
            path.read_text(encoding="utf-8")
        )

        return TransactionLog(
            records=[
                TransactionRecord(**item)
                for item in data
            ]
        )

    def save(
        self,
        log: TransactionLog,
        path: Path,
    ) -> None:

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                [asdict(item) for item in log.records],
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def append(
        self,
        log: TransactionLog,
        operation: str,
        title: str,
        status: str,
    ) -> None:

        log.records.append(
            TransactionRecord(
                operation=operation,
                title=title,
                status=status,
            )
        )
