from __future__ import annotations

import logging
import time

from pydantic import BaseModel

from ..llm.base import BaseLLMProvider
from ..prompts.schema_explorer import SCHEMA_EXPLORER_PROMPT
from ..services import RelationshipGraph, SchemaService

logger = logging.getLogger(__name__)


class SchemaExplorerOutput(BaseModel):

    relevant_tables: list[str]
    reasoning: str


class SchemaExplorerAgent:

    def __init__(
        self,
        llm: BaseLLMProvider,
        schema_service: SchemaService,
        relationship_graph: RelationshipGraph,
    ) -> None:

        self._llm = llm
        self._schema_service = schema_service
        self._relationship_graph = relationship_graph

    def explore(
        self,
        question: str,
    ) -> SchemaExplorerOutput:

        start = time.perf_counter()

        logger.info(
            "Exploring schema for question: %s",
            question,
        )

        llm_result = self._ask_llm(question)

        valid_tables = self._validate_tables(
            llm_result.relevant_tables,
        )

        final_tables = self._resolve_tables(
            valid_tables,
        )

        reasoning = self._build_reasoning(
            llm_result.reasoning,
            valid_tables,
            final_tables,
        )

        logger.info(
            "Schema exploration completed in %.2f ms.",
            (time.perf_counter() - start) * 1000,
        )

        return SchemaExplorerOutput(
            relevant_tables=final_tables,
            reasoning=reasoning,
        )

    
    def _ask_llm(
        self,
        question: str,
    ) -> SchemaExplorerOutput:

        prompt = SCHEMA_EXPLORER_PROMPT.format(
            schema_description=self._schema_service.get_schema_description(),
            question=question,
        )

        return self._llm.generate_structured(
            prompt=prompt,
            response_model=SchemaExplorerOutput,
            temperature=0.1,
        )

    def _validate_tables(
        self,
        tables: list[str],
    ) -> list[str]:

        valid_tables = self._schema_service.validate_tables(
            tables,
        )

        if not valid_tables:
            raise ValueError(
                "The LLM did not return any valid database tables."
            )

        return valid_tables

    def _resolve_tables(
        self,
        tables: list[str],
    ) -> list[str]:

        try:
            return self._relationship_graph.resolve_join_paths(
                tables,
            )

        except Exception:
            logger.exception(
                "Unable to resolve relationship graph."
            )

            return tables

    def _build_reasoning(
        self,
        reasoning: str,
        selected_tables: list[str],
        final_tables: list[str],
    ) -> str:

        if len(final_tables) == len(selected_tables):
            return reasoning

        explanation = (
            self._relationship_graph.get_connection_explanation(
                selected_tables,
                final_tables,
            )
        )

        return f"{reasoning}\n\n{explanation}"


