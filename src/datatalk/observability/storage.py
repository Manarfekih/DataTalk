from __future__ import annotations


import json

from pathlib import Path



from .models import TraceEvent




TRACE_DIR = Path(
    "logs"
)


TRACE_FILE = TRACE_DIR / "traces.json"





class TraceStorage:
   



    def __init__(self):

        TRACE_DIR.mkdir(
            exist_ok=True
        )




    def load_all(self) -> list[TraceEvent]:

        if not TRACE_FILE.exists():

            return []


        with open(
            TRACE_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            raw = json.load(file)


        return [
            TraceEvent(**item)
            for item in raw
        ]



    def save(
        self,
        event: TraceEvent,
    ):

        traces = []


        if TRACE_FILE.exists():

            with open(
                TRACE_FILE,
                "r",
                encoding="utf-8",
            ) as file:

                traces = json.load(file)



        traces.append(
            event.model_dump(
                mode="json"
            )
        )



        with open(
            TRACE_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                traces,
                file,
                indent=4,
            )