from datatalk.graph.nodes import GraphNodes



class FakeQuestionAgent:


    class Result:

        needs_clarification = False

        corrected_question = (
            "How many customers?"
        )


    def process(self, question):

        return self.Result()



class FakeSchemaAgent:


    class Result:

        relevant_tables = [
            "customers"
        ]

        reasoning = (
            "Customers table contains users."
        )


    def explore(self, question):

        return self.Result()




class FakeSQLWriter:


    class Result:

        sql_query = (
            "SELECT COUNT(*) FROM customers;"
        )


    def write_sql(
        self,
        question,
        tables
    ):

        return self.Result()




class FakeExecutor:


    class Result:

        success = True

        rows = [
            {
                "count":91
            }
        ]

        columns=[
            "count"
        ]

        error=None


    def execute(self,sql):

        return self.Result()




class FakeExplanation:


    class Result:

        explanation = (
            "There are 91 customers."
        )


    def explain(
        self,
        question,
        columns,
        rows
    ):

        return self.Result()



class FakeRetry:


    pass




def build_nodes():


    return GraphNodes(

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





def test_question_node():


    nodes = build_nodes()


    result = nodes.understand_question(

        {
            "question":
            "How many customers?"
        }

    )


    assert (
        result["clean_question"]
        ==
        "How many customers?"
    )





def test_schema_node():


    nodes = build_nodes()


    result = nodes.explore_schema(

        {
            "clean_question":
            "How many customers?"
        }

    )


    assert (
        "customers"
        in result["tables"]
    )





def test_sql_generation_node():


    nodes = build_nodes()


    result = nodes.generate_sql(

        {

        "clean_question":
        "How many customers?",


        "tables":
        ["customers"]

        }

    )


    assert (
        "SELECT"
        in result["sql_query"]
    )





def test_execution_node():


    nodes = build_nodes()


    result = nodes.execute_sql(

        {
            "sql_query":
            "SELECT COUNT(*) FROM customers;"
        }

    )


    assert result["rows"][0]["count"] == 91