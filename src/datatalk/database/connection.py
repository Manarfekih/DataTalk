from __future__ import annotations

import logging
import time
from typing import Optional, Any

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from ..config import settings

from ..models import SQLExecutionResult


logger = logging.getLogger(__name__)


class DatabaseManager:

    def __init__(self) -> None:

        self._engine: Optional[Engine] = None

        self._database_url = settings.database_url

        self._initialize_connection()


    @property
    def engine(self) -> Optional[Engine]:
        return self._engine


    def _initialize_connection(self):

        try:

            self._engine = create_engine(
                self._database_url,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10,
            )


            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))


            logger.info(
                "Database connection established."
            )


        except Exception:

            logger.exception(
                "Database connection failed."
            )

            self._engine = None



    def is_connected(self)->bool:

        return self._engine is not None



    def execute_query(
        self,
        query: str,
    ) -> SQLExecutionResult:

        if self._engine is None:

            return SQLExecutionResult(
                success=False,
                error="Database not connected.",
            )

        start = time.perf_counter()

        try:

            with self._engine.connect() as conn:

                result = conn.execute(text(query))

                rows = result.fetchall()

                columns = list(result.keys())

                return SQLExecutionResult(
                    success=True,
                    rows=[ dict(row._mapping) for row in rows],
                    columns=columns,
                    row_count=len(rows),
                    elapsed_ms=(time.perf_counter() - start) * 1000,
                )

        except SQLAlchemyError as exc:

            logger.exception("SQL execution failed.")

            return SQLExecutionResult(
                success=False,
                error=str(exc),
                elapsed_ms=(time.perf_counter() - start) * 1000,
            )

        except Exception as exc:

            logger.exception("Unexpected database error.")

            return SQLExecutionResult(
                success=False,
                error=str(exc),
                elapsed_ms=(time.perf_counter() - start) * 1000,
            ) 


db_manager = DatabaseManager()

