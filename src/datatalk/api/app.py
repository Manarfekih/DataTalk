from __future__ import annotations


import logging

from fastapi import FastAPI

from .routes import router

from datatalk.core import container


logger = logging.getLogger(__name__)



app = FastAPI(

    title="DataTalk",

    description=(
        "Conversational Analytics Agent with Text-to-SQL, "
        "SQL retry intelligence, and SQL memory."
    ),

    version="0.1.0",

)




app.include_router(
    router
)


@app.on_event("startup")
def startup_event() -> None:
    """
    Initialize DataTalk components when API starts.
    """

    logger.info(
        "Starting DataTalk API..."
    )

    container.initialize()

    logger.info(
        "DataTalk ready."
    )



@app.on_event("shutdown")
def shutdown_event() -> None:
    

    logger.info(
        "Stopping DataTalk API..."
    )




app.include_router(
    router
)