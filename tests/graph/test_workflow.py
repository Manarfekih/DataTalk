from datatalk.graph.workflow import DataTalkGraph

from datatalk.graph.nodes import GraphNodes



from tests.graph.test_nodes import (
    FakeQuestionAgent,
    FakeSchemaAgent,
    FakeSQLWriter,
    FakeExecutor,
    FakeRetry,
    FakeExplanation,
)





def build_graph():


    nodes = GraphNodes(

        question_agent=
            FakeQuestionAgent(),

        schema_explorer=
            FakeSchemaAgent(),

        sql_writer=
            FakeSQLWriter(),

        sql_executor=
            FakeExecutor(),

        sql_retry=
            FakeRetry(),

        explanation_agent=
            FakeExplanation(),

    )


    return DataTalkGraph(
        nodes
    )





def test_langgraph_full_execution():


    graph = build_graph()



    result = graph.invoke(

        {

            "question":
            "How many customers?",


            "retry_count":
            0,


            "max_retries":
            2,

        }

    )


    assert (
        result["clean_question"]
        ==
        "How many customers?"
    )


    assert (
        result["sql_query"]
        is not None
    )


    assert (
        result["explanation"]
        ==
        "There are 91 customers."
    )