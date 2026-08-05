from __future__ import annotations

import logging
import time

from ..guardrails import SQLSafety
from ..llm.base import BaseLLMProvider
from ..models.agent_outputs import SQLWriterOutput
from ..models.schema import TableSchemaContext
from ..prompts.sql_writer import SQL_WRITER_PROMPT
from ..services.schema_service import SchemaService


logger = logging.getLogger(__name__)


class SQLWriterAgent:
    """
    Generates SQL queries from natural language.

    Responsibilities:
        - Build schema context
        - Generate SQL
        - Validate SQL safety
    """

    def __init__(self, llm: BaseLLMProvider, schema_service: SchemaService) -> None:
        self._llm = llm
        self._schema_service = schema_service
        self._sql_safety = SQLSafety()

    def write_sql(self, question: str, tables: list[str]) -> SQLWriterOutput:
        self._validate_inputs(question, tables)

        start = time.perf_counter()
        schema_context = self._build_schema_context(tables)
        prompt = self._build_prompt(question=question, schema_context=schema_context)
        result = self._generate_sql(prompt)

        sql_query = self._sql_safety.validate_or_raise(result.sql_query)
        result = result.model_copy(update={"sql_query": sql_query})

        elapsed = (time.perf_counter() - start) * 1000
        logger.info("SQL generated in %.2f ms", elapsed)

        return result

    def _validate_inputs(self, question: str, tables: list[str]) -> None:
        if not question.strip():
            raise ValueError("Question cannot be empty.")

        if not tables:
            raise ValueError("No tables were provided.")

    def _build_prompt(self, *, question: str, schema_context: str) -> str:
        return SQL_WRITER_PROMPT.format(
            question=question,
            schema_context=schema_context,
        )

    def _generate_sql(self, prompt: str) -> SQLWriterOutput:
        return self._llm.generate_structured(
            prompt=prompt,
            response_model=SQLWriterOutput,
            temperature=0.0,
        )

    # Schema preparation
    def _build_schema_context(self, tables: list[str]) -> str:
        parts: list[str] = []

        for table in tables:
            schema = self._schema_service.get_table_schema(table)

            if schema is None:
                raise ValueError(f"Unknown table: {table}")

            parts.append(self._format_table(schema))

        return "\n\n".join(parts)

    @staticmethod
    def _format_table(schema: TableSchemaContext) -> str:
        lines = [
            f"Table: {schema.table_name}",
            "",
            "Columns:",
        ]

        for column in schema.columns:
            info = f"- {column.name} ({column.data_type})"

            if column.primary_key:
                info += " PRIMARY KEY"

            if not column.nullable:
                info += " NOT NULL"

            lines.append(info)

        if schema.foreign_keys:
            lines.extend([
                "",
                "Foreign Keys:",
            ])

            for fk in schema.foreign_keys:
                lines.append(
                    f"- {schema.table_name}.{','.join(fk.constrained_columns)} -> {fk.referred_table}.{','.join(fk.referred_columns)}"
                )

        return "\n".join(lines)
