from __future__ import annotations

import logging
import time

from ..database.schema import schema_extractor
from ..models.schema import TableSchemaContext


logger=logging.getLogger(__name__)


class SchemaService:


    def __init__(self):

        self._schema_cache: str | None = None

        self._table_cache: list[str] | None = None

        self._table_schemas: dict[
            str,
            TableSchemaContext
        ] = {}



    def get_schema_description(
        self,
        force_refresh: bool=False
    )->str:


        if self._schema_cache is None or force_refresh:


            start=time.perf_counter()


            self._schema_cache = (
                schema_extractor
                .get_schema_description()
            )


            logger.info(
                "Schema loaded %.2f ms",
                (time.perf_counter()-start)*1000
            )


        return self._schema_cache



    def get_all_tables(
        self,
        force_refresh:bool=False
    )->list[str]:


        if self._table_cache is None or force_refresh:


            self._table_cache=(
                schema_extractor
                .get_all_tables()
            )


        return self._table_cache



    def get_table_schema(
        self,
        table_name:str
    )->TableSchemaContext | None:


        if table_name not in self._table_schemas:


            schema = (
                schema_extractor
                .get_table_schema(table_name)
            )


            if schema:

                self._table_schemas[
                    table_name
                ] = schema



        return self._table_schemas.get(
            table_name
        )



    def validate_tables(
        self,
        table_names:list[str]
    )->list[str]:


        available=self.get_all_tables()


        return [
            table
            for table in table_names
            if table in available
        ]



    def get_table_columns(
        self,
        table_name:str
    )->list[str]:


        schema=self.get_table_schema(
            table_name
        )


        if not schema:
            return []


        return [
            column.name
            for column in schema.columns
        ]



schema_service=SchemaService()

