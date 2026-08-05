from __future__ import annotations

import logging
import time

from ..database.connection import DatabaseManager
from ..guardrails import SQLSafety
from ..models import SQLExecutionResult


logger=logging.getLogger(__name__)


class SQLExecutor:


    def __init__(
        self,
        db: DatabaseManager,
        safety: SQLSafety | None = None
    ):

        self._db=db

        self._safety=safety or SQLSafety()



    def execute(
        self,
        sql:str
    )->SQLExecutionResult:


        start=time.perf_counter()



        validation=self._safety.validate(sql)



        if not validation.is_valid:

            return SQLExecutionResult(
                success=False,
                error=validation.message,
                elapsed_ms=self._elapsed(start)
            )



        result=self._db.execute_query(
            validation.sanitized_query
        )



        result.elapsed_ms=self._elapsed(start)


        return result



    @staticmethod
    def _elapsed(
        start:float
    )->float:

        return (
            time.perf_counter()-start
        )*1000


