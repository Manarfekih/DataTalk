from __future__ import annotations

import pytest

from datatalk.agents.schema_explorer import (
    SchemaExplorerAgent,
    SchemaExplorerOutput,
)
from datatalk.services import (
    RelationshipGraph,
    schema_service,
)


class FakeLLM:

    def __init__(
        self,
        tables: list[str],
        reasoning: str = "Reasoning",
    ) -> None:

        self._tables = tables
        self._reasoning = reasoning

    def generate_structured(
        self,
        prompt: str,
        response_model,
        temperature: float = 0.1,
    ):

        return response_model(
            relevant_tables=self._tables,
            reasoning=self._reasoning,
        )


@pytest.fixture(scope="module")
def relationship_graph():

    return RelationshipGraph(schema_service)


def test_explore_returns_valid_tables(
    relationship_graph,
):

    llm = FakeLLM(
        tables=[
            "customers",
            "orders",
        ]
    )

    agent = SchemaExplorerAgent(
        llm=llm,
        schema_service=schema_service,
        relationship_graph=relationship_graph,
    )

    result = agent.explore(
        "Which customers placed the most orders?"
    )

    assert isinstance(
        result,
        SchemaExplorerOutput,
    )

    assert "customers" in result.relevant_tables
    assert "orders" in result.relevant_tables
    assert result.reasoning != ""


def test_invalid_tables_are_removed(
    relationship_graph,
):

    llm = FakeLLM(
        tables=[
            "customers",
            "fake_table",
            "orders",
        ]
    )

    agent = SchemaExplorerAgent(
        llm=llm,
        schema_service=schema_service,
        relationship_graph=relationship_graph,
    )

    result = agent.explore(
        "List customers."
    )

    assert "customers" in result.relevant_tables
    assert "orders" in result.relevant_tables
    assert "fake_table" not in result.relevant_tables


def test_bridge_tables_are_added(
    relationship_graph,
):

    llm = FakeLLM(
        tables=[
            "customers",
            "order_details",
        ]
    )

    agent = SchemaExplorerAgent(
        llm=llm,
        schema_service=schema_service,
        relationship_graph=relationship_graph,
    )

    result = agent.explore(
        "Products purchased by customers."
    )

    assert "customers" in result.relevant_tables
    assert "order_details" in result.relevant_tables

    assert len(result.relevant_tables) >= 2


def test_no_valid_table_raises(
    relationship_graph,
):

    llm = FakeLLM(
        tables=[
            "table_a",
            "table_b",
        ]
    )

    agent = SchemaExplorerAgent(
        llm=llm,
        schema_service=schema_service,
        relationship_graph=relationship_graph,
    )

    with pytest.raises(ValueError):
        agent.explore(
            "Random question."
        )