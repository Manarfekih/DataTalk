from datatalk.core import container


def test_query_workflow_with_explanation():

    container.initialize()

    result = container.query_workflow.ask(
        "How many customers are there?"
    )


    print("\nQUESTION:")
    print(result.question)


    print("\nSQL:")
    print(result.sql_query)


    print("\nROWS:")
    print(result.execution.rows)


    print("\nEXPLANATION:")
    print(result.explanation)



    assert result.question

    assert result.sql_query

    assert result.execution.success

    assert result.explanation
