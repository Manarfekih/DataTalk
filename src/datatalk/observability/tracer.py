from __future__ import annotations


import time
import uuid
import logging


from datetime import datetime



from .models import TraceEvent

from .storage import TraceStorage



logger = logging.getLogger(__name__)




class TracerSpan:


    def __init__(
        self,
        tracer,
        node_name: str,
        input_data: dict,
    ):

        self.tracer = tracer

        self.node_name = node_name

        self.input_data = input_data

        self.start = None




    def __enter__(self):

        self.start = time.perf_counter()

        return self





    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):


        end = time.perf_counter()



        event = TraceEvent(

            trace_id=str(
                uuid.uuid4()
            ),

            node_name=self.node_name,

            start_time=datetime.utcnow(),

            end_time=datetime.utcnow(),

            duration_ms=(

                end - self.start

            ) * 1000,


            input_data=self.input_data,


            success=(
                exc_value is None
            ),


            error=(
                str(exc_value)
                if exc_value
                else None
            ),

        )



        self.tracer.storage.save(
            event
        )





class DataTalkTracer:



    def __init__(self):

        self.storage = (
            TraceStorage()
        )




    def span(
        self,
        node_name: str,
        input_data: dict | None = None,
    ):


        return TracerSpan(

            self,

            node_name,

            input_data or {},

        )




tracer = DataTalkTracer()