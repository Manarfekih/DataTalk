from __future__ import annotations

import logging
from collections import deque
from functools import lru_cache

from .schema_service import SchemaService

logger = logging.getLogger(__name__)


class RelationshipGraph:
    """
    Undirected graph describing relationships between database tables.

    Nodes:
        Database tables.

    Edges:
        Foreign-key relationships.
    """

    def __init__(
        self,
        schema_service: SchemaService,
    ) -> None:

        self._graph: dict[str, set[str]] = {}

        self._build_graph(schema_service)

        logger.info(
            "Relationship graph created with %d tables.",
            len(self._graph),
        )

    @property
    def graph(self) -> dict[str, set[str]]:
        """Read-only access to the relationship graph."""
        return self._graph

    
    def _build_graph(
        self,
        schema_service: SchemaService,
    ) -> None:

        tables = schema_service.get_all_tables()

        for table in tables:
            self._graph[table] = set()

        for table in tables:

            schema = schema_service.get_table_schema(table)

            for fk in schema.foreign_keys:

                referenced_table = fk.referred_table

                self._graph[table].add(referenced_table)
                self._graph[referenced_table].add(table)

    @lru_cache(maxsize=128)
    def shortest_path(
        self,
        start: str,
        end: str,
    ) -> tuple[str, ...]:

        if start == end:
            return (start,)

        if (
            start not in self._graph
            or end not in self._graph
        ):
            return ()

        queue = deque([(start, [start])])
        visited = {start}

        while queue:

            node, path = queue.popleft()

            for neighbor in self._graph.get(node, set()):

                if neighbor == end:
                    return tuple(path + [neighbor])

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(
                        (
                            neighbor,
                            path + [neighbor],
                        )
                    )

        return ()

    def resolve_join_paths(
        self,
        tables: list[str],
    ) -> list[str]:

        if not tables:
            return []

        unique_tables = list(dict.fromkeys(tables))

        if len(unique_tables) == 1:
            return unique_tables

        resolved = set(unique_tables)

        for i in range(len(unique_tables)):
            for j in range(i + 1, len(unique_tables)):

                path = self.shortest_path(
                    unique_tables[i],
                    unique_tables[j],
                )

                resolved.update(path)

        return sorted(resolved)

    def get_neighbors(
        self,
        table: str,
    ) -> list[str]:

        return sorted(self._graph.get(table, set()))

    def get_connection_explanation(
        self,
        selected: list[str],
        resolved: list[str],
    ) -> str:

        added_tables = sorted(
            set(resolved) - set(selected)
        )

        if not added_tables:
            return (
                "All selected tables are directly connected."
            )

        return (
            "Added bridge table(s): "
            + ", ".join(added_tables)
            + " to connect the selected tables."
        )
