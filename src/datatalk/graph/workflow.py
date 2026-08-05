from __future__ import annotations


from langgraph.graph import (
    StateGraph,
    END,
)


from datatalk.graph.state import DataTalkState


from datatalk.graph.edges import execution_router



class DataTalkGraph:



    def __init__(
        self,
        nodes,
    ):


        self.nodes = nodes


        self.graph = self._build()



    def _build(self):


        workflow = StateGraph(
            DataTalkState
        )


        workflow.add_node(
            "question",
            self.nodes.understand_question
        )


        workflow.add_node(
            "schema",
            self.nodes.explore_schema
        )


        workflow.add_node(
            "sql",
            self.nodes.generate_sql
        )


        workflow.add_node(
            "execute",
            self.nodes.execute_sql
        )


        workflow.add_node(
            "retry",
            self.nodes.retry_sql
        )


        workflow.add_node(
            "explain",
            self.nodes.explain
        )



        workflow.set_entry_point(
            "question"
        )



        workflow.add_edge(
            "question",
            "schema"
        )


        workflow.add_edge(
            "schema",
            "sql"
        )


        workflow.add_edge(
            "sql",
            "execute"
        )



        workflow.add_conditional_edges(

            "execute",

            execution_router,

            {

                "success":
                    "explain",


                "retry":
                    "retry",

            }

        )


        workflow.add_edge(
            "retry",
            "execute"
        )


        workflow.add_edge(
            "explain",
            END
        )



        return workflow.compile()



    def invoke(
        self,
        state: DataTalkState,
    ):


        return self.graph.invoke(
            state
        )