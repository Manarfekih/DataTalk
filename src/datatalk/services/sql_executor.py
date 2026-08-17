from __future__ import annotations


import logging
import time



from ..database.connection import DatabaseManager

from ..guardrails import SQLSafety

from ..models import SQLExecutionResult



from ..observability import (
    execution_logger,
    ExecutionLog,
)



logger = logging.getLogger(__name__)





class SQLExecutor:



    def __init__(
        self,
        db: DatabaseManager,
        safety: SQLSafety | None = None,
    ):


        self._db = db

        self._safety = safety or SQLSafety()





    def execute(
        self,
        sql: str,
    ) -> SQLExecutionResult:


        start = time.perf_counter()



        try:


            validation = self._safety.validate(
                sql
            )



            if not validation.is_valid:


                elapsed = self._elapsed(
                    start
                )



                execution_logger.save(

                    ExecutionLog(

                        sql=sql,

                        success=False,

                        execution_time_ms=elapsed,

                        error=validation.message,

                    )

                )



                return SQLExecutionResult(

                    success=False,

                    error=validation.message,

                    elapsed_ms=elapsed,

                )





            result = self._db.execute_query(

                validation.sanitized_query

            )



            elapsed = self._elapsed(
                start
            )



            result.elapsed_ms = elapsed



            execution_logger.save(

                ExecutionLog(

                    sql=validation.sanitized_query,

                    success=result.success,

                    rows_returned=len(
                        result.rows
                    )
                    if result.rows
                    else 0,

                    execution_time_ms=elapsed,

                    error=result.error,

                )

            )



            return result





        except Exception as exc:


            elapsed = self._elapsed(
                start
            )



            logger.exception(
                "SQL execution failed"
            )



            execution_logger.save(

                ExecutionLog(

                    sql=sql,

                    success=False,

                    execution_time_ms=elapsed,

                    error=str(exc),

                )

            )



            return SQLExecutionResult(

                success=False,

                error=str(exc),

                elapsed_ms=elapsed,

            )






    @staticmethod
    def _elapsed(
        start: float,
    ) -> float:


        return (

            time.perf_counter()

            -

            start

        ) * 1000