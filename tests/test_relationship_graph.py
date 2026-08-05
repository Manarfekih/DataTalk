from datatalk.services import (
    RelationshipGraph,
    schema_service,
)


def test_graph_build():

    graph = RelationshipGraph(schema_service)

    assert len(graph.graph) > 0

    print(graph.graph)


def test_neighbors():

    graph = RelationshipGraph(schema_service)

    neighbors = graph.get_neighbors("orders")

    assert isinstance(neighbors, list)

    print(neighbors)


def test_join_resolution():

    graph = RelationshipGraph(schema_service)

    tables = graph.resolve_join_paths(
        [
            "customers",
            "order_details",
        ]
    )

    assert "customers" in tables
    assert "order_details" in tables

    print(tables)