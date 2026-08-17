from __future__ import annotations


import logging


from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)


from .dependencies import get_graph

from .mapper import (
    to_query_response
)


from .models import (
    HealthResponse,
    QueryRequest,
    QueryResponse,
)


from datatalk.graph.workflow import DataTalkGraph

from datatalk.database.connection import db_manager



logger = logging.getLogger(__name__)


router = APIRouter()






@router.get(
    "/",
    tags=["system"],
)
def root():


    return {
        "message":
        "DataTalk API running with LangGraph"
    }







@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["system"],
)
def health():


    return HealthResponse(

        status="ok",

        database=
            db_manager.is_connected(),

        llm=True,

    )








@router.post(
    "/query",
    response_model=QueryResponse,
    tags=["query"],
)
def query(

    request: QueryRequest,

    graph: DataTalkGraph =
        Depends(get_graph),

):


    try:


        result = graph.invoke(

            {

                "question":
                    request.question,


                "retry_count":
                    0,


                "max_retries":
                    2,

            }

        )


        return to_query_response(
            result
        )




    except ValueError as exc:


        raise HTTPException(

            status_code=
                status.HTTP_400_BAD_REQUEST,

            detail=str(exc),

        )




    except Exception as exc:


        logger.exception(
            "Query failed"
        )


        raise HTTPException(

            status_code=
                status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail=
                "Internal server error",

        )