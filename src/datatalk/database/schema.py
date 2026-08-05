from __future__ import annotations

import logging

from sqlalchemy import inspect
from sqlalchemy.engine import Engine

from .connection import db_manager
from ..models.schema import (
    ColumnContext,
    ForeignKeyContext,
    TableSchemaContext,
)

logger = logging.getLogger(__name__)


class SchemaExtractor:
   

    @property
    def _engine(self) -> Engine | None:
        return db_manager.engine

    def get_all_tables(self) -> list[str]:
        

        engine = self._engine

        if engine is None:
            return []

        try:
            inspector = inspect(engine)
            return inspector.get_table_names()

        except Exception:
            logger.exception("Failed to retrieve database tables.")
            return []

    def get_table_schema(
        self,
        table_name: str,
    ) -> TableSchemaContext | None:
        

        engine = self._engine

        if engine is None:
            return None

        try:
            inspector = inspect(engine)

            columns: list[ColumnContext] = []
            primary_keys: list[str] = []

            for column in inspector.get_columns(table_name):

                is_pk = column.get("primary_key", False)

                if is_pk:
                    primary_keys.append(column["name"])

                columns.append(
                    ColumnContext(
                        name=column["name"],
                        data_type=str(column["type"]),
                        nullable=column["nullable"],
                        primary_key=is_pk,
                    )
                )

            foreign_keys = [
                ForeignKeyContext(
                    constrained_columns=fk["constrained_columns"],
                    referred_table=fk["referred_table"],
                    referred_columns=fk["referred_columns"],
                )
                for fk in inspector.get_foreign_keys(table_name)
            ]

            return TableSchemaContext(
                table_name=table_name,
                columns=columns,
                primary_keys=primary_keys,
                foreign_keys=foreign_keys,
            )

        except Exception:
            logger.exception(
                "Failed to load schema for table '%s'.",
                table_name,
            )
            return None

    def get_schema_description(self) -> str:
        

        tables = self.get_all_tables()

        if not tables:
            return "No tables found."

        lines: list[str] = [
            "DATABASE SCHEMA:",
            "",
        ]

        for table in tables:

            schema = self.get_table_schema(table)

            if schema is None:
                continue

            lines.append(f"Table: {schema.table_name}")
            lines.append("Columns:")

            for column in schema.columns:

                suffix = ""

                if column.primary_key:
                    suffix += " [PK]"

                if not column.nullable:
                    suffix += " NOT NULL"

                lines.append(
                    f"  - {column.name}: "
                    f"{column.data_type}{suffix}"
                )

            if schema.foreign_keys:
                lines.append("Foreign Keys:")

                foreign_keys = (
                    schema.foreign_keys
                    if isinstance(schema.foreign_keys, (list, tuple))
                    else [schema.foreign_keys]
                )

                for fk in foreign_keys:
                    # fk may be a dataclass/object or a plain dict/FieldInfo-like object.
                    def _get(o, attr, default=None):
                        if hasattr(o, attr):
                            return getattr(o, attr)
                        if isinstance(o, dict):
                            return o.get(attr, default)
                        return default

                    constrained = _get(fk, "constrained_columns") or []
                    referred = _get(fk, "referred_columns") or []
                    referred_table = _get(fk, "referred_table") or ""

                    lines.append(
                        f"  - "
                        f"{', '.join(constrained)}"
                        f" -> "
                        f"{referred_table}"
                        f"("
                        f"{', '.join(referred)}"
                        f")"
                    )

            lines.append("")

        return "\n".join(lines)


schema_extractor = SchemaExtractor()

