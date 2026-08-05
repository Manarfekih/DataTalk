from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SQLExecutionResult:
    

    success: bool

    rows: list[dict[str, Any]] = field(
        default_factory=list
    )

    columns: list[str] = field(
        default_factory=list
    )

    row_count: int = 0

    error: str | None = None

    elapsed_ms: float = 0.0


    @property
    def has_rows(self) -> bool:
        return self.row_count > 0


    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "rows": self.rows,
            "columns": self.columns,
            "row_count": self.row_count,
            "error": self.error,
            "elapsed_ms": self.elapsed_ms,
        }