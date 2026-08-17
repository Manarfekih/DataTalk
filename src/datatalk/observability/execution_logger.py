from __future__ import annotations


import json

from pathlib import Path



from .execution_models import ExecutionLog




LOG_DIR = Path("logs")

LOG_FILE = LOG_DIR / "executions.json"





class ExecutionLogger:
    """
    Stores SQL execution history.
    """



    def __init__(self):

        LOG_DIR.mkdir(
            exist_ok=True
        )




    def load_all(self) -> list[ExecutionLog]:

        if not LOG_FILE.exists():

            return []


        with open(
            LOG_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            raw = json.load(file)


        return [
            ExecutionLog(**item)
            for item in raw
        ]



    def save(
        self,
        log: ExecutionLog,
    ):


        executions = []


        if LOG_FILE.exists():

            with open(
                LOG_FILE,
                "r",
                encoding="utf-8",
            ) as file:

                executions = json.load(file)



        executions.append(

            log.model_dump(
                mode="json"
            )

        )



        with open(
            LOG_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                executions,
                file,
                indent=4,
            )





execution_logger = ExecutionLogger()