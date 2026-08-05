from pydantic import BaseModel, Field


class SchemaExplorerOutput(BaseModel):

    relevant_tables: list[str]

    reasoning: str


class SQLWriterOutput(BaseModel):

     sql_query: str = Field(
        description="Executable PostgreSQL query."
    )