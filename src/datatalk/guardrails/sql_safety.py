from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(slots=True)
class SQLValidationResult:
    is_valid: bool
    message: str
    sanitized_query: str = ""


class SQLSafety:
    _ALLOWED_PREFIXES = (
        "SELECT",
        "WITH",
    )

    _BLOCKED_KEYWORDS = (
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "TRUNCATE",
        "MERGE",
        "GRANT",
        "REVOKE",
        "CALL",
        "EXEC",
        "EXECUTE",
        "COPY",
    )

    def validate(self, sql: str) -> SQLValidationResult:
        if not sql or not sql.strip():
            return SQLValidationResult(False, "Query is empty.")

        cleaned = self.sanitize(sql)
        upper_sql = cleaned.upper()

        if not upper_sql.startswith(self._ALLOWED_PREFIXES):
            return SQLValidationResult(False, "Only SELECT statements are allowed.")

        for keyword in self._BLOCKED_KEYWORDS:
            if re.search(rf"\b{keyword}\b", upper_sql):
                return SQLValidationResult(False, f"Blocked keyword: {keyword}")

        if ";" in cleaned.rstrip(";"):
            return SQLValidationResult(False, "Multiple SQL statements are not allowed.")

        return SQLValidationResult(True, "SQL is valid.", cleaned)

    def validate_or_raise(self, sql: str) -> str:
        result = self.validate(sql)

        if not result.is_valid:
            raise ValueError(result.message)

        return result.sanitized_query

    @staticmethod
    def sanitize(sql: str) -> str:
        sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
        sql = re.sub(r"--.*?$", "", sql, flags=re.MULTILINE)
        return sql.strip().rstrip(";")
