from __future__ import annotations

from pydantic import BaseModel, Field


class ForeignKeyContext(BaseModel):

    constrained_columns: list[str]

    referred_table: str

    referred_columns: list[str]



class ColumnContext(BaseModel):

    name: str

    data_type: str

    nullable: bool = True

    primary_key: bool = False



class TableSchemaContext(BaseModel):

    table_name: str

    columns: list[ColumnContext]

    primary_keys: list[str] = Field(
        default_factory=list
    )

    foreign_keys: list[ForeignKeyContext] = Field(
        default_factory=list
    )